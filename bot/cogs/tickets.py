# -*- coding: utf-8 -*-
"""
Cog de tickets de support pour COPBOT v4.0
Système complet de tickets avec création, assignation et transcripts
"""

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional, List
from datetime import datetime
import io
import asyncio

from config.settings import BotConfig, ERROR_MESSAGES, SUCCESS_MESSAGES
from utils.helpers import create_embed, ConfirmationView, safe_send
from utils.logger import bot_logger


class TicketCreateView(discord.ui.View):
    """
    Vue persistante pour la création de tickets
    """
    
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.select(
        placeholder="Choisissez une catégorie...",
        options=[
            discord.SelectOption(
                label="🛠️ Support Technique",
                description="Problèmes techniques et bugs",
                value="tech_support",
                emoji="🛠️"
            ),
            discord.SelectOption(
                label="❓ Question Générale",
                description="Questions sur le serveur",
                value="general_question",
                emoji="❓"
            ),
            discord.SelectOption(
                label="🚨 Signalement",
                description="Signaler un utilisateur ou un problème",
                value="report",
                emoji="🚨"
            ),
            discord.SelectOption(
                label="💡 Suggestion",
                description="Proposer une amélioration",
                value="suggestion",
                emoji="💡"
            ),
            discord.SelectOption(
                label="🎮 Autre",
                description="Autre demande",
                value="other",
                emoji="🎮"
            )
        ],
        custom_id="ticket_category_select"
    )
    async def select_category(self, interaction: discord.Interaction, select: discord.ui.Select):
        """Gère la sélection de catégorie de ticket"""
        
        category = select.values[0]
        
        # Obtenir le cog des tickets
        tickets_cog = interaction.client.get_cog("Tickets")
        if not tickets_cog:
            await interaction.response.send_message(
                "❌ Erreur système. Veuillez réessayer.", ephemeral=True
            )
            return
        
        # Créer le ticket
        await tickets_cog._create_ticket(interaction, category)


