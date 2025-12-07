# 📥 Cloner le Bot depuis GitHub sur VPS

Maintenant que le code est sur GitHub, voici comment le récupérer sur votre VPS Hostinger.

## 🚀 Sur le VPS Hostinger

### 1. Se connecter au VPS

```bash
ssh root@VOTRE_IP_HOSTINGER
```

### 2. Installer Git (si pas déjà installé)

```bash
apt update
apt install git -y
```

### 3. Cloner le repository

```bash
cd /root
git clone https://github.com/elonreevemuskllc/botquiclc.git bot-tiktok
cd bot-tiktok
```

### 4. Créer le fichier config.json

Le fichier `config.json` n'est pas sur GitHub (pour sécurité). Créez-le :

```bash
nano config.json
```

Collez ce contenu (avec vos vraies clés API) :

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

**Important** : Remplacez :
- `VOTRE_TOKEN_APIFY_ICI` par votre vrai token Apify
- `VOTRE_CLE_SMMFOLLOWS_ICI` par votre vraie clé smmfollows

Sauvegarder : `Ctrl+X`, puis `Y`, puis `Enter`

### 5. Installer les dépendances

```bash
apt install python3 python3-pip screen -y
pip3 install -r requirements.txt
pip3 install apify-client requests
```

### 6. Tester

```bash
python3 test_service_1321.py
```

### 7. Lancer le bot

```bash
screen -S bot-tiktok
python3 bot_apify.py
# Ctrl+A puis D pour détacher
```

## 🔄 Mettre à jour le code depuis GitHub

Si vous modifiez le code sur votre PC et le poussez sur GitHub, sur le VPS :

```bash
cd /root/bot-tiktok
git pull
systemctl restart bot-tiktok  # Si vous utilisez systemd
```

## ✅ Avantages de GitHub

- ✅ Code sauvegardé en ligne
- ✅ Facile à cloner sur le VPS
- ✅ Facile à mettre à jour
- ✅ Historique des modifications
- ✅ Fichiers sensibles protégés (.gitignore)

## 🔒 Sécurité

Les fichiers suivants ne sont **PAS** sur GitHub (grâce à .gitignore) :
- ✅ `config.json` (contient vos clés API)
- ✅ `videos_tracked.json` (base de données)
- ✅ `bot.log` (logs)
- ✅ Fichiers Python compilés

C'est sécurisé ! 🔐

