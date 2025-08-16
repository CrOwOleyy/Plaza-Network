# -*- coding: utf-8 -*-
"""
Cog de sondages pour COPBOT v4.0
Système de sondages avancés avec choix multiples et résultats détaillés
"""

import discord
from discord.ext import commands, tasks
from discord import app_commands
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import json
import asyncio

from config.settings import BotConfig, ERROR_MESSAGES, SUCCESS_MESSAGES
from utils.helpers import create_embed, parse_duration, format_duration, ConfirmationView
from utils.logger import bot_logger


class PollView(discord.ui.View):
    """
    Vue interactive pour les sondages
    """
    
    def __init__(self, poll_id: int, options: List[str], multiple_choice: bool = False):
        super().__init__(timeout=None)
        self.poll_id = poll_id
        self.multiple_choice = multiple_choice
        
        # Ajouter les boutons pour chaque option (max 25)
        for i, option in enumerate(options[:25]):
            style = discord.ButtonStyle.primary if i == 0 else discord.ButtonStyle.secondary
            self.add_item(PollButton(i, option, style))
        
        # Ajouter un bouton pour voir les résultats
        self.add_item(ResultsButton())


class PollButton(discord.ui.Button):
    """
    Bouton pour voter sur une option du sondage
    """
    
    def __init__(self, option_index: int, option_text: str, style: discord.ButtonStyle):
        self.option_index = option_index
        
        # Utiliser des émojis pour les options
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        emoji = emojis[option_index] if option_index < len(emojis) else "📊"
        
        super().__init__(
            style=style,
            label=option_text[:80],  # Limite Discord
            emoji=emoji,
            custom_id=f"poll_option_{option_index}"
        )
    
    async def callback(self, interaction: discord.Interaction):
        """Gère le vote sur cette option"""
        
        # Obtenir le cog des sondages
        polls_cog = interaction.client.get_cog("Sondages")
        if not polls_cog:
            await interaction.response.send_message(
                "❌ Erreur système. Veuillez réessayer.", ephemeral=True
            )
            return
        
        # Traiter le vote
        await polls_cog._handle_vote(interaction, self.view.poll_id, self.option_index)


class ResultsButton(discord.ui.Button):
    """
    Bouton pour afficher les résultats du sondage
    """
    
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.success,
            label="📊 Résultats",
            custom_id="poll_results"
        )
    
    async def callback(self, interaction: discord.Interaction):
        """Affiche les résultats du sondage"""
        
        # Obtenir le cog des sondages
        polls_cog = interaction.client.get_cog("Sondages")
        if not polls_cog:
            await interaction.response.send_message(
                "❌ Erreur système. Veuillez réessayer.", ephemeral=True
            )
            return
        
        # Afficher les résultats
        await polls_cog._show_results(interaction, self.view.poll_id)