class TicketControlView(discord.ui.View):
    """
    Vue de contrôle pour les tickets (fermer, assigner, etc.)
    """
    
    def __init__(self, ticket_id: int):
        super().__init__(timeout=None)
        self.ticket_id = ticket_id
    
    @discord.ui.button(label="🔒 Fermer", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Bouton pour fermer le ticket"""
        
        # Obtenir le cog des tickets
        tickets_cog = interaction.client.get_cog("Tickets")
        if not tickets_cog:
            await interaction.response.send_message(
                "❌ Erreur système. Veuillez réessayer.", ephemeral=True
            )
            return
        
        await tickets_cog._close_ticket_interaction(interaction, self.ticket_id)
    
    @discord.ui.button(label="📝 Transcript", style=discord.ButtonStyle.secondary, custom_id="transcript_ticket")
    async def transcript_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Bouton pour générer un transcript"""
        
        # Obtenir le cog des tickets
        tickets_cog = interaction.client.get_cog("Tickets")
        if not tickets_cog:
            await interaction.response.send_message(
                "❌ Erreur système. Veuillez réessayer.", ephemeral=True
            )
            return
        
        await tickets_cog._generate_transcript(interaction, self.ticket_id)
    
    @discord.ui.button(label="👤 Assigner", style=discord.ButtonStyle.primary, custom_id="assign_ticket")
    async def assign_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Bouton pour s'assigner le ticket"""
        
        # Obtenir le cog des tickets
        tickets_cog = interaction.client.get_cog("Tickets")
        if not tickets_cog:
            await interaction.response.send_message(
                "❌ Erreur système. Veuillez réessayer.", ephemeral=True
            )
            return
        
        await tickets_cog._assign_ticket(interaction, self.ticket_id)


class TicketsCog(commands.Cog, name="Tickets"):
    """
    Système de tickets de support complet
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.config = BotConfig()
        
        # Emojis pour les catégories
        self.category_emojis = {
            "tech_support": "🛠️",
            "general_question": "❓",
            "report": "🚨",
            "suggestion": "💡",
            "other": "🎮"
        }
        
        # Noms des catégories
        self.category_names = {
            "tech_support": "Support Technique",
            "general_question": "Question Générale",
            "report": "Signalement",
            "suggestion": "Suggestion",
            "other": "Autre"
        }
    
    # ==================== COMMANDES ====================
    
    @app_commands.command(name="setuptickets", description="Configure le système de tickets")
    @app_commands.describe(
        canal="Canal où sera envoyé le message de création de tickets",
        categorie="Catégorie où créer les salons de tickets"
    )
    @commands.has_permissions(manage_guild=True)
    async def setup_tickets(self, interaction: discord.Interaction, 
                           canal: discord.TextChannel, 
                           categorie: Optional[discord.CategoryChannel] = None):
        """Configure le système de tickets"""
        
        try:
            # Créer l'embed de présentation
            embed = create_embed(
                title="🎫 Système de Tickets",
                description="**Besoin d'aide ?** Créez un ticket de support !\n\n"
                           "Choisissez une catégorie ci-dessous pour créer votre ticket privé. "
                           "Un membre de l'équipe vous aidera dès que possible.\n\n"
                           "**Types de tickets disponibles :**\n"
                           "🛠️ **Support Technique** - Problèmes techniques et bugs\n"
                           "❓ **Question Générale** - Questions sur le serveur\n"
                           "🚨 **Signalement** - Signaler un utilisateur ou un problème\n"
                           "💡 **Suggestion** - Proposer une amélioration\n"
                           "🎮 **Autre** - Autre demande",
                color=self.config.COLOR_INFO
            )
            
            embed.set_footer(text="Les tickets sont privés et seuls vous et l'équipe pouvez les voir")
            
            # Créer la vue avec le menu de sélection
            view = TicketCreateView()
            
            # Envoyer le message dans le canal spécifié
            await canal.send(embed=embed, view=view)
            
            # Sauvegarder la configuration
            await self.bot.db.update_guild_setting(
                interaction.guild.id, 'tickets_channel', canal.id
            )
            
            if categorie:
                await self.bot.db.update_guild_setting(
                    interaction.guild.id, 'tickets_category', categorie.id
                )
            
            # Confirmation
            config_embed = create_embed(
                title="✅ Système de tickets configuré",
                description=f"**Canal de création :** {canal.mention}\n"
                           f"**Catégorie des tickets :** {categorie.mention if categorie else 'Par défaut'}",
                color=self.config.COLOR_SUCCESS
            )
            
            await interaction.response.send_message(embed=config_embed, ephemeral=True)
            
        except Exception as e:
            bot_logger.error_occurred(e, "setup_tickets")
            await interaction.response.send_message(
                ERROR_MESSAGES['database_error'], ephemeral=True
            )
    
    @app_commands.command(name="listetickets", description="Liste tous les tickets ouverts")
    @commands.has_permissions(manage_messages=True)
    async def list_tickets(self, interaction: discord.Interaction):
        """Liste tous les tickets ouverts du serveur"""
        
        try:
            async with self.bot.db.pool.acquire() as conn:
                tickets = await conn.fetch('''
                    SELECT * FROM tickets 
                    WHERE guild_id = $1 AND status = 'open'
                    ORDER BY created_at DESC
                ''', interaction.guild.id)
            
            if not tickets:
                embed = create_embed(
                    title="🎫 Tickets ouverts",
                    description="Aucun ticket ouvert actuellement.",
                    color=self.config.COLOR_INFO
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            embed = create_embed(
                title="🎫 Tickets ouverts",
                description=f"{len(tickets)} ticket(s) ouvert(s)",
                color=self.config.COLOR_INFO
            )
            
            for ticket in tickets[:10]:  # Limiter à 10
                # Utilisateur
                user = self.bot.get_user(ticket['user_id'])
                user_name = user.display_name if user else "Utilisateur inconnu"
                
                # Assigné à
                assigned_to = None
                if ticket['assigned_to']:
                    assigned_to = self.bot.get_user(ticket['assigned_to'])
                
                # Canal
                channel = interaction.guild.get_channel(ticket['channel_id'])
                channel_mention = channel.mention if channel else "Canal supprimé"
                
                # Informations
                ticket_info = f"**Utilisateur :** {user_name}\n"
                ticket_info += f"**Canal :** {channel_mention}\n"
                ticket_info += f"**Catégorie :** {self.category_names.get(ticket['category'], 'Autre')}\n"
                
                if assigned_to:
                    ticket_info += f"**Assigné à :** {assigned_to.display_name}\n"
                
                ticket_info += f"**Créé :** <t:{int(ticket['created_at'].timestamp())}:R>"
                
                embed.add_field(
                    name=f"🎫 Ticket #{ticket['id']}",
                    value=ticket_info,
                    inline=False
                )
            
            if len(tickets) > 10:
                embed.set_footer(text=f"Affichage de 10/{len(tickets)} tickets")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except Exception as e:
            bot_logger.error_occurred(e, "list_tickets")
            await interaction.response.send_message(
                ERROR_MESSAGES['database_error'], ephemeral=True
            )
    
    @app_commands.command(name="fermerticket", description="Ferme le ticket actuel")
    @commands.has_permissions(manage_messages=True)
    async def close_ticket_command(self, interaction: discord.Interaction):
        """Ferme le ticket dans le canal actuel"""
        
        try:
            # Vérifier si c'est un canal de ticket
            async with self.bot.db.pool.acquire() as conn:
                ticket = await conn.fetchrow('''
                    SELECT * FROM tickets 
                    WHERE channel_id = $1 AND status = 'open'
                ''', interaction.channel.id)
                
                if not ticket:
                    await interaction.response.send_message(
                        "❌ Ce canal n'est pas un ticket ouvert.", ephemeral=True
                    )
                    return
                
                # Fermer le ticket
                await self._close_ticket(ticket, interaction.user)
                
                embed = create_embed(
                    title="🔒 Ticket fermé",
                    description="Ce ticket a été fermé. Le canal sera supprimé dans 10 secondes.",
                    color=self.config.COLOR_SUCCESS
                )
                
                await interaction.response.send_message(embed=embed)
                
        except Exception as e:
            bot_logger.error_occurred(e, "close_ticket_command")
            await interaction.response.send_message(
                ERROR_MESSAGES['database_error'], ephemeral=True
            )
    
    # ==================== MÉTHODES UTILITAIRES ====================
    
    async def _create_ticket(self, interaction: discord.Interaction, category: str):
        """Crée un nouveau ticket"""
        
        try:
            # Vérifier si l'utilisateur a déjà un ticket ouvert
            async with self.bot.db.pool.acquire() as conn:
                existing_ticket = await conn.fetchrow('''
                    SELECT * FROM tickets 
                    WHERE guild_id = $1 AND user_id = $2 AND status = 'open'
                ''', interaction.guild.id, interaction.user.id)
                
                if existing_ticket:
                    channel = interaction.guild.get_channel(existing_ticket['channel_id'])
                    if channel:
                        await interaction.response.send_message(
                            f"❌ Vous avez déjà un ticket ouvert : {channel.mention}",
                            ephemeral=True
                        )
                    else:
                        # Canal supprimé, nettoyer la base
                        await conn.execute('DELETE FROM tickets WHERE id = $1', existing_ticket['id'])
                        await interaction.response.send_message(
                            "❌ Erreur avec votre ticket existant. Veuillez réessayer.",
                            ephemeral=True
                        )
                    return
            
            # Obtenir la configuration
            guild_settings = await self.bot.db.get_guild_settings(interaction.guild.id)
            tickets_category_id = guild_settings.get('tickets_category')
            
            # Obtenir la catégorie
            tickets_category = None
            if tickets_category_id:
                tickets_category = interaction.guild.get_channel(tickets_category_id)
            
            # Créer le salon de ticket
            category_emoji = self.category_emojis.get(category, "🎫")
            category_name = self.category_names.get(category, "Autre")
            
            channel_name = f"ticket-{interaction.user.display_name.lower()}"
            
            # Permissions du salon
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                ),
                interaction.guild.me: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    manage_messages=True,
                    embed_links=True
                )
            }
            
            # Ajouter les permissions pour les modérateurs
            for role in interaction.guild.roles:
                if role.permissions.manage_messages or role.permissions.administrator:
                    overwrites[role] = discord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=True,
                        read_message_history=True
                    )
            
            # Créer le canal
            ticket_channel = await interaction.guild.create_text_channel(
                name=channel_name,
                category=tickets_category,
                overwrites=overwrites,
                topic=f"Ticket de {interaction.user} - {category_name}",
                reason=f"Création de ticket par {interaction.user}"
            )
            
            # Enregistrer en base de données
            async with self.bot.db.pool.acquire() as conn:
                ticket_id = await conn.fetchval('''
                    INSERT INTO tickets (guild_id, user_id, channel_id, category)
                    VALUES ($1, $2, $3, $4)
                    RETURNING id
                ''', interaction.guild.id, interaction.user.id, ticket_channel.id, category)
            
            # Message de bienvenue dans le ticket
            welcome_embed = create_embed(
                title=f"{category_emoji} Ticket #{ticket_id} - {category_name}",
                description=f"Bonjour {interaction.user.mention} !\n\n"
                           f"Votre ticket a été créé avec succès. Un membre de l'équipe "
                           f"vous aidera dès que possible.\n\n"
                           f"**Merci de décrire votre problème ou votre demande en détail.**",
                color=self.config.COLOR_INFO
            )
            
            welcome_embed.add_field(
                name="ℹ️ Informations",
                value=f"**Catégorie :** {category_name}\n"
                      f"**Créé le :** <t:{int(datetime.utcnow().timestamp())}:F>\n"
                      f"**ID du ticket :** {ticket_id}",
                inline=False
            )
            
            # Vue de contrôle
            control_view = TicketControlView(ticket_id)
            
            await ticket_channel.send(
                content=f"{interaction.user.mention}",
                embed=welcome_embed,
                view=control_view
            )
            
            # Réponse à l'utilisateur
            await interaction.response.send_message(
                f"✅ Votre ticket a été créé : {ticket_channel.mention}",
                ephemeral=True
            )
            
            # Log de l'action
            bot_logger.command_used(
                interaction.user.id, interaction.guild.id, "create_ticket",
                ticket_id=ticket_id, category=category
            )
            
        except Exception as e:
            bot_logger.error_occurred(e, "_create_ticket")
            await interaction.response.send_message(
                "❌ Erreur lors de la création du ticket. Veuillez réessayer.",
                ephemeral=True
            )
    
    async def _close_ticket_interaction(self, interaction: discord.Interaction, ticket_id: int):
        """Ferme un ticket via interaction"""
        
        try:
            async with self.bot.db.pool.acquire() as conn:
                ticket = await conn.fetchrow('''
                    SELECT * FROM tickets WHERE id = $1
                ''', ticket_id)
                
                if not ticket or ticket['status'] != 'open':
                    await interaction.response.send_message(
                        "❌ Ticket introuvable ou déjà fermé.", ephemeral=True
                    )
                    return
                
                # Confirmation
                view = ConfirmationView(interaction.user)
                embed = create_embed(
                    title="Confirmation de fermeture",
                    description="Êtes-vous sûr de vouloir fermer ce ticket ?\n\n"
                               "⚠️ **Cette action est irréversible !**\n"
                               "Le salon sera supprimé définitivement.",
                    color=self.config.COLOR_WARNING
                )
                
                await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
                await view.wait()
                
                if not view.result:
                    await interaction.edit_original_response(
                        content="Fermeture annulée.", embed=None, view=None
                    )
                    return
                
                # Fermer le ticket
                await self._close_ticket(ticket, interaction.user)
                
                await interaction.edit_original_response(
                    content="✅ Ticket fermé avec succès.", embed=None, view=None
                )
                
        except Exception as e:
            bot_logger.error_occurred(e, "_close_ticket_interaction")
            await interaction.followup.send(
                "❌ Erreur lors de la fermeture du ticket.", ephemeral=True
            )
    
    async def _close_ticket(self, ticket_data: dict, closed_by: discord.Member):
        """Ferme un ticket et supprime le salon"""
        
        try:
            guild = self.bot.get_guild(ticket_data['guild_id'])
            if not guild:
                return
            
            channel = guild.get_channel(ticket_data['channel_id'])
            
            # Générer un transcript avant la suppression
            transcript = None
            if channel:
                transcript = await self._generate_transcript_data(channel)
            
            # Mettre à jour en base de données
            async with self.bot.db.pool.acquire() as conn:
                await conn.execute('''
                    UPDATE tickets 
                    SET status = 'closed', closed_at = NOW()
                    WHERE id = $1
                ''', ticket_data['id'])
            
            # Envoyer le transcript à l'utilisateur
            if transcript:
                user = guild.get_member(ticket_data['user_id'])
                if user:
                    try:
                        transcript_embed = create_embed(
                            title="📝 Transcript de votre ticket",
                            description=f"Voici le transcript de votre ticket #{ticket_data['id']} "
                                       f"qui a été fermé par {closed_by.display_name}.",
                            color=self.config.COLOR_INFO
                        )
                        
                        transcript_file = discord.File(
                            io.StringIO(transcript),
                            filename=f"ticket-{ticket_data['id']}-transcript.txt"
                        )
                        
                        await user.send(embed=transcript_embed, file=transcript_file)
                    except discord.Forbidden:
                        pass
            
            # Supprimer le salon après un délai
            if channel:
                await asyncio.sleep(10)
                await channel.delete(reason=f"Ticket fermé par {closed_by}")
            
            # Log de l'action
            bot_logger.moderation_action(
                closed_by.id, ticket_data['user_id'], "close_ticket",
                ticket_data['guild_id'], f"Ticket #{ticket_data['id']}"
            )
            
        except Exception as e:
            bot_logger.error_occurred(e, "_close_ticket")
    
    async def _generate_transcript(self, interaction: discord.Interaction, ticket_id: int):
        """Génère un transcript du ticket"""
        
        try:
            async with self.bot.db.pool.acquire() as conn:
                ticket = await conn.fetchrow('''
                    SELECT * FROM tickets WHERE id = $1
                ''', ticket_id)
                
                if not ticket:
                    await interaction.response.send_message(
                        "❌ Ticket introuvable.", ephemeral=True
                    )
                    return
            
            channel = interaction.guild.get_channel(ticket['channel_id'])
            if not channel:
                await interaction.response.send_message(
                    "❌ Canal de ticket introuvable.", ephemeral=True
                )
                return
            
            await interaction.response.defer(ephemeral=True)
            
            # Générer le transcript
            transcript_content = await self._generate_transcript_data(channel)
            
            # Créer le fichier
            transcript_file = discord.File(
                io.StringIO(transcript_content),
                filename=f"ticket-{ticket_id}-transcript.txt"
            )
            
            embed = create_embed(
                title="📝 Transcript généré",
                description=f"Transcript du ticket #{ticket_id} généré avec succès.",
                color=self.config.COLOR_SUCCESS
            )
            
            await interaction.followup.send(embed=embed, file=transcript_file, ephemeral=True)
            
        except Exception as e:
            bot_logger.error_occurred(e, "_generate_transcript")
            await interaction.followup.send(
                "❌ Erreur lors de la génération du transcript.", ephemeral=True
            )
    
    async def _generate_transcript_data(self, channel: discord.TextChannel) -> str:
        """Génère le contenu du transcript"""
        
        transcript_lines = []
        transcript_lines.append(f"=== TRANSCRIPT DU TICKET ===")
        transcript_lines.append(f"Canal: #{channel.name}")
        transcript_lines.append(f"Serveur: {channel.guild.name}")
        transcript_lines.append(f"Généré le: {datetime.utcnow().strftime('%d/%m/%Y à %H:%M:%S')} UTC")
        transcript_lines.append("=" * 50)
        transcript_lines.append("")
        
        try:
            messages = []
            async for message in channel.history(limit=None, oldest_first=True):
                messages.append(message)
            
            for message in messages:
                timestamp = message.created_at.strftime("%d/%m/%Y %H:%M:%S")
                author = f"{message.author.display_name} ({message.author})"
                
                transcript_lines.append(f"[{timestamp}] {author}")
                
                if message.content:
                    # Nettoyer le contenu
                    content = message.content.replace('\n', '\n    ')
                    transcript_lines.append(f"    {content}")
                
                if message.embeds:
                    for embed in message.embeds:
                        transcript_lines.append("    [EMBED]")
                        if embed.title:
                            transcript_lines.append(f"    Titre: {embed.title}")
                        if embed.description:
                            desc = embed.description.replace('\n', '\n    ')
                            transcript_lines.append(f"    Description: {desc}")
                
                if message.attachments:
                    for attachment in message.attachments:
                        transcript_lines.append(f"    [FICHIER: {attachment.filename}]")
                
                transcript_lines.append("")
            
        except Exception as e:
            transcript_lines.append(f"Erreur lors de la récupération des messages: {str(e)}")
        
        transcript_lines.append("=" * 50)
        transcript_lines.append("=== FIN DU TRANSCRIPT ===")
        
        return "\n".join(transcript_lines)
    
    async def _assign_ticket(self, interaction: discord.Interaction, ticket_id: int):
        """Assigne un ticket à un modérateur"""
        
        try:
            async with self.bot.db.pool.acquire() as conn:
                ticket = await conn.fetchrow('''
                    SELECT * FROM tickets WHERE id = $1
                ''', ticket_id)
                
                if not ticket or ticket['status'] != 'open':
                    await interaction.response.send_message(
                        "❌ Ticket introuvable ou déjà fermé.", ephemeral=True
                    )
                    return
                
                # Assigner le ticket
                await conn.execute('''
                    UPDATE tickets SET assigned_to = $1 WHERE id = $2
                ''', interaction.user.id, ticket_id)
                
                embed = create_embed(
                    title="👤 Ticket assigné",
                    description=f"Le ticket #{ticket_id} a été assigné à {interaction.user.mention}.",
                    color=self.config.COLOR_SUCCESS
                )
                
                await interaction.response.send_message(embed=embed)
                
                # Log de l'action
                bot_logger.moderation_action(
                    interaction.user.id, ticket['user_id'], "assign_ticket",
                    interaction.guild.id, f"Ticket #{ticket_id}"
                )
                
        except Exception as e:
            bot_logger.error_occurred(e, "_assign_ticket")
            await interaction.response.send_message(
                "❌ Erreur lors de l'assignation du ticket.", ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(TicketsCog(bot))