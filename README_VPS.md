# 🚀 Instructions Rapides pour VPS

## 📥 Cloner le Repository

```bash
ssh root@VOTRE_IP_HOSTINGER
cd /root
git clone https://github.com/elonreevemuskllc/botquiclc.git bot-tiktok
cd bot-tiktok
```

## ⚙️ Créer config.json

**IMPORTANT** : Vous devez créer `config.json` avec vos vraies clés API.

### Option 1 : Copier depuis votre PC

Sur votre PC, copiez le contenu de `config.json` (qui contient vos vraies clés).

Sur le VPS :

```bash
nano config.json
# Collez le contenu de votre config.json local
```

### Option 2 : Utiliser example_config.json comme base

```bash
cp example_config.json config.json
nano config.json
# Remplacez VOTRE_TOKEN_APIFY_ICI et VOTRE_CLE_SMMFOLLOWS_ICI par vos vraies clés
```

### Configuration Requise

Assurez-vous que `config.json` contient :

- ✅ `check_interval`: 1200 (20 minutes)
- ✅ `target_users`: ["bigjolan", "pasdurrrr"]
- ✅ `service_ids`: tous à 1321
- ✅ `views.enabled`: true
- ✅ `views.count`: 99999
- ✅ Vos vraies clés API (Apify et smmfollows)

## 🚀 Installer et Lancer

```bash
# Installer
apt update && apt install python3 python3-pip screen -y
pip3 install -r requirements.txt
pip3 install apify-client requests

# Tester
python3 test_service_1321.py

# Lancer
screen -S bot-tiktok
python3 bot_apify.py
# Ctrl+A puis D pour détacher
```

## ✅ Vérifier

```bash
# Voir les logs
tail -f bot.log

# Revenir à la session screen
screen -r bot-tiktok
```

C'est tout ! 🎯

