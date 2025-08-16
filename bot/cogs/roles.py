# -*- coding: utf-8 -*-
"""
Cog de gestion des rôles pour COPBOT v4.0
Système d'auto-rôles, attribution par réactions et menus
"""

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional, Dict, List
import asyncio

from config.settings import BotConfig, ERROR_MESSAGES, SUCCESS_MESSAGES
from utils.helpers import create_embed, has_permissions, ConfirmationView
from utils.logger import bot_logger


class RoleManagementView(discord.ui.View):
    """
    Vue persistante pour l'attribution de rôles via boutons
    """
    
    def __init__(self, bot, guild_id: int, role_configs: List[Dict]):
        super().__init__(timeout=None)
        self.bot = bot
        self.guild_id = guild_id
        
        # Ajouter les boutons pour chaque rôle configuré
        for config in role_configs[:25]:  # Limite Discord de 25 boutons
            self.add_item(RoleButton(config))


class RoleButton(discord.ui.Button):
    """
    Bouton pour attribuer/retirer un rôle
    """
    
    def __init__(self, role_config: Dict):
        self.role_id = role_config['role_id']
        emoji = role_config.get('emoji')
        
        super().__init__(
            style=discord.ButtonStyle.secondary,
            label=role_config.get('label', f"Rôle {self.role_id}"),
            emoji=emoji if emoji else None,
            custom_id=f"role_button_{self.role_id}"
        )
    
    async def callback(self, interaction: discord.Interaction):
        """Gère l'attribution/retrait du rôle"""
        
        role = interaction.guild.get_role(self.role_id)
        if not role:
            await interaction.response.send_message(
                "❌ Ce rôle n'existe plus.", ephemeral=True
            )
            return
        
        member = interaction.user
        
        if role in member.roles:
            # Retirer le rôle
            try:
                await member.remove_roles(role, reason="Retrait via menu auto-rôles")
                await interaction.response.send_message(
                    f"✅ Le rôle {role.mention} vous a été retiré.", ephemeral=True
                )
            except discord.Forbidden:
                await interaction.response.send_message(
                    "❌ Je n'ai pas la permission de retirer ce rôle.", ephemeral=True
                )
        else:
            # Ajouter le rôle
            try:
                await member.add_roles(role, reason="Attribution via menu auto-rôles")
                await interaction.response.send_message(
                    f"✅ Le rôle {role.mention} vous a été attribué.", ephemeral=True
                )
            except discord.Forbidden:
                await interaction.response.send_message(
                    "❌ Je n'ai pas la permission d'attribuer ce rôle.", ephemeral=True
                )


class RoleDropdown(discord.ui.Select):
    """
    Menu déroulant pour la sélection de rôles
    """
    
    def __init__(self, roles: List[discord.Role]):
        options = []
        
        for role in roles[:25]:  # Limite Discord
            options.append(discord.SelectOption(
                label=role.name,
                description=f"Obtenir le rôle {role.name}",
                value=str(role.id),
                emoji="🎭"
            ))
        
        super().__init__(
            placeholder="Choisissez un rôle...",
            options=options,
            min_values=0,
            max_values=len(options)
        )
    
    async def callback(self, interaction: discord.Interaction):
        """Gère la sélection multiple de rôles"""
        
        member = interaction.user
        selected_role_ids = [int(value) for value in self.values]
        
        roles_to_add = []
        roles_to_remove = []
        
        # Analyser tous les rôles disponibles dans le menu
        for option in self.options:
            role_id = int(option.value)
            role = interaction.guild.get_role(role_id)
            
            if not role:
                continue
            
            if role_id in selected_role_ids:
                # Rôle sélectionné
                if role not in member.roles:
                    roles_to_add.append(role)
            else:
                # Rôle non sélectionné
                if role in member.roles:
                    roles_to_remove.append(role)
        
        # Appliquer les changements
        try:
            if roles_to_add:
                await member.add_roles(*roles_to_add, reason="Attribution via menu auto-rôles")
            
            if roles_to_remove:
                await member.remove_roles(*roles_to_remove, reason="Retrait via menu auto-rôles")
            
            # Message de confirmation
            changes = []
            if roles_to_add:
                changes.append(f"✅ **Ajoutés:** {', '.join(role.name for role in roles_to_add)}")
            if roles_to_remove:
                changes.append(f"❌ **Retirés:** {', '.join(role.name for role in roles_to_remove)}")
            
            if changes:
                await interaction.response.send_message(
                    "\n".join(changes), ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "Aucun changement effectué.", ephemeral=True
                )
                
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Je n'ai pas les permissions nécessaires pour gérer ces rôles.",
                ephemeral=True
            )


