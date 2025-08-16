# -*- coding: utf-8 -*-
"""
Fonctions utilitaires pour COPBOT v4.0
"""

import re
import discord
from discord.ext import commands
from typing import Optional, Union, Tuple
from datetime import datetime, timedelta
import aiohttp
import asyncio


def parse_duration(duration_str: str) -> Optional[int]:
    """
    Parse une durée sous forme de chaîne en secondes
    Exemples: '1h30m', '2d', '45s', '1w'
    """
    if not duration_str:
        return None
    
    # Motifs de regex pour différentes unités
    patterns = {
        'w': 604800,  # semaines
        'd': 86400,   # jours
        'h': 3600,    # heures
        'm': 60,      # minutes
        's': 1        # secondes
    }
    
    total_seconds = 0
    
    # Regex pour capturer nombre + unité
    matches = re.findall(r'(\d+)([wdhms])', duration_str.lower())
    
    if not matches:
        return None
    
    for amount, unit in matches:
        if unit in patterns:
            total_seconds += int(amount) * patterns[unit]
    
    return total_seconds if total_seconds > 0 else None


def format_duration(seconds: int) -> str:
    """
    Formate une durée en secondes en chaîne lisible
    """
    if seconds == 0:
        return "0 seconde"
    
    units = [
        (604800, 'semaine'),
        (86400, 'jour'),
        (3600, 'heure'),
        (60, 'minute'),
        (1, 'seconde')
    ]
    
    parts = []
    
    for unit_seconds, unit_name in units:
        if seconds >= unit_seconds:
            amount = seconds // unit_seconds
            seconds %= unit_seconds
            
            if amount > 1:
                unit_name += 's'
            parts.append(f"{amount} {unit_name}")
    
    if len(parts) == 1:
        return parts[0]
    elif len(parts) == 2:
        return f"{parts[0]} et {parts[1]}"
    else:
        return f"{', '.join(parts[:-1])} et {parts[-1]}"


async def safe_send(
    destination: Union[discord.TextChannel, discord.User, discord.Member],
    content: str = None,
    embed: discord.Embed = None,
    **kwargs
) -> Optional[discord.Message]:
    """
    Envoie un message de manière sécurisée en gérant les erreurs
    """
    try:
        return await destination.send(content=content, embed=embed, **kwargs)
    except discord.Forbidden:
        # Pas de permissions pour envoyer
        return None
    except discord.HTTPException:
        # Erreur HTTP (message trop long, etc.)
        if embed and len(embed) > 6000:
            # Tenter de raccourcir l'embed
            if embed.description and len(embed.description) > 2000:
                embed.description = embed.description[:1997] + "..."
            return await safe_send(destination, content=content, embed=embed, **kwargs)
        return None
    except Exception:
        return None


def create_embed(
    title: str = None,
    description: str = None,
    color: int = 0x7289DA,
    author: discord.Member = None,
    thumbnail_url: str = None,
    image_url: str = None,
    footer_text: str = None,
    timestamp: datetime = None
) -> discord.Embed:
    """
    Crée un embed Discord avec les paramètres de base
    """
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=timestamp or datetime.utcnow()
    )
    
    if author:
        embed.set_author(
            name=str(author),
            icon_url=author.display_avatar.url
        )
    
    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)
    
    if image_url:
        embed.set_image(url=image_url)
    
    if footer_text:
        embed.set_footer(text=footer_text)
    else:
        embed.set_footer(text="COPBOT v4.0 • Plaza Network")
    
    return embed


def has_permissions(**perms):
    """
    Décorateur pour vérifier les permissions Discord
    """
    def predicate(ctx):
        if ctx.author.guild_permissions.administrator:
            return True
        
        user_perms = ctx.author.guild_permissions
        return all(getattr(user_perms, perm, False) for perm in perms)
    
    return commands.check(predicate)


