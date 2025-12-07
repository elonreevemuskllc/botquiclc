# 🚀 Guide Simple : Déployer le Bot sur VPS Hostinger

## 📋 Ce que fait le bot

- ✅ Surveille @bigjolan et @pasdurrrr toutes les 1 minute
- ✅ Détecte les nouvelles vidéos automatiquement
- ✅ Ajoute 99999 vues avec le service ID 1321
- ✅ Évite les doublons (ne traite que les nouvelles vidéos)

## 🔧 Étape 1 : Préparer les fichiers

### Option A : Créer un fichier ZIP (Recommandé)

Sur votre PC Windows :

1. Allez dans le dossier du bot : `C:\Users\Elon\Desktop\BOT PR CLC`
2. Sélectionnez tous les fichiers (Ctrl+A)
3. Clic droit → Envoyer vers → Dossier compressé
4. Vous obtenez `BOT PR CLC.zip`

### Option B : Utiliser Git (si vous avez un compte GitHub)

```bash
# Dans le dossier du bot
git init
git add .
git commit -m "Bot TikTok"
git remote add origin https://github.com/VOTRE_USERNAME/bot-tiktok.git
git push -u origin main
```

## 🔌 Étape 2 : Se connecter au VPS

### Via PuTTY (Windows)

1. Téléchargez PuTTY : https://www.putty.org/
2. Ouvrez PuTTY
3. Entrez l'IP de votre VPS Hostinger
4. Port : 22
5. Cliquez sur "Open"
6. Connectez-vous avec :
   - Username : `root` (ou celui fourni par Hostinger)
   - Password : (celui fourni par Hostinger)

### Via PowerShell (Windows 10/11)

```powershell
ssh root@VOTRE_IP_HOSTINGER
```

## 📦 Étape 3 : Transférer les fichiers

### Méthode 1 : Via FileZilla (Le plus simple)

1. Téléchargez FileZilla : https://filezilla-project.org/
2. Ouvrez FileZilla
3. Connectez-vous :
   - Hôte : `sftp://VOTRE_IP_HOSTINGER`
   - Utilisateur : `root`
   - Mot de passe : (votre mot de passe)
   - Port : 22
4. Glissez-déposez le fichier ZIP dans `/root/`
5. Ou glissez-déposez tous les fichiers du bot dans `/root/bot-tiktok/`

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

### Méthode 3 : Via Git (si vous avez poussé sur GitHub)

```bash
cd /root
git clone https://github.com/VOTRE_USERNAME/bot-tiktok.git
cd bot-tiktok
```

## 🐍 Étape 4 : Installer Python et les dépendances

Sur le VPS, exécutez :

```bash
# Mettre à jour le système
apt update && apt upgrade -y

# Installer Python et pip
apt install python3 python3-pip git screen -y

# Aller dans le dossier du bot
cd /root/bot-tiktok  # ou le chemin où vous avez mis les fichiers

# Installer les dépendances Python
pip3 install -r requirements.txt
pip3 install apify-client requests
```

## ⚙️ Étape 5 : Vérifier la configuration

```bash
# Éditer le fichier config.json
nano config.json
```

Vérifiez que :
- ✅ Token Apify est présent
- ✅ Clé API smmfollows est présente
- ✅ Service IDs sont tous à 1321
- ✅ Profils surveillés : `["bigjolan", "pasdurrrr"]`
- ✅ Views enabled : `true`
- ✅ Count : `99999`

Sauvegarder : `Ctrl+X`, puis `Y`, puis `Enter`

## 🧪 Étape 6 : Tester le bot

```bash
# Test rapide
python3 test_service_1321.py

# Si ça fonctionne, tester le bot (Ctrl+C pour arrêter)
python3 bot_apify.py
```

## 🚀 Étape 7 : Lancer le bot en arrière-plan

### Méthode 1 : Avec screen (Recommandé)

```bash
# Créer une session screen
screen -S bot-tiktok

# Lancer le bot
cd /root/bot-tiktok
python3 bot_apify.py

# Détacher de la session : Ctrl+A puis D
# Pour revenir : screen -r bot-tiktok
```

### Méthode 2 : Avec systemd (Service permanent)

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

# Activer le service (démarrage automatique)
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

# Voir le statut du service (si systemd)
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

### Mettre à jour le code

```bash
cd /root/bot-tiktok
# Si Git
git pull
# Sinon, retransférer les fichiers

# Redémarrer
systemctl restart bot-tiktok
```

## ✅ Checklist de Déploiement

- [ ] Fichiers transférés sur le VPS
- [ ] Python 3 installé
- [ ] Dépendances installées (`pip3 install -r requirements.txt`)
- [ ] `config.json` vérifié (clés API, service ID 1321)
- [ ] Test réussi (`python3 test_service_1321.py`)
- [ ] Bot lancé en arrière-plan (screen ou systemd)
- [ ] Logs vérifiés (`tail -f bot.log`)
- [ ] Bot fonctionne correctement

## 🎯 Résumé Rapide

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

## 🆘 Dépannage

### Le bot ne démarre pas

```bash
# Vérifier les erreurs
python3 bot_apify.py

# Vérifier Python
python3 --version

# Vérifier les dépendances
pip3 list | grep apify
```

### Le bot s'arrête

```bash
# Vérifier les logs
cat bot.log | tail -50

# Vérifier le solde smmfollows
python3 verifier_commandes.py
```

### Problème de permissions

```bash
chmod +x *.py
```

## 📝 Notes Importantes

1. **Sécurité** : Ne partagez jamais vos clés API
2. **Logs** : Les logs peuvent grossir, nettoyez-les régulièrement
3. **Ressources** : Le bot est léger, mais surveillez l'utilisation
4. **Service ID** : Toujours 1321, ne changez pas !

Bon déploiement ! 🚀

