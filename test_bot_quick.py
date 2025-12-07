"""
Test rapide du bot pour voir ce qu'il fait
"""
import json
from apify_scraper import ApifyTikTokScraper
from smmfollows_api import SMMFollowsAPI, TikTokSMMService

print("🔍 Test du bot TikTok\n")
print("=" * 60)

# Charger la config
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Test 1: Vérifier Apify
print("\n1️⃣ Test Apify...")
try:
    scraper = ApifyTikTokScraper(
        apify_token=config['apify']['api_token'],
        actor_id=config['apify']['actor_id']
    )
    print("✅ Scraper Apify initialisé")
    
    # Test avec un utilisateur
    target_user = config['tiktok']['target_users'][0] if config['tiktok']['target_users'] else None
    if target_user:
        print(f"   Test scraping pour @{target_user}...")
        videos = scraper.scrape_user_videos(target_user, max_results=2)
        print(f"   ✅ {len(videos)} vidéo(s) trouvée(s)")
        if videos:
            print(f"   📹 Exemple: {videos[0].get('url', 'N/A')}")
except Exception as e:
    print(f"   ❌ Erreur Apify: {e}")

# Test 2: Vérifier smmfollows
print("\n2️⃣ Test smmfollows...")
try:
    api = SMMFollowsAPI(config['smmfollows']['api_key'])
    balance = api.get_balance()
    print(f"✅ Solde: ${balance:.2f}")
    
    # Vérifier le service ID 1321
    service_id = config['smmfollows']['service_ids']['likes']
    print(f"   Service ID pour likes: {service_id}")
    
    # Trouver le service
    services = api.get_services()
    service = next((s for s in services if s['service'] == service_id), None)
    if service:
        print(f"   ✅ Service trouvé: {service['name']}")
        print(f"      Prix: ${service.get('rate', 'N/A')} par unité")
        print(f"      Min: {service.get('min', 'N/A')}, Max: {service.get('max', 'N/A')}")
    else:
        print(f"   ⚠️ Service ID {service_id} non trouvé")
        
except Exception as e:
    print(f"   ❌ Erreur smmfollows: {e}")

# Test 3: Test complet du workflow
print("\n3️⃣ Test du workflow complet...")
try:
    smm_service = TikTokSMMService(config['smmfollows']['api_key'])
    smm_service.set_service_id('likes', config['smmfollows']['service_ids']['likes'])
    
    # Test avec une URL de vidéo (exemple)
    test_url = "https://www.tiktok.com/@charlidamelio/video/1234567890"
    print(f"   Test création de commande pour: {test_url}")
    print("   ⚠️  Note: Cette commande sera réelle et consommera des crédits!")
    print("   Pour tester vraiment, décommentez la ligne suivante dans le code")
    
    # order_id = smm_service.add_likes(test_url, 10)
    # print(f"   ✅ Commande créée: Order ID {order_id}")
    
except Exception as e:
    print(f"   ❌ Erreur: {e}")

print("\n" + "=" * 60)
print("✅ Tests terminés!")
print("\n💡 Pour lancer le bot complet:")
print("   python bot_apify.py")

