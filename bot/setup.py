#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de configuration et de lancement pour COPBOT v4.0
"""

import os
import sys
import asyncio
import asyncpg
from pathlib import Path

# Ajouter le dossier parent au PATH pour les imports
sys.path.append(str(Path(__file__).parent))

from config.settings import BotConfig
from utils.database import DatabaseManager
from utils.logger import setup_logging


async def check_database_connection():
    """Vérifie la connexion à la base de données"""
    
    config = BotConfig()
    
    try:
        print("🔍 Vérification de la connexion à la base de données...")
        
        # Tenter de se connecter
        conn = await asyncpg.connect(config.database_url)
        await conn.close()
        
        print("✅ Connexion à la base de données réussie!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        print("\n💡 Vérifiez:")
        print("   - Que PostgreSQL est installé et en cours d'exécution")
        print("   - Que la variable DATABASE_URL est correctement définie")
        print("   - Que la base de données existe")
        print("   - Que l'utilisateur a les bonnes permissions")
        return False


async def setup_database():
    """Configure la base de données"""
    
    config = BotConfig()
    
    try:
        print("🛠️ Configuration de la base de données...")
        
        db = DatabaseManager(config.database_url)
        await db.connect()
        await db.setup_tables()
        await db.close()
        
        print("✅ Base de données configurée avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la configuration: {e}")
        return False


def check_environment():
    """Vérifie les variables d'environnement"""
    
    print("🔍 Vérification des variables d'environnement...")
    
    required_vars = ['DISCORD_TOKEN', 'DATABASE_URL']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables d'environnement manquantes: {', '.join(missing_vars)}")
        print("\n💡 Créez un fichier .env avec:")
        for var in missing_vars:
            print(f"   {var}=votre_valeur_ici")
        return False
    
    print("✅ Variables d'environnement configurées!")
    return True


def create_env_file():
    """Crée un fichier .env à partir du template"""
    
    env_file = Path(".env")
    example_file = Path(".env.example")
    
    if env_file.exists():
        print("ℹ️ Le fichier .env existe déjà.")
        return
    
    if not example_file.exists():
        print("❌ Fichier .env.example introuvable.")
        return
    
    try:
        # Copier le template
        with open(example_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Fichier .env créé à partir du template.")
        print("⚠️ N'oubliez pas de configurer vos valeurs dans le fichier .env")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du fichier .env: {e}")


async def main():
    """Fonction principale du setup"""
    
    print("🚀 Configuration de COPBOT v4.0")
    print("=" * 50)
    
    # 1. Vérifier le fichier .env
    if not Path(".env").exists():
        print("📝 Création du fichier de configuration...")
        create_env_file()
        print("\n⏸️ Configurez le fichier .env avant de continuer.")
        return
    
    # 2. Vérifier les variables d'environnement
    if not check_environment():
        return
    
    # 3. Vérifier la connexion à la base de données
    if not await check_database_connection():
        return
    
    # 4. Configurer la base de données
    if not await setup_database():
        return
    
    # 5. Créer les dossiers nécessaires
    print("📁 Création des dossiers...")
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    print("✅ Dossier logs créé!")
    
    print("\n🎉 Configuration terminée avec succès!")
    print("🤖 Vous pouvez maintenant lancer le bot avec: python main.py")


def run_bot():
    """Lance le bot"""
    
    print("🤖 Démarrage de COPBOT v4.0...")
    
    # Importer et lancer le bot
    from main import main as bot_main
    asyncio.run(bot_main())


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Configuration et lancement de COPBOT v4.0")
    parser.add_argument("--setup", action="store_true", help="Configuration initiale")
    parser.add_argument("--run", action="store_true", help="Lancer le bot")
    
    args = parser.parse_args()
    
    if args.setup or (not args.run and not args.setup):
        # Mode setup par défaut
        asyncio.run(main())
    elif args.run:
        # Mode lancement
        run_bot()
    else:
        parser.print_help()