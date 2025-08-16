# -*- coding: utf-8 -*-
"""
Cog de rappels pour COPBOT v4.0
Système de rappels personnels et collectifs avec récurrence
"""

import discord
from discord.ext import commands, tasks
from discord import app_commands
from typing import Optional, Dict, List
from datetime import datetime, timedelta
import asyncio

from config.settings import BotConfig, ERROR_MESSAGES, SUCCESS_MESSAGES
from utils.helpers import create_embed, parse_duration, format_duration
from utils.logger import bot_logger


class RemindersCog(commands.Cog, name="Rappels"):
    """
    Système de gestion des rappels
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.config = BotConfig()
        
        # Cache des rappels actifs pour optimiser les performances
        self.active_reminders: Dict[int, Dict] = {}
        
        # Tâches périodiques
        self.check_reminders.start()
        self.load_reminders.start()
    
    def cog_unload(self):
        """Nettoyage lors du déchargement"""
        self.check_reminders.cancel()
        self.load_reminders.cancel()
    
    @tasks.loop(minutes=1)
    async def check_reminders(self):
        """Vérifie et déclenche les rappels dus"""
        try:
            now = datetime.utcnow()
            
            # Vérifier les rappels en cache
            for reminder_id, reminder in list(self.active_reminders.items()):
                if reminder['remind_at'] <= now:
                    await self._trigger_reminder(reminder)
                    
                    # Gérer la récurrence
                    if reminder['recurring_interval']:
                        await self._schedule_next_occurrence(reminder)
                    else:
                        # Retirer du cache et désactiver en base
                        del self.active_reminders[reminder_id]
                        await self._deactivate_reminder(reminder_id)
                        
        except Exception as e:
            bot_logger.error_occurred(e, "check_reminders")
    
    @tasks.loop(hours=1)
    async def load_reminders(self):
        """Recharge les rappels depuis la base de données"""
        try:
            await self._load_active_reminders()
        except Exception as e:
            bot_logger.error_occurred(e, "load_reminders")
    
    @check_reminders.before_loop
    async def before_check_reminders(self):
        await self.bot.wait_until_ready()
        # Charger les rappels au démarrage
        await self._load_active_reminders()
    
    @load_reminders.before_loop
    async def before_load_reminders(self):
        await self.bot.wait_until_ready()
    
    # ==================== COMMANDES ====================
    
    @app_commands.command(name="rappel", description="Crée un rappel personnel ou collectif")
    @app_commands.describe(
        duree="Durée avant le rappel (ex: 1h30m, 2d)",
        message="Message du rappel",
        canal="Canal pour un rappel collectif (optionnel)",
        recurrence="Intervalle de récurrence (optionnel, ex: 1d, 1w)"
    )
    async def create_reminder(self, interaction: discord.Interaction, duree: str, 
                             message: str, canal: Optional[discord.TextChannel] = None,
                             recurrence: Optional[str] = None):
        """Crée un nouveau rappel"""
        
        # Parser la durée
        duration_seconds = parse_duration(duree)
        if not duration_seconds:
            await interaction.response.send_message(
                ERROR_MESSAGES['invalid_duration'], ephemeral=True
            )
            return
        
        if duration_seconds < 60:  # Minimum 1 minute
            await interaction.response.send_message(
                "❌ La durée minimale pour un rappel est de 1 minute.", ephemeral=True
            )
            return
        
        # Parser la récurrence si fournie
        recurring_interval = None
        if recurrence:
            recurring_interval = parse_duration(recurrence)
            if not recurring_interval:
                await interaction.response.send_message(
                    "❌ Format de récurrence invalide. Utilisez un format comme '1d', '1w'.",
                    ephemeral=True
                )
                return
            
            if recurring_interval < 3600:  # Minimum 1 heure pour la récurrence
                await interaction.response.send_message(
                    "❌ L'intervalle de récurrence minimal est de 1 heure.", ephemeral=True
                )
                return
        
        # Déterminer le canal de destination
        target_channel = canal or interaction.channel
        
        # Vérifier les permissions pour les rappels collectifs
        if canal and not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "❌ Vous devez avoir la permission 'Gérer les messages' pour créer des rappels collectifs.",
                ephemeral=True
            )
            return
        
        try:
            # Calculer la date du rappel
            remind_at = datetime.utcnow() + timedelta(seconds=duration_seconds)
            
            # Créer le rappel en base de données
            async with self.bot.db.pool.acquire() as conn:
                reminder_id = await conn.fetchval('''
                    INSERT INTO reminders (guild_id, user_id, channel_id, message, remind_at, recurring_interval)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    RETURNING id
                ''', interaction.guild.id, interaction.user.id, target_channel.id, 
                message, remind_at, recurring_interval)
            
            # Ajouter au cache
            self.active_reminders[reminder_id] = {
                'id': reminder_id,
                'guild_id': interaction.guild.id,
                'user_id': interaction.user.id,
                'channel_id': target_channel.id,
                'message': message,
                'remind_at': remind_at,
                'recurring_interval': recurring_interval
            }
            
            # Créer l'embed de confirmation
            embed = create_embed(
                title="✅ Rappel créé",
                description=f"**Message:** {message}\n"
                           f"**Déclenchement:** <t:{int(remind_at.timestamp())}:F>\n"
                           f"**Dans:** {format_duration(duration_seconds)}",
                color=self.config.COLOR_SUCCESS
            )
            
            if canal:
                embed.add_field(
                    name="📍 Canal",
                    value=target_channel.mention,
                    inline=True
                )
            else:
                embed.add_field(
                    name="📍 Type",
                    value="Rappel personnel (MP)",
                    inline=True
                )
            
            if recurring_interval:
                embed.add_field(
                    name="🔄 Récurrence",
                    value=f"Toutes les {format_duration(recurring_interval)}",
                    inline=True
                )
            
            embed.set_footer(text=f"ID du rappel: {reminder_id}")
            
            await interaction.response.send_message(embed=embed)
            
            # Log de l'action
            bot_logger.command_used(
                interaction.user.id, interaction.guild.id, "create_reminder",
                reminder_id=reminder_id, duration=duration_seconds
            )
            
        except Exception as e:
            bot_logger.error_occurred(e, "create_reminder")
            await interaction.response.send_message(
                ERROR_MESSAGES['database_error'], ephemeral=True
            )
    
    @app_commands.command(name="rappels", description="Liste vos rappels actifs")
    async def list_reminders(self, interaction: discord.Interaction):
        """Liste les rappels actifs de l'utilisateur"""
        
        try:
            async with self.bot.db.pool.acquire() as conn:
                reminders = await conn.fetch('''
                    SELECT * FROM reminders
                    WHERE guild_id = $1 AND user_id = $2 AND is_active = TRUE
                    ORDER BY remind_at ASC
                ''', interaction.guild.id, interaction.user.id)
            
            if not reminders:
                embed = create_embed(
                    title="📋 Vos rappels",
                    description="Vous n'avez aucun rappel actif.",
                    color=self.config.COLOR_INFO
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            embed = create_embed(
                title="📋 Vos rappels actifs",
                description=f"{len(reminders)} rappel(s) programmé(s)",
                color=self.config.COLOR_INFO
            )
            
            for reminder in reminders[:10]:  # Limiter à 10 pour éviter les embeds trop longs
                # Canal de destination
                channel = interaction.guild.get_channel(reminder['channel_id'])
                channel_name = channel.mention if channel else "Canal supprimé"
                
                # Informations du rappel
                reminder_info = f"**Message:** {reminder['message'][:100]}{'...' if len(reminder['message']) > 100 else ''}\n"
                reminder_info += f"**Déclenchement:** <t:{int(reminder['remind_at'].timestamp())}:R>\n"
                reminder_info += f"**Canal:** {channel_name}"
                
                if reminder['recurring_interval']:
                    reminder_info += f"\n**Récurrence:** {format_duration(reminder['recurring_interval'])}"
                
                embed.add_field(
                    name=f"🔔 Rappel #{reminder['id']}",
                    value=reminder_info,
                    inline=False
                )
            
            if len(reminders) > 10:
                embed.set_footer(text=f"Affichage de 10/{len(reminders)} rappels")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except Exception as e:
            bot_logger.error_occurred(e, "list_reminders")
            await interaction.response.send_message(
                ERROR_MESSAGES['database_error'], ephemeral=True
            )
    
    @app_commands.command(name="supprimerappel", description="Supprime un de vos rappels")
    @app_commands.describe(reminder_id="ID du rappel à supprimer")
    async def delete_reminder(self, interaction: discord.Interaction, reminder_id: int):
        """Supprime un rappel spécifique"""
        
        try:
            async with self.bot.db.pool.acquire() as conn:
                # Vérifier que le rappel existe et appartient à l'utilisateur
                reminder = await conn.fetchrow('''
                    SELECT * FROM reminders
                    WHERE id = $1 AND guild_id = $2 AND user_id = $3 AND is_active = TRUE
                ''', reminder_id, interaction.guild.id, interaction.user.id)
                
                if not reminder:
                    await interaction.response.send_message(
                        "❌ Rappel introuvable ou vous n'êtes pas autorisé à le supprimer.",
                        ephemeral=True
                    )
                    return
                
                # Désactiver le rappel
                await conn.execute('''
                    UPDATE reminders SET is_active = FALSE WHERE id = $1
                ''', reminder_id)
            
            # Retirer du cache
            if reminder_id in self.active_reminders:
                del self.active_reminders[reminder_id]
            
            embed = create_embed(
                title="🗑️ Rappel supprimé",
                description=f"Le rappel #{reminder_id} a été supprimé avec succès.\n\n"
                           f"**Message:** {reminder['message']}",
                color=self.config.COLOR_SUCCESS
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except Exception as e:
            bot_logger.error_occurred(e, "delete_reminder")
            await interaction.response.send_message(
                ERROR_MESSAGES['database_error'], ephemeral=True
            )
    
    @app_commands.command(name="purgerappels", description="Supprime tous vos rappels")
    @commands.has_permissions(manage_messages=True)
    async def purge_reminders(self, interaction: discord.Interaction, 
                             utilisateur: Optional[discord.Member] = None):
        """Supprime tous les rappels d'un utilisateur (admin seulement)"""
        
        target_user = utilisateur or interaction.user
        
        # Seuls les admins peuvent purger les rappels des autres
        if utilisateur and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Vous ne pouvez purger que vos propres rappels.", ephemeral=True
            )
            return
        
        try:
            async with self.bot.db.pool.acquire() as conn:
                # Compter les rappels actifs
                count = await conn.fetchval('''
                    SELECT COUNT(*) FROM reminders
                    WHERE guild_id = $1 AND user_id = $2 AND is_active = TRUE
                ''', interaction.guild.id, target_user.id)
                
                if count == 0:
                    username = target_user.display_name
                    await interaction.response.send_message(
                        f"❌ {username} n'a aucun rappel actif.", ephemeral=True
                    )
                    return
                
                # Désactiver tous les rappels
                await conn.execute('''
                    UPDATE reminders SET is_active = FALSE
                    WHERE guild_id = $1 AND user_id = $2 AND is_active = TRUE
                ''', interaction.guild.id, target_user.id)
            
            # Nettoyer le cache
            for reminder_id in list(self.active_reminders.keys()):
                if self.active_reminders[reminder_id]['user_id'] == target_user.id:
                    del self.active_reminders[reminder_id]
            
            username = target_user.display_name
            embed = create_embed(
                title="🗑️ Rappels purgés",
                description=f"**{count}** rappel(s) de {username} ont été supprimés.",
                color=self.config.COLOR_SUCCESS
            )
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            bot_logger.error_occurred(e, "purge_reminders")
            await interaction.response.send_message(
                ERROR_MESSAGES['database_error'], ephemeral=True
            )
    
    # ==================== MÉTHODES UTILITAIRES ====================
    
    async def _load_active_reminders(self):
        """Charge les rappels actifs depuis la base de données"""
        
        try:
            async with self.bot.db.pool.acquire() as conn:
                reminders = await conn.fetch('''
                    SELECT * FROM reminders
                    WHERE is_active = TRUE AND remind_at > NOW()
                    ORDER BY remind_at ASC
                ''')
            
            # Nettoyer le cache et le recharger
            self.active_reminders.clear()
            
            for reminder in reminders:
                self.active_reminders[reminder['id']] = {
                    'id': reminder['id'],
                    'guild_id': reminder['guild_id'],
                    'user_id': reminder['user_id'],
                    'channel_id': reminder['channel_id'],
                    'message': reminder['message'],
                    'remind_at': reminder['remind_at'],
                    'recurring_interval': reminder['recurring_interval']
                }
            
            bot_logger.database_operation(
                "load", "reminders", True, 
                f"Loaded {len(reminders)} active reminders"
            )
            
        except Exception as e:
            bot_logger.error_occurred(e, "_load_active_reminders")
    
    async def _trigger_reminder(self, reminder: Dict):
        """Déclenche un rappel"""
        
        try:
            # Obtenir les objets Discord
            guild = self.bot.get_guild(reminder['guild_id'])
            if not guild:
                return
            
            user = guild.get_member(reminder['user_id'])
            if not user:
                return
            
            channel = guild.get_channel(reminder['channel_id'])
            
            # Créer l'embed du rappel
            embed = create_embed(
                title="🔔 Rappel",
                description=reminder['message'],
                color=self.config.COLOR_WARNING
            )
            
            embed.add_field(
                name="👤 Pour",
                value=user.mention,
                inline=True
            )
            
            embed.add_field(
                name="⏰ Programmé",
                value=f"<t:{int(reminder['remind_at'].timestamp())}:R>",
                inline=True
            )
            
            # Envoyer le rappel
            if channel and channel.permissions_for(guild.me).send_messages:
                # Rappel collectif dans le canal
                await channel.send(content=user.mention, embed=embed)
            else:
                # Rappel personnel en MP
                try:
                    await user.send(embed=embed)
                except discord.Forbidden:
                    # Si impossible d'envoyer en MP, essayer dans le canal de modération
                    guild_settings = await self.bot.db.get_guild_settings(guild.id)
                    mod_channel_id = guild_settings.get('mod_log_channel')
                    
                    if mod_channel_id:
                        mod_channel = guild.get_channel(mod_channel_id)
                        if mod_channel:
                            embed.set_footer(text="⚠️ Impossible d'envoyer en MP à l'utilisateur")
                            await mod_channel.send(content=user.mention, embed=embed)
            
            bot_logger.command_used(
                reminder['user_id'], reminder['guild_id'], "reminder_triggered",
                reminder_id=reminder['id']
            )
            
        except Exception as e:
            bot_logger.error_occurred(e, "_trigger_reminder")
    
    async def _schedule_next_occurrence(self, reminder: Dict):
        """Programme la prochaine occurrence d'un rappel récurrent"""
        
        try:
            # Calculer la prochaine date
            next_remind_at = reminder['remind_at'] + timedelta(seconds=reminder['recurring_interval'])
            
            # Mettre à jour en base de données
            async with self.bot.db.pool.acquire() as conn:
                await conn.execute('''
                    UPDATE reminders SET remind_at = $1 WHERE id = $2
                ''', next_remind_at, reminder['id'])
            
            # Mettre à jour le cache
            self.active_reminders[reminder['id']]['remind_at'] = next_remind_at
            
        except Exception as e:
            bot_logger.error_occurred(e, "_schedule_next_occurrence")
    
    async def _deactivate_reminder(self, reminder_id: int):
        """Désactive un rappel en base de données"""
        
        try:
            async with self.bot.db.pool.acquire() as conn:
                await conn.execute('''
                    UPDATE reminders SET is_active = FALSE WHERE id = $1
                ''', reminder_id)
                
        except Exception as e:
            bot_logger.error_occurred(e, "_deactivate_reminder")


async def setup(bot):
    await bot.add_cog(RemindersCog(bot))