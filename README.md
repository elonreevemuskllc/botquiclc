# Bot TikTok - Surveillance et Interaction Automatisée

Bot Python pour surveiller les nouvelles vidéos TikTok et automatiser les interactions (likes, commentaires, vues) via des APIs externes.

## 🚀 Fonctionnalités

- ✅ Surveillance automatique des nouvelles vidéos TikTok
- ✅ Détection des nouvelles publications
- ✅ **Intégration avec Apify** pour un scraping fiable et professionnel
- ✅ Support des utilisateurs et hashtags TikTok
- ✅ Intégration avec des services API pour :
  - Ajouter des likes
  - Ajouter des commentaires
  - Augmenter les vues
- ✅ Configuration flexible via fichier JSON
- ✅ Logging complet des actions

## 📋 Prérequis

- Python 3.8+
- Compte Apify (gratuit) - [Créer un compte](https://console.apify.com/sign-up)
- Token API Apify - [Obtenir le token](https://console.apify.com/account/integrations)
- Accès à des services API pour TikTok (likes, commentaires, vues)

## 🔧 Installation

1. Cloner ou télécharger ce projet

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Pour utiliser le scraping web (optionnel) :
```bash
# Installer Playwright
playwright install
```

## ⚙️ Configuration

### Configuration avec Apify (Recommandé)

Éditez le fichier `config.json` :

```json
{
  "tiktok": {
    "username": "votre_username",
    "check_interval": 60,
    "target_users": ["user1", "user2"],
    "target_hashtags": ["trending", "viral"]
  },
  "apify": {
    "enabled": true,
    "api_token": "votre_token_apify",
    "actor_id": "GdWCkxBtKWOsKjdch",
    "max_results": 10
  },
  "services": {
    "likes": {
      "enabled": true,
      "count": 10,
      "api_url": "https://votre-api.com/likes",
      "api_key": "votre_cle_api"
    },
    "comments": {
      "enabled": true,
      "count": 5,
      "api_url": "https://votre-api.com/comments",
      "api_key": "votre_cle_api",
      "templates": ["Super vidéo ! 🔥", "J'adore ! ❤️"]
    }
  }
}
```

### Obtenir votre token Apify

1. Créez un compte sur [Apify](https://console.apify.com/sign-up)
2. Allez dans [Account > Integrations](https://console.apify.com/account/integrations)
3. Copiez votre **Personal API token**
4. Collez-le dans `config.json` sous `apify.api_token`

### Paramètres de configuration :

- **check_interval** : Intervalle en secondes entre chaque vérification
- **target_users** : Liste des utilisateurs TikTok à surveiller (sans @)
- **target_hashtags** : Liste des hashtags à surveiller (sans #)
- **apify.enabled** : Active/désactive l'utilisation d'Apify
- **apify.api_token** : Token API Apify (obligatoire si Apify activé)
- **apify.actor_id** : ID de l'acteur Apify (défaut: GdWCkxBtKWOsKjdch)
- **apify.max_results** : Nombre maximum de résultats par requête
- **api_url** : URL de votre service API
- **api_key** : Clé d'API pour authentification
- **count** : Nombre de likes/commentaires/vues à envoyer

## 🎯 Utilisation

### Avec Apify (Recommandé)

Lancer le bot avec Apify :

```bash
python bot_apify.py
```

### Sans Apify (Scraping basique)

Lancer le bot basique :

```bash
python bot.py
```

### Avec Selenium (Scraping avancé)

Lancer le bot avec Selenium :

```bash
python bot_advanced.py
```

Le bot va :
1. Vérifier périodiquement les nouvelles vidéos des utilisateurs/hashtags ciblés
2. Détecter les nouvelles publications
3. Extraire les URLs et métadonnées des vidéos
4. Envoyer automatiquement les interactions via les APIs configurées
5. Logger toutes les actions dans `bot.log`

## 📝 Configuration smmfollows.com

Le bot supporte l'API [smmfollows.com](https://smmfollows.com) pour commander automatiquement des likes, commentaires et vues.

### 1. Obtenir votre clé API

1. Créez un compte sur [smmfollows.com](https://smmfollows.com)
2. Allez dans **Account** pour obtenir votre clé API
3. Ajoutez des crédits à votre compte

### 2. Trouver les IDs des services TikTok

Exécutez le script utilitaire :

```bash
python check_smmfollows_services.py
```

Ce script va :
- Afficher votre solde
- Lister tous les services TikTok disponibles
- Vous donner les IDs à ajouter dans `config.json`

### 3. Configurer dans config.json

```json
{
  "smmfollows": {
    "api_key": "VOTRE_CLE_API",
    "service_ids": {
      "likes": 123,
      "comments": 456,
      "views": 789
    }
  },
  "services": {
    "likes": {
      "enabled": true,
      "count": 10,
      "use_smmfollows": true
    }
  }
}
```

### 4. Format de l'API smmfollows

L'API utilise POST vers `https://smmfollows.com/api/v2` :

**Créer une commande :**
```
key: VOTRE_CLE
action: add
service: ID_DU_SERVICE
link: URL_VIDEO_TIKTOK
quantity: NOMBRE
```

**Vérifier le statut :**
```
key: VOTRE_CLE
action: status
order: ID_COMMANDE
```

**Vérifier le solde :**
```
key: VOTRE_CLE
action: balance
```

## ⚠️ Notes importantes

1. **Apify (Recommandé pour le scraping)** : 
   - L'API Apify offre un scraping fiable et professionnel de TikTok
   - L'acteur utilisé : [GdWCkxBtKWOsKjdch](https://console.apify.com/actors/GdWCkxBtKWOsKjdch/input)
   - Apify gère automatiquement les anti-bots et les limitations
   - Un compte gratuit Apify offre des crédits limités

2. **smmfollows.com (Recommandé pour les interactions)** :
   - Service professionnel pour commander des likes, commentaires, vues
   - API simple et documentée
   - Supporte TikTok et autres plateformes
   - Nécessite un compte avec crédits

3. **Scraping alternatifs** :
   - `bot_advanced.py` utilise Selenium pour le scraping web
   - `bot.py` utilise une simulation (pour tests uniquement)

4. **Services API personnalisés** : 
   - Vous pouvez aussi utiliser vos propres APIs en désactivant `use_smmfollows`
   - Configurez `api_url` et `api_key` dans chaque service

5. **Respect des ToS** : Assurez-vous de respecter les conditions d'utilisation de TikTok et d'utiliser ce bot de manière éthique.

## 🔄 Améliorations possibles

- Intégration avec TikTokApi pour un vrai scraping
- Support de l'authentification TikTok
- Interface web pour la configuration
- Base de données pour le tracking
- Notifications (email, Discord, etc.)

## 📄 Licence

Ce projet est fourni à titre éducatif. Utilisez-le de manière responsable.

