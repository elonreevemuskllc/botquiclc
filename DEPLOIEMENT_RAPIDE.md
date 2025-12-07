# 🚀 Déploiement Rapide sur VPS Hostinger

## 📦 Étape 1 : Préparer les fichiers sur votre PC

### Créer un ZIP du projet

1. Allez dans `C:\Users\Elon\Desktop\BOT PR CLC`
2. Sélectionnez tous les fichiers (Ctrl+A)
3. Clic droit → **Envoyer vers** → **Dossier compressé**
4. Vous obtenez `BOT PR CLC.zip`

## 🔌 Étape 2 : Se connecter au VPS

### Option A : Via PuTTY (Recommandé pour Windows)

1. Téléchargez PuTTY : https://www.putty.org/
2. Ouvrez PuTTY
3. Entrez :
   - **Host Name** : L'IP de votre VPS Hostinger
   - **Port** : 22
   - **Connection type** : SSH
4. Cliquez sur **Open**
5. Connectez-vous avec :
   - Username : `root`
   - Password : (votre mot de passe Hostinger)

### Option B : Via PowerShell

```powershell
ssh root@VOTRE_IP_HOSTINGER
```

## 📤 Étape 3 : Transférer les fichiers

### Méthode 1 : FileZilla (Le plus simple) ⭐

1. Téléchargez FileZilla : https://filezilla-project.org/
2. Ouvrez FileZilla
3. En haut, entrez :
   - **Hôte** : `sftp://VOTRE_IP_HOSTINGER`
   - **Nom d'utilisateur** : `root`
   - **Mot de passe** : (votre mot de passe)
   - **Port** : 22
4. Cliquez sur **Connexion rapide**
5. À gauche : votre PC (glissez le fichier ZIP ou le dossier)
6. À droite : le VPS (glissez dans `/root/`)

### Méthode 2 : Via SCP (PowerShell)

```powershell
# Depuis votre PC Windows
scp "C:\Users\Elon\Desktop\BOT PR CLC.zip" root@VOTRE_IP:/root/
```

Puis sur le VPS :

```bash
cd /root
unzip "BOT PR CLC.zip" -d bot-tiktok
cd bot-tiktok
```

## 🐍 Étape 4 : Installer Python et dépendances

Sur le VPS, exécutez ces commandes une par une :

```bash
# 1. Mettre à jour le système
apt update && apt upgrade -y

# 2. Installer Python et les outils nécessaires
apt install python3 python3-pip git screen -y

# 3. Aller dans le dossier du bot
cd /root/bot-tiktok  # ou le chemin où vous avez mis les fichiers

# 4. Installer les dépendances Python
pip3 install -r requirements.txt
pip3 install apify-client requests
```

## ⚙️ Étape 5 : Vérifier la configuration

```bash
# Éditer le fichier config.json
nano config.json
```

Vérifiez que tout est correct :
- ✅ Token Apify présent
- ✅ Clé API smmfollows présente
- ✅ Service IDs tous à 1321
- ✅ Intervalle : 1200 (20 minutes)
- ✅ Profils : `["bigjolan", "pasdurrrr"]`

**Pour sauvegarder dans nano** : `Ctrl+X`, puis `Y`, puis `Enter`

## 🧪 Étape 6 : Tester le bot

```bash
# Test rapide
python3 test_service_1321.py

# Si ça fonctionne, tester le bot (Ctrl+C pour arrêter)
python3 bot_apify.py
```

## 🚀 Étape 7 : Lancer le bot en arrière-plan

### Méthode 1 : Avec screen (Simple) ⭐

```bash
# Créer une session screen
screen -S bot-tiktok

# Lancer le bot
cd /root/bot-tiktok
python3 bot_apify.py

# Détacher de la session : Appuyez sur Ctrl+A puis D
# Pour revenir à la session : screen -r bot-tiktok
```

### Méthode 2 : Avec systemd (Service permanent) ⭐⭐

Créer le service :

```bash
nano /etc/systemd/system/bot-tiktok.service
```

Coller ce contenu :

```ini
[Unit]
Description=Bot TikTok - Surveillance et ajout de vues
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/bot-tiktok
ExecStart=/usr/bin/python3 /root/bot-tiktok/bot_apify.py
Restart=always
RestartSec=10
StandardOutput=append:/root/bot-tiktok/bot.log
StandardError=append:/root/bot-tiktok/bot.log

[Install]
WantedBy=multi-user.target
```

Activer et démarrer :

```bash
# Recharger systemd
systemctl daemon-reload

# Activer le service (démarrage automatique au boot)
systemctl enable bot-tiktok

# Démarrer le service
systemctl start bot-tiktok

# Vérifier le statut
systemctl status bot-tiktok
```

## 📊 Étape 8 : Surveiller le bot

### Voir les logs en temps réel

```bash
# Si avec screen
screen -r bot-tiktok

# Si avec systemd
journalctl -u bot-tiktok -f

# Ou directement le fichier log
tail -f /root/bot-tiktok/bot.log
```

### Vérifier que le bot tourne

```bash
# Voir les processus Python
ps aux | grep python

# Voir le statut (si systemd)
systemctl status bot-tiktok
```

## 🔧 Commandes Utiles

### Arrêter le bot

```bash
# Si screen
screen -r bot-tiktok
# Puis Ctrl+C

# Si systemd
systemctl stop bot-tiktok
```

### Redémarrer le bot

```bash
systemctl restart bot-tiktok
```

### Voir les logs

```bash
tail -f /root/bot-tiktok/bot.log
```

## ✅ Checklist Rapide

- [ ] Fichiers transférés sur le VPS (FileZilla ou SCP)
- [ ] Python 3 installé (`apt install python3 python3-pip screen -y`)
- [ ] Dépendances installées (`pip3 install -r requirements.txt`)
- [ ] `config.json` vérifié (clés API, service ID 1321, intervalle 1200)
- [ ] Test réussi (`python3 test_service_1321.py`)
- [ ] Bot lancé en arrière-plan (screen ou systemd)
- [ ] Logs vérifiés (`tail -f bot.log`)

## 🎯 Résumé Ultra-Rapide

```bash
# 1. Se connecter
ssh root@VOTRE_IP

# 2. Installer
apt update && apt install python3 python3-pip screen -y

# 3. Transférer les fichiers (via FileZilla ou SCP)

# 4. Installer dépendances
cd /root/bot-tiktok
pip3 install -r requirements.txt
pip3 install apify-client requests

# 5. Vérifier config.json
nano config.json

# 6. Tester
python3 test_service_1321.py

# 7. Lancer avec screen
screen -S bot-tiktok
python3 bot_apify.py
# Ctrl+A puis D pour détacher

# 8. Voir les logs
screen -r bot-tiktok
# ou
tail -f bot.log
```

## 🆘 Si ça ne marche pas

### Le bot ne démarre pas

```bash
# Voir les erreurs
python3 bot_apify.py

# Vérifier Python
python3 --version

# Vérifier les dépendances
pip3 list | grep apify
```

### Le bot s'arrête

```bash
# Voir les logs
cat bot.log | tail -50
```

C'est tout ! 🚀

