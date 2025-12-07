# 🚀 Setup Complet sur VPS - Instructions Détaillées

## 📋 Ce que fait le bot

- ✅ Surveille **@bigjolan** et **@pasdurrrr** toutes les **20 minutes**
- ✅ Pause automatique entre **2h et 8h** du matin
- ✅ Détecte les nouvelles vidéos automatiquement
- ✅ Ajoute **99999 vues** avec le service ID **1321 uniquement**
- ✅ Évite les doublons (ne traite que les nouvelles vidéos)

## 🔧 Configuration Requise

### Sur le VPS, vous devez créer `config.json` avec :

```json
{
  "tiktok": {
    "username": "",
    "check_interval": 1200,
    "target_users": ["bigjolan", "pasdurrrr"],
    "target_hashtags": []
  },
  "apify": {
    "enabled": true,
    "api_token": "VOTRE_TOKEN_APIFY_ICI",
    "actor_id": "GdWCkxBtKWOsKjdch",
    "max_results": 10
  },
  "smmfollows": {
    "api_key": "VOTRE_CLE_SMMFOLLOWS_ICI",
    "service_ids": {
      "likes": 1321,
      "comments": 1321,
      "views": 1321
    }
  },
  "services": {
    "likes": {
      "enabled": false,
      "count": 10,
      "use_smmfollows": true,
      "api_url": "",
      "api_key": "",
      "service_id": null
    },
    "comments": {
      "enabled": false,
      "count": 5,
      "use_smmfollows": true,
      "api_url": "",
      "api_key": "",
      "service_id": null,
      "templates": [
        "Super vidéo ! 🔥",
        "J'adore ! ❤️",
        "Trop bien ! 👏",
        "Excellent contenu ! 💯"
      ]
    },
    "views": {
      "enabled": true,
      "count": 99999,
      "use_smmfollows": true,
      "api_url": "",
      "api_key": "",
      "service_id": null
    }
  },
  "database": {
    "file": "videos_tracked.json"
  }
}
```

## 🚀 Déploiement Complet sur VPS

### Étape 1 : Cloner depuis GitHub

```bash
ssh root@VOTRE_IP_HOSTINGER
cd /root
git clone https://github.com/elonreevemuskllc/botquiclc.git bot-tiktok
cd bot-tiktok
```

### Étape 2 : Créer config.json

```bash
nano config.json
```

Copiez-collez le JSON ci-dessus avec vos vraies clés API.

### Étape 3 : Installer tout

```bash
apt update && apt upgrade -y
apt install python3 python3-pip screen git -y
pip3 install -r requirements.txt
pip3 install apify-client requests
```

### Étape 4 : Tester

```bash
python3 test_service_1321.py
```

### Étape 5 : Lancer

```bash
screen -S bot-tiktok
python3 bot_apify.py
# Ctrl+A puis D pour détacher
```

## ✅ Vérifications Importantes

1. **config.json existe** : `ls -la config.json`
2. **Clés API présentes** : `cat config.json | grep api`
3. **Service ID 1321** : `cat config.json | grep 1321`
4. **Profils corrects** : `cat config.json | grep bigjolan`
5. **Intervalle 1200** : `cat config.json | grep check_interval`

## 🎯 Résumé Configuration

- **Profils surveillés** : @bigjolan et @pasdurrrr
- **Intervalle** : 1200 secondes (20 minutes)
- **Pause** : 2h-8h du matin
- **Service ID** : 1321 uniquement
- **Action** : 99999 vues par nouvelle vidéo

C'est tout ! 🚀

