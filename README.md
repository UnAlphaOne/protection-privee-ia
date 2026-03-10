# 🛡️ Protection Privée IA - Protection Vie Privée

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)]()

Un puissant proxy anti-publicité et anti-tracking avec intelligence artificielle auto-apprenante.  
Protège votre vie privée en bloquant les trackers, publicités et en brouillant votre empreinte numérique.

## ✨ Fonctionnalités

### 🧠 Intelligence Artificielle Auto-apprenante
- Détecte automatiquement les nouveaux domaines publicitaires
- Crée des patterns regex à partir des domaines détectés
- Apprentissage continu sans intervention manuelle
- Sauvegarde persistante des connaissances

### 🎭 Brouillage de Profil
- Rotation automatique des user-agents
- Génération de faux profils navigateur
- Cookies factices pour dérouter les trackers
- Changement de profil toutes les minutes

### 🚫 Blocage Multi-niveaux
- **Liste noire** de +150 domaines publicitaires
- **Patterns avancés** pour détecter les publicités
- **Détection intelligente** des nouveaux trackers
- **Blocage HTTPS** via tunnels CONNECT

### 📊 Interface Graphique Complète
- 7 onglets pour tout visualiser :
  - 📊 **Tableau de bord** : métriques en temps réel
  - 🔍 **Trackers** : analyse détaillée des trackers
  - 📢 **Publicités** : statistiques des publicités
  - 🎭 **Profils** : gestion des faux profils
  - 📈 **Statistiques** : graphiques d'évolution
  - 🧠 **IA** : apprentissage et découvertes
  - 📝 **Logs** : journal d'activité complet

### 💾 Persistance des Données
- Sauvegarde automatique des domaines appris
- Conservation des patterns créés
- Historique des faux profils
- Export des logs

## 🚀 Installation

### Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation rapide
```bash
# Cloner le repository
git clone https://github.com/UnAlphaOne/protection-privee-ia.git
cd protection-privee-ia

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python protection_privee_gui_v1.py

Dépendances
text

tkinter (inclus avec Python)

Optionnel pour les fonctionnalités ML avancées :
bash

pip install scikit-learn numpy joblib

📖 Guide d'utilisation
Configuration rapide

    Lancez l'application

    Cliquez sur "🧠 DÉMARRER LA PROTECTION"

    Configurez votre navigateur avec le proxy 127.0.0.1:8080

    Naviguez normalement - la protection est active !

Configuration navigateur

Firefox :

    Menu → Paramètres → Paramètres réseau

    Configuration manuelle du proxy

    Proxy HTTP : 127.0.0.1 Port : 8080

    Proxy HTTPS : 127.0.0.1 Port : 8080

    Cocher "Utiliser ce proxy pour tous les protocoles"

Chrome/Edge :
bash

chrome --proxy-server="127.0.0.1:8080"

Configuration système (Windows) :

    Paramètres → Réseau et Internet → Proxy

    Activer "Utiliser un serveur proxy"

    Adresse : 127.0.0.1 Port : 8080


🔧 Personnalisation
Ajouter des domaines à la liste noire

Modifiez la méthode charger_blacklist() dans le code pour ajouter vos propres domaines.
Modifier la fréquence de rotation des profils

Changez la valeur time.sleep(60) dans la méthode rotation_profils().
Ajuster les patterns de détection

Personnalisez les patterns dans generer_patterns_avances().
📈 Statistiques

Le programme collecte en temps réel :

    Nombre de trackers bloqués

    Publicités interceptées

    Données économisées (Ko)

    Domaines appris par l'IA

    Patterns créés

    Profils utilisés

🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

    Fork le projet

    Créer une branche (git checkout -b feature/amelioration)

    Commit vos changements (git commit -m 'Ajout de fonctionnalité')

    Push (git push origin feature/amelioration)

    Ouvrir une Pull Request

📝 Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
⚠️ Avertissement

Cet outil est conçu pour protéger votre vie privée. Utilisez-le de manière éthique et responsable. L'auteur n'est pas responsable d'une mauvaise utilisation.
🙏 Remerciements

    Communauté Python pour les bibliothèques

    Projets open-source de blocage de publicités

    Contributeurs et testeurs

📧 Contact

Pour toute question ou suggestion :

    Ouvrir une issue sur GitHub


Développé avec ❤️ pour la protection de la vie privée
