# Guide d'utilisation de smmfollows.com

## 🎯 Qu'est-ce que smmfollows.com ?

smmfollows.com est une plateforme SMM (Social Media Marketing) qui permet de commander des interactions sociales (likes, commentaires, vues, followers) sur différentes plateformes, y compris TikTok.

## 📝 Configuration étape par étape

### 1. Créer un compte et obtenir la clé API

1. Allez sur [smmfollows.com](https://smmfollows.com)
2. Créez un compte
3. Connectez-vous et allez dans **Account**
4. Trouvez votre **API Key** et copiez-la
5. Ajoutez des crédits à votre compte (nécessaire pour passer des commandes)

### 2. Trouver les IDs des services TikTok

Le bot inclut un script utilitaire pour trouver automatiquement les services TikTok :

```bash
python check_smmfollows_services.py
```

Ce script va :
- ✅ Vérifier votre solde
- ✅ Lister tous les services TikTok disponibles
- ✅ Vous donner les IDs à copier dans `config.json`

**Exemple de sortie :**
```
🎵 SERVICES TIKTOK TROUVÉS:
📌 Service ID: 123
   Nom: TikTok Likes
   Type: Default
   Prix: $0.90 par unité
   Min: 50
   Max: 10000
```

### 3. Configurer config.json

Éditez `config.json` :

```json
{
  "smmfollows": {
    "api_key": "VOTRE_CLE_API_ICI",
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
    },
    "comments": {
      "enabled": true,
      "count": 5,
      "use_smmfollows": true
    },
    "views": {
      "enabled": false,
      "count": 100,
      "use_smmfollows": true
    }
  }
}
```

### 4. Lancer le bot

```bash
python bot_apify.py
```

Le bot va automatiquement :
1. Scraper les nouvelles vidéos TikTok via Apify
2. Créer des commandes sur smmfollows pour chaque vidéo
3. Logger les IDs de commande créés

## 🔍 Comment ça fonctionne

### Workflow complet

1. **Scraping** : Le bot détecte une nouvelle vidéo TikTok
2. **Commande** : Pour chaque service activé (likes, comments, views), le bot crée une commande sur smmfollows
3. **Suivi** : Chaque commande reçoit un Order ID unique
4. **Exécution** : smmfollows exécute la commande automatiquement

### Exemple de log

```
✨ Nouvelle vidéo détectée: https://www.tiktok.com/@user/video/123
📹 Traitement de la vidéo: https://www.tiktok.com/@user/video/123
✅ Commande de 10 likes créée (Order ID: 23501)
✅ Commande de 5 commentaires créée (Order ID: 23502)
```

## 💰 Coûts et crédits

- Chaque service a un prix par unité (ex: $0.90 pour 1000 likes)
- Les crédits sont débités automatiquement lors de la création de commande
- Vérifiez votre solde avec `check_smmfollows_services.py`

## 🔧 Dépannage

### Erreur : "Service Likes non trouvé"

➡️ Les IDs de service n'ont pas été trouvés automatiquement. Solutions :
1. Exécutez `python check_smmfollows_services.py` pour trouver les IDs
2. Ajoutez-les manuellement dans `config.json` sous `smmfollows.service_ids`

### Erreur : "Insufficient balance"

➡️ Votre compte n'a pas assez de crédits. Ajoutez des crédits sur smmfollows.com

### Erreur : "Incorrect order ID"

➡️ L'ID de service est incorrect. Vérifiez avec `check_smmfollows_services.py`

### Les commandes ne sont pas créées

➡️ Vérifiez que :
- `use_smmfollows: true` est activé pour le service
- La clé API est correcte
- Les IDs de service sont corrects
- Vous avez assez de crédits

## 📊 Vérifier le statut des commandes

Vous pouvez vérifier le statut d'une commande avec l'API smmfollows :

```python
from smmfollows_api import SMMFollowsAPI

api = SMMFollowsAPI("VOTRE_CLE")
status = api.get_order_status(23501)
print(status)
```

Réponse :
```json
{
  "charge": "0.27819",
  "start_count": "3572",
  "status": "Partial",
  "remains": "157",
  "currency": "USD"
}
```

## 🎯 Services disponibles

smmfollows propose généralement :
- ✅ **Likes** : Ajouter des likes à une vidéo
- ✅ **Comments** : Ajouter des commentaires (générés automatiquement)
- ✅ **Views** : Augmenter le nombre de vues
- ✅ **Followers** : Ajouter des followers à un profil
- ✅ **Shares** : Partager la vidéo

## 📚 Ressources

- [Documentation API smmfollows](https://smmfollows.com/api-docs)
- [Site smmfollows](https://smmfollows.com)
- [Support smmfollows](https://smmfollows.com/support)

