# Guide d'utilisation d'Apify avec le Bot TikTok

## 🎯 Pourquoi utiliser Apify ?

Apify est une plateforme de scraping professionnelle qui offre :
- ✅ Scraping fiable et stable
- ✅ Gestion automatique des anti-bots
- ✅ Pas besoin de maintenir du code de scraping
- ✅ API simple et documentée
- ✅ Compte gratuit disponible

## 📝 Étapes pour configurer Apify

### 1. Créer un compte Apify

1. Allez sur [https://console.apify.com/sign-up](https://console.apify.com/sign-up)
2. Créez un compte (gratuit)
3. Confirmez votre email

### 2. Obtenir votre token API

1. Connectez-vous à votre compte Apify
2. Allez dans **Account** > **Integrations** : [https://console.apify.com/account/integrations](https://console.apify.com/account/integrations)
3. Copiez votre **Personal API token**
4. ⚠️ Gardez ce token secret, ne le partagez jamais !

### 3. Configurer le bot

Éditez `config.json` :

```json
{
  "apify": {
    "enabled": true,
    "api_token": "VOTRE_TOKEN_ICI",
    "actor_id": "GdWCkxBtKWOsKjdch",
    "max_results": 10
  },
  "tiktok": {
    "target_users": ["username1", "username2"],
    "target_hashtags": ["trending", "viral"],
    "check_interval": 60
  }
}
```

### 4. Lancer le bot

```bash
python bot_apify.py
```

## 🔍 L'acteur Apify utilisé

L'acteur utilisé est : **GdWCkxBtKWOsKjdch**

Vous pouvez le consulter ici : [https://console.apify.com/actors/GdWCkxBtKWOsKjdch/input](https://console.apify.com/actors/GdWCkxBtKWOsKjdch/input)

Cet acteur peut :
- Scraper les vidéos d'un utilisateur TikTok
- Scraper les vidéos d'un hashtag
- Récupérer les métadonnées (likes, vues, commentaires, etc.)
- Extraire les URLs des vidéos

## 📊 Données récupérées

Pour chaque vidéo, Apify retourne :
- **URL de la vidéo** : Lien direct vers la vidéo TikTok
- **ID de la vidéo** : Identifiant unique
- **Description** : Texte de la vidéo
- **Statistiques** : Likes, vues, commentaires, partages
- **Auteur** : Nom d'utilisateur
- **Date de création** : Timestamp de publication

## 💰 Coûts Apify

- **Compte gratuit** : 5$ de crédits par mois
- Chaque exécution de l'acteur consomme des crédits
- Le coût dépend du nombre de résultats demandés

## 🔧 Dépannage

### Erreur : "Token API Apify manquant"

➡️ Vérifiez que vous avez bien copié le token dans `config.json` sous `apify.api_token`

### Erreur : "Apify n'est pas activé"

➡️ Mettez `"enabled": true` dans la section `apify` de `config.json`

### Erreur : "Insufficient credits"

➡️ Vous avez épuisé vos crédits Apify. Attendez le renouvellement mensuel ou passez à un plan payant.

### Le bot ne détecte pas de nouvelles vidéos

➡️ Vérifiez que :
- Les noms d'utilisateurs sont corrects (sans @)
- Les hashtags sont corrects (sans #)
- Les utilisateurs/hashtags existent bien sur TikTok

## 🚀 Exemple complet

```json
{
  "tiktok": {
    "check_interval": 300,
    "target_users": ["charlidamelio", "khaby00"],
    "target_hashtags": ["fyp", "viral"]
  },
  "apify": {
    "enabled": true,
    "api_token": "apify_api_xxxxxxxxxxxxxxxxxxxxx",
    "actor_id": "GdWCkxBtKWOsKjdch",
    "max_results": 20
  },
  "services": {
    "likes": {
      "enabled": true,
      "count": 10,
      "api_url": "https://votre-api.com/likes",
      "api_key": "votre_cle"
    }
  }
}
```

## 📚 Ressources

- [Documentation Apify](https://docs.apify.com/)
- [SDK Python Apify](https://docs.apify.com/sdk/python/)
- [Console Apify](https://console.apify.com/)

