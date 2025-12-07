# Guide de Déploiement sur VPS Hostinger

## 📋 Prérequis

- VPS Hostinger avec accès SSH
- Python 3.8+ installé sur le VPS
- Accès root ou utilisateur avec sudo

## 🚀 Étapes de Déploiement

### 1. Se connecter au VPS via SSH

```bash
ssh root@VOTRE_IP_HOSTINGER
# ou
ssh utilisateur@VOTRE_IP_HOSTINGER
```

### 2. Installer Python et les dépendances système

```bash
# Mettre à jour le système
apt update && apt upgrade -y

# Installer Python et pip
apt install python3 python3-pip git -y

# Vérifier l'installation
python3 --version
pip3 --version
```

### 3. Transférer les fichiers du bot

#### Option A : Via Git (Recommandé)

```bash
# Cloner votre repository (si vous avez poussé le code sur GitHub/GitLab)
git clone https://github.com/VOTRE_USERNAME/BOT-PR-CLC.git
cd BOT-PR-CLC
```

#### Option B : Via SCP (depuis votre machine locale)

Depuis votre machine Windows (PowerShell) :

```powershell
# Créer un fichier zip du projet
Compress-Archive -Path "C:\Users\Elon\Desktop\BOT PR CLC\*" -DestinationPath "bot.zip"

# Transférer via SCP (remplacez par vos identifiants)
scp bot.zip root@VOTRE_IP:/root/
```

Puis sur le VPS :

```bash
cd /root
unzip bot.zip -d bot-tiktok
cd bot-tiktok
```

#### Option C : Via SFTP (FileZilla, WinSCP, etc.)

1. Connectez-vous au VPS avec FileZilla/WinSCP
2. Transférez tous les fichiers du projet dans `/root/bot-tiktok/`

### 4. Installer les dépendances Python

```bash
cd /root/bot-tiktok  # ou le chemin où vous avez mis les fichiers

# Installer les dépendances
pip3 install -r requirements.txt

# Vérifier que apify-client est installé
pip3 install apify-client requests
```

### 5. Configurer le bot

```bash
# Éditer le fichier config.json
nano config.json
```

Vérifiez que toutes vos clés API sont bien configurées :
- Token Apify
- Clé API smmfollows
- Profils à surveiller
- Service IDs

### 6. Tester le bot

```bash
# Test rapide
python3 test_bot_quick.py

# Si ça fonctionne, tester le bot complet (Ctrl+C pour arrêter)
python3 bot_apify.py
```

### 7. Lancer le bot en arrière-plan avec screen ou tmux

#### Option A : Utiliser screen (Recommandé)

```bash
# Installer screen
apt install screen -y

# Créer une session screen
screen -S bot-tiktok

# Lancer le bot
cd /root/bot-tiktok
python3 bot_apify.py

# Détacher de la session : Ctrl+A puis D
# Pour revenir à la session : screen -r bot-tiktok
```

#### Option B : Utiliser tmux

```bash
# Installer tmux
apt install tmux -y

# Créer une session tmux
tmux new -s bot-tiktok

# Lancer le bot
cd /root/bot-tiktok
python3 bot_apify.py

# Détacher : Ctrl+B puis D
# Revenir : tmux attach -t bot-tiktok
```

#### Option C : Utiliser systemd (Service permanent)

Créer un service systemd :

```bash
nano /etc/systemd/system/bot-tiktok.service
```

Contenu du fichier :

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

[Install]
WantedBy=multi-user.target
```

Activer et démarrer le service :

```bash
# Recharger systemd
systemctl daemon-reload

# Activer le service (démarrage automatique au boot)
systemctl enable bot-tiktok

# Démarrer le service
systemctl start bot-tiktok

# Vérifier le statut
systemctl status bot-tiktok

# Voir les logs
journalctl -u bot-tiktok -f
```

### 8. Vérifier que le bot fonctionne

```bash
# Vérifier les logs
tail -f /root/bot-tiktok/bot.log

# Ou si vous utilisez systemd
journalctl -u bot-tiktok -f

# Vérifier les processus Python
ps aux | grep python
```

## 🔧 Commandes Utiles

### Arrêter le bot

```bash
# Si dans screen/tmux
screen -r bot-tiktok  # puis Ctrl+C

# Si service systemd
systemctl stop bot-tiktok
```

### Redémarrer le bot

```bash
# Service systemd
systemctl restart bot-tiktok

# Screen
screen -r bot-tiktok
# Puis relancer python3 bot_apify.py
```

### Voir les logs en temps réel

```bash
tail -f /root/bot-tiktok/bot.log
```

### Mettre à jour le code

```bash
cd /root/bot-tiktok
# Si Git
git pull

# Puis redémarrer
systemctl restart bot-tiktok
```

## ⚠️ Notes Importantes

1. **Sécurité** : Ne partagez jamais vos clés API publiquement
2. **Firewall** : Le bot n'a pas besoin de ports ouverts (il fait des requêtes sortantes)
3. **Ressources** : Le bot est léger, mais surveillez l'utilisation CPU/RAM
4. **Logs** : Les logs peuvent grossir, pensez à les nettoyer régulièrement :

```bash
# Nettoyer les anciens logs (garder les 1000 dernières lignes)
tail -n 1000 bot.log > bot.log.tmp && mv bot.log.tmp bot.log
```

## 🐛 Dépannage

### Le bot ne démarre pas

```bash
# Vérifier les erreurs
python3 bot_apify.py

# Vérifier les dépendances
pip3 list | grep apify
pip3 list | grep requests
```

### Le bot s'arrête

```bash
# Vérifier les logs
cat bot.log | tail -50

# Vérifier le solde smmfollows
python3 check_smmfollows_services.py
```

### Problème de permissions

```bash
# Donner les permissions d'exécution
chmod +x bot_apify.py
chmod +x *.py
```

## 📊 Monitoring

### Surveiller l'utilisation des ressources

```bash
# CPU et RAM
htop
# ou
top

# Espace disque
df -h
```

### Vérifier que le bot tourne toujours

```bash
# Script de vérification simple
crontab -e

# Ajouter cette ligne pour vérifier toutes les heures
0 * * * * pgrep -f bot_apify.py || systemctl restart bot-tiktok
```

## ✅ Checklist de Déploiement

- [ ] VPS Hostinger accessible via SSH
- [ ] Python 3.8+ installé
- [ ] Fichiers du bot transférés
- [ ] Dépendances installées (`pip3 install -r requirements.txt`)
- [ ] `config.json` configuré avec les bonnes clés API
- [ ] Test réussi (`python3 test_bot_quick.py`)
- [ ] Bot lancé en arrière-plan (screen/tmux/systemd)
- [ ] Logs vérifiés (`tail -f bot.log`)
- [ ] Bot fonctionne correctement

## 🎯 Résumé

Une fois déployé, votre bot :
- ✅ Surveille @bigjolan et @pasdurrrr toutes les 1 minute
- ✅ Ajoute 99999 vues automatiquement à chaque nouvelle vidéo
- ✅ Tourne 24/7 sur votre VPS Hostinger
- ✅ Logs disponibles dans `bot.log`

Bon déploiement ! 🚀

