# -*- coding: utf-8 -*-
"""
Gestionnaire de base de données pour COPBOT v4.0
"""

import asyncpg
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta


class DatabaseManager:
    """
    Gestionnaire de base de données PostgreSQL pour COPBOT
    """
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool: Optional[asyncpg.Pool] = None
    
    async def connect(self):
        """
        Établit la connexion à la base de données
        """
        try:
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=1,
                max_size=10,
                command_timeout=60
            )
            logging.info("Connexion à la base de données établie")
        except Exception as e:
            logging.error(f"Erreur de connexion à la base de données: {e}")
            raise
    
    async def close(self):
        """
        Ferme la connexion à la base de données
        """
        if self.pool:
            await self.pool.close()
            logging.info("Connexion à la base de données fermée")
    
    async def setup_tables(self):
        """
        Crée les tables nécessaires si elles n'existent pas
        """
        async with self.pool.acquire() as conn:
            # Table des paramètres de guilde
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS guild_settings (
                    guild_id BIGINT PRIMARY KEY,
                    prefix VARCHAR(10) DEFAULT '!',
                    mod_log_channel BIGINT,
                    welcome_channel BIGINT,
                    auto_role BIGINT,
                    max_warnings INTEGER DEFAULT 3,
                    mute_role BIGINT,
                    anti_spam_enabled BOOLEAN DEFAULT TRUE,
                    anti_raid_enabled BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            ''')
            
            # Table des auto-rôles
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS auto_roles (
                    id SERIAL PRIMARY KEY,
                    guild_id BIGINT NOT NULL,
                    role_id BIGINT NOT NULL,
                    emoji VARCHAR(100),
                    message_id BIGINT,
                    channel_id BIGINT,
                    type VARCHAR(50) DEFAULT 'reaction',
                    created_at TIMESTAMP DEFAULT NOW()
                )
            ''')
            
            # Table des événements
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id SERIAL PRIMARY KEY,
                    guild_id BIGINT NOT NULL,
                    creator_id BIGINT NOT NULL,
                    title VARCHAR(200) NOT NULL,
                    description TEXT,
                    start_time TIMESTAMP NOT NULL,
                    end_time TIMESTAMP,
                    max_participants INTEGER,
                    location VARCHAR(200),
                    created_at TIMESTAMP DEFAULT NOW()
                )
            ''')
            
            # Table des participants aux événements
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS event_participants (
                    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
                    user_id BIGINT NOT NULL,
                    status VARCHAR(20) DEFAULT 'attending',
                    joined_at TIMESTAMP DEFAULT NOW(),
                    PRIMARY KEY (event_id, user_id)
                )
            ''')
            
            # Table des rappels
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS reminders (
                    id SERIAL PRIMARY KEY,
                    guild_id BIGINT NOT NULL,
                    user_id BIGINT NOT NULL,
                    channel_id BIGINT NOT NULL,
                    message TEXT NOT NULL,
                    remind_at TIMESTAMP NOT NULL,
                    recurring_interval INTEGER,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            ''')
            
            # Table des avertissements
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS warnings (
                    id SERIAL PRIMARY KEY,
                    guild_id BIGINT NOT NULL,
                    user_id BIGINT NOT NULL,
                    moderator_id BIGINT NOT NULL,
                    reason TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            ''')
            
            # Table des sanctions
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS sanctions (
                    id SERIAL PRIMARY KEY,
                    guild_id BIGINT NOT NULL,
                    user_id BIGINT NOT NULL,
                    moderator_id BIGINT NOT NULL,
                    type VARCHAR(20) NOT NULL,
                    reason TEXT,
                    duration INTEGER,
                    expires_at TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            ''')
            
            # Table des commandes personnalisées
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS custom_commands (
                    id SERIAL PRIMARY KEY,
                    guild_id BIGINT NOT NULL,
                    name VARCHAR(50) NOT NULL,
                    response TEXT NOT NULL,
                    creator_id BIGINT NOT NULL,
                    usage_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT NOW(),
                    UNIQUE(guild_id, name)
                )
            ''')
            
            # Table des tickets
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS tickets (
                    id SERIAL PRIMARY KEY,
                    guild_id BIGINT NOT NULL,
                    user_id BIGINT NOT NULL,
                    channel_id BIGINT UNIQUE NOT NULL,
                    assigned_to BIGINT,
                    category VARCHAR(50),
                    status VARCHAR(20) DEFAULT 'open',
                    created_at TIMESTAMP DEFAULT NOW(),
                    closed_at TIMESTAMP
                )
            ''')
            
            # Table des logs d'activité
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS activity_logs (
                    id SERIAL PRIMARY KEY,
                    guild_id BIGINT NOT NULL,
                    user_id BIGINT,
                    action VARCHAR(50) NOT NULL,
                    target_id BIGINT,
                    details JSONB,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            ''')
            
            # Table des sondages
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS polls (
                    id SERIAL PRIMARY KEY,
                    guild_id BIGINT NOT NULL,
                    creator_id BIGINT NOT NULL,
                    channel_id BIGINT NOT NULL,
                    message_id BIGINT NOT NULL,
                    title VARCHAR(200) NOT NULL,
                    options JSONB NOT NULL,
                    votes JSONB DEFAULT '{}',
                    expires_at TIMESTAMP,
                    multiple_choice BOOLEAN DEFAULT FALSE,
                    anonymous BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            ''')
            
            logging.info("Tables de base de données créées/vérifiées")
    
    async def setup_guild(self, guild_id: int):
        """
        Initialise les paramètres pour une nouvelle guilde
        """
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO guild_settings (guild_id) 
                VALUES ($1) 
                ON CONFLICT (guild_id) DO NOTHING
            ''', guild_id)
    
    async def get_guild_settings(self, guild_id: int) -> Dict[str, Any]:
        """
        Récupère les paramètres d'une guilde
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow('''
                SELECT * FROM guild_settings WHERE guild_id = $1
            ''', guild_id)
            
            if row:
                return dict(row)
            return {}
    
    async def update_guild_setting(self, guild_id: int, setting: str, value: Any):
        """
        Met à jour un paramètre de guilde
        """
        async with self.pool.acquire() as conn:
            await conn.execute(f'''
                UPDATE guild_settings 
                SET {setting} = $1, updated_at = NOW() 
                WHERE guild_id = $2
            ''', value, guild_id)
    
    async def add_warning(self, guild_id: int, user_id: int, moderator_id: int, reason: str):
        """
        Ajoute un avertissement à un utilisateur
        """
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO warnings (guild_id, user_id, moderator_id, reason)
                VALUES ($1, $2, $3, $4)
            ''', guild_id, user_id, moderator_id, reason)
    
    async def get_user_warnings(self, guild_id: int, user_id: int) -> List[Dict[str, Any]]:
        """
        Récupère les avertissements d'un utilisateur
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch('''
                SELECT * FROM warnings 
                WHERE guild_id = $1 AND user_id = $2 
                ORDER BY created_at DESC
            ''', guild_id, user_id)
            
            return [dict(row) for row in rows]
    
    async def add_sanction(self, guild_id: int, user_id: int, moderator_id: int, 
                          sanction_type: str, reason: str, duration: Optional[int] = None):
        """
        Ajoute une sanction à un utilisateur
        """
        expires_at = None
        if duration:
            expires_at = datetime.utcnow() + timedelta(seconds=duration)
        
        async with self.pool.acquire() as conn:
            return await conn.fetchval('''
                INSERT INTO sanctions (guild_id, user_id, moderator_id, type, reason, duration, expires_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING id
            ''', guild_id, user_id, moderator_id, sanction_type, reason, duration, expires_at)
    
    async def remove_sanction(self, sanction_id: int):
        """
        Retire une sanction
        """
        async with self.pool.acquire() as conn:
            await conn.execute('''
                UPDATE sanctions SET is_active = FALSE WHERE id = $1
            ''', sanction_id)
    
    async def get_active_sanctions(self, guild_id: int, user_id: int, sanction_type: str) -> List[Dict[str, Any]]:
        """
        Récupère les sanctions actives d'un utilisateur
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch('''
                SELECT * FROM sanctions 
                WHERE guild_id = $1 AND user_id = $2 AND type = $3 AND is_active = TRUE
                AND (expires_at IS NULL OR expires_at > NOW())
            ''', guild_id, user_id, sanction_type)
            
            return [dict(row) for row in rows]
    
    async def log_activity(self, guild_id: int, action: str, user_id: Optional[int] = None, 
                          target_id: Optional[int] = None, details: Optional[Dict] = None):
        """
        Enregistre une activité dans les logs
        """
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO activity_logs (guild_id, user_id, action, target_id, details)
                VALUES ($1, $2, $3, $4, $5)
            ''', guild_id, user_id, action, target_id, details)