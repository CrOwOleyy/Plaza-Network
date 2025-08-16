# -*- coding: utf-8 -*-
"""
Cog d'aide et utilitaires pour COPBOT v4.0
Commandes d'information et d'aide pour les utilisateurs
"""

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import psutil
import platform
from datetime import datetime

from config.settings import BotConfig
from utils.helpers import create_embed, format_duration
from utils.logger import bot_logger


class HelpCog(commands.Cog, name="Aide"):
    """
    Commandes d'aide et d'information sur le bot
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.config = BotConfig()
    
    @app_commands.command(name="aide", description="Affiche l'aide du bot")
    async def help_command(self, interaction: discord.Interaction):
        """Commande d'aide principale"""
        
        embed = create_embed(
            title="🤖 COPBOT v4.0 - Aide",
            description="Bot Discord utilitaire complet pour la gestion de serveur",
            color=self.config.COLOR_INFO
        )
        
        # Catégories de commandes
        categories = {
            "🛡️ Modération": [
                "`/warn` - Avertir un utilisateur",
                "`/mute` - Mettre en sourdine",
                "`/ban` - Bannir un utilisateur",
                "`/unmute` - Retirer la sourdine"
            ],
            "🔒 Sécurité": [
                "`/antispam` - Configurer l'anti-spam",
                "`/motinterdits` - Gérer les mots interdits"
            ],
            "🎭 Rôles": [
                "`/autorole` - Rôle automatique nouveaux membres",
                "`/reactionrole` - Rôles par réaction",
                "`/rolemenu` - Menu de sélection de rôles",
                "`/roleinfo` - Informations sur un rôle"
            ],
            "📅 Événements": [
                "`/evenement` - Créer un événement",
                "`/listevenements` - Liste des événements",
                "`/infoevenement` - Détails d'un événement"
            ],
            "⏰ Rappels": [
                "`/rappel` - Créer un rappel",
                "`/rappels` - Vos rappels actifs",
                "`/supprimerappel` - Supprimer un rappel"
            ],
            "📊 Sondages": [
                "`/sondage` - Créer un sondage complet",
                "`/sondagerapide` - Sondage Oui/Non rapide",
                "`/listesondages` - Sondages actifs"
            ],
            "🎫 Tickets": [
                "`/setuptickets` - Configurer le système",
                "`/listetickets` - Tickets ouverts",
                "`/fermerticket` - Fermer le ticket actuel"
            ],
            "ℹ️ Informations": [
                "`/info` - Informations sur le bot",
                "`/serverinfo` - Informations sur le serveur",
                "`/userinfo` - Informations sur un utilisateur",
                "`/ping` - Test de latence"
            ]
        }
        
        for category, commands_list in categories.items():
            embed.add_field(
                name=category,
                value="\n".join(commands_list),
                inline=False
            )
        
        embed.add_field(
            name="🔗 Liens utiles",
            value="[Support](https://discord.gg/votre-serveur) • [Site Web](https://plaza-network.com)",
            inline=False
        )
        
        embed.set_footer(text="Utilisez /aide [commande] pour plus de détails sur une commande")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="info", description="Informations sur le bot")
    async def bot_info(self, interaction: discord.Interaction):
        """Affiche les informations du bot"""
        
        # Statistiques du bot
        total_members = sum(guild.member_count for guild in self.bot.guilds)
        
        # Informations système
        process = psutil.Process()
        memory_usage = process.memory_info().rss / 1024 / 1024  # MB
        cpu_usage = process.cpu_percent()
        
        # Uptime
        uptime_delta = datetime.utcnow() - self.bot.start_time if hasattr(self.bot, 'start_time') else None
        uptime_str = format_duration(int(uptime_delta.total_seconds())) if uptime_delta else "Inconnu"
        
        embed = create_embed(
            title="📊 Informations du Bot",
            color=self.config.COLOR_INFO
        )
        
        embed.add_field(
            name="🤖 Bot",
            value=f"**Version:** 4.0\n"
                  f"**Uptime:** {uptime_str}\n"
                  f"**Ping:** {round(self.bot.latency * 1000)}ms",
            inline=True
        )
        
        embed.add_field(
            name="📈 Statistiques",
            value=f"**Serveurs:** {len(self.bot.guilds)}\n"
                  f"**Utilisateurs:** {total_members:,}\n"
                  f"**Commandes:** {len(self.bot.tree.get_commands())}",
            inline=True
        )
        
        embed.add_field(
            name="⚙️ Système",
            value=f"**RAM:** {memory_usage:.1f} MB\n"
                  f"**CPU:** {cpu_usage:.1f}%\n"
                  f"**Python:** {platform.python_version()}",
            inline=True
        )
        
        embed.add_field(
            name="🔧 Développement",
            value=f"**Développeur:** CrOwOleyy\n"
                  f"**Framework:** discord.py {discord.__version__}\n"
                  f"**Base de données:** PostgreSQL",
            inline=False
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="serverinfo", description="Informations sur le serveur")
    async def server_info(self, interaction: discord.Interaction):
        """Affiche les informations du serveur"""
        
        guild = interaction.guild
        
        # Comptage des membres par statut
        online = sum(1 for member in guild.members if member.status != discord.Status.offline)
        bots = sum(1 for member in guild.members if member.bot)
        
        # Comptage des salons par type
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        
        embed = create_embed(
            title=f"📊 Informations - {guild.name}",
            color=self.config.COLOR_INFO
        )
        
        embed.add_field(
            name="👥 Membres",
            value=f"**Total:** {guild.member_count:,}\n"
                  f"**En ligne:** {online:,}\n"
                  f"**Bots:** {bots:,}",
            inline=True
        )
        
        embed.add_field(
            name="💬 Salons",
            value=f"**Texte:** {text_channels}\n"
                  f"**Vocal:** {voice_channels}\n"
                  f"**Catégories:** {categories}",
            inline=True
        )
        
        embed.add_field(
            name="🎭 Rôles",
            value=f"**Total:** {len(guild.roles)}\n"
                  f"**Boost Tier:** {guild.premium_tier}\n"
                  f"**Boosts:** {guild.premium_subscription_count}",
            inline=True
        )
        
        embed.add_field(
            name="ℹ️ Informations",
            value=f"**Créé le:** <t:{int(guild.created_at.timestamp())}:D>\n"
                  f"**Propriétaire:** {guild.owner.mention if guild.owner else 'Inconnu'}\n"
                  f"**ID:** {guild.id}",
            inline=False
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="userinfo", description="Informations sur un utilisateur")
    @app_commands.describe(utilisateur="L'utilisateur à analyser (optionnel)")
    async def user_info(self, interaction: discord.Interaction, utilisateur: Optional[discord.Member] = None):
        """Affiche les informations d'un utilisateur"""
        
        member = utilisateur or interaction.user
        
        # Calcul de l'ancienneté
        join_delta = datetime.utcnow() - member.joined_at if member.joined_at else None
        create_delta = datetime.utcnow() - member.created_at
        
        embed = create_embed(
            title=f"👤 Informations - {member.display_name}",
            color=member.color if member.color != discord.Color.default() else self.config.COLOR_INFO
        )
        
        embed.add_field(
            name="📋 Général",
            value=f"**Nom d'utilisateur:** {member}\n"
                  f"**Surnom:** {member.display_name}\n"
                  f"**ID:** {member.id}",
            inline=True
        )
        
        embed.add_field(
            name="📅 Dates",
            value=f"**Compte créé:** <t:{int(member.created_at.timestamp())}:R>\n"
                  f"**Rejoint le:** <t:{int(member.joined_at.timestamp())}:R>" if member.joined_at else "**Rejoint le:** Inconnu",
            inline=True
        )
        
        # Rôles (limité à 10 pour éviter les embeds trop longs)
        roles = [role.mention for role in member.roles[1:]]  # Exclure @everyone
        if len(roles) > 10:
            roles = roles[:10] + [f"... et {len(roles) - 10} autres"]
        
        embed.add_field(
            name=f"🎭 Rôles ({len(member.roles) - 1})",
            value=" ".join(roles) if roles else "Aucun rôle",
            inline=False
        )
        
        # Permissions clés
        perms = member.guild_permissions
        key_perms = []
        
        if perms.administrator:
            key_perms.append("👑 Administrateur")
        if perms.manage_guild:
            key_perms.append("🛠️ Gérer le serveur")
        if perms.manage_messages:
            key_perms.append("🗑️ Gérer les messages")
        if perms.ban_members:
            key_perms.append("🔨 Bannir des membres")
        if perms.kick_members:
            key_perms.append("👢 Expulser des membres")
        
        if key_perms:
            embed.add_field(
                name="🔑 Permissions clés",
                value=" • ".join(key_perms),
                inline=False
            )
        
        # Badges (Nitro, etc.)
        badges = []
        if member.premium_since:
            badges.append("💎 Booster")
        if member.bot:
            badges.append("🤖 Bot")
        
        if badges:
            embed.add_field(
                name="🏆 Badges",
                value=" • ".join(badges),
                inline=False
            )
        
        embed.set_thumbnail(url=member.display_avatar.url)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="ping", description="Teste la latence du bot")
    async def ping(self, interaction: discord.Interaction):
        """Commande de test de latence"""
        
        latency = round(self.bot.latency * 1000)
        
        if latency < 100:
            emoji = "🟢"
            status = "Excellent"
        elif latency < 200:
            emoji = "🟡"
            status = "Bon"
        else:
            emoji = "🔴"
            status = "Élevé"
        
        embed = create_embed(
            title=f"{emoji} Pong!",
            description=f"**Latence:** {latency}ms ({status})",
            color=self.config.COLOR_SUCCESS
        )
        
        await interaction.response.send_message(embed=embed)
        
        # Log de la commande
        bot_logger.command_used(
            interaction.user.id, interaction.guild.id if interaction.guild else 0,
            "ping", latency=latency
        )


async def setup(bot):
    await bot.add_cog(HelpCog(bot))