# -*- coding: utf-8 -*-
"""
Cog de modération pour COPBOT v4.0
Gestion des sanctions, avertissements et modération automatique
"""

import discord
from discord.ext import commands, tasks
from discord import app_commands
from typing import Optional, Union
from datetime import datetime, timedelta
import asyncio
import re

from config.settings import BotConfig, ERROR_MESSAGES, SUCCESS_MESSAGES
from utils.helpers import (
    parse_duration, format_duration, create_embed, 
    has_permissions, ConfirmationView, safe_send, get_member_safely
)
from utils.logger import bot_logger


class ModerationCog(commands.Cog, name="Modération"):
    """
    Commandes et fonctionnalités de modération
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.config = BotConfig()
        
        # Anti-spam tracking
        self.message_tracking = {}
        self.spam_warnings = {}
        
        # Tâches périodiques
        self.cleanup_expired_sanctions.start()
    
    def cog_unload(self):
        """Nettoyage lors du déchargement du cog"""
        self.cleanup_expired_sanctions.cancel()
    
    @tasks.loop(minutes=5)
    async def cleanup_expired_sanctions(self):
        """Nettoie les sanctions expirées"""
        try:
            # Cette tâche sera implémentée pour retirer automatiquement les mutes/bans temporaires
            pass
        except Exception as e:
            bot_logger.error_occurred(e, "cleanup_expired_sanctions")
    
    @cleanup_expired_sanctions.before_loop
    async def before_cleanup(self):
        await self.bot.wait_until_ready()
    
    # ==================== COMMANDES DE MODÉRATION ====================
    
    @app_commands.command(name="warn", description="Donne un avertissement à un utilisateur")
    @app_commands.describe(
        utilisateur="L'utilisateur à avertir",
        raison="Raison de l'avertissement"
    )
    async def warn_user(self, interaction: discord.Interaction, utilisateur: discord.Member, raison: str):
        """Commande pour avertir un utilisateur"""
        
        # Vérifications de permissions
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(ERROR_MESSAGES['no_permission'], ephemeral=True)
            return
        
        # Vérifications de base
        if utilisateur == interaction.user:
            await interaction.response.send_message(ERROR_MESSAGES['self_action'], ephemeral=True)
            return
        
        if utilisateur.bot:
            await interaction.response.send_message(ERROR_MESSAGES['bot_action'], ephemeral=True)
            return
        
        if utilisateur.top_role >= interaction.user.top_role and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(ERROR_MESSAGES['higher_role'], ephemeral=True)
            return
        
        try:
            # Ajouter l'avertissement en base
            await self.bot.db.add_warning(
                interaction.guild.id,
                utilisateur.id,
                interaction.user.id,
                raison
            )
            
            # Récupérer le nombre total d'avertissements
            warnings = await self.bot.db.get_user_warnings(interaction.guild.id, utilisateur.id)
            warning_count = len(warnings)
            
            # Créer l'embed de confirmation
            embed = create_embed(
                title="Avertissement donné",
                description=f"**Utilisateur:** {utilisateur.mention}\n"
                           f"**Modérateur:** {interaction.user.mention}\n"
                           f"**Raison:** {raison}\n"
                           f"**Total d'avertissements:** {warning_count}",
                color=self.config.COLOR_WARNING
            )
            
            await interaction.response.send_message(embed=embed)
            
            # Notifier l'utilisateur par MP
            try:
                user_embed = create_embed(
                    title=f"Avertissement reçu - {interaction.guild.name}",
                    description=f"**Raison:** {raison}\n"
                               f"**Modérateur:** {interaction.user}\n"
                               f"**Total d'avertissements:** {warning_count}",
                    color=self.config.COLOR_WARNING
                )
                await safe_send(utilisateur, embed=user_embed)
            except:
                pass
            
            # Vérifier si sanctions automatiques nécessaires
            guild_settings = await self.bot.db.get_guild_settings(interaction.guild.id)
            max_warnings = guild_settings.get('max_warnings', 3)
            
            if warning_count >= max_warnings:
                # Sanctions automatiques après trop d'avertissements
                await self._apply_automatic_sanction(interaction.guild, utilisateur, interaction.user, warning_count)
            
            # Log de l'action
            bot_logger.moderation_action(
                interaction.user.id, utilisateur.id, "warn", 
                interaction.guild.id, raison
            )
            
        except Exception as e:
            bot_logger.error_occurred(e, "warn_user")
            await interaction.followup.send(ERROR_MESSAGES['database_error'], ephemeral=True)
    
    @app_commands.command(name="mute", description="Met un utilisateur en sourdine")
    @app_commands.describe(
        utilisateur="L'utilisateur à mettre en sourdine",
        durée="Durée du mute (ex: 1h30m, 2d)",
        raison="Raison du mute"
    )
    async def mute_user(self, interaction: discord.Interaction, utilisateur: discord.Member, 
                       durée: Optional[str] = None, raison: str = "Aucune raison spécifiée"):
        """Commande pour mettre un utilisateur en sourdine"""
        
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(ERROR_MESSAGES['no_permission'], ephemeral=True)
            return
        
        # Vérifications de base
        if utilisateur == interaction.user:
            await interaction.response.send_message(ERROR_MESSAGES['self_action'], ephemeral=True)
            return
        
        if utilisateur.bot:
            await interaction.response.send_message(ERROR_MESSAGES['bot_action'], ephemeral=True)
            return
        
        if utilisateur.top_role >= interaction.user.top_role and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(ERROR_MESSAGES['higher_role'], ephemeral=True)
            return
        
        # Parser la durée
        duration_seconds = None
        if durée:
            duration_seconds = parse_duration(durée)
            if duration_seconds is None:
                await interaction.response.send_message(ERROR_MESSAGES['invalid_duration'], ephemeral=True)
                return
        else:
            duration_seconds = self.config.default_mute_duration
        
        try:
            # Vérifier si déjà mute
            active_mutes = await self.bot.db.get_active_sanctions(
                interaction.guild.id, utilisateur.id, "mute"
            )
            
            if active_mutes:
                await interaction.response.send_message(ERROR_MESSAGES['already_muted'], ephemeral=True)
                return
            
            # Obtenir ou créer le rôle "Muted"
            mute_role = await self._get_or_create_mute_role(interaction.guild)
            if not mute_role:
                await interaction.response.send_message(
                    "❌ Impossible de créer le rôle de sourdine. Vérifiez les permissions du bot.",
                    ephemeral=True
                )
                return
            
            # Appliquer le rôle
            await utilisateur.add_roles(mute_role, reason=f"Mute par {interaction.user}: {raison}")
            
            # Enregistrer en base
            sanction_id = await self.bot.db.add_sanction(
                interaction.guild.id,
                utilisateur.id,
                interaction.user.id,
                "mute",
                raison,
                duration_seconds
            )
            
            # Créer l'embed de confirmation
            duration_text = format_duration(duration_seconds) if duration_seconds else "Indéfini"
            
            embed = create_embed(
                title="Utilisateur mis en sourdine",
                description=f"**Utilisateur:** {utilisateur.mention}\n"
                           f"**Modérateur:** {interaction.user.mention}\n"
                           f"**Durée:** {duration_text}\n"
                           f"**Raison:** {raison}",
                color=self.config.COLOR_WARNING
            )
            
            await interaction.response.send_message(embed=embed)
            
            # Notifier l'utilisateur
            try:
                user_embed = create_embed(
                    title=f"Mis en sourdine - {interaction.guild.name}",
                    description=f"**Durée:** {duration_text}\n"
                               f"**Raison:** {raison}\n"
                               f"**Modérateur:** {interaction.user}",
                    color=self.config.COLOR_WARNING
                )
                await safe_send(utilisateur, embed=user_embed)
            except:
                pass
            
            # Programmer le unmute automatique si durée définie
            if duration_seconds:
                await asyncio.sleep(duration_seconds)
                await self._auto_unmute(interaction.guild, utilisateur, sanction_id)
            
            # Log de l'action
            bot_logger.moderation_action(
                interaction.user.id, utilisateur.id, "mute",
                interaction.guild.id, raison
            )
            
        except Exception as e:
            bot_logger.error_occurred(e, "mute_user")
            await interaction.followup.send(ERROR_MESSAGES['database_error'], ephemeral=True)
    
    @app_commands.command(name="unmute", description="Retire la sourdine d'un utilisateur")
    @app_commands.describe(
        utilisateur="L'utilisateur à démuter",
        raison="Raison du démute"
    )
    async def unmute_user(self, interaction: discord.Interaction, utilisateur: discord.Member,
                         raison: str = "Aucune raison spécifiée"):
        """Commande pour retirer la sourdine d'un utilisateur"""
        
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(ERROR_MESSAGES['no_permission'], ephemeral=True)
            return
        
        try:
            # Vérifier si l'utilisateur est mute
            active_mutes = await self.bot.db.get_active_sanctions(
                interaction.guild.id, utilisateur.id, "mute"
            )
            
            if not active_mutes:
                await interaction.response.send_message(ERROR_MESSAGES['not_muted'], ephemeral=True)
                return
            
            # Retirer le rôle mute
            guild_settings = await self.bot.db.get_guild_settings(interaction.guild.id)
            mute_role_id = guild_settings.get('mute_role')
            
            if mute_role_id:
                mute_role = interaction.guild.get_role(mute_role_id)
                if mute_role and mute_role in utilisateur.roles:
                    await utilisateur.remove_roles(mute_role, reason=f"Unmute par {interaction.user}: {raison}")
            
            # Retirer les sanctions actives
            for mute in active_mutes:
                await self.bot.db.remove_sanction(mute['id'])
            
            # Créer l'embed de confirmation
            embed = create_embed(
                title="Sourdine retirée",
                description=f"**Utilisateur:** {utilisateur.mention}\n"
                           f"**Modérateur:** {interaction.user.mention}\n"
                           f"**Raison:** {raison}",
                color=self.config.COLOR_SUCCESS
            )
            
            await interaction.response.send_message(embed=embed)
            
            # Log de l'action
            bot_logger.moderation_action(
                interaction.user.id, utilisateur.id, "unmute",
                interaction.guild.id, raison
            )
            
        except Exception as e:
            bot_logger.error_occurred(e, "unmute_user")
            await interaction.followup.send(ERROR_MESSAGES['database_error'], ephemeral=True)
    
    @app_commands.command(name="ban", description="Bannit un utilisateur du serveur")
    @app_commands.describe(
        utilisateur="L'utilisateur à bannir",
        durée="Durée du ban (optionnel, ex: 7d)",
        supprimer_messages="Nombre de jours de messages à supprimer (0-7)",
        raison="Raison du bannissement"
    )
    async def ban_user(self, interaction: discord.Interaction, utilisateur: Union[discord.Member, discord.User],
                      durée: Optional[str] = None, supprimer_messages: int = 1,
                      raison: str = "Aucune raison spécifiée"):
        """Commande pour bannir un utilisateur"""
        
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message(ERROR_MESSAGES['no_permission'], ephemeral=True)
            return
        
        # Vérifications pour les membres présents sur le serveur
        if isinstance(utilisateur, discord.Member):
            if utilisateur == interaction.user:
                await interaction.response.send_message(ERROR_MESSAGES['self_action'], ephemeral=True)
                return
            
            if utilisateur.top_role >= interaction.user.top_role and not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message(ERROR_MESSAGES['higher_role'], ephemeral=True)
                return
        
        # Validation de la suppression de messages
        if supprimer_messages < 0 or supprimer_messages > 7:
            await interaction.response.send_message(
                "❌ Le nombre de jours de messages à supprimer doit être entre 0 et 7.",
                ephemeral=True
            )
            return
        
        # Parser la durée si fournie
        duration_seconds = None
        if durée:
            duration_seconds = parse_duration(durée)
            if duration_seconds is None:
                await interaction.response.send_message(ERROR_MESSAGES['invalid_duration'], ephemeral=True)
                return
        
        try:
            # Confirmation pour un ban permanent
            if duration_seconds is None:
                view = ConfirmationView(interaction.user)
                confirm_embed = create_embed(
                    title="Confirmation de bannissement",
                    description=f"Êtes-vous sûr de vouloir bannir **{utilisateur}** de manière permanente ?\n\n"
                               f"**Raison:** {raison}",
                    color=self.config.COLOR_WARNING
                )
                
                await interaction.response.send_message(embed=confirm_embed, view=view, ephemeral=True)
                await view.wait()
                
                if not view.result:
                    await interaction.edit_original_response(
                        content="Bannissement annulé.", embed=None, view=None
                    )
                    return
            else:
                await interaction.response.defer()
            
            # Exécuter le ban
            await interaction.guild.ban(
                utilisateur,
                reason=f"Ban par {interaction.user}: {raison}",
                delete_message_days=supprimer_messages
            )
            
            # Enregistrer en base si c'est temporaire
            if duration_seconds:
                await self.bot.db.add_sanction(
                    interaction.guild.id,
                    utilisateur.id,
                    interaction.user.id,
                    "ban",
                    raison,
                    duration_seconds
                )
            
            # Créer l'embed de confirmation
            duration_text = format_duration(duration_seconds) if duration_seconds else "Permanent"
            
            embed = create_embed(
                title="Utilisateur banni",
                description=f"**Utilisateur:** {utilisateur}\n"
                           f"**Modérateur:** {interaction.user.mention}\n"
                           f"**Durée:** {duration_text}\n"
                           f"**Messages supprimés:** {supprimer_messages} jour(s)\n"
                           f"**Raison:** {raison}",
                color=self.config.COLOR_ERROR
            )
            
            if interaction.response.is_done():
                await interaction.edit_original_response(embed=embed, view=None)
            else:
                await interaction.response.send_message(embed=embed)
            
            # Programmer le unban automatique si durée définie
            if duration_seconds:
                await asyncio.sleep(duration_seconds)
                await self._auto_unban(interaction.guild, utilisateur)
            
            # Log de l'action
            bot_logger.moderation_action(
                interaction.user.id, utilisateur.id, "ban",
                interaction.guild.id, raison
            )
            
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ Je n'ai pas la permission de bannir cet utilisateur.",
                ephemeral=True
            )
        except Exception as e:
            bot_logger.error_occurred(e, "ban_user")
            await interaction.followup.send(ERROR_MESSAGES['database_error'], ephemeral=True)
    
    # ==================== MÉTHODES UTILITAIRES ====================
    
    async def _get_or_create_mute_role(self, guild: discord.Guild) -> Optional[discord.Role]:
        """Obtient ou crée le rôle de sourdine"""
        
        # Vérifier s'il existe déjà en base
        guild_settings = await self.bot.db.get_guild_settings(guild.id)
        mute_role_id = guild_settings.get('mute_role')
        
        if mute_role_id:
            mute_role = guild.get_role(mute_role_id)
            if mute_role:
                return mute_role
        
        # Chercher un rôle existant
        for role in guild.roles:
            if role.name.lower() in ['muted', 'muet', 'silencé']:
                await self.bot.db.update_guild_setting(guild.id, 'mute_role', role.id)
                return role
        
        # Créer le rôle
        try:
            mute_role = await guild.create_role(
                name="Muted",
                color=discord.Color.dark_grey(),
                reason="Rôle de sourdine automatique créé par COPBOT"
            )
            
            # Configurer les permissions dans tous les salons
            for channel in guild.channels:
                try:
                    if isinstance(channel, discord.TextChannel):
                        await channel.set_permissions(
                            mute_role,
                            send_messages=False,
                            add_reactions=False,
                            create_public_threads=False,
                            create_private_threads=False
                        )
                    elif isinstance(channel, discord.VoiceChannel):
                        await channel.set_permissions(
                            mute_role,
                            speak=False,
                            stream=False
                        )
                except discord.Forbidden:
                    continue
            
            # Sauvegarder en base
            await self.bot.db.update_guild_setting(guild.id, 'mute_role', mute_role.id)
            return mute_role
            
        except discord.Forbidden:
            return None
    
    async def _apply_automatic_sanction(self, guild: discord.Guild, user: discord.Member, 
                                      moderator: discord.Member, warning_count: int):
        """Applique des sanctions automatiques après trop d'avertissements"""
        
        if warning_count == 3:
            # Premier dépassement: mute 1 heure
            await self._auto_mute(guild, user, moderator, 3600, "Trop d'avertissements")
        elif warning_count == 5:
            # Deuxième dépassement: mute 1 jour
            await self._auto_mute(guild, user, moderator, 86400, "Persistance des infractions")
        elif warning_count >= 7:
            # Troisième dépassement: ban temporaire 3 jours
            await self._auto_ban(guild, user, moderator, 259200, "Récidive répétée")
    
    async def _auto_mute(self, guild: discord.Guild, user: discord.Member, 
                        moderator: discord.Member, duration: int, reason: str):
        """Mute automatique"""
        try:
            mute_role = await self._get_or_create_mute_role(guild)
            if mute_role:
                await user.add_roles(mute_role, reason=f"Sanction automatique: {reason}")
                
                await self.bot.db.add_sanction(
                    guild.id, user.id, moderator.id, "mute", reason, duration
                )
                
                bot_logger.moderation_action(
                    moderator.id, user.id, "auto_mute", guild.id, reason
                )
        except Exception as e:
            bot_logger.error_occurred(e, "_auto_mute")
    
    async def _auto_ban(self, guild: discord.Guild, user: discord.Member,
                       moderator: discord.Member, duration: int, reason: str):
        """Ban automatique temporaire"""
        try:
            await guild.ban(user, reason=f"Sanction automatique: {reason}")
            
            await self.bot.db.add_sanction(
                guild.id, user.id, moderator.id, "ban", reason, duration
            )
            
            bot_logger.moderation_action(
                moderator.id, user.id, "auto_ban", guild.id, reason
            )
        except Exception as e:
            bot_logger.error_occurred(e, "_auto_ban")
    
    async def _auto_unmute(self, guild: discord.Guild, user: discord.Member, sanction_id: int):
        """Unmute automatique après expiration"""
        try:
            guild_settings = await self.bot.db.get_guild_settings(guild.id)
            mute_role_id = guild_settings.get('mute_role')
            
            if mute_role_id:
                mute_role = guild.get_role(mute_role_id)
                if mute_role and mute_role in user.roles:
                    await user.remove_roles(mute_role, reason="Fin de la sanction")
            
            await self.bot.db.remove_sanction(sanction_id)
            
            bot_logger.moderation_action(
                self.bot.user.id, user.id, "auto_unmute", guild.id, "Expiration"
            )
        except Exception as e:
            bot_logger.error_occurred(e, "_auto_unmute")
    
    async def _auto_unban(self, guild: discord.Guild, user: Union[discord.User, discord.Member]):
        """Unban automatique après expiration"""
        try:
            await guild.unban(user, reason="Fin de la sanction temporaire")
            
            bot_logger.moderation_action(
                self.bot.user.id, user.id, "auto_unban", guild.id, "Expiration"
            )
        except Exception as e:
            bot_logger.error_occurred(e, "_auto_unban")


async def setup(bot):
    await bot.add_cog(ModerationCog(bot))