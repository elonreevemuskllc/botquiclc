# 📤 Guide Complet : Transférer le Bot avec FileZilla

## 📥 Étape 1 : Télécharger et Installer FileZilla

1. Allez sur : https://filezilla-project.org/
2. Cliquez sur **Download FileZilla Client**
3. Téléchargez la version Windows
4. Installez FileZilla (suivez l'assistant d'installation)

## 🔌 Étape 2 : Préparer vos identifiants VPS

Avant de commencer, vous devez avoir :
- ✅ L'**IP de votre VPS Hostinger** (exemple : `185.123.45.67`)
- ✅ Le **nom d'utilisateur** (généralement `root`)
- ✅ Le **mot de passe** de votre VPS

Ces informations sont dans votre panneau Hostinger.

## 🚀 Étape 3 : Se connecter au VPS avec FileZilla

### 3.1 Ouvrir FileZilla

1. Lancez FileZilla
2. Vous verrez une interface avec 2 panneaux :
   - **Gauche** : Votre PC (Local site)
   - **Droite** : Le serveur distant (Remote site)

### 3.2 Se connecter

En haut de FileZilla, dans la barre de connexion rapide :

1. **Hôte** : Entrez `sftp://VOTRE_IP` 
   - Exemple : `sftp://185.123.45.67`
   - ⚠️ Important : Commencez par `sftp://`

2. **Nom d'utilisateur** : `root`

3. **Mot de passe** : Votre mot de passe VPS

4. **Port** : `22`

5. Cliquez sur **Connexion rapide**

### 3.3 Accepter la clé SSH

La première fois, FileZilla vous demandera d'accepter la clé SSH :
- Cochez **"Toujours faire confiance à cet hôte"**
- Cliquez sur **OK**

### 3.4 Vérifier la connexion

Si la connexion réussit :
- ✅ Le panneau de droite affiche les fichiers du VPS
- ✅ Vous verrez probablement `/root/` ou `/home/`
- ✅ En bas, vous verrez "Connexion établie"

## 📁 Étape 4 : Naviguer dans FileZilla

### Sur votre PC (panneau de gauche)

1. Naviguez jusqu'à : `C:\Users\Elon\Desktop\BOT PR CLC`
2. Vous devriez voir tous les fichiers du bot :
   - `bot_apify.py`
   - `config.json`
   - `requirements.txt`
   - `apify_scraper.py`
   - etc.

### Sur le VPS (panneau de droite)

1. Naviguez jusqu'à : `/root/`
2. Si le dossier `bot-tiktok` n'existe pas, créez-le :
   - Clic droit dans le panneau de droite
   - **Créer un répertoire**
   - Nommez-le : `bot-tiktok`
   - Entrez dedans (double-clic)

## 📤 Étape 5 : Transférer les fichiers

### Méthode 1 : Glisser-Déposer (Le plus simple) ⭐

1. Dans le panneau de **gauche** (votre PC), sélectionnez tous les fichiers :
   - Cliquez sur le premier fichier
   - Maintenez `Shift` et cliquez sur le dernier (pour tout sélectionner)
   - Ou `Ctrl+A` pour tout sélectionner

2. **Glissez** les fichiers vers le panneau de **droite** (VPS)
   - Glissez vers `/root/bot-tiktok/`

3. FileZilla va commencer le transfert
   - Vous verrez la progression en bas de la fenêtre
   - Attendez que tous les fichiers soient transférés

### Méthode 2 : Clic droit

1. Sélectionnez tous les fichiers dans le panneau de gauche
2. Clic droit → **Téléverser** (Upload)
3. Les fichiers seront transférés vers le dossier actuel du panneau de droite

## ✅ Étape 6 : Vérifier le transfert

Dans le panneau de droite (VPS), vérifiez que tous les fichiers sont là :

