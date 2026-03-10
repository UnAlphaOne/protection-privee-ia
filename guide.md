# 📘 Guide d'utilisation détaillé - Privacy Shield IA

## Table des matières
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Premier lancement](#premier-lancement)
4. [Configuration du navigateur](#configuration-du-navigateur)
5. [Les 7 onglets expliqués](#les-7-onglets-expliqués)
6. [Fonctionnement de l'IA](#fonctionnement-de-lia)
7. [Astuces et optimisation](#astuces-et-optimisation)
8. [Dépannage](#dépannage)

## Introduction

**Protection Privée IA** est un proxy intelligent qui agit comme un bouclier entre votre navigateur et Internet. Il analyse chaque requête en temps réel pour bloquer les publicités et les trackers, tout en apprenant continuellement de nouvelles menaces.

### Comment ça marche ?
1. Votre navigateur envoie une requête au proxy
2. Le proxy analyse l'URL avec l'IA
3. Si c'est une pub/tracker → blocage
4. Sinon → transmission au site web
5. L'IA apprend et s'améliore

## Installation

### Étape 1 : Vérifier Python
```bash
python --version
# Doit afficher Python 3.7 ou supérieur

Étape 2 : Télécharger le projet
bash

# Option 1 - Git
git clone https://github.com/UnAlphaOne/protection-privee-ia.git

# Option 2 - ZIP
# Téléchargez et décompressez le ZIP

Étape 3 : Installer les dépendances
bash

cd protection-privee-ia

# Dépendances de base (obligatoires)
# tkinter est normalement inclus avec Python

# Dépendances optionnelles (recommandé)
pip install scikit-learn numpy joblib

Premier lancement
Lancer l'application
bash

python protection_privee_gui_v1.py

Interface au démarrage
text

╔══════════════════════════════════════════════════════════╗
║   PROTECTION PRIVEE IA - PROTECTION VIE PRIVÉE           ║
║   7 onglets pour tout visualiser :                       ║
║   📊 Tableau de bord                                     ║
║   🔍 Trackers                                            ║
║   📢 Publicités                                          ║
║   🎭 Profils                                             ║
║   📈 Statistiques                                        ║
║   🧠 IA                                                  ║
║   📝 Logs                                                ║
╚══════════════════════════════════════════════════════════╝

Démarrer la protection

    Cliquez sur "🧠 DÉMARRER LA PROTECTION"

    Le proxy démarre sur 127.0.0.1:8080

    Vous verrez :
    text

    [12:30:13] ✅ Proxy IA démarré sur 127.0.0.1:8080
    [12:30:13] 🧠 IA auto-apprenante active
    [12:30:13] 🎭 Profil actuel: a87fb995b00b0a21
    [12:30:13] 📊 139 domaines en liste noire

Configuration du navigateur
🔥 Firefox

    Menu (☰) → Paramètres

    Descendre à Paramètres réseau

    Cliquer sur Paramètres...

    Sélectionner Configuration manuelle du proxy

    Remplir :

        Proxy HTTP : 127.0.0.1 Port : 8080

        Proxy SSL : 127.0.0.1 Port : 8080

    Cocher "Utiliser ce proxy pour tous les protocoles"

    ✅ OK

🌐 Chrome / Edge

Méthode 1 : Ligne de commande
bash

chrome --proxy-server="127.0.0.1:8080"

Méthode 2 : Extension SwitchyOmega

    Installer SwitchyOmega

    Créer un profil "Privacy Shield"

    Configurer : 127.0.0.1:8080

    Activer le profil

🪟 Configuration Windows

    Paramètres → Réseau et Internet → Proxy

    Activer "Utiliser un serveur proxy"

    Adresse : 127.0.0.1

    Port : 8080

    ⚠️ N'oubliez pas de désactiver après utilisation

Les 7 onglets expliqués
📊 Tableau de bord

Métriques en temps réel :

    Trackers bloqués

    Publicités bloquées

    Total des blocages

    Vitesse (blocages/minute)

    Données économisées

Informations :

    Statut du proxy

    Profil actuel

    Dernier blocage

    Temps de protection

🔍 Trackers

Analyse détaillée :

    Top domaines trackers

    Méthodes de détection

        Liste noire

        Patterns IA

        Domaines appris

        Patterns regex

📢 Publicités

Statistiques publicitaires :

    Total publicités

    Répartition par type

    Domaines publicitaires fréquents

🎭 Profils

Gestion des faux profils :

    Profil actuel (User-Agent, résolution, langue)

    Liste de tous les profils

    Historique des rotations

    Boutons :

        🎭 Nouveau profil

        🔄 Rotation forcée

📈 Statistiques

Graphiques et prévisions :

    Graphique d'évolution (20 dernières minutes)

    Prévisions IA :

        Total blocages

        Vitesse actuelle

        Prévision prochaine heure

        Top domaines prévus

        Répartition pubs/trackers

🧠 IA

Apprentissage automatique :

    Domaines appris

    Patterns créés

    Dernières découvertes

    Extrait de la liste noire

    Patterns actifs

📝 Logs

Journal complet :

    Filtres par type (INFO, ✅, 🚫, 🧠, ⚠️, ❌)

    Horodatage précis

    Détails des blocages

    Export possible

Fonctionnement de l'IA
Comment l'IA apprend-elle ?

    Détection initiale : Patterns avancés + liste noire

    Apprentissage : Chaque nouveau domaine est enregistré

    Création de patterns : Génération automatique de regex

    Sauvegarde : Persistance dans modeles_ia/

Exemple d'apprentissage
text

[12:30:24] 🧠 NOUVEAU DOMAINE APPRIS: googleads.g.doubleclick.net (blacklist)
[12:30:24]    └─ 2 pattern(s) créé(s)

Patterns créés automatiquement
json

{
    "regex": "googleads\\.g\\.doubleclick\\.net",
    "type": "blacklist",
    "confiance": 0.8
},
{
    "regex": "[a-z0-9-]+\\.doubleclick\\.net",
    "type": "blacklist",
    "confiance": 0.7
}

Astuces et optimisation
🚀 Performance

    Laissez tourner le proxy en arrière-plan

    Utilisez l'auto-raffraîchissement pour les stats

    Nettoyez périodiquement les vieux logs

🎯 Efficacité

    Visitez des sites variés pour enrichir l'IA

    L'IA devient plus précise avec le temps

    Les faux profils tournent toutes les minutes

💾 Persistance

    Les connaissances sont sauvegardées toutes les 30 secondes

    Dossier modeles_ia/ à conserver

    Exportez les logs pour analyse

Dépannage
❌ Le proxy ne démarre pas

Erreur : Address already in use

    Solution : Changez le port (ligne self.port = 8080)

    Ou tuez le processus utilisant le port 8080

❌ Les sites ne chargent pas

Erreur : PR_END_OF_FILE_ERROR

    Vérifiez la configuration du navigateur

    Redémarrez le proxy

    Désactivez/réactivez la protection

❌ Aucun blocage détecté

Symptôme : Stats à zéro

    Vérifiez que le proxy est bien configuré

    Naviguez sur des sites avec publicités

    Regardez les logs pour voir les requêtes

❌ L'IA n'apprend pas

Symptôme : 0 domaines appris

    Vérifiez les permissions d'écriture

    Le dossier modeles_ia/ doit être accessible

    Redémarrez l'application

❌ Erreurs de connexion

Erreur : getaddrinfo failed

    Vérifiez votre connexion Internet

    Désactivez/réactivez le proxy

    Redémarrez le navigateur

Support
Besoin d'aide ?

    Consultez les logs (onglet 📝 Logs)

    Vérifiez la configuration du proxy

    Ouvrez une issue sur GitHub

    Décrivez votre problème avec :

        Version de l'application

        Système d'exploitation

        Navigateur utilisé

        Extrait des logs

✨ Profitez d'une navigation sans publicité et respectueuse de votre vie privée ! ✨
text
