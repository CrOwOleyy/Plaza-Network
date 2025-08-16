# -*- coding: utf-8 -*-
"""
Système de logging pour COPBOT v4.0
"""

import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logging(log_level: str = "INFO", log_file: str = "logs/copbot.log"):
    """
    Configure le système de logging du bot
    """
    # Création du dossier de logs s'il n'existe pas
    log_dir = Path(log_file).parent
    log_dir.mkdir(exist_ok=True)
    
    # Configuration du niveau de logging
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Format des messages de log
    log_format = (
        "%(asctime)s | %(levelname)8s | %(name)20s | %(funcName)15s:%(lineno)4d | %(message)s"
    )
    
    # Configuration du logger principal
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=[
            # Handler pour le fichier
            logging.FileHandler(
                log_file,
                encoding='utf-8',
                mode='a'
            ),
            # Handler pour la console
            logging.StreamHandler()
        ]
    )
    
    # Réduction du niveau de logging pour certaines bibliothèques
    logging.getLogger('discord').setLevel(logging.WARNING)
    logging.getLogger('asyncpg').setLevel(logging.WARNING)
    logging.getLogger('aiohttp').setLevel(logging.WARNING)
    
    logging.info(f"Système de logging initialisé - Niveau: {log_level}")


class BotLogger:
    """
    Logger spécialisé pour les actions du bot
    """
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def command_used(self, user_id: int, guild_id: int, command: str, **kwargs):
        """
        Log l'utilisation d'une commande
        """
        extra_info = " | ".join([f"{k}: {v}" for k, v in kwargs.items()])
        self.logger.info(
            f"Commande utilisée: {command} | "
            f"Utilisateur: {user_id} | "
            f"Serveur: {guild_id}"
            f"{' | ' + extra_info if extra_info else ''}"
        )
    
    def moderation_action(self, moderator_id: int, target_id: int, action: str, 
                         guild_id: int, reason: str = None):
        """
        Log une action de modération
        """
        self.logger.info(
            f"Action de modération: {action} | "
            f"Modérateur: {moderator_id} | "
            f"Cible: {target_id} | "
            f"Serveur: {guild_id}"
            f"{' | Raison: ' + reason if reason else ''}"
        )
    
    def security_event(self, event_type: str, details: str, guild_id: int, user_id: int = None):
        """
        Log un événement de sécurité
        """
        self.logger.warning(
            f"Événement de sécurité: {event_type} | "
            f"Détails: {details} | "
            f"Serveur: {guild_id}"
            f"{' | Utilisateur: ' + str(user_id) if user_id else ''}"
        )
    
    def error_occurred(self, error: Exception, context: str = None):
        """
        Log une erreur
        """
        context_str = f" | Contexte: {context}" if context else ""
        self.logger.error(f"Erreur: {type(error).__name__}: {error}{context_str}", exc_info=True)
    
    def database_operation(self, operation: str, table: str, success: bool, details: str = None):
        """
        Log une opération de base de données
        """
        status = "SUCCÈS" if success else "ÉCHEC"
        details_str = f" | Détails: {details}" if details else ""
        self.logger.info(f"DB {operation} sur {table}: {status}{details_str}")


# Logger global pour le bot
bot_logger = BotLogger("COPBOT")


def log_performance(func):
    """
    Décorateur pour mesurer les performances des fonctions
    """
    import functools
    import time
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            if hasattr(func, '__call__') and hasattr(func, '__name__'):
                if func.__name__.startswith('async'):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
            else:
                result = await func(*args, **kwargs)
            
            execution_time = time.time() - start_time
            if execution_time > 1.0:  # Log seulement si > 1 seconde
                logging.info(f"Performance: {func.__name__} exécutée en {execution_time:.2f}s")
            
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logging.error(f"Erreur dans {func.__name__} après {execution_time:.2f}s: {e}")
            raise
    
    return wrapper