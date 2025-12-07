"""
Script utilitaire pour vérifier les services disponibles sur smmfollows
et trouver les IDs des services TikTok
"""
import json
import sys
from smmfollows_api import SMMFollowsAPI

def main():
    """Affiche les services disponibles et permet de trouver les IDs TikTok"""
    
    # Charger la configuration
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Fichier config.json introuvable")
        sys.exit(1)
    
    api_key = config.get('smmfollows', {}).get('api_key')
    if not api_key:
        print("❌ Clé API smmfollows non configurée dans config.json")
        print("   Ajoutez votre clé dans: smmfollows.api_key")
        sys.exit(1)
    
    # Initialiser l'API
    api = SMMFollowsAPI(api_key)
    
    # Vérifier le solde
    print("=" * 60)
    print("💰 Vérification du solde...")
    balance = api.get_balance()
    if balance is not None:
        print(f"✅ Solde disponible: ${balance:.2f}")
    else:
        print("⚠️  Impossible de récupérer le solde")
    print("=" * 60)
    
    # Récupérer tous les services
    print("\n📋 Récupération de la liste des services...")
    services = api.get_services(force_refresh=True)
    
    if not services:
        print("❌ Aucun service trouvé ou erreur API")
        sys.exit(1)
    
    print(f"\n✅ {len(services)} service(s) disponible(s)\n")
    
    # Filtrer les services TikTok
    tiktok_services = []
    for service in services:
        name = service.get('name', '').lower()
        if 'tiktok' in name or 'tik tok' in name:
            tiktok_services.append(service)
    
    if tiktok_services:
        print("=" * 60)
        print("🎵 SERVICES TIKTOK TROUVÉS:")
        print("=" * 60)
        
        for service in tiktok_services:
            print(f"\n📌 Service ID: {service['service']}")
            print(f"   Nom: {service['name']}")
            print(f"   Type: {service.get('type', 'N/A')}")
            print(f"   Catégorie: {service.get('category', 'N/A')}")
            print(f"   Prix: ${service.get('rate', 'N/A')} par unité")
            print(f"   Min: {service.get('min', 'N/A')}")
            print(f"   Max: {service.get('max', 'N/A')}")
            print(f"   Refill: {'Oui' if service.get('refill') else 'Non'}")
            print(f"   Annulable: {'Oui' if service.get('cancel') else 'Non'}")
        
        print("\n" + "=" * 60)
        print("💡 Pour utiliser ces services, ajoutez les IDs dans config.json:")
        print("=" * 60)
        print("\n{")
        print('  "smmfollows": {')
        print(f'    "api_key": "{api_key}",')
        print('    "service_ids": {')
        
        # Essayer de deviner les types
        likes_id = None
        comments_id = None
        views_id = None
        
        for service in tiktok_services:
            name = service['name'].lower()
            service_id = service['service']
            
            if 'like' in name:
                likes_id = service_id
            elif 'comment' in name:
                comments_id = service_id
            elif 'view' in name or 'vue' in name:
                views_id = service_id
        
        print(f'      "likes": {likes_id if likes_id else "null"},')
        print(f'      "comments": {comments_id if comments_id else "null"},')
        print(f'      "views": {views_id if views_id else "null"}')
        print('    }')
        print('  }')
        print('}')
        
    else:
        print("\n⚠️  Aucun service TikTok trouvé dans la liste")
        print("   Vérifiez que smmfollows propose des services TikTok")
    
    # Afficher tous les services (optionnel)
    print("\n" + "=" * 60)
    response = input("Afficher tous les services ? (o/n): ").strip().lower()
    if response == 'o':
        print("\n📋 TOUS LES SERVICES:")
        print("=" * 60)
        for service in services:
            print(f"\nID: {service['service']} | {service['name']} | {service.get('type', 'N/A')} | ${service.get('rate', 'N/A')}")

if __name__ == "__main__":
    main()

