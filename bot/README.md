# COPBOT v4.0 - Setup et Guide d'Installation

## Description
COPBOT v4.0 est un bot Discord utilitaire complet conçu pour la gestion avancée de serveurs Discord. Il offre des fonctionnalités de modération, anti-spam, gestion d'événements, système de rappels, et bien plus.

## Fonctionnalités principales

### 🛡️ Modération & Sécurité
- **Système de sanctions** : Avertissements, mutes, bans temporaires/permanents
- **Anti-spam intelligent** : Détection automatique de spam, flood, répétitions
- **Anti-raid** : Protection contre les arrivées massives
- **Filtrage de contenu** : Mots interdits, URLs suspectes
- **Logs complets** : Journalisation de toutes les actions

### 🎯 Gestion & Organisation
- **Auto-rôles** : Attribution automatique via réactions/menus
- **Système d'événements** : Création, gestion, RSVP
- **Rappels intelligents** : Personnels et collectifs, récurrents
- **Sondages avancés** : Choix multiples, délais, résultats détaillés
- **Tickets de support** : Système complet avec transcripts

### 🤖 Automation
- **Notifications externes** : Twitch, YouTube, Twitter/X, RSS
- **Commandes personnalisées** : Raccourcis créés par les admins
- **Rapports automatiques** : Statistiques régulières
- **Tâches programmées** : Nettoyage, maintenances

## Installation

### Prérequis
- Python 3.8 ou supérieur
- PostgreSQL 12 ou supérieur
- Un token de bot Discord

### 1. Installation des dépendances
```bash
cd bot/
pip install -r requirements.txt
```

### 2. Configuration de la base de données
Créez une base de données PostgreSQL :
```sql
CREATE DATABASE copbot;
CREATE USER copbot_user WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE copbot TO copbot_user;
```

### 3. Configuration des variables d'environnement
Copiez `.env.example` vers `.env` et configurez vos valeurs :
```bash
cp .env.example .env
nano .env
```

Variables obligatoires :
- `DISCORD_TOKEN` : Token de votre bot Discord
- `DATABASE_URL` : URL de connexion PostgreSQL

### 4. Lancement du bot

**Option 1: Configuration automatique (recommandée)**
```bash
python setup.py --setup
```
Puis:
```bash
python setup.py --run
```

**Option 2: Lancement direct**
```bash
python main.py
```

## Configuration Discord

### Permissions requises
Le bot nécessite les permissions suivantes :
- Gérer les messages
- Gérer les rôles
- Bannir des membres
- Gérer les salons
- Voir les salons
- Envoyer des messages
- Utiliser les commandes slash
- Gérer les webhooks
- Lire l'historique des messages

### Intents Discord
Les intents suivants doivent être activés dans le portail développeur Discord :
- Message Content Intent
- Server Members Intent
- Guild Messages Intent

## Structure du projet

```
bot/
├── main.py              # Point d'entrée principal
├── config/
│   ├── __init__.py
│   └── settings.py      # Configuration et constantes
├── utils/
│   ├── __init__.py
│   ├── database.py      # Gestionnaire de base de données
│   ├── logger.py        # Système de logging
│   └── helpers.py       # Fonctions utilitaires
├── cogs/
│   ├── __init__.py
│   ├── moderation.py    # Modération et sanctions
│   ├── antispam.py      # Anti-spam et sécurité
│   ├── help.py          # Aide et informations
│   ├── roles.py         # Gestion des rôles (à implémenter)
│   ├── events.py        # Système d'événements (à implémenter)
│   ├── reminders.py     # Rappels (à implémenter)
│   ├── polls.py         # Sondages (à implémenter)
│   ├── tickets.py       # Système de tickets (à implémenter)
│   └── automation.py    # Intégrations externes (à implémenter)
├── logs/                # Dossier des logs (créé automatiquement)
├── requirements.txt     # Dépendances Python
└── .env.example        # Exemple de configuration
```

## Commandes principales

### Modération
- `/warn <utilisateur> <raison>` - Avertir un utilisateur
- `/mute <utilisateur> [durée] [raison]` - Mettre en sourdine
- `/unmute <utilisateur> [raison]` - Retirer la sourdine
- `/ban <utilisateur> [durée] [raison]` - Bannir un utilisateur

### Configuration
- `/antispam <activer> [canal_logs]` - Configurer l'anti-spam
- `/motinterdits <action> [mot]` - Gérer les mots interdits

### Informations
- `/aide` - Aide générale du bot
- `/info` - Informations sur le bot
- `/serverinfo` - Informations sur le serveur
- `/userinfo [utilisateur]` - Informations sur un utilisateur
- `/ping` - Test de latence

## Support et développement

### Développeur
- **Nom :** CrOwOleyy
- **Contact :** pepepakstassion@gmail.com

### Contributions
Les contributions sont les bienvenues ! Veuillez suivre les bonnes pratiques :
1. Forkez le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers votre branche
5. Ouvrez une Pull Request

### Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## Changelog

### Version 4.0 (Actuelle)
- ✅ Architecture modulaire avec cogs
- ✅ Système de modération complet (warn, mute, ban avec durées)
- ✅ Anti-spam et sécurité avancés avec détection automatique
- ✅ Base de données PostgreSQL avec schéma complet
- ✅ Logging complet et gestion d'erreurs
- ✅ Configuration par serveur personnalisable
- ✅ Système d'auto-rôles avec réactions et menus
- ✅ Gestion d'événements avec RSVP et rappels
- ✅ Système de rappels personnels et collectifs avec récurrence
- ✅ Sondages avancés avec choix multiples et résultats détaillés
- ✅ Système de tickets de support complet avec transcripts
- ✅ Interface utilisateur intuitive avec boutons et menus
- ✅ Support complet en français
- ✅ Script de configuration automatique

## Dépannage

### Problèmes courants

**Le bot ne répond pas aux commandes**
- Vérifiez que les intents sont activés
- Vérifiez les permissions du bot
- Consultez les logs pour les erreurs

**Erreurs de base de données**
- Vérifiez la connexion PostgreSQL
- Assurez-vous que l'utilisateur a les bonnes permissions
- Vérifiez l'URL de connexion dans .env

**Le bot se déconnecte régulièrement**
- Vérifiez votre connexion internet
- Surveillez l'utilisation des ressources
- Consultez les logs Discord

Pour plus d'aide, consultez les logs dans le dossier `logs/` ou contactez le support.