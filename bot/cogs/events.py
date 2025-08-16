# -*- coding: utf-8 -*-
"""
Cog de gestion d'événements pour COPBOT v4.0
Système de création, gestion et RSVP d'événements
"""

import discord
from discord.ext import commands, tasks
from discord import app_commands
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import asyncio
from dateutil import parser as date_parser

from config.settings import BotConfig, ERROR_MESSAGES, SUCCESS_MESSAGES
from utils.helpers import create_embed, parse_duration, format_duration, ConfirmationView
from utils.logger import bot_logger


class EventRSVPView(discord.ui.View):
    """
    Vue pour les boutons RSVP des événements
    """
    
    def __init__(self, event_id: int):
        super().__init__(timeout=None)
        self.event_id = event_id
    
    @discord.ui.button(label="✅ Participer", style=discord.ButtonStyle.success, custom_id="event_join")
    async def join_event(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Bouton pour rejoindre l'événement"""
        await self._handle_rsvp(interaction, "attending")
    
    @discord.ui.button(label="❓ Peut-être", style=discord.ButtonStyle.secondary, custom_id="event_maybe")
    async def maybe_event(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Bouton pour indiquer une participation incertaine"""
        await self._handle_rsvp(interaction, "maybe")
    
    @discord.ui.button(label="❌ Décliner", style=discord.ButtonStyle.danger, custom_id="event_decline")
    async def decline_event(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Bouton pour décliner l'événement"""
        await self._handle_rsvp(interaction, "declined")
    
    async def _handle_rsvp(self, interaction: discord.Interaction, status: str):
        """Gère les réponses RSVP"""
        
        user_id = interaction.user.id
        
        try:
            # Obtenir le cog des événements
            events_cog = interaction.client.get_cog("Événements")
            if not events_cog:
                await interaction.response.send_message(
                    "❌ Erreur système. Veuillez réessayer.", ephemeral=True
                )
                return
            
            # Mettre à jour la participation
            await events_cog._update_event_participation(self.event_id, user_id, status)
            
            # Messages de confirmation
            messages = {
                "attending": "✅ Vous participez à cet événement !",
                "maybe": "❓ Votre participation est marquée comme incertaine.",
                "declined": "❌ Vous avez décliné cet événement."
            }
            
            await interaction.response.send_message(
                messages.get(status, "✅ Participation mise à jour."), 
                ephemeral=True
            )
            
            # Mettre à jour l'embed de l'événement
            await events_cog._update_event_message(interaction.message, self.event_id)
            
        except Exception as e:
            bot_logger.error_occurred(e, "_handle_rsvp")
            await interaction.response.send_message(
                "❌ Erreur lors de la mise à jour de votre participation.", ephemeral=True
            )


class EventModal(discord.ui.Modal, title="Créer un événement"):
    """
    Modal pour la création d'événements
    """
    
    def __init__(self):
        super().__init__()
    
    title_input = discord.ui.TextInput(
        label="Titre de l'événement",
        placeholder="Ex: Soirée jeux vidéo",
        max_length=200,
        required=True
    )
    
    description_input = discord.ui.TextInput(
        label="Description",
        placeholder="Décrivez votre événement...",
        style=discord.TextStyle.paragraph,
        max_length=1000,
        required=False
    )
    
    date_input = discord.ui.TextInput(
        label="Date et heure",
        placeholder="Ex: 2024-12-25 20:00 ou demain 19h",
        max_length=100,
        required=True
    )
    
    location_input = discord.ui.TextInput(
        label="Lieu (optionnel)",
        placeholder="Ex: Salon vocal Gaming ou Discord",
        max_length=200,
        required=False
    )
    
    max_participants_input = discord.ui.TextInput(
        label="Participants max (optionnel)",
        placeholder="Nombre maximum de participants",
        max_length=10,
        required=False
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        """Traitement de la soumission du modal"""
        
        try:
            # Parser la date
            try:
                event_date = self._parse_date(self.date_input.value)
            except ValueError as e:
                await interaction.response.send_message(
                    f"❌ Format de date invalide: {str(e)}", ephemeral=True
                )
                return
            
            # Vérifier que la date est dans le futur
            if event_date <= datetime.utcnow():
                await interaction.response.send_message(
                    "❌ L'événement doit avoir lieu dans le futur.", ephemeral=True
                )
                return
            
            # Parser le nombre maximum de participants
            max_participants = None
            if self.max_participants_input.value:
                try:
                    max_participants = int(self.max_participants_input.value)
                    if max_participants <= 0:
                        raise ValueError()
                except ValueError:
                    await interaction.response.send_message(
                        "❌ Le nombre de participants doit être un nombre entier positif.", 
                        ephemeral=True
                    )
                    return
            
            # Obtenir le cog des événements
            events_cog = interaction.client.get_cog("Événements")
            if not events_cog:
                await interaction.response.send_message(
                    "❌ Erreur système. Veuillez réessayer.", ephemeral=True
                )
                return
            
            # Créer l'événement
            event_id = await events_cog._create_event(
                guild_id=interaction.guild.id,
                creator_id=interaction.user.id,
                title=self.title_input.value,
                description=self.description_input.value or None,
                start_time=event_date,
                location=self.location_input.value or None,
                max_participants=max_participants
            )
            
            if event_id:
                # Créer l'embed de l'événement
                embed = await events_cog._create_event_embed(event_id)
                view = EventRSVPView(event_id)
                
                await interaction.response.send_message(
                    "✅ Événement créé avec succès !", embed=embed, view=view
                )
            else:
                await interaction.response.send_message(
                    "❌ Erreur lors de la création de l'événement.", ephemeral=True
                )
                
        except Exception as e:
            bot_logger.error_occurred(e, "event_modal_submit")
            await interaction.response.send_message(
                "❌ Erreur lors de la création de l'événement.", ephemeral=True
            )
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse une chaîne de date en objet datetime"""
        
        date_str = date_str.strip().lower()
        now = datetime.utcnow()
        
        # Raccourcis temporels
        if date_str in ["maintenant", "now"]:
            return now
        elif date_str in ["demain", "tomorrow"]:
            return now.replace(hour=20, minute=0, second=0, microsecond=0) + timedelta(days=1)
        elif date_str.startswith("dans "):
            # Format: "dans 2h", "dans 1j 3h"
            duration_str = date_str[5:]  # Retirer "dans "
            duration = parse_duration(duration_str)
            if duration:
                return now + timedelta(seconds=duration)
        
        # Essayer le parsing automatique
        try:
            return date_parser.parse(date_str, default=now)
        except Exception:
            raise ValueError("Format de date non reconnu. Utilisez un format comme '2024-12-25 20:00' ou 'demain 19h'")


class EventsCog(commands.Cog, name="Événements"):
    """
    Système de gestion d'événements avec RSVP
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.config = BotConfig()
        
        # Tâches périodiques
        self.check_event_reminders.start()
    
    def cog_unload(self):
        """Nettoyage lors du déchargement"""
        self.check_event_reminders.cancel()
    
    @tasks.loop(minutes=15)
    async def check_event_reminders(self):
        """Vérifie et envoie les rappels d'événements"""
        try:
            now = datetime.utcnow()
            reminder_time = now + timedelta(hours=1)  # Rappel 1h avant
            
            async with self.bot.db.pool.acquire() as conn:
                # Événements qui commencent dans 1h
                events = await conn.fetch('''
                    SELECT e.*, g.mod_log_channel
                    FROM events e
                    JOIN guild_settings g ON e.guild_id = g.guild_id
                    WHERE e.start_time BETWEEN $1 AND $2
                    AND e.start_time > NOW()
                ''', now, reminder_time)
                
                for event in events:
                    await self._send_event_reminder(event)
                    
        except Exception as e:
            bot_logger.error_occurred(e, "check_event_reminders")
    
    @check_event_reminders.before_loop
    async def before_check_reminders(self):
        await self.bot.wait_until_ready()
    
    # ==================== COMMANDES ====================
    
    @app_commands.command(name="evenement", description="Crée un nouvel événement")
    @commands.has_permissions(manage_events=True)
    async def create_event_command(self, interaction: discord.Interaction):
        """Commande pour créer un événement via modal"""
        
        modal = EventModal()
        await interaction.response.send_modal(modal)
    
    @app_commands.command(name="listevenements", description="Liste les événements à venir")
    async def list_events(self, interaction: discord.Interaction):
        """Liste tous les événements à venir du serveur"""
        
        try:
            async with self.bot.db.pool.acquire() as conn:
                events = await conn.fetch('''
                    SELECT * FROM events 
                    WHERE guild_id = $1 AND start_time > NOW()
                    ORDER BY start_time ASC
                    LIMIT 10
                ''', interaction.guild.id)
            
            if not events:
                embed = create_embed(
                    title="📅 Événements à venir",
                    description="Aucun événement prévu pour le moment.",
                    color=self.config.COLOR_INFO
                )
                await interaction.response.send_message(embed=embed)
                return
            
            embed = create_embed(
                title="📅 Événements à venir",
                description=f"{len(events)} événement(s) prévu(s)",
                color=self.config.COLOR_INFO
            )
            
            for event in events:
                # Compter les participants
                participant_count = await self._get_participant_count(event['id'])
                
                # Créateur
                creator = self.bot.get_user(event['creator_id'])
                creator_name = creator.display_name if creator else "Inconnu"
                
                # Informations de l'événement
                event_info = f"**Créateur:** {creator_name}\n"
                event_info += f"**Date:** <t:{int(event['start_time'].timestamp())}:F>\n"
                event_info += f"**Participants:** {participant_count}"
                
                if event['max_participants']:
                    event_info += f"/{event['max_participants']}"
                
                if event['location']:
                    event_info += f"\n**Lieu:** {event['location']}"
                
                embed.add_field(
                    name=f"🎉 {event['title']}",
                    value=event_info,
                    inline=False
                )
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            bot_logger.error_occurred(e, "list_events")
            await interaction.response.send_message(
                ERROR_MESSAGES['database_error'], ephemeral=True
            )
    
    @app_commands.command(name="infoevenement", description="Affiche les détails d'un événement")
    @app_commands.describe(event_id="ID de l'événement")
    async def event_info(self, interaction: discord.Interaction, event_id: int):
        """Affiche les informations détaillées d'un événement"""
        
        try:
            embed = await self._create_event_embed(event_id)
            if embed:
                view = EventRSVPView(event_id)
                await interaction.response.send_message(embed=embed, view=view)
            else:
                await interaction.response.send_message(
                    "❌ Événement introuvable.", ephemeral=True
                )
                
        except Exception as e:
            bot_logger.error_occurred(e, "event_info")
            await interaction.response.send_message(
                ERROR_MESSAGES['database_error'], ephemeral=True
            )
    
    @app_commands.command(name="supprimerevenement", description="Supprime un événement")
    @app_commands.describe(event_id="ID de l'événement à supprimer")
    @commands.has_permissions(manage_events=True)
    async def delete_event(self, interaction: discord.Interaction, event_id: int):
        """Supprime un événement"""
        
        try:
            # Vérifier que l'événement existe et appartient au serveur
            async with self.bot.db.pool.acquire() as conn:
                event = await conn.fetchrow('''
                    SELECT * FROM events 
                    WHERE id = $1 AND guild_id = $2
                ''', event_id, interaction.guild.id)
                
                if not event:
                    await interaction.response.send_message(
                        "❌ Événement introuvable.", ephemeral=True
                    )
                    return
                
                # Vérifier les permissions (créateur ou admin)
                if (event['creator_id'] != interaction.user.id and 
                    not interaction.user.guild_permissions.administrator):
                    await interaction.response.send_message(
                        "❌ Vous ne pouvez supprimer que vos propres événements.", 
                        ephemeral=True
                    )
                    return
                
                # Confirmation
                view = ConfirmationView(interaction.user)
                embed = create_embed(
                    title="Confirmation de suppression",
                    description=f"Êtes-vous sûr de vouloir supprimer l'événement **{event['title']}** ?",
                    color=self.config.COLOR_WARNING
                )
                
                await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
                await view.wait()
                
                if not view.result:
                    await interaction.edit_original_response(
                        content="Suppression annulée.", embed=None, view=None
                    )
                    return
                
                # Supprimer l'événement
                await conn.execute('DELETE FROM events WHERE id = $1', event_id)
                
                embed = create_embed(
                    title="Événement supprimé",
                    description=f"L'événement **{event['title']}** a été supprimé avec succès.",
                    color=self.config.COLOR_SUCCESS
                )
                
                await interaction.edit_original_response(embed=embed, view=None)
                
        except Exception as e:
            bot_logger.error_occurred(e, "delete_event")
            await interaction.followup.send(
                ERROR_MESSAGES['database_error'], ephemeral=True
            )
    
    # ==================== MÉTHODES UTILITAIRES ====================
    
    async def _create_event(self, guild_id: int, creator_id: int, title: str,
                           description: Optional[str], start_time: datetime,
                           location: Optional[str] = None, 
                           max_participants: Optional[int] = None) -> Optional[int]:
        """Crée un nouvel événement en base de données"""
        
        try:
            async with self.bot.db.pool.acquire() as conn:
                event_id = await conn.fetchval('''
                    INSERT INTO events (guild_id, creator_id, title, description, start_time, location, max_participants)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                    RETURNING id
                ''', guild_id, creator_id, title, description, start_time, location, max_participants)
                
                # Log de l'action
                bot_logger.command_used(
                    creator_id, guild_id, "create_event",
                    event_id=event_id, title=title
                )
                
                return event_id
                
        except Exception as e:
            bot_logger.error_occurred(e, "_create_event")
            return None
    
    async def _create_event_embed(self, event_id: int) -> Optional[discord.Embed]:
        """Crée l'embed d'affichage d'un événement"""
        
        try:
            async with self.bot.db.pool.acquire() as conn:
                event = await conn.fetchrow('SELECT * FROM events WHERE id = $1', event_id)
                
                if not event:
                    return None
                
                # Compter les participants par statut
                participants = await conn.fetch('''
                    SELECT status, COUNT(*) as count
                    FROM event_participants
                    WHERE event_id = $1
                    GROUP BY status
                ''', event_id)
                
                participant_counts = {row['status']: row['count'] for row in participants}
                attending = participant_counts.get('attending', 0)
                maybe = participant_counts.get('maybe', 0)
                declined = participant_counts.get('declined', 0)
                
                # Créateur
                creator = self.bot.get_user(event['creator_id'])
                creator_name = creator.display_name if creator else "Inconnu"
                
                # Embed principal
                embed = create_embed(
                    title=f"🎉 {event['title']}",
                    description=event['description'] or "Aucune description",
                    color=self.config.COLOR_INFO
                )
                
                # Informations temporelles
                embed.add_field(
                    name="📅 Date et heure",
                    value=f"<t:{int(event['start_time'].timestamp())}:F>\n"
                          f"<t:{int(event['start_time'].timestamp())}:R>",
                    inline=True
                )
                
                # Informations générales
                info_text = f"**Créateur:** {creator_name}"
                if event['location']:
                    info_text += f"\n**Lieu:** {event['location']}"
                
                embed.add_field(
                    name="ℹ️ Informations",
                    value=info_text,
                    inline=True
                )
                
                # Participants
                total_participants = attending + maybe
                participants_text = f"✅ **Participants:** {attending}"
                
                if event['max_participants']:
                    participants_text += f"/{event['max_participants']}"
                
                if maybe > 0:
                    participants_text += f"\n❓ **Incertains:** {maybe}"
                
                if declined > 0:
                    participants_text += f"\n❌ **Déclinés:** {declined}"
                
                embed.add_field(
                    name="👥 Participation",
                    value=participants_text,
                    inline=True
                )
                
                # Vérifier si l'événement est complet
                if event['max_participants'] and attending >= event['max_participants']:
                    embed.add_field(
                        name="⚠️ Statut",
                        value="**COMPLET** - Plus de places disponibles",
                        inline=False
                    )
                
                embed.set_footer(text=f"ID de l'événement: {event_id}")
                
                return embed
                
        except Exception as e:
            bot_logger.error_occurred(e, "_create_event_embed")
            return None
    
    async def _update_event_participation(self, event_id: int, user_id: int, status: str):
        """Met à jour la participation d'un utilisateur à un événement"""
        
        async with self.bot.db.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO event_participants (event_id, user_id, status)
                VALUES ($1, $2, $3)
                ON CONFLICT (event_id, user_id)
                DO UPDATE SET status = $3, joined_at = NOW()
            ''', event_id, user_id, status)
    
    async def _update_event_message(self, message: discord.Message, event_id: int):
        """Met à jour l'affichage d'un message d'événement"""
        
        try:
            embed = await self._create_event_embed(event_id)
            if embed:
                await message.edit(embed=embed)
        except Exception as e:
            bot_logger.error_occurred(e, "_update_event_message")
    
    async def _get_participant_count(self, event_id: int) -> int:
        """Obtient le nombre de participants confirmés à un événement"""
        
        async with self.bot.db.pool.acquire() as conn:
            count = await conn.fetchval('''
                SELECT COUNT(*) FROM event_participants
                WHERE event_id = $1 AND status = 'attending'
            ''', event_id)
            
            return count or 0
    
    async def _send_event_reminder(self, event_data: dict):
        """Envoie un rappel d'événement"""
        
        try:
            guild = self.bot.get_guild(event_data['guild_id'])
            if not guild:
                return
            
            # Canal de logs/annonces
            channel_id = event_data.get('mod_log_channel')
            if not channel_id:
                return
            
            channel = guild.get_channel(channel_id)
            if not channel:
                return
            
            # Créer l'embed de rappel
            embed = create_embed(
                title="⏰ Rappel d'événement",
                description=f"L'événement **{event_data['title']}** commence dans moins d'une heure !",
                color=self.config.COLOR_WARNING
            )
            
            embed.add_field(
                name="📅 Début",
                value=f"<t:{int(event_data['start_time'].timestamp())}:F>",
                inline=True
            )
            
            if event_data['location']:
                embed.add_field(
                    name="📍 Lieu",
                    value=event_data['location'],
                    inline=True
                )
            
            # Mentionner les participants
            async with self.bot.db.pool.acquire() as conn:
                participants = await conn.fetch('''
                    SELECT user_id FROM event_participants
                    WHERE event_id = $1 AND status = 'attending'
                ''', event_data['id'])
                
                if participants:
                    mentions = []
                    for p in participants[:20]:  # Limiter pour éviter les messages trop longs
                        user = guild.get_member(p['user_id'])
                        if user:
                            mentions.append(user.mention)
                    
                    if mentions:
                        embed.add_field(
                            name="👥 Participants",
                            value=" ".join(mentions),
                            inline=False
                        )
            
            await channel.send(embed=embed)
            
        except Exception as e:
            bot_logger.error_occurred(e, "_send_event_reminder")


async def setup(bot):
    await bot.add_cog(EventsCog(bot))