#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application de Protection de la Vie Privée
Interface avec onglets détaillés pour visualiser en temps réel
"""

import os
import sys
import socket
import threading
import time
import json
import random
import re
import hashlib
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, urlunparse
import platform
import queue
from collections import deque, defaultdict, Counter
from pathlib import Path
import ssl
import select

# Interface graphique
try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox, font
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    print("⚠️ Tkinter n'est pas disponible.")

# Pour l'IA
try:
    import numpy as np
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("⚠️ NumPy non disponible.")


class IAAutoApprentissage:
    """
    IA auto-apprenante pour détecter les publicités et trackers
    """
    
    def __init__(self, logger):
        self.logger = logger
        self.dossier_modele = Path("modeles_ia")
        self.dossier_modele.mkdir(exist_ok=True)
        
        # Base de connaissances
        self.connaissances = {
            'domaines_connus': {},
            'patterns_regex': [],
            'faux_profils': []
        }
        
        # Statistiques d'apprentissage
        self.statistiques_ia = {
            'domaines_appris': 0,
            'patterns_crees': 0,
            'faux_profils_crees': 0,
            'previsions_total': 0,
            'previsions_correctes': 0,
            'nouveaux_patrons': 0,
            'dernier_apprentissage': None,
            'dernier_pattern': None,
            'dernier_domaine': None
        }
        
        # Historique des blocages
        self.historique_blocages = deque(maxlen=1000)
        self.historique_apprentissages = deque(maxlen=500)
        
        # Liste noire de base (étendue)
        self.blacklist_base = self.charger_blacklist()
        
        # Patterns avancés
        self.patterns_avances = self.generer_patterns_avances()
        
        # Charge les connaissances existantes
        self.charger_connaissances()
        
        # Démarrer le thread d'apprentissage
        self.apprentissage_actif = True
        threading.Thread(target=self.apprentissage_en_arriere_plan, daemon=True).start()
    
    def charger_blacklist(self):
        """Charge une liste noire étendue"""
        return [
            # Google
            'doubleclick.net', 'googleadservices.com', 'googlesyndication.com',
            'google-analytics.com', 'googletagmanager.com', 'google.com/ads',
            'google.com/pagead', 'google.com/analytics', 'google.com/tagmanager',
            'google.fr/ads', 'google.co.uk/ads', 'gstatic.com/ads',
            
            # Facebook
            'facebook.com/tr', 'connect.facebook.net', 'facebook.com/pixel',
            'facebook.com/impression', 'facebook.com/click', 'facebook.com/conversion',
            'fbcdn.net/ads', 'fb.com/tr', 'facebook.net/tr',
            
            # Amazon
            'amazon-adsystem.com', 'amazon.com/ads', 'amazon.com/pixel',
            'amazon.com/tracking', 'amazon.co.uk/ads', 'amazon.de/ads',
            'amazon.fr/ads', 'amazonaws.com/ads',
            
            # Microsoft
            'bing.com/ads', 'microsoft.com/ads', 'msn.com/ads',
            'live.com/ads', 'outlook.com/ads', 'bing.com/analytics',
            'clarity.ms', 'bat.bing.com',
            
            # Twitter/X
            'twitter.com/ads', 'twitter.com/analytics', 'twitter.com/pixel',
            'twimg.com/ads', 'x.com/ads', 't.co/ads',
            
            # LinkedIn
            'linkedin.com/analytics', 'linkedin.com/ads', 'licdn.com/ads',
            
            # Pinterest
            'pinterest.com/pixel', 'pinterest.com/ads', 'pinimg.com/ads',
            
            # Snapchat
            'snapchat.com/pixel', 'snapchat.com/ads', 'scanalytics.com',
            
            # TikTok
            'tiktok.com/pixel', 'tiktok.com/ads', 'tiktok.com/analytics',
            'byteoversea.com/ads', 'tik-tok.com/ads',
            
            # Analytics
            'matomo.org', 'hotjar.com', 'mouseflow.com', 'fullstory.com',
            'mixpanel.com', 'segment.com', 'amplitude.com', 'heap.com',
            'clicky.com', 'chartbeat.com', 'quantcast.com', 'comscore.com',
            'nr-data.net', 'newrelic.com', 'dynatrace.com',
            
            # Régies publicitaires
            'criteo.com', 'taboola.com', 'outbrain.com', 'revcontent.com',
            'adroll.com', 'perfectaudience.com', 'addthis.com',
            'sharethis.com', 'addtoany.com', 'disqus.com',
            
            # Ad servers
            'adnxs.com', 'rubiconproject.com', 'openx.net', 'pubmatic.com',
            'sonobi.com', 'indexww.com', 'lijit.com', 'sovrn.com',
            'media.net', 'yieldmo.com', 'contextweb.com', 'turn.com',
            'invitemedia.com', '2mdn.net', 'adtech.com', 'advertising.com',
            
            # DSP
            'c1exchange.com', 'tidaltv.com', 'spotxchange.com', 'telaria.com',
            'improvedigital.com', 'rhythmone.com', 'triplelift.com',
            
            # Mobile
            'smaato.com', 'inmobi.com', 'vungle.com', 'chartboost.com',
            'applovin.com', 'unityads.unity3d.com', 'ironsrc.com',
            
            # Email marketing
            'mailchimp.com/track', 'constantcontact.com/track',
            'sendinblue.com/track', 'mailjet.com/track', 'campaignmonitor.com/track',
            
            # A/B testing
            'optimizely.com', 'vwo.com', 'convert.com', 'abtasty.com',
            
            # Support client
            'intercom.com/track', 'zendesk.com/track', 'freshdesk.com/track',
            'olark.com', 'usabilla.com', 'survicate.com', 'qualaroo.com',
            
            # Heatmaps
            'crazyegg.com', 'luckyorange.com', 'clicktale.com',
            'sessioncam.com', 'inspectlet.com',
            
            # Délégation
            'edgesuite.net', 'akamaihd.net', 'cloudfront.net',
            'fastly.net', 'stackpathcdn.com', 'cloudflare.com/analytics'
        ]
    
    def generer_patterns_avances(self):
        """Génère des patterns avancés"""
        return {
            'pubs_standard': [
                r'/ad[s]?/',
                r'/ads?[_-]',
                r'/banner[s]?',
                r'/sponsor[s]?',
                r'/promo[s]?',
                r'/campaign[s]?',
                r'/conversion[s]?',
                r'/affiliate[s]?',
                r'/redirect[s]?',
                r'/pop[_-]?up',
                r'/pop[_-]?under',
                r'/interstitial'
            ],
            'trackers': [
                r'/track[s]?/',
                r'/tracker[s]?/',
                r'/analytics?/',
                r'/stat[s]?/',
                r'/pixel[s]?/',
                r'/beacon[s]?/',
                r'/collector[s]?/',
                r'/ingest[s]?/',
                r'/event[s]?/',
                r'/impression[s]?/'
            ],
            'parametres_suspects': [
                r'\?utm_',
                r'\?_ga=',
                r'\&_ga=',
                r'\?fbclid=',
                r'\&fbclid=',
                r'\?gclid=',
                r'\&gclid=',
                r'\?msclkid=',
                r'\&msclkid=',
                r'\?twclid=',
                r'\&twclid='
            ],
            'cookies_trackers': [
                r'_ga[^a-z]',
                r'_gid',
                r'_fbp',
                r'_hjid',
                r'_hj',
                r'_gauges',
                r'_gat',
                r'_gali',
                r'__utm',
                r'utm_source',
                r'utm_medium',
                r'utm_campaign'
            ]
        }
    
    def charger_connaissances(self):
        """Charge les connaissances"""
        try:
            # Domaines
            fichier = self.dossier_modele / "domaines_connus.json"
            if fichier.exists():
                with open(fichier, 'r', encoding='utf-8') as f:
                    self.connaissances['domaines_connus'] = json.load(f)
                    self.statistiques_ia['domaines_appris'] = len(self.connaissances['domaines_connus'])
                    self.logger.info(f"📚 {len(self.connaissances['domaines_connus'])} domaines chargés")
            
            # Patterns
            fichier = self.dossier_modele / "patterns_regex.json"
            if fichier.exists():
                with open(fichier, 'r', encoding='utf-8') as f:
                    self.connaissances['patterns_regex'] = json.load(f)
                    self.statistiques_ia['patterns_crees'] = len(self.connaissances['patterns_regex'])
                    self.logger.info(f"🔍 {len(self.connaissances['patterns_regex'])} patterns chargés")
            
            # Faux profils
            fichier = self.dossier_modele / "faux_profils.json"
            if fichier.exists():
                with open(fichier, 'r', encoding='utf-8') as f:
                    self.connaissances['faux_profils'] = json.load(f)
                    self.statistiques_ia['faux_profils_crees'] = len(self.connaissances['faux_profils'])
                    self.logger.info(f"🎭 {len(self.connaissances['faux_profils'])} faux profils chargés")
            
        except Exception as e:
            self.logger.error(f"Erreur chargement: {e}")
    
    def sauvegarder_connaissances(self):
        """Sauvegarde les connaissances"""
        try:
            with open(self.dossier_modele / "domaines_connus.json", 'w', encoding='utf-8') as f:
                json.dump(self.connaissances['domaines_connus'], f, indent=2)
            
            with open(self.dossier_modele / "patterns_regex.json", 'w', encoding='utf-8') as f:
                json.dump(self.connaissances['patterns_regex'], f, indent=2)
            
            with open(self.dossier_modele / "faux_profils.json", 'w', encoding='utf-8') as f:
                json.dump(self.connaissances['faux_profils'], f, indent=2)
            
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde: {e}")
    
    def analyser_url(self, url, stats=None):
        """Analyse une URL et retourne les détails"""
        url_lower = url.lower()
        parsed = urlparse(url)
        domaine = parsed.netloc
        chemin = parsed.path
        query = parsed.query
        
        details = {
            'bloque': False,
            'confiance': 0,
            'type': None,
            'methode': None,
            'raison': [],
            'domaine': domaine,
            'url': url,
            'timestamp': datetime.now()
        }
        
        # 1. Vérifier liste noire
        for domaine_noir in self.blacklist_base:
            if domaine_noir in domaine or domaine_noir in url_lower:
                details['bloque'] = True
                details['confiance'] = 0.95
                details['type'] = 'blacklist'
                details['methode'] = 'Liste noire'
                details['raison'].append(f"Domaine en liste noire: {domaine_noir}")
                
                # APPRENDRE CE DOMAINE MÊME S'IL EST EN LISTE NOIRE
                if domaine not in self.connaissances['domaines_connus']:
                    self.apprendre_nouveau_patron(domaine, 'blacklist', url)
                
                self.enregistrer_blocage(details, stats)
                return details
        
        # 2. Vérifier domaines appris
        if domaine in self.connaissances['domaines_connus']:
            info = self.connaissances['domaines_connus'][domaine]
            details['bloque'] = True
            details['confiance'] = 0.90
            details['type'] = info.get('type', 'appris')
            details['methode'] = 'IA - Appris'
            details['raison'].append(f"Déjà appris comme: {info.get('type', 'inconnu')}")
            self.enregistrer_blocage(details, stats)
            return details
        
        # 3. Vérifier patterns
        for categorie, patterns in self.patterns_avances.items():
            for pattern in patterns:
                if re.search(pattern, url_lower, re.IGNORECASE):
                    details['bloque'] = True
                    details['confiance'] = 0.85
                    details['type'] = categorie
                    details['methode'] = 'Pattern avancé'
                    details['raison'].append(f"Pattern {categorie}: {pattern}")
                    
                    # Apprendre ce nouveau domaine
                    self.apprendre_nouveau_patron(domaine, categorie, url)
                    
                    self.enregistrer_blocage(details, stats)
                    return details
        
        # 4. Vérifier patterns appris
        for pattern in self.connaissances['patterns_regex']:
            if isinstance(pattern, dict) and 'regex' in pattern:
                if re.search(pattern['regex'], url_lower, re.IGNORECASE):
                    details['bloque'] = True
                    details['confiance'] = pattern.get('confiance', 0.8)
                    details['type'] = pattern.get('type', 'pattern')
                    details['methode'] = 'Pattern appris'
                    details['raison'].append(f"Match pattern: {pattern.get('type', 'inconnu')}")
                    
                    # Apprendre si nouveau
                    if domaine not in self.connaissances['domaines_connus']:
                        self.apprendre_nouveau_patron(domaine, pattern.get('type', 'pattern'), url)
                    
                    self.enregistrer_blocage(details, stats)
                    return details
        
        # 5. Détection intelligente pour les domaines inconnus
        if not details['bloque'] and domaine:
            # Compter les points suspects
            score = 0
            raisons = []
            
            # Trop de sous-domaines
            if domaine.count('.') > 3:
                score += 1
                raisons.append("Trop de sous-domaines")
            
            # Domaines avec chiffres
            if re.search(r'\d{4,}', domaine):
                score += 1
                raisons.append("Chiffres dans le domaine")
            
            # Mots suspects dans le chemin
            mots_suspects = ['ad', 'ads', 'banner', 'sponsor', 'promo', 'track', 'pixel', 'beacon']
            for mot in mots_suspects:
                if mot in chemin.lower():
                    score += 2
                    raisons.append(f"Mot suspect: {mot}")
            
            if score >= 2:
                details['bloque'] = True
                details['confiance'] = 0.7 + (score * 0.05)
                details['type'] = 'ia_detecte'
                details['methode'] = 'Détection intelligente'
                details['raison'] = raisons
                
                # Apprendre ce nouveau domaine
                self.apprendre_nouveau_patron(domaine, 'ia_detecte', url)
                self.enregistrer_blocage(details, stats)
                return details
        
        self.statistiques_ia['previsions_total'] += 1
        return details
    
    def enregistrer_blocage(self, details, stats=None):
        """Enregistre un blocage dans l'historique"""
        if stats:
            # Catégorisation plus précise
            type_blocage = details.get('type', '')
            domaine = details.get('domaine', '')
            
            # Liste des domaines publicitaires connus
            domaines_pubs = ['doubleclick.net', 'googleadservices.com', 'googlesyndication.com', 
                            'criteo.com', 'taboola.com', 'outbrain.com']
            
            # Si c'est un domaine publicitaire connu
            if any(pub_domain in domaine for pub_domain in domaines_pubs):
                stats.incrementer_pub('regie_pub')
                stats.ajouter_donnees_economisees(random.randint(2048, 8192))
            # Si c'est un pattern de pub
            elif any(pub_type in str(type_blocage) for pub_type in ['pubs', 'publicite', 'banner', 'pop', 'ad']):
                stats.incrementer_pub(type_blocage)
                stats.ajouter_donnees_economisees(random.randint(1024, 4096))
            # Sinon c'est un tracker
            else:
                stats.incrementer_tracker(type_blocage)
                stats.ajouter_donnees_economisees(random.randint(512, 2048))
            
            # Ajouter le domaine aux stats
            if domaine:
                stats.ajouter_domaine(domaine)
        
        self.historique_blocages.append(details)
        self.statistiques_ia['previsions_total'] += 1
        self.statistiques_ia['previsions_correctes'] += 1
    
    def apprendre_nouveau_patron(self, domaine, type_pub, url):
        """Apprend un nouveau patron avec plus de détails"""
        if domaine not in self.connaissances['domaines_connus']:
            self.connaissances['domaines_connus'][domaine] = {
                'type': type_pub,
                'premier_vu': datetime.now().isoformat(),
                'dernier_vu': datetime.now().isoformat(),
                'compteur': 1,
                'exemple_url': url[:200],
                'patterns_detectes': []
            }
            
            self.statistiques_ia['domaines_appris'] += 1
            self.statistiques_ia['dernier_domaine'] = domaine
            self.statistiques_ia['nouveaux_patrons'] += 1
            self.statistiques_ia['dernier_apprentissage'] = datetime.now()
            
            # Créer un pattern à partir du domaine
            pattern_domaine = domaine.replace('.', '\\.')
            
            # Créer plusieurs patterns
            patterns_a_ajouter = [
                {
                    'regex': pattern_domaine,
                    'type': type_pub,
                    'confiance': 0.8,
                    'source': domaine,
                    'appris': datetime.now().isoformat()
                }
            ]
            
            # Ajouter un pattern pour le domaine avec sous-domaines
            parties = domaine.split('.')
            if len(parties) > 2:
                pattern_wildcard = r'[a-z0-9-]+\.' + parties[-2] + r'\.' + parties[-1]
                patterns_a_ajouter.append({
                    'regex': pattern_wildcard,
                    'type': type_pub,
                    'confiance': 0.7,
                    'source': domaine + '_wildcard',
                    'appris': datetime.now().isoformat()
                })
            
            # Ajouter les nouveaux patterns
            for pattern in patterns_a_ajouter:
                # Vérifier si le pattern existe déjà
                existe = False
                for p in self.connaissances['patterns_regex']:
                    if isinstance(p, dict) and p.get('regex') == pattern['regex']:
                        existe = True
                        break
                
                if not existe:
                    self.connaissances['patterns_regex'].append(pattern)
                    self.statistiques_ia['patterns_crees'] += 1
                    self.statistiques_ia['dernier_pattern'] = pattern
            
            self.historique_apprentissages.append({
                'timestamp': datetime.now(),
                'type': 'nouveau_domaine',
                'domaine': domaine,
                'categorie': type_pub,
                'patterns_crees': len(patterns_a_ajouter)
            })
            
            self.logger.ia(f"🧠 NOUVEAU DOMAINE APPRIS: {domaine} ({type_pub})")
            self.logger.ia(f"   └─ {len(patterns_a_ajouter)} pattern(s) créé(s)")
            
            # Sauvegarder immédiatement
            self.sauvegarder_connaissances()
        
        else:
            # Mettre à jour le compteur
            self.connaissances['domaines_connus'][domaine]['compteur'] += 1
            self.connaissances['domaines_connus'][domaine]['dernier_vu'] = datetime.now().isoformat()
    
    def creer_faux_profil(self):
        """Crée un faux profil"""
        profil = {
            'id': hashlib.md5(str(random.random()).encode()).hexdigest()[:16],
            'user_agent': self.generer_user_agent_aleatoire(),
            'resolution': random.choice(['1920x1080', '1366x768', '1536x864', '1440x900', '2560x1440']),
            'langue': random.choice(['fr-FR,fr;q=0.9', 'en-US,en;q=0.8', 'de-DE,de;q=0.7']),
            'fuseau_horaire': random.choice(['Europe/Paris', 'America/New_York', 'Asia/Tokyo']),
            'do_not_track': random.choice(['0', '1']),
            'cookies_acceptes': random.choice([True, False]),
            'date_creation': datetime.now().isoformat(),
            'cookies_factices': self.generer_cookies_aleatoires()
        }
        
        self.connaissances['faux_profils'].append(profil)
        self.statistiques_ia['faux_profils_crees'] += 1
        
        self.historique_apprentissages.append({
            'timestamp': datetime.now(),
            'type': 'nouveau_profil',
            'profil_id': profil['id']
        })
        
        self.logger.ia(f"🎭 NOUVEAU FAUX PROFIL: {profil['id']}")
        return profil
    
    def generer_user_agent_aleatoire(self):
        """Génère un user agent aléatoire"""
        systemes = [
            f"Windows NT {random.choice(['10.0', '6.3', '6.2', '6.1'])}; Win64; x64",
            f"Macintosh; Intel Mac OS X 10_{random.randint(13, 15)}_{random.randint(0, 7)}",
            f"X11; Linux x86_64",
            f"iPhone; CPU iPhone OS {random.randint(14, 17)}_{random.randint(0, 5)} like Mac OS X"
        ]
        
        navigateurs = [
            f"AppleWebKit/537.36 Chrome/{random.randint(110, 120)}.0.0.0 Safari/537.36",
            f"AppleWebKit/605.1.15 Version/{random.randint(15, 17)}.0 Safari/605.1.15",
            f"Gecko/20100101 Firefox/{random.randint(110, 121)}.0"
        ]
        
        return f"Mozilla/5.0 ({random.choice(systemes)}) {random.choice(navigateurs)}"
    
    def generer_cookies_aleatoires(self):
        """Génère des cookies aléatoires"""
        return {
            '_ga': f"GA1.2.{random.randint(1000000000, 9999999999)}.{int(time.time())}",
            '_gid': f"GA1.2.{random.randint(1000000000, 9999999999)}",
            '_fbp': f"fb.1.{int(time.time())}.{random.randint(1000000000, 9999999999)}",
            'theme': random.choice(['light', 'dark']),
            'language': random.choice(['fr', 'en', 'de', 'es'])
        }
    
    def apprentissage_en_arriere_plan(self):
        """Thread d'apprentissage avec sauvegarde fréquente"""
        while self.apprentissage_actif:
            time.sleep(30)  # Sauvegarde toutes les 30 secondes au lieu de 60
            
            # Créer un nouveau profil si nécessaire
            if len(self.connaissances['faux_profils']) < 10:
                self.creer_faux_profil()
            
            # Analyser les tendances des dernières minutes
            self.analyser_tendances()
            
            # Sauvegarder TOUTES les connaissances
            self.sauvegarder_connaissances()
            
            # Log de l'activité d'apprentissage
            if self.statistiques_ia['nouveaux_patrons'] > 0:
                self.logger.ia(f"💾 Sauvegarde auto: {self.statistiques_ia['domaines_appris']} domaines, {self.statistiques_ia['patterns_crees']} patterns")
    
    def obtenir_historique_blocages(self, limite=100):
        """Retourne l'historique des blocages"""
        return list(self.historique_blocages)[:limite]
    
    def obtenir_historique_apprentissages(self, limite=100):
        """Retourne l'historique des apprentissages"""
        return list(self.historique_apprentissages)[:limite]
    
    def obtenir_statistiques_ia(self):
        """Retourne les stats IA"""
        precision = 0
        if self.statistiques_ia['previsions_total'] > 0:
            precision = (self.statistiques_ia['previsions_correctes'] / 
                        self.statistiques_ia['previsions_total'] * 100)
        
        return {
            'domaines_appris': self.statistiques_ia['domaines_appris'],
            'patterns_crees': self.statistiques_ia['patterns_crees'],
            'faux_profils': self.statistiques_ia['faux_profils_crees'],
            'previsions_total': self.statistiques_ia['previsions_total'],
            'previsions_correctes': self.statistiques_ia['previsions_correctes'],
            'precision': round(precision, 1),
            'dernier_apprentissage': self.statistiques_ia['dernier_apprentissage'],
            'dernier_domaine': self.statistiques_ia['dernier_domaine'],
            'dernier_pattern': self.statistiques_ia['dernier_pattern']
        }
    
    def arreter(self):
        self.apprentissage_actif = False
        self.sauvegarder_connaissances()


    def analyser_tendances(self):
        """Analyse les tendances pour détecter de nouveaux types de trackers"""
        if len(self.historique_blocages) < 10:
            return
        
        # Analyser les 50 derniers blocages
        derniers_blocages = list(self.historique_blocages)[-50:]
        
        # Grouper par domaine
        domaines_recents = {}
        for blocage in derniers_blocages:
            domaine = blocage.get('domaine', '')
            if domaine:
                domaines_recents[domaine] = domaines_recents.get(domaine, 0) + 1
        
        # Détecter les nouveaux domaines fréquents
        for domaine, count in domaines_recents.items():
            if count >= 3 and domaine not in self.connaissances['domaines_connus']:
                # Nouveau domaine potentiel
                type_propose = self.detecter_type_domaine(domaine)
                self.logger.ia(f"🔍 Nouveau domaine potentiel détecté: {domaine} ({count} fois)")
                self.logger.ia(f"   └─ Type suggéré: {type_propose}")
                
                # Apprendre automatiquement si confiance élevée
                if count >= 5:
                    self.apprendre_nouveau_patron(domaine, type_propose, f"https://{domaine}/")

    def detecter_type_domaine(self, domaine):
        """Détecte automatiquement le type d'un domaine"""
        domaine_lower = domaine.lower()
        
        if 'ad' in domaine_lower or 'ads' in domaine_lower:
            return 'publicite'
        elif 'track' in domaine_lower or 'analytics' in domaine_lower:
            return 'tracker'
        elif 'pixel' in domaine_lower or 'beacon' in domaine_lower:
            return 'pixel'
        elif 'doubleclick' in domaine_lower or 'googlead' in domaine_lower:
            return 'google_ads'
        elif 'facebook' in domaine_lower or 'fb' in domaine_lower:
            return 'facebook'
        elif 'amazon' in domaine_lower:
            return 'amazon'
        else:
            return 'inconnu'
    