class RoleDropdownView(discord.ui.View):
    """
    Vue contenant le menu déroulant des rôles
    """
    
    def __init__(self, roles: List[discord.Role]):
        super().__init__(timeout=None)
        self.add_item(RoleDropdown(roles))


class RolesCog(commands.Cog, name="Rôles"):
    """
    Système de gestion des rôles automatiques
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.config = BotConfig()
        
        # Cache des auto-rôles par serveur
        self.auto_roles_cache: Dict[int, List[Dict]] = {}
    
    async def cog_load(self):
        """Chargement initial du cog"""
        await self._load_auto_roles_cache()
    
    async def _load_auto_roles_cache(self):
        """Charge les auto-rôles en cache depuis la base de données"""
        try:
            async with self.bot.db.pool.acquire() as conn:
                rows = await conn.fetch('SELECT * FROM auto_roles')
                
                for row in rows:
                    guild_id = row['guild_id']
                    if guild_id not in self.auto_roles_cache:
                        self.auto_roles_cache[guild_id] = []
                    
                    self.auto_roles_cache[guild_id].append({
                        'id': row['id'],
                        'role_id': row['role_id'],
                        'emoji': row['emoji'],
                        'message_id': row['message_id'],
                        'channel_id': row['channel_id'],
                        'type': row['type']
                    })
        except Exception as e:
            bot_logger.error_occurred(e, "_load_auto_roles_cache")
    
    # ==================== ÉVÉNEMENTS ====================
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gère l'attribution de rôles par réaction"""
        
        if payload.user_id == self.bot.user.id:
            return
        
        await self._handle_reaction_role(payload, action="add")
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Gère le retrait de rôles par réaction"""
        
        if payload.user_id == self.bot.user.id:
            return
        
        await self._handle_reaction_role(payload, action="remove")
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Attribution automatique de rôles aux nouveaux membres"""
        
        guild_settings = await self.bot.db.get_guild_settings(member.guild.id)
        auto_role_id = guild_settings.get('auto_role')
        
        if auto_role_id:
            auto_role = member.guild.get_role(auto_role_id)
            if auto_role:
                try:
                    await member.add_roles(auto_role, reason="Rôle automatique nouveau membre")
                    bot_logger.moderation_action(
                        self.bot.user.id, member.id, "auto_role_assign",
                        member.guild.id, f"Rôle automatique: {auto_role.name}"
                    )
                except discord.Forbidden:
                    bot_logger.error_occurred(
                        Exception("Permission denied"), 
                        f"auto_role_assign for user {member.id}"
                    )
    
    async def _handle_reaction_role(self, payload: discord.RawReactionActionEvent, action: str):
        """Traite l'attribution/retrait de rôles via réactions"""
        
        guild_id = payload.guild_id
        if guild_id not in self.auto_roles_cache:
            return
        
        # Chercher une configuration correspondante
        matching_config = None
        for config in self.auto_roles_cache[guild_id]:
            if (config['message_id'] == payload.message_id and 
                config['type'] == 'reaction' and
                config['emoji'] == str(payload.emoji)):
                matching_config = config
                break
        
        if not matching_config:
            return
        
        # Obtenir les objets Discord
        guild = self.bot.get_guild(guild_id)
        if not guild:
            return
        
        member = guild.get_member(payload.user_id)
        if not member:
            return
        
        role = guild.get_role(matching_config['role_id'])
        if not role:
            return
        
        # Appliquer l'action
        try:
            if action == "add" and role not in member.roles:
                await member.add_roles(role, reason="Attribution via réaction auto-rôle")
                bot_logger.moderation_action(
                    payload.user_id, member.id, "reaction_role_add",
                    guild_id, f"Rôle: {role.name}"
                )
            elif action == "remove" and role in member.roles:
                await member.remove_roles(role, reason="Retrait via réaction auto-rôle")
                bot_logger.moderation_action(
                    payload.user_id, member.id, "reaction_role_remove",
                    guild_id, f"Rôle: {role.name}"
                )
        except discord.Forbidden:
            pass
    
    # ==================== COMMANDES ====================
    
    @app_commands.command(name="autorole", description="Configure le rôle automatique pour nouveaux membres")
    @app_commands.describe(role="Le rôle à attribuer automatiquement (None pour désactiver)")
    @commands.has_permissions(manage_roles=True)
    async def set_auto_role(self, interaction: discord.Interaction, role: Optional[discord.Role] = None):
        """Configure le rôle automatique pour nouveaux membres"""
        
        try:
            if role:
                # Vérifier la hiérarchie des rôles
                if role.position >= interaction.guild.me.top_role.position:
                    await interaction.response.send_message(
                        "❌ Je ne peux pas attribuer un rôle qui est au-dessus de mon rôle le plus élevé.",
                        ephemeral=True
                    )
                    return
                
                if role.managed:
                    await interaction.response.send_message(
                        "❌ Je ne peux pas attribuer un rôle géré automatiquement par Discord.",
                        ephemeral=True
                    )
                    return
                
                await self.bot.db.update_guild_setting(
                    interaction.guild.id, 'auto_role', role.id
                )
                
                embed = create_embed(
                    title="Rôle automatique configuré",
                    description=f"Le rôle {role.mention} sera automatiquement attribué aux nouveaux membres.",
                    color=self.config.COLOR_SUCCESS
                )
            else:
                await self.bot.db.update_guild_setting(
                    interaction.guild.id, 'auto_role', None
                )
                
                embed = create_embed(
                    title="Rôle automatique désactivé",
                    description="Aucun rôle ne sera plus attribué automatiquement aux nouveaux membres.",
                    color=self.config.COLOR_SUCCESS
                )
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            bot_logger.error_occurred(e, "set_auto_role")
            await interaction.response.send_message(
                ERROR_MESSAGES['database_error'], ephemeral=True
            )
    
    @app_commands.command(name="reactionrole", description="Crée un système de rôles par réaction")
    @app_commands.describe(
        message="ID du message ou lien vers le message",
        role="Le rôle à attribuer",
        emoji="L'émoji à utiliser"
    )
    @commands.has_permissions(manage_roles=True)
    async def setup_reaction_role(self, interaction: discord.Interaction, 
                                 message: str, role: discord.Role, emoji: str):
        """Configure un système de rôles par réaction"""
        
        try:
            # Parser l'ID du message
            try:
                if message.startswith('https://'):
                    # Lien Discord
                    parts = message.split('/')
                    message_id = int(parts[-1])
                    channel_id = int(parts[-2])
                else:
                    # ID direct
                    message_id = int(message)
                    channel_id = interaction.channel.id
            except (ValueError, IndexError):
                await interaction.response.send_message(
                    "❌ Format de message invalide. Utilisez un ID ou un lien Discord.",
                    ephemeral=True
                )
                return
            
            # Obtenir le message
            channel = interaction.guild.get_channel(channel_id)
            if not channel:
                await interaction.response.send_message(
                    "❌ Canal introuvable.", ephemeral=True
                )
                return
            
            try:
                target_message = await channel.fetch_message(message_id)
            except discord.NotFound:
                await interaction.response.send_message(
                    "❌ Message introuvable.", ephemeral=True
                )
                return
            
            # Vérifier la hiérarchie des rôles
            if role.position >= interaction.guild.me.top_role.position:
                await interaction.response.send_message(
                    "❌ Je ne peux pas gérer un rôle qui est au-dessus de mon rôle le plus élevé.",
                    ephemeral=True
                )
                return
            
            # Ajouter la réaction au message
            try:
                await target_message.add_reaction(emoji)
            except discord.HTTPException:
                await interaction.response.send_message(
                    "❌ Impossible d'ajouter cette réaction. Vérifiez que l'émoji est valide.",
                    ephemeral=True
                )
                return
            
            # Enregistrer en base de données
            async with self.bot.db.pool.acquire() as conn:
                await conn.execute('''
                    INSERT INTO auto_roles (guild_id, role_id, emoji, message_id, channel_id, type)
                    VALUES ($1, $2, $3, $4, $5, $6)
                ''', interaction.guild.id, role.id, emoji, message_id, channel_id, 'reaction')
            
            # Mettre à jour le cache
            if interaction.guild.id not in self.auto_roles_cache:
                self.auto_roles_cache[interaction.guild.id] = []
            
            self.auto_roles_cache[interaction.guild.id].append({
                'role_id': role.id,
                'emoji': emoji,
                'message_id': message_id,
                'channel_id': channel_id,
                'type': 'reaction'
            })
            
            embed = create_embed(
                title="Rôle par réaction configuré",
                description=f"**Rôle:** {role.mention}\n"
                           f"**Émoji:** {emoji}\n"
                           f"**Message:** [Lien]({target_message.jump_url})\n\n"
                           f"Les utilisateurs peuvent maintenant réagir avec {emoji} pour obtenir le rôle.",
                color=self.config.COLOR_SUCCESS
            )
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            bot_logger.error_occurred(e, "setup_reaction_role")
            await interaction.response.send_message(
                ERROR_MESSAGES['database_error'], ephemeral=True
            )
    
    @app_commands.command(name="rolemenu", description="Crée un menu de sélection de rôles")
    @app_commands.describe(
        titre="Titre du menu de rôles",
        roles="Liste des rôles séparés par des espaces (@role1 @role2...)"
    )
    @commands.has_permissions(manage_roles=True)
    async def create_role_menu(self, interaction: discord.Interaction, 
                              titre: str, roles: str):
        """Crée un menu de sélection de rôles"""
        
        await interaction.response.defer()
        
        try:
            # Parser les rôles mentionnés
            mentioned_roles = interaction.message.role_mentions if hasattr(interaction, 'message') else []
            
            # Si pas de mentions, essayer de parser manuellement
            if not mentioned_roles:
                # Extraire les IDs de rôles du texte
                import re
                role_ids = re.findall(r'<@&(\d+)>', roles)
                mentioned_roles = [interaction.guild.get_role(int(role_id)) for role_id in role_ids]
                mentioned_roles = [role for role in mentioned_roles if role]
            
            if not mentioned_roles:
                await interaction.followup.send(
                    "❌ Aucun rôle valide trouvé. Utilisez @role1 @role2 etc.",
                    ephemeral=True
                )
                return
            
            # Vérifier les permissions pour tous les rôles
            invalid_roles = []
            for role in mentioned_roles:
                if role.position >= interaction.guild.me.top_role.position or role.managed:
                    invalid_roles.append(role)
            
            if invalid_roles:
                invalid_names = [role.name for role in invalid_roles]
                await interaction.followup.send(
                    f"❌ Je ne peux pas gérer ces rôles: {', '.join(invalid_names)}",
                    ephemeral=True
                )
                return
            
            # Créer l'embed du menu
            embed = create_embed(
                title=titre,
                description="Utilisez le menu ci-dessous pour sélectionner vos rôles.\n"
                           "Vous pouvez sélectionner plusieurs rôles à la fois.",
                color=self.config.COLOR_INFO
            )
            
            roles_text = "\n".join([f"🎭 {role.mention} - {role.name}" for role in mentioned_roles])
            embed.add_field(
                name="Rôles disponibles",
                value=roles_text,
                inline=False
            )
            
            # Créer la vue avec le menu déroulant
            view = RoleDropdownView(mentioned_roles)
            
            await interaction.followup.send(embed=embed, view=view)
            
        except Exception as e:
            bot_logger.error_occurred(e, "create_role_menu")
            await interaction.followup.send(
                ERROR_MESSAGES['database_error'], ephemeral=True
            )
    
    @app_commands.command(name="roleinfo", description="Affiche les informations d'un rôle")
    @app_commands.describe(role="Le rôle à analyser")
    async def role_info(self, interaction: discord.Interaction, role: discord.Role):
        """Affiche les informations détaillées d'un rôle"""
        
        # Compter les membres avec ce rôle
        member_count = len(role.members)
        
        # Permissions importantes
        perms = role.permissions
        key_permissions = []
        
        if perms.administrator:
            key_permissions.append("👑 Administrateur")
        if perms.manage_guild:
            key_permissions.append("🛠️ Gérer le serveur")
        if perms.manage_roles:
            key_permissions.append("🎭 Gérer les rôles")
        if perms.manage_channels:
            key_permissions.append("📝 Gérer les salons")
        if perms.ban_members:
            key_permissions.append("🔨 Bannir des membres")
        if perms.kick_members:
            key_permissions.append("👢 Expulser des membres")
        
        embed = create_embed(
            title=f"🎭 Informations - {role.name}",
            color=role.color if role.color != discord.Color.default() else self.config.COLOR_INFO
        )
        
        embed.add_field(
            name="📋 Général",
            value=f"**Nom:** {role.name}\n"
                  f"**ID:** {role.id}\n"
                  f"**Mention:** {role.mention}",
            inline=True
        )
        
        embed.add_field(
            name="📊 Statistiques",
            value=f"**Membres:** {member_count:,}\n"
                  f"**Position:** {role.position}\n"
                  f"**Géré:** {'Oui' if role.managed else 'Non'}",
            inline=True
        )
        
        embed.add_field(
            name="🎨 Apparence",
            value=f"**Couleur:** {str(role.color).upper()}\n"
                  f"**Affiché séparément:** {'Oui' if role.hoist else 'Non'}\n"
                  f"**Mentionnable:** {'Oui' if role.mentionable else 'Non'}",
            inline=True
        )
        
        if key_permissions:
            embed.add_field(
                name="🔑 Permissions importantes",
                value=" • ".join(key_permissions),
                inline=False
            )
        
        embed.add_field(
            name="📅 Informations temporelles",
            value=f"**Créé le:** <t:{int(role.created_at.timestamp())}:D>\n"
                  f"**Il y a:** <t:{int(role.created_at.timestamp())}:R>",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="listroles", description="Liste tous les rôles du serveur")
    async def list_roles(self, interaction: discord.Interaction):
        """Liste tous les rôles du serveur avec leurs informations"""
        
        roles = sorted(interaction.guild.roles[1:], key=lambda r: r.position, reverse=True)  # Exclure @everyone
        
        if not roles:
            await interaction.response.send_message(
                "Ce serveur n'a aucun rôle personnalisé.", ephemeral=True
            )
            return
        
        embed = create_embed(
            title=f"🎭 Rôles de {interaction.guild.name}",
            description=f"Total: {len(roles)} rôles",
            color=self.config.COLOR_INFO
        )
        
        # Diviser en pages si nécessaire
        roles_per_page = 20
        roles_text = []
        
        for i, role in enumerate(roles[:roles_per_page]):
            member_count = len(role.members)
            color_indicator = "🔴" if role.color != discord.Color.default() else "⚪"
            managed_indicator = "🤖" if role.managed else "👤"
            
            roles_text.append(
                f"{color_indicator}{managed_indicator} {role.mention} "
                f"({member_count} membre{'s' if member_count != 1 else ''})"
            )
        
        embed.add_field(
            name="Liste des rôles (par position)",
            value="\n".join(roles_text) if roles_text else "Aucun rôle",
            inline=False
        )
        
        if len(roles) > roles_per_page:
            embed.set_footer(text=f"Affichage de {roles_per_page}/{len(roles)} rôles")
        
        embed.add_field(
            name="Légende",
            value="🔴 Rôle coloré • ⚪ Rôle par défaut\n🤖 Géré automatiquement • 👤 Géré manuellement",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(RolesCog(bot))