class ConfirmationView(discord.ui.View):
    """
    Vue de confirmation avec boutons Oui/Non
    """
    
    def __init__(self, author: discord.Member, timeout: int = 60):
        super().__init__(timeout=timeout)
        self.author = author
        self.result = None
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.author
    
    @discord.ui.button(label="Confirmer", style=discord.ButtonStyle.green, emoji="✅")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.result = True
        self.stop()
        await interaction.response.edit_message(view=None)
    
    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.red, emoji="❌")
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.result = False
        self.stop()
        await interaction.response.edit_message(view=None)


class PaginationView(discord.ui.View):
    """
    Vue de pagination pour les listes longues
    """
    
    def __init__(self, embeds: list, author: discord.Member, timeout: int = 300):
        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.author = author
        self.current_page = 0
        self.max_pages = len(embeds)
        
        # Désactiver les boutons si une seule page
        if self.max_pages <= 1:
            self.previous_button.disabled = True
            self.next_button.disabled = True
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.author
    
    @discord.ui.button(label="◀", style=discord.ButtonStyle.blurple)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
    
    @discord.ui.button(label="▶", style=discord.ButtonStyle.blurple)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.max_pages - 1:
            self.current_page += 1
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)


async def get_member_safely(guild: discord.Guild, user_id: int) -> Optional[discord.Member]:
    """
    Récupère un membre de manière sécurisée
    """
    try:
        member = guild.get_member(user_id)
        if member is None:
            member = await guild.fetch_member(user_id)
        return member
    except discord.NotFound:
        return None
    except discord.HTTPException:
        return None


async def get_user_safely(bot: commands.Bot, user_id: int) -> Optional[discord.User]:
    """
    Récupère un utilisateur de manière sécurisée
    """
    try:
        user = bot.get_user(user_id)
        if user is None:
            user = await bot.fetch_user(user_id)
        return user
    except discord.NotFound:
        return None
    except discord.HTTPException:
        return None


def is_url_safe(url: str) -> bool:
    """
    Vérifie si une URL est sûre (détection basique de phishing)
    """
    # Liste de domaines suspects (à étendre)
    suspicious_domains = [
        'bit.ly', 'tinyurl.com', 'discord.gg', 'discordapp.com',
        'discord-app.com', 'discord-nitro.com'
    ]
    
    # Mots-clés suspects
    suspicious_keywords = [
        'free-nitro', 'discord-nitro', 'steam-gift', 'free-gift'
    ]
    
    url_lower = url.lower()
    
    # Vérifier les domaines suspects
    for domain in suspicious_domains:
        if domain in url_lower:
            return False
    
    # Vérifier les mots-clés suspects
    for keyword in suspicious_keywords:
        if keyword in url_lower:
            return False
    
    return True


class RateLimiter:
    """
    Limiteur de taux pour prévenir le spam de commandes
    """
    
    def __init__(self, max_uses: int = 5, per_seconds: int = 60):
        self.max_uses = max_uses
        self.per_seconds = per_seconds
        self.usage = {}
    
    def is_rate_limited(self, user_id: int) -> bool:
        """
        Vérifie si un utilisateur a dépassé la limite
        """
        now = datetime.utcnow()
        
        if user_id not in self.usage:
            self.usage[user_id] = []
        
        # Nettoyer les anciens usages
        self.usage[user_id] = [
            timestamp for timestamp in self.usage[user_id]
            if (now - timestamp).total_seconds() < self.per_seconds
        ]
        
        # Vérifier la limite
        if len(self.usage[user_id]) >= self.max_uses:
            return True
        
        # Ajouter l'usage actuel
        self.usage[user_id].append(now)
        return False


async def clean_old_messages(channel: discord.TextChannel, days: int = 7, limit: int = 100):
    """
    Nettoie les anciens messages d'un salon
    """
    cutoff = datetime.utcnow() - timedelta(days=days)
    deleted_count = 0
    
    try:
        async for message in channel.history(limit=limit, before=cutoff):
            try:
                await message.delete()
                deleted_count += 1
                await asyncio.sleep(0.5)  # Rate limiting
            except (discord.NotFound, discord.Forbidden):
                continue
    except discord.Forbidden:
        pass
    
    return deleted_count