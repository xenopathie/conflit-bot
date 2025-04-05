🤖 Bot Discord – Modération automatique + Whitelist

Un bot Discord polyvalent permettant de modérer automatiquement les messages toxiques, de gérer une whitelist, et de protéger le bot via un mini-serveur Flask (utile pour Replit ou des hébergements qui coupent les processus inactifs).

✨ Fonctionnalités

🔞 Filtrage automatique des propos inappropriés

Suppression immédiate de messages contenant des mots interdits.

Système d'avertissements progressifs (⚠️ → ⚠️ Dernier avertissement → Timeout 15 min).

👑 Système de whitelist

Les utilisateurs ajoutés ne sont pas affectés par la modération automatique.

🛠️ Commandes d'administration

-wl @user : Ajouter un utilisateur à la whitelist.

-unwl @user : Retirer un utilisateur de la whitelist.

-owner @user : Donner le rôle owner à un utilisateur.

-unowner @user : Retirer le rôle owner.

-aide : Affiche la liste des commandes.

⏱️ Logs de timeout

Affiche dans un salon #logs quand un utilisateur est mis en timeout.

🛡️ Protection anti-kick (keep_alive)

Serveur Flask léger pour maintenir le bot actif sur Replit ou d'autres plateformes.

📦 Prérequis
Python 3.8+

Un token de bot Discord (via le Portail développeur Discord)

Un fichier .env contenant :

DISCORD_TOKEN=ton_token_ici

🛠️ Installation

Clone ce dépôt :

git clone https://github.com/tonpseudo/discord-bot-modération.git
cd discord-bot-modération

Installe les dépendances :

pip install -r requirements.txt

Crée un fichier .env :

DISCORD_TOKEN=ton_token_secret

Lance le bot :

python conflit.py

✅ À venir (TODO)

Ajout d'un panneau de signalement via bouton 🚨

Gestion des infractions avec persistance plus détaillée

Dashboard web minimal

💡 Aide & Contribuer

Tu peux proposer des améliorations, ouvrir une issue ou faire une pull request si tu veux contribuer !

📄 Licence

Ce projet est open-source, sous licence MIT.