class PollModal(discord.ui.Modal, title="Créer un sondage"):
    """
    Modal pour la création de sondages
    """
    
    def __init__(self):
        super().__init__()
    
    title_input = discord.ui.TextInput(
        label="Titre du sondage",
        placeholder="Ex: Quel jeu préférez-vous ?",
        max_length=200,
        required=True
    )
    
    options_input = discord.ui.TextInput(
        label="Options (une par ligne)",
        placeholder="Option 1\nOption 2\nOption 3\n...",
        style=discord.TextStyle.paragraph,
        max_length=1000,
        required=True
    )
    
    duration_input = discord.ui.TextInput(
        label="Durée (optionnel)",
        placeholder="Ex: 1h, 2d, 1w (vide = infini)",
        max_length=20,
        required=False
    )
    
    settings_input = discord.ui.TextInput(
        label="Paramètres (optionnel)",
        placeholder="multiple (choix multiples), anonymous (anonyme)",
        max_length=100,
        required=False
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        """Traitement de la soumission du modal"""
        
        try:
            # Parser les options
            options = [opt.strip() for opt in self.options_input.value.split('\n') if opt.strip()]
            
            if len(options) < 2:
                await interaction.response.send_message(
                    "❌ Un sondage doit avoir au moins 2 options.", ephemeral=True
                )
                return
            
            if len(options) > 25:
                await interaction.response.send_message(
                    "❌ Un sondage ne peut pas avoir plus de 25 options.", ephemeral=True
                )
                return
            
            # Parser la durée
            expires_at = None
            if self.duration_input.value:
                duration = parse_duration(self.duration_input.value)
                if not duration:
                    await interaction.response.send_message(
                        "❌ Format de durée invalide.", ephemeral=True
                    )
                    return
                expires_at = datetime.utcnow() + timedelta(seconds=duration)
            
            # Parser les paramètres
            settings = self.settings_input.value.lower() if self.settings_input.value else ""
            multiple_choice = "multiple" in settings
            anonymous = "anonymous" in settings or "anonyme" in settings
            
            # Obtenir le cog des sondages
            polls_cog = interaction.client.get_cog("Sondages")
            if not polls_cog:
                await interaction.response.send_message(
                    "❌ Erreur système. Veuillez réessayer.", ephemeral=True
                )
                return
            
            # Créer le sondage
            poll_id = await polls_cog._create_poll(
                guild_id=interaction.guild.id,
                creator_id=interaction.user.id,
                channel_id=interaction.channel.id,
                title=self.title_input.value,
                options=options,
                multiple_choice=multiple_choice,
                anonymous=anonymous,
                expires_at=expires_at
            )
            
            if poll_id:
                # Créer l'embed et la vue du sondage
                embed = await polls_cog._create_poll_embed(poll_id)
                view = PollView(poll_id, options, multiple_choice)
                
                # Envoyer le sondage et enregistrer l'ID du message
                message = await interaction.response.send_message(embed=embed, view=view)
                
                # Mettre à jour l'ID du message en base
                if hasattr(message, 'id'):
                    await polls_cog._update_poll_message_id(poll_id, message.id)
                else:
                    # Pour les interactions, récupérer le message après envoi
                    sent_message = await interaction.original_response()
                    await polls_cog._update_poll_message_id(poll_id, sent_message.id)
            else:
                await interaction.response.send_message(
                    "❌ Erreur lors de la création du sondage.", ephemeral=True
                )
                
        except Exception as e:
            bot_logger.error_occurred(e, "poll_modal_submit")
            await interaction.response.send_message(
                "❌ Erreur lors de la création du sondage.", ephemeral=True
            )


class PollsCog(commands.Cog, name="Sondages"):
    """
    Système de sondages avancés
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.config = BotConfig()
        
        # Tâches périodiques
        self.check_expired_polls.start()
    
    def cog_unload(self):
        """Nettoyage lors du déchargement"""
        self.check_expired_polls.cancel()
    
    @tasks.loop(minutes=10)
    async def check_expired_polls(self):
        """Vérifie et ferme les sondages expirés"""
        try:
            now = datetime.utcnow()
            
            async with self.bot.db.pool.acquire() as conn:
                # Sondages qui viennent d'expirer
                expired_polls = await conn.fetch('''
                    SELECT * FROM polls
                    WHERE expires_at <= $1 AND expires_at > $1 - INTERVAL '10 minutes'
                ''', now)
                
                for poll in expired_polls:
                    await self._close_poll(poll)
                    
        except Exception as e:
            bot_logger.error_occurred(e, "check_expired_polls")
    
    @check_expired_polls.before_loop
    async def before_check_expired_polls(self):
        await self.bot.wait_until_ready()
    
    # ==================== COMMANDES ====================
    
    @app_commands.command(name="sondage", description="Crée un nouveau sondage")
    @commands.has_permissions(manage_messages=True)
    async def create_poll_command(self, interaction: discord.Interaction):
        """Commande pour créer un sondage via modal"""
        
        modal = PollModal()
        await interaction.response.send_modal(modal)
    
    @app_commands.command(name="sondagerapide", description="Crée un sondage simple Oui/Non")
    @app_commands.describe(
        question="La question du sondage",
        duree="Durée du sondage (optionnel)"
    )
    @commands.has_permissions(manage_messages=True)
    async def quick_poll(self, interaction: discord.Interaction, question: str,
                        duree: Optional[str] = None):
        """Crée un sondage Oui/Non rapide"""
        
        # Parser la durée
        expires_at = None
        if duree:
            duration = parse_duration(duree)
            if not duration:
                await interaction.response.send_message(
                    "❌ Format de durée invalide.", ephemeral=True
                )
                return
            expires_at = datetime.utcnow() + timedelta(seconds=duration)
        
        try:
            # Créer le sondage
            poll_id = await self._create_poll(
                guild_id=interaction.guild.id,
                creator_id=interaction.user.id,
                channel_id=interaction.channel.id,
                title=question,
                options=["✅ Oui", "❌ Non"],
                multiple_choice=False,
                anonymous=False,
                expires_at=expires_at
            )
            
            if poll_id:
                # Créer l'embed et la vue
                embed = await self._create_poll_embed(poll_id)
                view = PollView(poll_id, ["✅ Oui", "❌ Non"], False)
                
                message = await interaction.response.send_message(embed=embed, view=view)
                
                # Mettre à jour l'ID du message
                sent_message = await interaction.original_response()
                await self._update_poll_message_id(poll_id, sent_message.id)
            else:
                await interaction.response.send_message(
                    "❌ Erreur lors de la création du sondage.", ephemeral=True
                )
                
        except Exception as e:
            bot_logger.error_occurred(e, "quick_poll")
            await interaction.response.send_message(
                "❌ Erreur lors de la création du sondage.", ephemeral=True
            )
    
    @app_commands.command(name="fermersondage", description="Ferme un sondage prématurément")
    @app_commands.describe(poll_id="ID du sondage à fermer")
    @commands.has_permissions(manage_messages=True)
    async def close_poll_command(self, interaction: discord.Interaction, poll_id: int):
        """Ferme un sondage avant son expiration"""
        
        try:
            async with self.bot.db.pool.acquire() as conn:
                poll = await conn.fetchrow('''
                    SELECT * FROM polls WHERE id = $1 AND guild_id = $2
                ''', poll_id, interaction.guild.id)
                
                if not poll:
                    await interaction.response.send_message(
                        "❌ Sondage introuvable.", ephemeral=True
                    )
                    return
                
                # Vérifier les permissions
                if (poll['creator_id'] != interaction.user.id and 
                    not interaction.user.guild_permissions.administrator):
                    await interaction.response.send_message(
                        "❌ Vous ne pouvez fermer que vos propres sondages.", ephemeral=True
                    )
                    return
                
                # Fermer le sondage
                await self._close_poll(poll)
                
                embed = create_embed(
                    title="🔒 Sondage fermé",
                    description=f"Le sondage **{poll['title']}** a été fermé manuellement.",
                    color=self.config.COLOR_SUCCESS
                )
                
                await interaction.response.send_message(embed=embed)
                
        except Exception as e:
            bot_logger.error_occurred(e, "close_poll_command")
            await interaction.response.send_message(
                ERROR_MESSAGES['database_error'], ephemeral=True
            )
    
    @app_commands.command(name="listesondages", description="Liste les sondages actifs")
    async def list_polls(self, interaction: discord.Interaction):
        """Liste tous les sondages actifs du serveur"""
        
        try:
            async with self.bot.db.pool.acquire() as conn:
                polls = await conn.fetch('''
                    SELECT * FROM polls 
                    WHERE guild_id = $1 AND (expires_at IS NULL OR expires_at > NOW())
                    ORDER BY created_at DESC
                    LIMIT 10
                ''', interaction.guild.id)
            
            if not polls:
                embed = create_embed(
                    title="📊 Sondages actifs",
                    description="Aucun sondage actif pour le moment.",
                    color=self.config.COLOR_INFO
                )
                await interaction.response.send_message(embed=embed)
                return
            
            embed = create_embed(
                title="📊 Sondages actifs",
                description=f"{len(polls)} sondage(s) en cours",
                color=self.config.COLOR_INFO
            )
            
            for poll in polls:
                # Créateur
                creator = self.bot.get_user(poll['creator_id'])
                creator_name = creator.display_name if creator else "Inconnu"
                
                # Compter les votes
                votes_data = json.loads(poll['votes'])
                total_votes = sum(len(voters) for voters in votes_data.values())
                
                # Informations du sondage
                poll_info = f"**Créateur:** {creator_name}\n"
                poll_info += f"**Votes:** {total_votes}\n"
                
                if poll['expires_at']:
                    poll_info += f"**Expire:** <t:{int(poll['expires_at'].timestamp())}:R>"
                else:
                    poll_info += f"**Durée:** Illimitée"
                
                embed.add_field(
                    name=f"#{poll['id']} - {poll['title']}",
                    value=poll_info,
                    inline=False
                )
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            bot_logger.error_occurred(e, "list_polls")
            await interaction.response.send_message(
                ERROR_MESSAGES['database_error'], ephemeral=True
            )
    
    # ==================== MÉTHODES UTILITAIRES ====================
    
    async def _create_poll(self, guild_id: int, creator_id: int, channel_id: int,
                          title: str, options: List[str], multiple_choice: bool = False,
                          anonymous: bool = False, expires_at: Optional[datetime] = None) -> Optional[int]:
        """Crée un nouveau sondage en base de données"""
        
        try:
            async with self.bot.db.pool.acquire() as conn:
                poll_id = await conn.fetchval('''
                    INSERT INTO polls (guild_id, creator_id, channel_id, title, options, 
                                     multiple_choice, anonymous, expires_at)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    RETURNING id
                ''', guild_id, creator_id, channel_id, title, json.dumps(options),
                multiple_choice, anonymous, expires_at)
                
                # Log de l'action
                bot_logger.command_used(
                    creator_id, guild_id, "create_poll",
                    poll_id=poll_id, title=title, options_count=len(options)
                )
                
                return poll_id
                
        except Exception as e:
            bot_logger.error_occurred(e, "_create_poll")
            return None
    
    async def _create_poll_embed(self, poll_id: int) -> Optional[discord.Embed]:
        """Crée l'embed d'affichage d'un sondage"""
        
        try:
            async with self.bot.db.pool.acquire() as conn:
                poll = await conn.fetchrow('SELECT * FROM polls WHERE id = $1', poll_id)
                
                if not poll:
                    return None
                
                # Créateur
                creator = self.bot.get_user(poll['creator_id'])
                creator_name = creator.display_name if creator else "Inconnu"
                
                # Options et votes
                options = json.loads(poll['options'])
                votes_data = json.loads(poll['votes'])
                
                # Calculer les statistiques
                total_votes = sum(len(voters) for voters in votes_data.values())
                
                # Embed principal
                embed = create_embed(
                    title=f"📊 {poll['title']}",
                    color=self.config.COLOR_INFO
                )
                
                # Afficher les options avec les résultats
                for i, option in enumerate(options):
                    voters = votes_data.get(str(i), [])
                    vote_count = len(voters)
                    percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
                    
                    # Barre de progression visuelle
                    bar_length = 20
                    filled_length = int(bar_length * percentage / 100)
                    bar = "█" * filled_length + "░" * (bar_length - filled_length)
                    
                    option_text = f"`{bar}` {percentage:.1f}% ({vote_count} vote{'s' if vote_count != 1 else ''})"
                    
                    embed.add_field(
                        name=f"{['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟'][i] if i < 10 else '📊'} {option}",
                        value=option_text,
                        inline=False
                    )
                
                # Informations générales
                info_text = f"**Créateur:** {creator_name}\n"
                info_text += f"**Total des votes:** {total_votes}\n"
                
                if poll['multiple_choice']:
                    info_text += "**Type:** Choix multiples\n"
                
                if poll['anonymous']:
                    info_text += "**Mode:** Anonyme\n"
                
                if poll['expires_at']:
                    info_text += f"**Expire:** <t:{int(poll['expires_at'].timestamp())}:R>"
                else:
                    info_text += "**Durée:** Illimitée"
                
                embed.add_field(
                    name="ℹ️ Informations",
                    value=info_text,
                    inline=False
                )
                
                embed.set_footer(text=f"ID du sondage: {poll_id} • Utilisez les boutons pour voter")
                
                return embed
                
        except Exception as e:
            bot_logger.error_occurred(e, "_create_poll_embed")
            return None
    
    async def _handle_vote(self, interaction: discord.Interaction, poll_id: int, option_index: int):
        """Gère le vote d'un utilisateur"""
        
        try:
            user_id = interaction.user.id
            
            async with self.bot.db.pool.acquire() as conn:
                poll = await conn.fetchrow('SELECT * FROM polls WHERE id = $1', poll_id)
                
                if not poll:
                    await interaction.response.send_message(
                        "❌ Sondage introuvable.", ephemeral=True
                    )
                    return
                
                # Vérifier si le sondage est toujours actif
                if poll['expires_at'] and poll['expires_at'] <= datetime.utcnow():
                    await interaction.response.send_message(
                        "❌ Ce sondage a expiré.", ephemeral=True
                    )
                    return
                
                # Charger les votes actuels
                votes_data = json.loads(poll['votes'])
                
                # Vérifier si l'utilisateur a déjà voté
                user_voted_options = []
                for opt_idx, voters in votes_data.items():
                    if user_id in voters:
                        user_voted_options.append(int(opt_idx))
                
                # Gerer le vote selon le type de sondage
                if not poll['multiple_choice']:
                    # Choix unique: retirer tous les anciens votes
                    for opt_idx in list(votes_data.keys()):
                        if user_id in votes_data[opt_idx]:
                            votes_data[opt_idx].remove(user_id)
                
                # Ajouter ou retirer le vote sur l'option sélectionnée
                option_key = str(option_index)
                if option_key not in votes_data:
                    votes_data[option_key] = []
                
                if user_id in votes_data[option_key]:
                    # Retirer le vote
                    votes_data[option_key].remove(user_id)
                    action = "retiré"
                else:
                    # Ajouter le vote
                    votes_data[option_key].append(user_id)
                    action = "ajouté"
                
                # Mettre à jour en base de données
                await conn.execute('''
                    UPDATE polls SET votes = $1 WHERE id = $2
                ''', json.dumps(votes_data), poll_id)
                
                # Message de confirmation
                options = json.loads(poll['options'])
                option_name = options[option_index]
                
                await interaction.response.send_message(
                    f"✅ Vote {action} pour **{option_name}**", ephemeral=True
                )
                
                # Mettre à jour l'affichage du sondage
                embed = await self._create_poll_embed(poll_id)
                if embed:
                    try:
                        await interaction.edit_original_response(embed=embed)
                    except:
                        # Si on ne peut pas éditer, on ignore silencieusement
                        pass
                
        except Exception as e:
            bot_logger.error_occurred(e, "_handle_vote")
            await interaction.response.send_message(
                "❌ Erreur lors du vote.", ephemeral=True
            )
    
    async def _show_results(self, interaction: discord.Interaction, poll_id: int):
        """Affiche les résultats détaillés d'un sondage"""
        
        try:
            async with self.bot.db.pool.acquire() as conn:
                poll = await conn.fetchrow('SELECT * FROM polls WHERE id = $1', poll_id)
                
                if not poll:
                    await interaction.response.send_message(
                        "❌ Sondage introuvable.", ephemeral=True
                    )
                    return
                
                # Préparer les données
                options = json.loads(poll['options'])
                votes_data = json.loads(poll['votes'])
                total_votes = sum(len(voters) for voters in votes_data.values())
                
                embed = create_embed(
                    title=f"📊 Résultats détaillés - {poll['title']}",
                    color=self.config.COLOR_INFO
                )
                
                # Afficher les résultats de chaque option
                for i, option in enumerate(options):
                    voters = votes_data.get(str(i), [])
                    vote_count = len(voters)
                    percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
                    
                    result_text = f"**{vote_count}** vote{'s' if vote_count != 1 else ''} ({percentage:.1f}%)"
                    
                    # Afficher les votants si le sondage n'est pas anonyme
                    if not poll['anonymous'] and voters:
                        guild = interaction.guild
                        voter_names = []
                        
                        for voter_id in voters[:10]:  # Limiter à 10 pour éviter les embeds trop longs
                            member = guild.get_member(voter_id)
                            if member:
                                voter_names.append(member.display_name)
                        
                        if voter_names:
                            result_text += f"\n*{', '.join(voter_names)}*"
                        
                        if len(voters) > 10:
                            result_text += f"\n*... et {len(voters) - 10} autre(s)*"
                    
                    embed.add_field(
                        name=f"{option}",
                        value=result_text,
                        inline=False
                    )
                
                embed.add_field(
                    name="📈 Statistiques",
                    value=f"**Total des votes:** {total_votes}\n"
                          f"**Sondage créé:** <t:{int(poll['created_at'].timestamp())}:R>\n"
                          f"**Type:** {'Choix multiples' if poll['multiple_choice'] else 'Choix unique'}\n"
                          f"**Mode:** {'Anonyme' if poll['anonymous'] else 'Public'}",
                    inline=False
                )
                
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
        except Exception as e:
            bot_logger.error_occurred(e, "_show_results")
            await interaction.response.send_message(
                "❌ Erreur lors de l'affichage des résultats.", ephemeral=True
            )
    
    async def _update_poll_message_id(self, poll_id: int, message_id: int):
        """Met à jour l'ID du message du sondage"""
        
        try:
            async with self.bot.db.pool.acquire() as conn:
                await conn.execute('''
                    UPDATE polls SET message_id = $1 WHERE id = $2
                ''', message_id, poll_id)
        except Exception as e:
            bot_logger.error_occurred(e, "_update_poll_message_id")
    
    async def _close_poll(self, poll_data: dict):
        """Ferme un sondage et affiche les résultats finaux"""
        
        try:
            guild = self.bot.get_guild(poll_data['guild_id'])
            if not guild:
                return
            
            channel = guild.get_channel(poll_data['channel_id'])
            if not channel:
                return
            
            # Obtenir le message du sondage
            if poll_data['message_id']:
                try:
                    message = await channel.fetch_message(poll_data['message_id'])
                    
                    # Créer l'embed de fermeture
                    embed = await self._create_poll_embed(poll_data['id'])
                    if embed:
                        embed.title += " [FERMÉ]"
                        embed.color = discord.Color.red()
                        embed.set_footer(text=f"Sondage fermé • ID: {poll_data['id']}")
                        
                        # Retirer les boutons
                        await message.edit(embed=embed, view=None)
                
                except discord.NotFound:
                    pass
            
            # Log de fermeture
            bot_logger.command_used(
                poll_data['creator_id'], poll_data['guild_id'], "poll_closed",
                poll_id=poll_data['id']
            )
            
        except Exception as e:
            bot_logger.error_occurred(e, "_close_poll")


async def setup(bot):
    await bot.add_cog(PollsCog(bot))