#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COPBOT v4.0 - Extension Utilitaire Complète
Bot Discord avancé pour la gestion de serveur avec fonctionnalités IA

Auteur: CrOwOleyy
Version: 4.0
Licence: MIT
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

import discord
from discord.ext import commands
import aiohttp
import asyncpg

from config.settings import BotConfig
from utils.database import DatabaseManager
from utils.logger import setup_logging


class COPBOT(commands.Bot):
    """
    Bot principal COPBOT v4.0 avec fonctionnalités étendues
    """
    
    def __init__(self):
        # Configuration des intents Discord
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        intents.guild_reactions = True
        intents.voice_states = True
        
        super().__init__(
            command_prefix=commands.when_mentioned_or('!'),
            intents=intents,
            help_command=None,
            description="COPBOT v4.0 - Bot Discord utilitaire complet"
        )
        
        self.config = BotConfig()
        self.db: DatabaseManager = None
        self.session: aiohttp.ClientSession = None
        self.start_time = datetime.utcnow()
        
    async def setup_hook(self):
        """
        Configuration initiale du bot
        """
        # Création de la session HTTP
        self.session = aiohttp.ClientSession()
        
        # Initialisation de la base de données
        self.db = DatabaseManager(self.config.database_url)
        await self.db.connect()
        await self.db.setup_tables()
        
        # Chargement des cogs (modules)
        await self.load_cogs()
        
        # Synchronisation des commandes slash
        try:
            synced = await self.tree.sync()
            logging.info(f"Synchronisé {len(synced)} commande(s) slash")
        except Exception as e:
            logging.error(f"Erreur lors de la synchronisation des commandes: {e}")
    
    async def load_cogs(self):
        """
        Chargement de tous les modules (cogs) du bot
        """
        cogs_directory = Path("cogs")
        
        for cog_file in cogs_directory.glob("*.py"):
            if cog_file.name.startswith("_"):
                continue
                
            cog_name = f"cogs.{cog_file.stem}"
            try:
                await self.load_extension(cog_name)
                logging.info(f"Cog chargé: {cog_name}")
            except Exception as e:
                logging.error(f"Erreur lors du chargement de {cog_name}: {e}")
    
    async def on_ready(self):
        """
        Événement déclenché quand le bot est prêt
        """
        logging.info(f"{self.user} est connecté et prêt!")
        logging.info(f"ID du bot: {self.user.id}")
        logging.info(f"Connecté à {len(self.guilds)} serveur(s)")
        
        # Configuration du statut
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Plaza Network | /aide"
            )
        )
    
    async def on_guild_join(self, guild):
        """
        Événement déclenché quand le bot rejoint un serveur
        """
        logging.info(f"Bot ajouté au serveur: {guild.name} (ID: {guild.id})")
        
        # Initialisation des paramètres du serveur
        await self.db.setup_guild(guild.id)
        
    async def on_guild_remove(self, guild):
        """
        Événement déclenché quand le bot quitte un serveur
        """
        logging.info(f"Bot retiré du serveur: {guild.name} (ID: {guild.id})")
    
    async def close(self):
        """
        Nettoyage lors de l'arrêt du bot
        """
        if self.session:
            await self.session.close()
        
        if self.db:
            await self.db.close()
            
        await super().close()


async def main():
    """
    Fonction principale d'exécution du bot
    """
    # Configuration du logging
    setup_logging()
    
    # Vérification des variables d'environnement
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logging.error("Token Discord manquant! Définissez la variable DISCORD_TOKEN")
        sys.exit(1)
    
    # Lancement du bot
    bot = COPBOT()
    
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        logging.info("Arrêt du bot par l'utilisateur")
    except Exception as e:
        logging.error(f"Erreur critique: {e}")
    finally:
        await bot.close()


if __name__ == "__main__":
    # Point d'entrée du programme
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Programme interrompu")