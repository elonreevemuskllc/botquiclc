# Guide de Test du Bot

## ✅ Vérification que tout fonctionne

### 1. Vérifier les dépendances

```bash
pip install -r requirements.txt
```

Dépendances requises :
- ✅ `requests` - Pour les appels API
- ✅ `apify-client` - Pour le scraping Apify
- ✅ `selenium` (optionnel) - Pour le scraping avancé
- ✅ `beautifulsoup4` (optionnel)
- ✅ `playwright` (optionnel)

### 2. Configuration minimale pour tester

Éditez `config.json` avec au minimum :

```json
{
  "tiktok": {
    "check_interval": 300,
    "target_users": ["test_user"],
    "target_hashtags": []
  },
  "apify": {
    "enabled": true,
    "api_token": "VOTRE_TOKEN_APIFY",
    "actor_id": "GdWCkxBtKWOsKjdch",
    "max_results": 5
  },
  "smmfollows": {
    "api_key": "VOTRE_CLE_SMMFOLLOWS",
    "service_ids": {
      "likes": null,
      "comments": null,
      "views": null
    }
  },
  "services": {
    "likes": {
      "enabled": true,
      "count": 10,
      "use_smmfollows": true
    },
    "comments": {
      "enabled": false,
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

### 3. Tests étape par étape

#### Test 1 : Vérifier la configuration

```bash
python check_smmfollows_services.py
```

**Résultat attendu :**
- ✅ Affichage du solde
- ✅ Liste des services TikTok
- ✅ IDs de services à copier

#### Test 2 : Vérifier Apify (sans lancer le bot)

Créez un fichier `test_apify.py` :

```python
from apify_scraper import ApifyTikTokScraper

scraper = ApifyTikTokScraper(
    apify_token="VOTRE_TOKEN",
    actor_id="GdWCkxBtKWOsKjdch"
)

videos = scraper.scrape_user_videos("test_user", max_results=1)
print(f"Vidéos trouvées: {len(videos)}")
```

#### Test 3 : Vérifier smmfollows (sans lancer le bot)

Créez un fichier `test_smmfollows.py` :

```python
from smmfollows_api import SMMFollowsAPI

api = SMMFollowsAPI("VOTRE_CLE")
balance = api.get_balance()
print(f"Solde: ${balance}")

services = api.get_services()
tiktok_services = [s for s in services if 'tiktok' in s['name'].lower()]
print(f"Services TikTok: {len(tiktok_services)}")
```

#### Test 4 : Lancer le bot en mode test

Modifiez temporairement `check_interval` à 60 secondes et lancez :

```bash
python bot_apify.py
```

**Vérifiez dans les logs :**
- ✅ Bot initialisé
- ✅ Scraper Apify connecté
- ✅ Services smmfollows configurés
- ✅ Surveillance des utilisateurs/hashtags activée

### 4. Checklist de fonctionnement

Avant de lancer le bot en production, vérifiez :

- [ ] Token Apify configuré et valide
- [ ] Clé API smmfollows configurée et valide
- [ ] Solde smmfollows suffisant
- [ ] IDs de services TikTok trouvés et configurés
- [ ] Au moins un utilisateur ou hashtag à surveiller
- [ ] Services activés (likes, comments, views)
- [ ] `check_interval` configuré (minimum 60 secondes recommandé)

### 5. Problèmes courants

#### ❌ "Apify n'est pas activé"
➡️ Mettez `"enabled": true` dans la section `apify` de `config.json`

#### ❌ "Token API Apify manquant"
➡️ Ajoutez votre token dans `apify.api_token`

#### ❌ "Service Likes non trouvé"
➡️ Exécutez `python check_smmfollows_services.py` et ajoutez les IDs dans `config.json`

#### ❌ "Insufficient balance"
➡️ Ajoutez des crédits sur smmfollows.com

#### ❌ "Aucun utilisateur ou hashtag cible configuré"
➡️ Ajoutez des utilisateurs dans `target_users` ou des hashtags dans `target_hashtags`

### 6. Test complet du workflow

1. **Scraping** : Le bot détecte une nouvelle vidéo
   - ✅ Log : "✨ Nouvelle vidéo détectée"

2. **Commande likes** : Création d'une commande smmfollows
   - ✅ Log : "✅ Commande de X likes créée (Order ID: XXXX)"

3. **Commande comments** : Si activé
   - ✅ Log : "✅ Commande de X commentaires créée (Order ID: XXXX)"

4. **Commande views** : Si activé
   - ✅ Log : "✅ Commande de X vues créée (Order ID: XXXX)"

5. **Vidéo traitée** : Marquage comme traitée
   - ✅ Log : "✅ Vidéo X traitée avec succès"

### 7. Monitoring en production

Surveillez le fichier `bot.log` :

```bash
tail -f bot.log
```

Vérifiez régulièrement :
- Les nouvelles vidéos détectées
- Les commandes créées
- Les erreurs éventuelles
- Le solde smmfollows (via `check_smmfollows_services.py`)

## 🎯 Résumé

Le bot est **entièrement fonctionnel** si :
1. ✅ Toutes les dépendances sont installées
2. ✅ Apify est configuré et fonctionne
3. ✅ smmfollows est configuré avec les bons IDs de services
4. ✅ Le bot détecte les nouvelles vidéos
5. ✅ Les commandes sont créées sur smmfollows
6. ✅ Les vidéos sont marquées comme traitées

Si tous ces points sont vérifiés, le bot fonctionne de bout en bout ! 🚀

