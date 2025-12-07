"""
Script de configuration initiale
"""
import json
import os

def setup_config():
    """Configure le fichier config.json interactivement"""
    print("🔧 Configuration du Bot TikTok\n")
    
    config = {
        "tiktok": {
            "username": input("Nom d'utilisateur TikTok (optionnel): ").strip() or "",
            "check_interval": int(input("Intervalle de vérification en secondes (défaut: 60): ").strip() or "60"),
            "target_users": []
        },
        "services": {
            "likes": {
                "enabled": input("Activer les likes ? (o/n, défaut: o): ").strip().lower() != 'n',
                "count": int(input("Nombre de likes par vidéo (défaut: 10): ").strip() or "10"),
                "api_url": input("URL API pour les likes: ").strip(),
                "api_key": input("Clé API pour les likes: ").strip()
            },
            "comments": {
                "enabled": input("Activer les commentaires ? (o/n, défaut: o): ").strip().lower() != 'n',
                "count": int(input("Nombre de commentaires par vidéo (défaut: 5): ").strip() or "5"),
                "api_url": input("URL API pour les commentaires: ").strip(),
                "api_key": input("Clé API pour les commentaires: ").strip(),
                "templates": [
                    "Super vidéo ! 🔥",
                    "J'adore ! ❤️",
                    "Trop bien ! 👏",
                    "Excellent contenu ! 💯"
                ]
            },
            "views": {
                "enabled": input("Activer les vues ? (o/n, défaut: n): ").strip().lower() == 'o',
                "count": int(input("Nombre de vues par vidéo (défaut: 100): ").strip() or "100"),
                "api_url": input("URL API pour les vues: ").strip(),
                "api_key": input("Clé API pour les vues: ").strip()
            }
        },
        "database": {
            "file": "videos_tracked.json"
        }
    }
    
    # Demander les utilisateurs à surveiller
    print("\nUtilisateurs TikTok à surveiller (un par ligne, laissez vide pour terminer):")
    users = []
    while True:
        user = input("> ").strip()
        if not user:
            break
        users.append(user)
    config["tiktok"]["target_users"] = users
    
    # Sauvegarder la configuration
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("\n✅ Configuration sauvegardée dans config.json")
    print("🚀 Vous pouvez maintenant lancer le bot avec: python bot.py")

if __name__ == "__main__":
    setup_config()

