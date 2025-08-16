# -*- coding: utf-8 -*-
"""
Cog anti-spam et sécurité pour COPBOT v4.0
Détection automatique de spam, flood, raid et contenu suspect
"""

import discord
from discord.ext import commands, tasks
from discord import app_commands
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
from collections import defaultdict, deque
import re
import asyncio

from config.settings import BotConfig, ERROR_MESSAGES
from utils.helpers import create_embed, is_url_safe, RateLimiter
from utils.logger import bot_logger


class AntiSpamCog(commands.Cog, name="Anti-Spam"):
    """
    Système de protection contre le spam, flood et raids
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.config = BotConfig()
        
        # Tracking des messages pour détection de spam
        self.message_tracking: Dict[int, Dict[int, deque]] = defaultdict(lambda: defaultdict(deque))
        self.user_warnings: Dict[int, Dict[int, int]] = defaultdict(lambda: defaultdict(int))
        
        # Tracking des joins pour anti-raid
        self.recent_joins: Dict[int, deque] = defaultdict(deque)
        
        # Mots interdits par serveur
        self.banned_words: Dict[int, Set[str]] = defaultdict(set)
        
        # Rate limiters
        self.command_rate_limiter = RateLimiter(max_uses=10, per_seconds=60)
        
        # Patterns de détection
        self.setup_detection_patterns()
        
        # Tâches de nettoyage
        self.cleanup_tracking.start()
    
    def cog_unload(self):
        """Nettoyage lors du déchargement"""
        self.cleanup_tracking.cancel()
    
    def setup_detection_patterns(self):
        """Configure les patterns de détection de spam"""
        
        # Patterns d'URLs suspectes
        self.suspicious_url_patterns = [
            r'discord[-.]?(nitro|gift|app|gg)',
            r'steam[-.]?(community|gift|free)',
            r'free[-.]?(nitro|gift|games?)',
            r'bit\.ly|tinyurl\.com|t\.co',
        ]
        
        # Patterns de spam communs
        self.spam_patterns = [
            r'(.)\1{4,}',  # Répétition de caractères
            r'[🎉🎊🎁💎💰]{3,}',  # Émojis spam
            r'@(everyone|here)',  # Mentions masse
            r'[A-Z]{10,}',  # CAPS LOCK
        ]
        
        # Mots interdits de base (extensible par serveur)
        self.base_banned_words = {
            'insultes', 'spam', 'scam', 'hack', 'cheat'
        }
    
    @tasks.loop(minutes=30)
    async def cleanup_tracking(self):
        """Nettoie les données de tracking anciennes"""
        try:
            cutoff = datetime.utcnow() - timedelta(hours=1)
            
            # Nettoyer le tracking des messages
            for guild_id in list(self.message_tracking.keys()):
                for user_id in list(self.message_tracking[guild_id].keys()):
                    messages = self.message_tracking[guild_id][user_id]
                    while messages and messages[0] < cutoff:
                        messages.popleft()
                    
                    if not messages:
                        del self.message_tracking[guild_id][user_id]
                
                if not self.message_tracking[guild_id]:
                    del self.message_tracking[guild_id]
            
            # Nettoyer le tracking des joins
            for guild_id in list(self.recent_joins.keys()):
                joins = self.recent_joins[guild_id]
                while joins and joins[0][0] < cutoff:
                    joins.popleft()
                
                if not joins:
                    del self.recent_joins[guild_id]
                    
        except Exception as e:
            bot_logger.error_occurred(e, "cleanup_tracking")
    
    @cleanup_tracking.before_loop
    async def before_cleanup(self):
        await self.bot.wait_until_ready()
    
    # ==================== ÉVÉNEMENTS DE DÉTECTION ====================
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Analyse automatique des messages pour détecter le spam"""
        
        if not message.guild or message.author.bot:
            return
        
        # Vérifier si l'anti-spam est activé pour ce serveur
        guild_settings = await self.bot.db.get_guild_settings(message.guild.id)
        if not guild_settings.get('anti_spam_enabled', True):
            return
        
        # Ignorer les modérateurs
        if message.author.guild_permissions.manage_messages:
            return
        
        # Analyser le message
        await self._analyze_message(message)
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Détection anti-raid basée sur les arrivées massives"""
        
        guild_settings = await self.bot.db.get_guild_settings(member.guild.id)
        if not guild_settings.get('anti_raid_enabled', True):
            return
        
        # Ajouter à la liste des joins récents
        now = datetime.utcnow()
        self.recent_joins[member.guild.id].append((now, member.id))
        
        # Vérifier si raid potentiel (plus de 5 joins en 10 secondes)
        recent_count = 0
        cutoff = now - timedelta(seconds=10)
        
        for join_time, _ in self.recent_joins[member.guild.id]:
            if join_time > cutoff:
                recent_count += 1
        
        if recent_count >= 5:
            await self._handle_raid_detection(member.guild, recent_count)
    
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        """Vérifie les messages édités pour éviter le contournement"""
        
        if not after.guild or after.author.bot:
            return
        
        # Re-analyser le message édité
        await self._analyze_message(after)
    
    # ==================== MÉTHODES D'ANALYSE ====================
    
    async def _analyze_message(self, message: discord.Message):
        """Analyse complète d'un message pour détecter le spam"""
        
        content = message.content.lower()
        violations = []
        
        # 1. Vérifier la répétition de messages
        if await self._check_message_spam(message):
            violations.append("message_spam")
        
        # 2. Vérifier les patterns de spam
        if self._check_spam_patterns(content):
            violations.append("spam_pattern")
        
        # 3. Vérifier les mots interdits
        if await self._check_banned_words(message.guild.id, content):
            violations.append("banned_words")
        
        # 4. Vérifier les URLs suspectes
        if self._check_suspicious_urls(content):
            violations.append("suspicious_url")
        
        # 5. Vérifier le flood d'émojis/mentions
        if self._check_emoji_flood(message):
            violations.append("emoji_flood")
        
        # 6. Vérifier les mentions en masse
        if self._check_mass_mentions(message):
            violations.append("mass_mentions")
        
        # Appliquer les sanctions si violations détectées
        if violations:
            await self._handle_violations(message, violations)
    
    async def _check_message_spam(self, message: discord.Message) -> bool:
        """Vérifie la répétition de messages identiques"""
        
        user_messages = self.message_tracking[message.guild.id][message.author.id]
        now = datetime.utcnow()
        
        # Ajouter le message actuel
        user_messages.append(now)
        
        # Compter les messages dans les 30 dernières secondes
        cutoff = now - timedelta(seconds=30)
        recent_count = sum(1 for msg_time in user_messages if msg_time > cutoff)
        
        # Spam si plus de 5 messages en 30 secondes
        return recent_count > 5
    
    def _check_spam_patterns(self, content: str) -> bool:
        """Vérifie les patterns de spam dans le contenu"""
        
        for pattern in self.spam_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    async def _check_banned_words(self, guild_id: int, content: str) -> bool:
        """Vérifie les mots interdits"""
        
        # Combiner mots de base et mots spécifiques au serveur
        all_banned = self.base_banned_words | self.banned_words[guild_id]
        
        words = content.split()
        for word in words:
            if word.lower() in all_banned:
                return True
        
        return False
    
    def _check_suspicious_urls(self, content: str) -> bool:
        """Vérifie les URLs suspectes"""
        
        # Extraire les URLs
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, content)
        
        for url in urls:
            if not is_url_safe(url):
                return True
            
            # Vérifier contre nos patterns suspects
            for pattern in self.suspicious_url_patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    return True
        
        return False
    
    def _check_emoji_flood(self, message: discord.Message) -> bool:
        """Vérifie le flood d'émojis ou réactions"""
        
        content = message.content
        
        # Compter les émojis Unicode
        emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]'
        emoji_count = len(re.findall(emoji_pattern, content))
        
        # Compter les émojis Discord personnalisés
        custom_emoji_pattern = r'<a?:[a-zA-Z0-9_]+:[0-9]+>'
        custom_emoji_count = len(re.findall(custom_emoji_pattern, content))
        
        total_emojis = emoji_count + custom_emoji_count
        
        # Flood si plus de 8 émojis
        return total_emojis > 8
    
    def _check_mass_mentions(self, message: discord.Message) -> bool:
        """Vérifie les mentions en masse"""
        
        # Compter les mentions d'utilisateurs uniques
        unique_mentions = len(set(message.mentions))
        
        # Vérifier @everyone/@here
        has_everyone = '@everyone' in message.content or '@here' in message.content
        
        # Violation si plus de 5 mentions ou @everyone/@here sans permission
        return (unique_mentions > 5 or 
                (has_everyone and not message.author.guild_permissions.mention_everyone))
    
    async def _handle_violations(self, message: discord.Message, violations: List[str]):
        """Gère les violations détectées"""
        
        try:
            # Supprimer le message
            await message.delete()
            
            # Incrémenter les avertissements
            self.user_warnings[message.guild.id][message.author.id] += 1
            warning_count = self.user_warnings[message.guild.id][message.author.id]
            
            # Créer l'embed d'avertissement
            embed = create_embed(
                title="Message supprimé - Violation détectée",
                description=f"**Utilisateur:** {message.author.mention}\n"
                           f"**Salon:** {message.channel.mention}\n"
                           f"**Violations:** {', '.join(violations)}\n"
                           f"**Avertissements:** {warning_count}/3",
                color=self.config.COLOR_WARNING
            )
            
            # Envoyer dans le salon de modération
            guild_settings = await self.bot.db.get_guild_settings(message.guild.id)
            mod_channel_id = guild_settings.get('mod_log_channel')
            
            if mod_channel_id:
                mod_channel = message.guild.get_channel(mod_channel_id)
                if mod_channel:
                    await mod_channel.send(embed=embed)
            
            # Sanctionner si trop d'avertissements
            if warning_count >= 3:
                await self._apply_spam_sanction(message.author, violations)
            else:
                # Avertir l'utilisateur par MP
                try:
                    user_embed = create_embed(
                        title=f"Avertissement - {message.guild.name}",
                        description=f"Votre message a été supprimé pour violation des règles.\n\n"
                                   f"**Violations:** {', '.join(violations)}\n"
                                   f"**Avertissements:** {warning_count}/3\n\n"
                                   f"Attention: 3 avertissements entraînent une sanction automatique.",
                        color=self.config.COLOR_WARNING
                    )
                    await message.author.send(embed=user_embed)
                except:
                    pass
            
            # Log de sécurité
            bot_logger.security_event(
                "spam_detection",
                f"Violations: {violations}, Avertissements: {warning_count}",
                message.guild.id,
                message.author.id
            )
            
        except discord.NotFound:
            # Message déjà supprimé
            pass
        except Exception as e:
            bot_logger.error_occurred(e, "_handle_violations")
    
    async def _apply_spam_sanction(self, user: discord.Member, violations: List[str]):
        """Applique une sanction pour spam répété"""
        
        try:
            # Déterminer la durée selon la gravité
            if "suspicious_url" in violations or "mass_mentions" in violations:
                duration = 3600  # 1 heure pour les violations graves
            else:
                duration = 600   # 10 minutes pour spam normal
            
            # Obtenir le cog de modération pour appliquer un mute
            moderation_cog = self.bot.get_cog("Modération")
            if moderation_cog:
                mute_role = await moderation_cog._get_or_create_mute_role(user.guild)
                if mute_role:
                    await user.add_roles(mute_role, reason="Sanction automatique anti-spam")
                    
                    # Enregistrer en base
                    await self.bot.db.add_sanction(
                        user.guild.id,
                        user.id,
                        self.bot.user.id,
                        "mute",
                        f"Spam automatique: {', '.join(violations)}",
                        duration
                    )
                    
                    # Programmer le unmute
                    await asyncio.sleep(duration)
                    await user.remove_roles(mute_role, reason="Fin de sanction anti-spam")
            
            # Reset des avertissements après sanction
            self.user_warnings[user.guild.id][user.id] = 0
            
            bot_logger.moderation_action(
                self.bot.user.id, user.id, "auto_spam_mute",
                user.guild.id, f"Violations: {violations}"
            )
            
        except Exception as e:
            bot_logger.error_occurred(e, "_apply_spam_sanction")
    
    async def _handle_raid_detection(self, guild: discord.Guild, join_count: int):
        """Gère la détection de raid"""
        
        try:
            # Log de l'événement
            bot_logger.security_event(
                "raid_detection",
                f"{join_count} joins en 10 secondes",
                guild.id
            )
            
            # Alerter les modérateurs
            embed = create_embed(
                title="🚨 RAID DÉTECTÉ",
                description=f"**{join_count} nouveaux membres** ont rejoint en moins de 10 secondes.\n\n"
                           f"Considérez l'activation du mode de vérification ou du ralentissement temporaire.",
                color=self.config.COLOR_ERROR
            )
            
            guild_settings = await self.bot.db.get_guild_settings(guild.id)
            mod_channel_id = guild_settings.get('mod_log_channel')
            
            if mod_channel_id:
                mod_channel = guild.get_channel(mod_channel_id)
                if mod_channel:
                    await mod_channel.send(embed=embed)
            
            # Enregistrer l'événement
            await self.bot.db.log_activity(
                guild.id,
                "raid_detection",
                details={"join_count": join_count, "timeframe": "10s"}
            )
            
        except Exception as e:
            bot_logger.error_occurred(e, "_handle_raid_detection")
    
    # ==================== COMMANDES DE CONFIGURATION ====================
    
    @app_commands.command(name="antispam", description="Configure les paramètres anti-spam")
    @app_commands.describe(
        activer="Activer ou désactiver l'anti-spam",
        canal_logs="Canal pour les logs de modération"
    )
    @commands.has_permissions(manage_guild=True)
    async def configure_antispam(self, interaction: discord.Interaction, 
                                activer: bool, canal_logs: Optional[discord.TextChannel] = None):
        """Configure les paramètres anti-spam du serveur"""
        
        try:
            # Mettre à jour les paramètres
            await self.bot.db.update_guild_setting(
                interaction.guild.id, 
                'anti_spam_enabled', 
                activer
            )
            
            if canal_logs:
                await self.bot.db.update_guild_setting(
                    interaction.guild.id,
                    'mod_log_channel',
                    canal_logs.id
                )
            
            # Créer l'embed de confirmation
            embed = create_embed(
                title="Configuration Anti-Spam",
                description=f"**Anti-spam:** {'✅ Activé' if activer else '❌ Désactivé'}\n"
                           f"**Canal de logs:** {canal_logs.mention if canal_logs else 'Non défini'}",
                color=self.config.COLOR_SUCCESS
            )
            
            await interaction.response.send_message(embed=embed)
            
            # Log de l'action
            bot_logger.command_used(
                interaction.user.id, interaction.guild.id, "antispam",
                enabled=activer, log_channel=canal_logs.id if canal_logs else None
            )
            
        except Exception as e:
            bot_logger.error_occurred(e, "configure_antispam")
            await interaction.response.send_message(
                ERROR_MESSAGES['database_error'], ephemeral=True
            )
    
    @app_commands.command(name="motinterdits", description="Gère la liste des mots interdits")
    @app_commands.describe(
        action="Action à effectuer",
        mot="Mot à ajouter ou supprimer"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="Ajouter", value="add"),
        app_commands.Choice(name="Supprimer", value="remove"),
        app_commands.Choice(name="Lister", value="list")
    ])
    @commands.has_permissions(manage_messages=True)
    async def manage_banned_words(self, interaction: discord.Interaction, 
                                 action: str, mot: Optional[str] = None):
        """Gère les mots interdits sur le serveur"""
        
        guild_id = interaction.guild.id
        
        if action == "add":
            if not mot:
                await interaction.response.send_message(
                    "❌ Vous devez spécifier un mot à ajouter.", ephemeral=True
                )
                return
            
            self.banned_words[guild_id].add(mot.lower())
            
            embed = create_embed(
                title="Mot interdit ajouté",
                description=f"Le mot `{mot}` a été ajouté à la liste des mots interdits.",
                color=self.config.COLOR_SUCCESS
            )
            
        elif action == "remove":
            if not mot:
                await interaction.response.send_message(
                    "❌ Vous devez spécifier un mot à supprimer.", ephemeral=True
                )
                return
            
            if mot.lower() in self.banned_words[guild_id]:
                self.banned_words[guild_id].remove(mot.lower())
                embed = create_embed(
                    title="Mot interdit supprimé",
                    description=f"Le mot `{mot}` a été retiré de la liste des mots interdits.",
                    color=self.config.COLOR_SUCCESS
                )
            else:
                await interaction.response.send_message(
                    f"❌ Le mot `{mot}` n'est pas dans la liste des mots interdits.",
                    ephemeral=True
                )
                return
        
        else:  # list
            banned_list = list(self.banned_words[guild_id])
            if not banned_list:
                content = "Aucun mot interdit configuré."
            else:
                content = "```\n" + "\n".join(banned_list) + "\n```"
            
            embed = create_embed(
                title="Mots interdits",
                description=content,
                color=self.config.COLOR_INFO
            )
        
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(AntiSpamCog(bot))