class Logger:
    """Gestionnaire de logs"""
    def __init__(self, max_logs=1000):
        self.logs = deque(maxlen=max_logs)
        self.queue = queue.Queue()
        self.historique_logs = []
    
    def add_log(self, niveau, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'niveau': niveau,
            'message': message,
            'datetime': datetime.now()
        }
        self.logs.appendleft(log_entry)
        self.historique_logs.append(log_entry)
        self.queue.put(log_entry)
    
    def info(self, message): self.add_log("INFO", message)
    def warning(self, message): self.add_log("⚠️", message)
    def error(self, message): self.add_log("❌", message)
    def success(self, message): self.add_log("✅", message)
    def block(self, message): self.add_log("🚫", message)
    def ia(self, message): self.add_log("🧠", message)
    
    def get_logs(self, limit=100):
        return list(self.logs)[:limit]
    
    def get_historique(self, niveau=None, limite=500):
        if niveau:
            return [l for l in self.historique_logs[-limite:] if l['niveau'] == niveau]
        return self.historique_logs[-limite:]


class Statistiques:
    """Gestionnaire des statistiques détaillées"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.trackers_bloques = 0
        self.pubs_bloquees = 0
        self.requetes_analysees = 0
        self.donnees_economisees = 0
        self.profils_utilises = 0
        self.heure_demarrage = None
        
        self.categories = Counter()
        self.methodes = Counter()
        self.domaines = Counter()
        self.historique_minute = deque(maxlen=60)
        self.dernier_blocage = None
    
    def demarrer(self):
        self.heure_demarrage = datetime.now()
    
    def incrementer_tracker(self, categorie='tracker'):
        self.trackers_bloques += 1
        self.categories[categorie] += 1
        self.methodes[categorie] += 1
        self.requetes_analysees += 1
        self.dernier_blocage = datetime.now()
        self.historique_minute.append({
            'time': datetime.now(),
            'type': 'tracker',
            'categorie': categorie
        })
    
    def incrementer_pub(self, categorie='publicite'):
        self.pubs_bloquees += 1
        self.categories[categorie] = self.categories.get(categorie, 0) + 1
        self.methodes['publicite'] = self.methodes.get('publicite', 0) + 1  # Changé ici
        self.requetes_analysees += 1
        self.dernier_blocage = datetime.now()
        self.historique_minute.append({
            'time': datetime.now(),
            'type': 'pub',
            'categorie': categorie
        })
        print(f"PUB INC: {categorie} - Total: {self.pubs_bloquees}")  # Debug
    
    def ajouter_donnees_economisees(self, octets):
        self.donnees_economisees += octets / 1024
    
    def utiliser_profil(self):
        self.profils_utilises += 1
    
    def ajouter_domaine(self, domaine):
        self.domaines[domaine] += 1
    
    def obtenir_resume(self):
        temps = datetime.now() - self.heure_demarrage if self.heure_demarrage else timedelta()
        vitesse = len([x for x in self.historique_minute 
                      if (datetime.now() - x['time']).seconds < 60])
        
        return {
            'trackers': self.trackers_bloques,
            'pubs': self.pubs_bloquees,
            'total': self.trackers_bloques + self.pubs_bloquees,
            'donnees_economisees': round(self.donnees_economisees, 2),
            'temps': str(temps).split('.')[0],
            'profils': self.profils_utilises,
            'vitesse': vitesse,
            'dernier': self.dernier_blocage.strftime("%H:%M:%S") if self.dernier_blocage else "-",
            'categories': dict(self.categories.most_common(10)),
            'methodes': dict(self.methodes.most_common(5)),
            'top_domaines': dict(self.domaines.most_common(10))
        }


class ProxyHandler(BaseHTTPRequestHandler):
    """Gestionnaire proxy"""
    
    def __init__(self, *args, parent=None, **kwargs):
        self.parent = parent
        super().__init__(*args, **kwargs)
    
    def log_message(self, format, *args):
        pass
    
    def _brouiller_requete(self):
        if self.parent and self.parent.profil_actuel:
            profil = self.parent.profil_actuel
            self.headers['User-Agent'] = profil['user_agent']
            self.headers['Accept-Language'] = profil['langue']
            self.headers['DNT'] = profil['do_not_track']
    
    def do_CONNECT(self):
        try:
            host, port = self.path.split(':')
            port = int(port)
            
            # Analyser
            details = self.parent.ia.analyser_url(f"https://{host}", self.parent.stats)
            
            if details['bloque']:
                # Déterminer si c'est une pub ou un tracker
                domaines_pubs = ['doubleclick.net', 'googleadservices.com', 'googlesyndication.com']
                if any(pub_domain in host for pub_domain in domaines_pubs):
                    self.parent.stats.incrementer_pub('regie_pub')
                else:
                    self.parent.stats.incrementer_tracker('https')
                
                self.parent.logger.block(f"🚫 HTTPS: {host}")
                for raison in details['raison']:
                    self.parent.logger.ia(f"   └─ {raison}")
                self.send_response(403)
                self.end_headers()
                return
            
            # Tunnel
            try:
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.settimeout(30)
                remote.connect((host, port))
                
                self.send_response(200, 'Connection Established')
                self.end_headers()
                
                self.connection.setblocking(False)
                remote.setblocking(False)
                
                while True:
                    r, _, _ = select.select([self.connection, remote], [], [], 1)
                    for sock in r:
                        other = remote if sock is self.connection else self.connection
                        try:
                            data = sock.recv(8192)
                            if not data:
                                return
                            other.sendall(data)
                        except:
                            return
            except Exception as e:
                self.parent.logger.error(f"Erreur tunnel: {e}")
            finally:
                remote.close()
                
        except Exception as e:
            self.parent.logger.error(f"Erreur CONNECT: {e}")
    
    def do_GET(self):
        self._handle_http()
    
    def do_POST(self):
        self._handle_http()
    
    def _handle_http(self):
        try:
            self._brouiller_requete()
            
            host = self.headers.get('Host', '')
            url = f"http://{host}{self.path}"
            
            # Analyser
            details = self.parent.ia.analyser_url(url, self.parent.stats)
            
            if details['bloque']:
                # Déterminer le type pour les stats
                if 'pubs' in str(details['type']) or details['type'] in ['pubs_standard']:
                    self.parent.stats.incrementer_pub(details['type'])
                else:
                    self.parent.stats.incrementer_tracker(details['type'])
                
                self.parent.stats.ajouter_donnees_economisees(random.randint(1024, 20480))
                self.parent.logger.block(f"🚫 HTTP: {host}{self.path}")
                for raison in details['raison']:
                    self.parent.logger.ia(f"   └─ {raison}")
                self.parent.stats.ajouter_domaine(details['domaine'])
                self.send_response(204)
                self.end_headers()
                return
            
            # Proxy normal
            if not host:
                self.send_error(400)
                return
            
            if ':' in host:
                hostname, port = host.split(':')
                port = int(port)
            else:
                hostname = host
                port = 80
            
            try:
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.settimeout(30)
                remote.connect((hostname, port))
                
                # Envoyer requête
                remote.send(f"{self.command} {self.path} HTTP/1.1\r\n".encode())
                for k, v in self.headers.items():
                    if k.lower() not in ['proxy-connection', 'connection']:
                        remote.send(f"{k}: {v}\r\n".encode())
                remote.send(b"Connection: close\r\n\r\n")
                
                # Recevoir réponse
                response = b''
                while True:
                    try:
                        data = remote.recv(8192)
                        if not data:
                            break
                        response += data
                    except:
                        break
                
                if response:
                    self.wfile.write(response)
                else:
                    self.send_error(502)
                    
            except Exception as e:
                self.parent.logger.error(f"Erreur proxy: {e}")
                self.send_error(502)
            finally:
                remote.close()
                
        except Exception as e:
            self.parent.logger.error(f"Erreur: {e}")
            self.send_error(500)


class ThreadedHTTPServer(HTTPServer):
    def process_request(self, request, client_address):
        threading.Thread(target=self.process_request_thread,
                        args=(request, client_address)).start()
    
    def process_request_thread(self, request, client_address):
        try:
            self.finish_request(request, client_address)
        except Exception:
            self.handle_error(request, client_address)
        finally:
            self.shutdown_request(request)


class ProtectionViePrivee:
    """Serveur proxy"""
    
    def __init__(self, logger, stats, ia):
        self.logger = logger
        self.stats = stats
        self.ia = ia
        self.hote = '127.0.0.1'
        self.port = 8080
        self.proxy_actif = False
        self.serveur_proxy = None
        self.thread_proxy = None
        self.profil_actuel = None
        self.rotation_active = True
        self.historique_profils = deque(maxlen=100)
        
        threading.Thread(target=self.rotation_profils, daemon=True).start()
    
    def rotation_profils(self):
        while self.rotation_active:
            time.sleep(60)
            if self.proxy_actif and self.ia.connaissances['faux_profils']:
                ancien = self.profil_actuel['id'] if self.profil_actuel else "aucun"
                self.profil_actuel = random.choice(self.ia.connaissances['faux_profils'])
                self.stats.utiliser_profil()
                self.historique_profils.append({
                    'timestamp': datetime.now(),
                    'ancien': ancien,
                    'nouveau': self.profil_actuel['id']
                })
                self.logger.ia(f"🔄 ROTATION PROFIL: {ancien} → {self.profil_actuel['id']}")
    
    def demarrer(self):
        if self.proxy_actif:
            return False
        
        try:
            self.serveur_proxy = ThreadedHTTPServer(
                (self.hote, self.port),
                lambda *a, **k: ProxyHandler(*a, parent=self, **k)
            )
            
            self.proxy_actif = True
            self.stats.demarrer()
            
            if not self.ia.connaissances['faux_profils']:
                self.profil_actuel = self.ia.creer_faux_profil()
            else:
                self.profil_actuel = random.choice(self.ia.connaissances['faux_profils'])
            
            self.logger.success(f"✅ Proxy IA démarré sur {self.hote}:{self.port}")
            self.logger.ia(f"🧠 IA auto-apprenante active")
            self.logger.ia(f"🎭 Profil actuel: {self.profil_actuel['id']}")
            self.logger.ia(f"📊 {len(self.ia.blacklist_base)} domaines en liste noire")
            self.logger.ia(f"🔍 {len(self.ia.patterns_avances)} catégories de patterns")
            
            self.thread_proxy = threading.Thread(target=self.serveur_proxy.serve_forever)
            self.thread_proxy.daemon = True
            self.thread_proxy.start()
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur démarrage: {e}")
            return False
    
    def arreter(self):
        if self.serveur_proxy:
            self.serveur_proxy.shutdown()
            self.serveur_proxy.server_close()
            self.proxy_actif = False
            self.rotation_active = False
            self.logger.info("Proxy IA arrêté")
            return True
        return False
    
    def basculer(self):
        if self.proxy_actif:
            return self.arreter()
        else:
            return self.demarrer()


class ApplicationGUI:
    """Interface graphique avec onglets"""
    
    def __init__(self):
        if not TKINTER_AVAILABLE:
            print("❌ Tkinter non disponible")
            sys.exit(1)
        
        self.root = tk.Tk()
        self.root.title("🧠 Protection IA - Vue par onglets")
        self.root.geometry("1400x900")
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.colors = {
            'bg': '#f0f2f5',
            'primary': '#667eea',
            'secondary': '#764ba2',
            'ia': '#6f42c1',
            'success': '#28a745',
            'danger': '#dc3545',
            'warning': '#ffc107',
            'info': '#17a2b8'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Composants
        self.logger = Logger()
        self.stats = Statistiques()
        self.ia = IAAutoApprentissage(self.logger)
        self.proxy = ProtectionViePrivee(self.logger, self.stats, self.ia)
        
        # Variables
        self.proxy_actif = tk.BooleanVar(value=False)
        self.auto_refresh = tk.BooleanVar(value=True)
        
        # Interface
        self.setup_ui()
        self.mettre_a_jour_stats()
        
        self.root.protocol("WM_DELETE_WINDOW", self.fermer)
    
    def setup_ui(self):
        """Configure l'interface avec onglets"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # En-tête avec contrôle
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Titre
        title = tk.Label(
            header_frame,
            text="🧠 PROTECTION IA - TABLEAU DE BORD COMPLET",
            font=('Arial', 18, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['ia']
        )
        title.pack(side=tk.LEFT)
        
        # Bouton principal
        self.btn_toggle = tk.Button(
            header_frame,
            text="🧠 DÉMARRER",
            command=self.toggle_proxy,
            font=('Arial', 11, 'bold'),
            bg=self.colors['ia'],
            fg='white',
            padx=20,
            pady=5,
            cursor='hand2'
        )
        self.btn_toggle.pack(side=tk.RIGHT, padx=5)
        
        # Checkbox auto-refresh
        ttk.Checkbutton(
            header_frame,
            text="Rafraîchissement auto",
            variable=self.auto_refresh
        ).pack(side=tk.RIGHT, padx=5)
        
        # Créer le Notebook (onglets)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Créer les 7 onglets
        self.creer_onglet_tableau_bord()
        self.creer_onglet_trackers()
        self.creer_onglet_publicites()
        self.creer_onglet_profils()
        self.creer_onglet_statistiques()
        self.creer_onglet_ia()
        self.creer_onglet_logs()
        
        # Barre de statut
        self.setup_status_bar()
    
    def creer_onglet_tableau_bord(self):
        """Onglet 1: Tableau de bord principal"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Tableau de bord")
        
        # Métriques principales en haut
        metrics_frame = ttk.LabelFrame(frame, text="Métriques en direct", padding="10")
        metrics_frame.pack(fill=tk.X, pady=5)
        
        # Grid de métriques
        self.metrics_labels = {}
        row = ttk.Frame(metrics_frame)
        row.pack(fill=tk.X, pady=5)
        
        metrics = [
            ('Trackers', 'trackers', '🔴', self.colors['danger']),
            ('Publicités', 'pubs', '📢', self.colors['warning']),
            ('Total', 'total', '🛡️', self.colors['primary']),
            ('Vitesse', 'vitesse', '⚡', self.colors['info']),
            ('Données', 'donnees', '💾', self.colors['success'])
        ]
        
        for label, key, emoji, color in metrics:
            frame_metric = ttk.Frame(row, relief='solid', borderwidth=1)
            frame_metric.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
            
            tk.Label(frame_metric, text=f"{emoji} {label}", font=('Arial', 10), bg='white').pack(pady=(5, 0))
            self.metrics_labels[key] = tk.Label(
                frame_metric, text="0", font=('Arial', 24, 'bold'),
                fg=color, bg='white'
            )
            self.metrics_labels[key].pack(pady=(0, 5))
        
        # Info en temps réel
        info_frame = ttk.LabelFrame(frame, text="Informations temps réel", padding="10")
        info_frame.pack(fill=tk.X, pady=5)
        
        # Créer un grid pour les infos
        self.info_labels = {}
        infos = [
            ('Statut proxy', 'statut', 'Arrêté'),
            ('Profil actuel', 'profil', 'Aucun'),
            ('Dernier blocage', 'dernier', '-'),
            ('Temps protection', 'temps', '00:00:00'),
            ('Domaines appris', 'domaines', '0'),
            ('Faux profils', 'nb_profils', '0')
        ]
        
        row = ttk.Frame(info_frame)
        row.pack(fill=tk.X, pady=2)
        
        for i, (label, key, default) in enumerate(infos):
            frame_info = ttk.Frame(row)
            frame_info.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            tk.Label(frame_info, text=label, font=('Arial', 9, 'bold')).pack(anchor=tk.W)
            self.info_labels[key] = tk.Label(frame_info, text=default, font=('Arial', 10))
            self.info_labels[key].pack(anchor=tk.W)
        
        # Graphique des dernières minutes (simulé avec des barres)
        graph_frame = ttk.LabelFrame(frame, text="Activité des dernières minutes", padding="10")
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.canvas = tk.Canvas(graph_frame, bg='white', height=150)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Derniers blocages
        derniers_frame = ttk.LabelFrame(frame, text="Derniers blocages", padding="10")
        derniers_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.liste_derniers = scrolledtext.ScrolledText(
            derniers_frame, height=8, font=('Consolas', 9)
        )
        self.liste_derniers.pack(fill=tk.BOTH, expand=True)
    
    def creer_onglet_trackers(self):
        """Onglet 2: Trackers détaillés"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔍 Trackers")
        
        # Stats trackers
        stats_frame = ttk.LabelFrame(frame, text="Statistiques des trackers", padding="10")
        stats_frame.pack(fill=tk.X, pady=5)
        
        self.trackers_labels = {}
        row = ttk.Frame(stats_frame)
        row.pack(fill=tk.X)
        
        stats = [
            ('Total trackers', 'total_trackers', '0'),
            ('Par heure', 'par_heure', '0'),
            ('Par minute', 'par_minute', '0'),
            ('Moyenne', 'moyenne', '0/min')
        ]
        
        for label, key, default in stats:
            frame_stat = ttk.Frame(row, relief='solid', borderwidth=1)
            frame_stat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
            
            tk.Label(frame_stat, text=label, font=('Arial', 9)).pack(pady=(2, 0))
            self.trackers_labels[key] = tk.Label(
                frame_stat, text=default, font=('Arial', 16, 'bold'),
                fg=self.colors['danger']
            )
            self.trackers_labels[key].pack(pady=(0, 2))
        
        # Top domaines trackers
        top_frame = ttk.LabelFrame(frame, text="Top domaines trackers", padding="10")
        top_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.top_trackers = scrolledtext.ScrolledText(
            top_frame, height=10, font=('Consolas', 10)
        )
        self.top_trackers.pack(fill=tk.BOTH, expand=True)
        
        # Méthodes de détection
        methodes_frame = ttk.LabelFrame(frame, text="Méthodes de détection", padding="10")
        methodes_frame.pack(fill=tk.X, pady=5)
        
        self.methodes_labels = {}
        row = ttk.Frame(methodes_frame)
        row.pack(fill=tk.X)
        
        methodes = [
            ('Liste noire', 'blacklist', '0'),
            ('Patterns IA', 'ia_detecte', '0'),
            ('Domaines appris', 'appris', '0'),
            ('Patterns regex', 'pattern', '0')
        ]
        
        for label, key, default in methodes:
            frame_meth = ttk.Frame(row, relief='solid', borderwidth=1)
            frame_meth.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
            
            tk.Label(frame_meth, text=label, font=('Arial', 9)).pack(pady=(2, 0))
            self.methodes_labels[key] = tk.Label(
                frame_meth, text=default, font=('Arial', 14, 'bold'),
                fg=self.colors['secondary']
            )
            self.methodes_labels[key].pack(pady=(0, 2))
    
    def creer_onglet_publicites(self):
        """Onglet 3: Publicités détaillées"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📢 Publicités")
        
        # Stats pubs
        stats_frame = ttk.LabelFrame(frame, text="Statistiques des publicités", padding="10")
        stats_frame.pack(fill=tk.X, pady=5)
        
        self.pubs_labels = {}
        row = ttk.Frame(stats_frame)
        row.pack(fill=tk.X)
        
        stats = [
            ('Total pubs', 'total_pubs', '0'),
            ('Bannières', 'bannieres', '0'),
            ('Pop-ups', 'popups', '0'),
            ('Vidéos', 'videos', '0')
        ]
        
        for label, key, default in stats:
            frame_stat = ttk.Frame(row, relief='solid', borderwidth=1)
            frame_stat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
            
            tk.Label(frame_stat, text=label, font=('Arial', 9)).pack(pady=(2, 0))
            self.pubs_labels[key] = tk.Label(
                frame_stat, text=default, font=('Arial', 16, 'bold'),
                fg=self.colors['warning']
            )
            self.pubs_labels[key].pack(pady=(0, 2))
        
        # Répartition par type
        repartition_frame = ttk.LabelFrame(frame, text="Répartition par type", padding="10")
        repartition_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.repartition_pubs = scrolledtext.ScrolledText(
            repartition_frame, height=15, font=('Consolas', 10)
        )
        self.repartition_pubs.pack(fill=tk.BOTH, expand=True)
    
    def creer_onglet_profils(self):
        """Onglet 4: Gestion des profils"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎭 Profils")
        
        # Profil actuel
        current_frame = ttk.LabelFrame(frame, text="Profil actuel", padding="10")
        current_frame.pack(fill=tk.X, pady=5)
        
        self.current_profil_text = scrolledtext.ScrolledText(
            current_frame, height=8, font=('Consolas', 10)
        )
        self.current_profil_text.pack(fill=tk.BOTH, expand=True)
        
        # Boutons de contrôle
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            btn_frame,
            text="🎭 Nouveau profil",
            command=self.creer_faux_profil
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            btn_frame,
            text="🔄 Rotation forcée",
            command=self.forcer_rotation
        ).pack(side=tk.LEFT, padx=2)
        
        # Liste des profils
        list_frame = ttk.LabelFrame(frame, text="Tous les profils", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.liste_profils = scrolledtext.ScrolledText(
            list_frame, height=15, font=('Consolas', 9)
        )
        self.liste_profils.pack(fill=tk.BOTH, expand=True)
        
        # Historique des rotations
        hist_frame = ttk.LabelFrame(frame, text="Historique des rotations", padding="10")
        hist_frame.pack(fill=tk.X, pady=5)
        
        self.historique_rotations = scrolledtext.ScrolledText(
            hist_frame, height=5, font=('Consolas', 9)
        )
        self.historique_rotations.pack(fill=tk.BOTH, expand=True)
    
    def creer_onglet_statistiques(self):
        """Onglet 5: Statistiques détaillées"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📈 Statistiques")
        
        # Statistiques globales
        global_frame = ttk.LabelFrame(frame, text="Statistiques globales", padding="10")
        global_frame.pack(fill=tk.X, pady=5)
        
        self.global_stats_text = scrolledtext.ScrolledText(
            global_frame, height=8, font=('Consolas', 10)
        )
        self.global_stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Graphiques (simulés)
        graph_frame = ttk.LabelFrame(frame, text="Évolution", padding="10")
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.graph_canvas = tk.Canvas(graph_frame, bg='white', height=200)
        self.graph_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Prévisions
        prev_frame = ttk.LabelFrame(frame, text="Prévisions IA", padding="10")
        prev_frame.pack(fill=tk.X, pady=5)
        
        self.previsions_text = scrolledtext.ScrolledText(
            prev_frame, height=5, font=('Consolas', 10)
        )
        self.previsions_text.pack(fill=tk.BOTH, expand=True)
    
    def creer_onglet_ia(self):
        """Onglet 6: Intelligence Artificielle"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🧠 IA")
        
        # Métriques IA
        metrics_frame = ttk.LabelFrame(frame, text="Métriques d'apprentissage", padding="10")
        metrics_frame.pack(fill=tk.X, pady=5)
        
        self.ia_metrics_labels = {}
        row = ttk.Frame(metrics_frame)
        row.pack(fill=tk.X)
        
        metrics = [
            ('Domaines appris', 'ia_domaines', '0'),
            ('Patterns créés', 'ia_patterns', '0'),
            ('Précision', 'ia_precision', '0%'),
            ('Prévisions', 'ia_previsions', '0')
        ]
        
        for label, key, default in metrics:
            frame_metric = ttk.Frame(row, relief='solid', borderwidth=1)
            frame_metric.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
            
            tk.Label(frame_metric, text=label, font=('Arial', 9)).pack(pady=(2, 0))
            self.ia_metrics_labels[key] = tk.Label(
                frame_metric, text=default, font=('Arial', 16, 'bold'),
                fg=self.colors['ia']
            )
            self.ia_metrics_labels[key].pack(pady=(0, 2))
        
        # Derniers apprentissages
        apprentissages_frame = ttk.LabelFrame(frame, text="Derniers apprentissages", padding="10")
        apprentissages_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.apprentissages_text = scrolledtext.ScrolledText(
            apprentissages_frame, height=10, font=('Consolas', 10)
        )
        self.apprentissages_text.pack(fill=tk.BOTH, expand=True)
        
        # Liste noire
        blacklist_frame = ttk.LabelFrame(frame, text="Liste noire (extrait)", padding="10")
        blacklist_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.blacklist_text = scrolledtext.ScrolledText(
            blacklist_frame, height=8, font=('Consolas', 9)
        )
        self.blacklist_text.pack(fill=tk.BOTH, expand=True)
        
        # Patterns
        patterns_frame = ttk.LabelFrame(frame, text="Patterns actifs", padding="10")
        patterns_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.patterns_text = scrolledtext.ScrolledText(
            patterns_frame, height=8, font=('Consolas', 9)
        )
        self.patterns_text.pack(fill=tk.BOTH, expand=True)

        # Prévisions
        prev_frame = ttk.LabelFrame(frame, text="Prévisions IA", padding="10")
        prev_frame.pack(fill=tk.X, pady=5)

        self.previsions_text = scrolledtext.ScrolledText(
            prev_frame, height=5, font=('Consolas', 10)
        )
        self.previsions_text.pack(fill=tk.BOTH, expand=True)

    def creer_onglet_logs(self):
        """Onglet 7: Logs complets"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📝 Logs")
        
        # Filtres
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Filtre:").pack(side=tk.LEFT, padx=5)
        
        self.log_filter = tk.StringVar(value="TOUS")
        filters = ["TOUS", "INFO", "✅", "🚫", "🧠", "⚠️", "❌"]
        
        for f in filters:
            ttk.Radiobutton(
                filter_frame,
                text=f,
                variable=self.log_filter,
                value=f
            ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            filter_frame,
            text="Effacer",
            command=self.effacer_logs
        ).pack(side=tk.RIGHT, padx=5)
        
        # Zone de logs
        self.logs_text = scrolledtext.ScrolledText(
            frame, height=30, font=('Consolas', 9), wrap=tk.WORD
        )
        self.logs_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Tags de couleur
        self.logs_text.tag_config("INFO", foreground="black")
        self.logs_text.tag_config("⚠️", foreground="orange", font=('Consolas', 9, 'bold'))
        self.logs_text.tag_config("❌", foreground="red", font=('Consolas', 9, 'bold'))
        self.logs_text.tag_config("✅", foreground="green", font=('Consolas', 9, 'bold'))
        self.logs_text.tag_config("🚫", foreground="red", font=('Consolas', 9, 'bold'))
        self.logs_text.tag_config("🧠", foreground="purple", font=('Consolas', 9, 'bold'))
    
    def setup_status_bar(self):
        """Barre de statut"""
        self.status_bar = ttk.Frame(self.root, relief='sunken', padding=(2, 0))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = tk.Label(
            self.status_bar, text="Prêt", anchor=tk.W, font=('Arial', 9)
        )
        self.status_label.pack(side=tk.LEFT)
        
        self.clock_label = tk.Label(
            self.status_bar, text=datetime.now().strftime("%H:%M:%S"), font=('Arial', 9)
        )
        self.clock_label.pack(side=tk.RIGHT)
        
        # Infos supplémentaires
        self.stats_status = tk.Label(
            self.status_bar, text="", anchor=tk.W, font=('Arial', 9)
        )
        self.stats_status.pack(side=tk.LEFT, padx=20)
        
        self.mettre_a_jour_horloge()
    
    def mettre_a_jour_horloge(self):
        self.clock_label.config(text=datetime.now().strftime("%H:%M:%S"))
        self.root.after(1000, self.mettre_a_jour_horloge)
    
    def toggle_proxy(self):
        if not self.proxy_actif.get():
            if self.proxy.demarrer():
                self.proxy_actif.set(True)
                self.btn_toggle.config(
                    text="🛑 ARRÊTER",
                    bg=self.colors['danger']
                )
                self.status_label.config(text="🧠 IA active - Protection en cours")
        else:
            self.proxy.arreter()
            self.proxy_actif.set(False)
            self.btn_toggle.config(
                text="🧠 DÉMARRER",
                bg=self.colors['ia']
            )
            self.status_label.config(text="Protection arrêtée")
    
    def creer_faux_profil(self):
        self.ia.creer_faux_profil()
    
    def forcer_rotation(self):
        if self.proxy.proxy_actif and self.ia.connaissances['faux_profils']:
            self.proxy.profil_actuel = random.choice(self.ia.connaissances['faux_profils'])
            self.logger.ia(f"🔄 Rotation forcée vers: {self.proxy.profil_actuel['id']}")
    
    def effacer_logs(self):
        self.logs_text.delete(1.0, tk.END)
    
    def mettre_a_jour_stats(self):
        """Met à jour tous les onglets"""
        if self.auto_refresh.get() or not self.proxy_actif.get():
            stats = self.stats.obtenir_resume()
            ia_stats = self.ia.obtenir_statistiques_ia()
            
            # Tableau de bord
            self.metrics_labels['trackers'].config(text=str(stats['trackers']))
            self.metrics_labels['pubs'].config(text=str(stats['pubs']))
            self.metrics_labels['total'].config(text=str(stats['total']))
            self.metrics_labels['vitesse'].config(text=f"{stats['vitesse']}/min")
            self.metrics_labels['donnees'].config(text=f"{stats['donnees_economisees']} Ko")
            
            # Infos
            self.info_labels['statut'].config(text="Actif" if self.proxy_actif.get() else "Arrêté")
            if self.proxy.profil_actuel:
                self.info_labels['profil'].config(text=self.proxy.profil_actuel['id'][:8])
            self.info_labels['dernier'].config(text=stats['dernier'])
            self.info_labels['temps'].config(text=stats['temps'])
            self.info_labels['domaines'].config(text=str(ia_stats['domaines_appris']))
            self.info_labels['nb_profils'].config(text=str(ia_stats['faux_profils']))
            
            # Trackers
            self.trackers_labels['total_trackers'].config(text=str(stats['trackers']))
            self.trackers_labels['par_heure'].config(text=str(stats['vitesse'] * 60))
            self.trackers_labels['par_minute'].config(text=str(stats['vitesse']))
            
            # Méthodes
            cat = stats['categories']
            self.methodes_labels['blacklist'].config(text=str(cat.get('blacklist', 0)))
            self.methodes_labels['ia_detecte'].config(text=str(cat.get('ia_detecte', 0)))
            self.methodes_labels['appris'].config(text=str(cat.get('appris', 0)))
            self.methodes_labels['pattern'].config(text=str(cat.get('pattern', 0)))
            
            # Publicités
            self.pubs_labels['total_pubs'].config(text=str(stats['pubs']))
            
            # IA
            self.ia_metrics_labels['ia_domaines'].config(text=str(ia_stats['domaines_appris']))
            self.ia_metrics_labels['ia_patterns'].config(text=str(ia_stats['patterns_crees']))
            self.ia_metrics_labels['ia_precision'].config(text=f"{ia_stats['precision']}%")
            self.ia_metrics_labels['ia_previsions'].config(text=str(ia_stats['previsions_total']))
            
            # Top domaines trackers - VERSION CORRIGÉE
            if hasattr(self, 'top_trackers'):
                self.top_trackers.delete(1.0, tk.END)
                
                # Compter les domaines depuis l'historique des blocages
                domaines_comptes = {}
                for blocage in list(self.ia.historique_blocages)[-200:]:  # Derniers 200 blocages
                    domaine = blocage.get('domaine', '')
                    if domaine:
                        domaines_comptes[domaine] = domaines_comptes.get(domaine, 0) + 1
                
                if domaines_comptes:
                    self.top_trackers.insert(tk.END, "📊 TOP DOMAINES BLOQUÉS:\n\n")
                    for domaine, count in sorted(domaines_comptes.items(), key=lambda x: x[1], reverse=True)[:15]:
                        self.top_trackers.insert(tk.END, f"{domaine:<45} {count:>3} fois\n")
                else:
                    self.top_trackers.insert(tk.END, "Aucun domaine bloqué pour l'instant...\n")
                    self.top_trackers.insert(tk.END, "Naviguez sur des sites pour voir les blocages !")
            
            # Répartition publicités
            if hasattr(self, 'repartition_pubs'):
                self.repartition_pubs.delete(1.0, tk.END)
                
                # Filtrer les blocages de type publicité
                pubs_par_type = {}
                for blocage in list(self.ia.historique_blocages)[-200:]:
                    type_b = blocage.get('type', '')
                    if any(pub_type in str(type_b) for pub_type in ['pub', 'ad', 'banner', 'doubleclick', 'googlead']):
                        pubs_par_type[type_b] = pubs_par_type.get(type_b, 0) + 1
                
                if pubs_par_type:
                    self.repartition_pubs.insert(tk.END, "📊 RÉPARTITION DES PUBLICITÉS:\n\n")
                    total_pubs = sum(pubs_par_type.values())
                    for type_pub, count in sorted(pubs_par_type.items(), key=lambda x: x[1], reverse=True):
                        pourcent = (count / total_pubs) * 100
                        self.repartition_pubs.insert(tk.END, f"{type_pub:<20} {count:>3} ({pourcent:.1f}%)\n")
                    
                    self.repartition_pubs.insert(tk.END, f"\nTotal pubs: {total_pubs}")
                else:
                    # Utiliser les stats normales
                    stats = self.stats.obtenir_resume()
                    if stats['pubs'] > 0:
                        self.repartition_pubs.insert(tk.END, f"Total publicités: {stats['pubs']}\n")
                        for cat, count in stats['categories'].items():
                            if 'pub' in cat:
                                self.repartition_pubs.insert(tk.END, f"{cat}: {count}\n")
                    else:
                        self.repartition_pubs.insert(tk.END, "Aucune publicité détectée...\n")
                        self.repartition_pubs.insert(tk.END, "Les publicités seront comptées ici !")
            
            # Profil actuel
            if hasattr(self, 'current_profil_text') and self.proxy.profil_actuel:
                self.current_profil_text.delete(1.0, tk.END)
                profil = self.proxy.profil_actuel
                self.current_profil_text.insert(tk.END, f"ID: {profil['id']}\n")
                self.current_profil_text.insert(tk.END, f"User-Agent: {profil['user_agent']}\n")
                self.current_profil_text.insert(tk.END, f"Résolution: {profil['resolution']}\n")
                self.current_profil_text.insert(tk.END, f"Langue: {profil['langue']}\n")
                self.current_profil_text.insert(tk.END, f"Do Not Track: {profil['do_not_track']}\n")
            
            # Liste des profils
            if hasattr(self, 'liste_profils'):
                self.liste_profils.delete(1.0, tk.END)
                for profil in self.ia.connaissances['faux_profils'][-10:]:
                    self.liste_profils.insert(tk.END, 
                        f"🎭 {profil['id']} - {profil['user_agent'][:50]}...\n")
            
            # Historique rotations
            if hasattr(self, 'historique_rotations'):
                self.historique_rotations.delete(1.0, tk.END)
                for rot in list(self.proxy.historique_profils)[-5:]:
                    self.historique_rotations.insert(tk.END,
                        f"[{rot['timestamp'].strftime('%H:%M:%S')}] {rot['ancien']} → {rot['nouveau']}\n")
            
            # Statistiques globales
            if hasattr(self, 'global_stats_text'):
                self.global_stats_text.delete(1.0, tk.END)
                self.global_stats_text.insert(tk.END, 
                    f"Temps de protection: {stats['temps']}\n"
                    f"Requêtes analysées: {self.stats.requetes_analysees}\n"
                    f"Données économisées: {stats['donnees_economisees']} Ko\n"
                    f"Profils utilisés: {stats['profils']}\n"
                    f"Trackers/min: {stats['vitesse']}\n")
            
            # Derniers apprentissages
            if hasattr(self, 'apprentissages_text'):
                self.apprentissages_text.delete(1.0, tk.END)
                
                # Afficher les statistiques d'apprentissage
                self.apprentissages_text.insert(tk.END, "🧠 ACTIVITÉ D'APPRENTISSAGE\n\n")
                
                # Derniers apprentissages
                apprentissages_recents = list(self.ia.historique_apprentissages)[-15:]
                if apprentissages_recents:
                    for app in reversed(apprentissages_recents):
                        if app['type'] == 'nouveau_domaine':
                            self.apprentissages_text.insert(tk.END,
                                f"[{app['timestamp'].strftime('%H:%M:%S')}] "
                                f"📚 NOUVEAU: {app['domaine']}\n")
                            self.apprentissages_text.insert(tk.END,
                                f"   └─ Type: {app['categorie']}, Patterns: {app.get('patterns_crees', 1)}\n")
                        elif app['type'] == 'nouveau_profil':
                            self.apprentissages_text.insert(tk.END,
                                f"[{app['timestamp'].strftime('%H:%M:%S')}] "
                                f"🎭 NOUVEAU PROFIL: {app['profil_id']}\n")
                else:
                    self.apprentissages_text.insert(tk.END, "En attente de nouveaux apprentissages...\n")
                    self.apprentissages_text.insert(tk.END, "L'IA apprend automatiquement en naviguant !\n")
                
                # Statistiques d'apprentissage
                self.apprentissages_text.insert(tk.END, f"\n📊 STATISTIQUES D'APPRENTISSAGE:\n")
                self.apprentissages_text.insert(tk.END, f"   • Domaines appris: {self.ia.statistiques_ia['domaines_appris']}\n")
                self.apprentissages_text.insert(tk.END, f"   • Patterns créés: {self.ia.statistiques_ia['patterns_crees']}\n")
                self.apprentissages_text.insert(tk.END, f"   • Faux profils: {self.ia.statistiques_ia['faux_profils_crees']}\n")
                
                if self.ia.statistiques_ia['dernier_domaine']:
                    self.apprentissages_text.insert(tk.END, 
                        f"\n🔍 Dernier domaine appris: {self.ia.statistiques_ia['dernier_domaine']}\n")
            
            # Liste noire
            if hasattr(self, 'blacklist_text'):
                self.blacklist_text.delete(1.0, tk.END)
                for i, domaine in enumerate(self.ia.blacklist_base[:20]):
                    self.blacklist_text.insert(tk.END, f"{domaine}\n")
            
            # Patterns
            if hasattr(self, 'patterns_text'):
                self.patterns_text.delete(1.0, tk.END)
                for cat, patterns in self.ia.patterns_avances.items():
                    self.patterns_text.insert(tk.END, f"\n{cat.upper()}:\n")
                    for p in patterns[:3]:
                        self.patterns_text.insert(tk.END, f"  {p}\n")
            
            # Graphique
            if hasattr(self, 'canvas'):
                self.dessiner_graphique()

            # Prévisions IA
            if hasattr(self, 'previsions_text'):
                self.previsions_text.delete(1.0, tk.END)
                
                # Calculer quelques statistiques
                total_blocages = len(self.ia.historique_blocages)
                derniere_minute = len([b for b in list(self.ia.historique_blocages)[-60:] 
                                      if (datetime.now() - b.get('timestamp', datetime.now())).seconds < 60])
                
                if total_blocages > 0:
                    # Calculer les tendances
                    self.previsions_text.insert(tk.END, "📈 PRÉVISIONS ET TENDANCES\n\n")
                    
                    # Tendance générale
                    self.previsions_text.insert(tk.END, f"📊 Total blocages: {total_blocages}\n")
                    self.previsions_text.insert(tk.END, f"⚡ Vitesse actuelle: {derniere_minute}/min\n\n")
                    
                    # Prévision sur l'heure
                    prevision_heure = derniere_minute * 60
                    self.previsions_text.insert(tk.END, f"🔮 Prévision prochaine heure: {prevision_heure} blocages\n")
                    
                    # Top domaines prévus
                    domaines_frequents = {}
                    for blocage in list(self.ia.historique_blocages)[-100:]:
                        domaine = blocage.get('domaine', '')
                        if domaine:
                            domaines_frequents[domaine] = domaines_frequents.get(domaine, 0) + 1
                    
                    if domaines_frequents:
                        self.previsions_text.insert(tk.END, "\n🎯 Domaines les plus actifs:\n")
                        for domaine, count in sorted(domaines_frequents.items(), key=lambda x: x[1], reverse=True)[:5]:
                            self.previsions_text.insert(tk.END, f"   • {domaine}: {count} fois\n")
                    
                    # Taux de blocage par type
                    pubs = len([b for b in self.ia.historique_blocages 
                               if 'doubleclick' in str(b.get('domaine', '')) or 'googlead' in str(b.get('domaine', ''))])
                    trackers = total_blocages - pubs
                    
                    if total_blocages > 0:
                        self.previsions_text.insert(tk.END, f"\n📊 Répartition:\n")
                        self.previsions_text.insert(tk.END, f"   • Publicités: {pubs} ({pubs*100/total_blocages:.1f}%)\n")
                        self.previsions_text.insert(tk.END, f"   • Trackers: {trackers} ({trackers*100/total_blocages:.1f}%)\n")
                    
                    # Message d'information
                    self.previsions_text.insert(tk.END, "\n💡 L'IA apprend en continu...")
                else:
                    self.previsions_text.insert(tk.END, "📊 En attente de données...\n\n")
                    self.previsions_text.insert(tk.END, "Pour voir les prévisions :\n")
                    self.previsions_text.insert(tk.END, "1. Laissez le proxy actif\n")
                    self.previsions_text.insert(tk.END, "2. Naviguez sur des sites\n")
                    self.previsions_text.insert(tk.END, "3. Revenez dans quelques minutes")
                    
            # Barre de statut
            self.stats_status.config(
                text=f"Total: {stats['total']} | Trackers: {stats['trackers']} | Pubs: {stats['pubs']}"
            )
        
        # Logs
        while not self.logger.queue.empty():
            log_entry = self.logger.queue.get_nowait()
            
            # Forcer la mise à jour des stats à chaque nouveau log de blocage
            if log_entry['niveau'] == '🚫':
                # Rafraîchir les métriques immédiatement
                stats = self.stats.obtenir_resume()
                self.metrics_labels['trackers'].config(text=str(stats['trackers']))
                self.metrics_labels['pubs'].config(text=str(stats['pubs']))
                self.metrics_labels['total'].config(text=str(stats['total']))
            
            niveau = log_entry['niveau']
            message = log_entry['message']
            
            # Appliquer le filtre
            filtre = self.log_filter.get()
            if filtre != "TOUS" and niveau != filtre and not (filtre == "✅" and niveau == "✅"):
                continue
            
            timestamp = log_entry['timestamp']
            line = f"[{timestamp}] {niveau} {message}\n"
            
            self.logs_text.insert(tk.END, line, niveau)
            self.logs_text.see(tk.END)
        
        self.root.after(500, self.mettre_a_jour_stats)
    
    def dessiner_graphique(self):
        """Dessine un graphique d'évolution"""
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        if w < 10 or h < 10:
            return
        
        # Récupérer les dernières minutes depuis l'historique des blocages
        maintenant = datetime.now()
        points = []
        
        # Prendre les 20 dernières minutes
        for i in range(20):
            minute = maintenant - timedelta(minutes=19-i)
            count = 0
            for blocage in list(self.ia.historique_blocages)[-200:]:
                if blocage.get('timestamp', maintenant).minute == minute.minute:
                    count += 1
            points.append(count)
        
        if not points or max(points) == 0:
            self.canvas.create_text(w//2, h//2, 
                                   text="📊 En attente de données...\nNaviguez sur des sites pour voir l'activité",
                                   font=('Arial', 12))
            return
        
        # Dessiner le graphique
        marge_gauche = 50
        marge_droite = 30
        marge_haut = 20
        marge_bas = 40
        
        largeur_utile = w - marge_gauche - marge_droite
        hauteur_utile = h - marge_haut - marge_bas
        
        max_points = max(points) if max(points) > 0 else 1
        
        # Dessiner les axes
        self.canvas.create_line(marge_gauche, h - marge_bas, 
                               w - marge_droite, h - marge_bas, width=2)  # axe X
        self.canvas.create_line(marge_gauche, marge_haut, 
                               marge_gauche, h - marge_bas, width=2)  # axe Y
        
        # Graduations axe Y
        for i in range(0, max_points + 1, max(1, max_points // 5)):
            y = h - marge_bas - (i * hauteur_utile / max_points)
            self.canvas.create_line(marge_gauche - 5, y, marge_gauche, y)
            self.canvas.create_text(marge_gauche - 10, y, text=str(i), anchor='e')
        
        # Dessiner les barres
        bar_width = largeur_utile / len(points)
        
        for i, count in enumerate(points):
            x1 = marge_gauche + i * bar_width
            x2 = x1 + bar_width - 2
            y1 = h - marge_bas
            y2 = h - marge_bas - (count * hauteur_utile / max_points)
            
            # Couleur selon le type
            if count > 0:
                self.canvas.create_rectangle(x1, y2, x2, y1, 
                                           fill='#ff6b6b', outline='#dc3545')
                
                # Ajouter le nombre
                if count > 0:
                    self.canvas.create_text(x1 + bar_width/2, y2 - 10, 
                                          text=str(count), font=('Arial', 8))
            
            # Étiquettes des minutes
            minute = (maintenant - timedelta(minutes=19-i)).strftime('%H:%M')
            self.canvas.create_text(x1 + bar_width/2, h - marge_bas + 15, 
                                   text=minute, font=('Arial', 8), angle=45)
        
        # Titre
        self.canvas.create_text(w//2, marge_haut//2, 
                               text="Activité des dernières 20 minutes", 
                               font=('Arial', 10, 'bold'))
    
    def mettre_a_jour_logs(self):
        """Met à jour les logs avec filtre"""
        while not self.logger.queue.empty():
            log_entry = self.logger.queue.get_nowait()
            
            niveau = log_entry['niveau']
            message = log_entry['message']
            
            # Appliquer le filtre
            filtre = self.log_filter.get()
            if filtre != "TOUS" and niveau != filtre and not (filtre == "✅" and niveau == "✅"):
                continue
            
            timestamp = log_entry['timestamp']
            line = f"[{timestamp}] {niveau} {message}\n"
            
            self.logs_text.insert(tk.END, line, niveau)
            self.logs_text.see(tk.END)
    
    def fermer(self):
        if self.proxy.proxy_actif:
            self.proxy.arreter()
        self.ia.arreter()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()


def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   PROTECTION IA                                          ║
    ║   7 onglets pour tout visualiser :                       ║
    ║   📊 Tableau de bord                                     ║
    ║   🔍 Trackers                                            ║
    ║   📢 Publicités                                          ║
    ║   🎭 Profils                                             ║
    ║   📈 Statistiques                                        ║
    ║   🧠 IA                                                  ║
    ║   📝 Logs                                                ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    app = ApplicationGUI()
    app.run()


if __name__ == "__main__":
    main()
    
    