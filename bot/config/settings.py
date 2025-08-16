# -*- coding: utf-8 -*-
"""
Configuration du bot COPBOT v4.0
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class BotConfig:
    """
    Configuration principale du bot
    """
    
    # Configuration Discord
    token: str = os.getenv('DISCORD_TOKEN', '')
    
    # Configuration base de données
    database_url: str = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/copbot')
    
    # Configuration logging
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    log_file: str = os.getenv('LOG_FILE', 'logs/copbot.log')
    
    # Configuration IA (pour futures intégrations)
    openai_api_key: Optional[str] = os.getenv('OPENAI_API_KEY')
    huggingface_token: Optional[str] = os.getenv('HUGGINGFACE_TOKEN')
    
    # Configuration des webhooks et intégrations externes
    twitch_client_id: Optional[str] = os.getenv('TWITCH_CLIENT_ID')
    twitch_client_secret: Optional[str] = os.getenv('TWITCH_CLIENT_SECRET')
    youtube_api_key: Optional[str] = os.getenv('YOUTUBE_API_KEY')
    twitter_bearer_token: Optional[str] = os.getenv('TWITTER_BEARER_TOKEN')
    
    # Configuration générale
    debug_mode: bool = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
    max_warnings_before_action: int = int(os.getenv('MAX_WARNINGS', '3'))
    default_mute_duration: int = int(os.getenv('DEFAULT_MUTE_DURATION', '600'))  # en secondes
    
    # Couleurs pour les embeds
    COLOR_SUCCESS = 0x00FF00
    COLOR_ERROR = 0xFF0000
    COLOR_WARNING = 0xFFFF00
    COLOR_INFO = 0x00FFFF
    COLOR_PRIMARY = 0x7289DA


# Configuration des permissions par défaut
DEFAULT_PERMISSIONS = {
    'moderation': ['administrator', 'manage_guild', 'manage_messages'],
    'roles': ['administrator', 'manage_guild', 'manage_roles'],
    'events': ['administrator', 'manage_guild', 'manage_events'],
    'tickets': ['administrator', 'manage_guild'],
    'automod': ['administrator', 'manage_guild'],
}

# Messages d'erreur standardisés
ERROR_MESSAGES = {
    'no_permission': "❌ Vous n'avez pas la permission d'utiliser cette commande.",
    'user_not_found': "❌ Utilisateur introuvable.",
    'invalid_duration': "❌ Durée invalide. Utilisez un format comme '1h', '30m', '2d'.",
    'already_muted': "❌ Cet utilisateur est déjà muet.",
    'not_muted': "❌ Cet utilisateur n'est pas muet.",
    'self_action': "❌ Vous ne pouvez pas effectuer cette action sur vous-même.",
    'bot_action': "❌ Impossible d'effectuer cette action sur un bot.",
    'higher_role': "❌ Vous ne pouvez pas effectuer cette action sur un utilisateur ayant un rôle supérieur.",
    'database_error': "❌ Erreur de base de données. Veuillez réessayer plus tard.",
    'rate_limit': "❌ Vous utilisez trop rapidement cette commande. Attendez un peu.",
}

# Messages de succès standardisés
SUCCESS_MESSAGES = {
    'user_muted': "✅ Utilisateur mis en sourdine avec succès.",
    'user_unmuted': "✅ Utilisateur retiré de la sourdine avec succès.",
    'user_banned': "✅ Utilisateur banni avec succès.",
    'user_unbanned': "✅ Utilisateur débanni avec succès.",
    'user_warned': "✅ Avertissement donné avec succès.",
    'message_deleted': "✅ Message supprimé avec succès.",
    'channel_created': "✅ Salon créé avec succès.",
    'role_assigned': "✅ Rôle attribué avec succès.",
    'event_created': "✅ Événement créé avec succès.",
    'reminder_set': "✅ Rappel programmé avec succès.",
}