- ✅ `bot_apify.py`
- ✅ `config.json`
- ✅ `requirements.txt`
- ✅ `apify_scraper.py`
- ✅ `smmfollows_api.py`
- ✅ `api_service.py`
- ✅ Tous les autres fichiers `.py`
- ✅ `README.md`
- ✅ etc.

## 🔍 Étape 7 : Vérifier les permissions (optionnel)

Pour être sûr que les fichiers sont exécutables :

1. Dans FileZilla, panneau de droite
2. Clic droit sur un fichier `.py` → **Permissions de fichier**
3. Cochez **Exécuter** pour le propriétaire
4. Cliquez sur **OK**

Ou faites-le via SSH après (voir ci-dessous).

## 🎯 Résumé Visuel de l'Interface FileZilla

```
┌─────────────────────────────────────────────────────────┐
│  FileZilla                                              │
├──────────────────┬──────────────────────────────────────┤
│                  │                                      │
│  VOTRE PC        │        VPS HOSTINGER                 │
│  (Local)         │        (Remote)                      │
│                  │                                      │
│  C:\Users\...    │  /root/bot-tiktok/                   │
│  BOT PR CLC\     │                                      │
│  ├─ bot_apify.py │  (vide - fichiers à transférer ici)  │
│  ├─ config.json  │                                      │
│  └─ ...          │                                      │
│                  │                                      │
│  ↓ GLISSEZ ICI   │  ↓ VERS ICI                          │
│                  │                                      │
└──────────────────┴──────────────────────────────────────┘
```

## 📋 Checklist de Transfert

- [ ] FileZilla installé
- [ ] Connecté au VPS (sftp://IP, port 22)
- [ ] Navigué vers `/root/bot-tiktok/` sur le VPS
- [ ] Navigué vers `C:\Users\Elon\Desktop\BOT PR CLC` sur le PC
- [ ] Tous les fichiers sélectionnés
- [ ] Fichiers glissés-déposés vers le VPS
- [ ] Transfert terminé (barre de progression en bas)
- [ ] Fichiers visibles dans `/root/bot-tiktok/` sur le VPS

## 🆘 Problèmes Courants

### "Connexion refusée"

**Solution** :
- Vérifiez que vous utilisez `sftp://` avant l'IP
- Vérifiez le port (22)
- Vérifiez que le VPS est allumé

### "Authentification échouée"

**Solution** :
- Vérifiez le nom d'utilisateur (`root`)
- Vérifiez le mot de passe
- Réessayez

### Les fichiers ne se transfèrent pas

**Solution** :
- Vérifiez que vous avez les permissions d'écriture
- Essayez de créer un dossier d'abord
- Vérifiez l'espace disque du VPS

### "Permission denied"

**Solution** :
- Assurez-vous d'être dans `/root/` (pas `/home/`)
- Créez le dossier `bot-tiktok` d'abord
- Vérifiez les permissions après le transfert

## 🎯 Après le Transfert

Une fois les fichiers transférés, connectez-vous en SSH pour continuer :

```bash
# Se connecter en SSH
ssh root@VOTRE_IP

# Aller dans le dossier
cd /root/bot-tiktok

# Vérifier que les fichiers sont là
ls -la

# Installer Python et dépendances
apt update && apt install python3 python3-pip screen -y
pip3 install -r requirements.txt
pip3 install apify-client requests

# Lancer le bot
screen -S bot-tiktok
python3 bot_apify.py
```

## 💡 Astuces FileZilla

1. **Sauvegarder la connexion** :
   - Fichier → Gestionnaire de sites
   - Nouveau site
   - Entrez vos identifiants
   - Sauvegarder pour réutilisation

2. **Voir les fichiers cachés** :
   - Serveur → Forcer l'affichage des fichiers cachés

3. **Transférer en arrière-plan** :
   - Les transferts continuent même si vous fermez la fenêtre de transfert

4. **Queue de transfert** :
   - En bas, onglet "Files queued" pour voir les fichiers en attente

C'est tout ! 🚀

