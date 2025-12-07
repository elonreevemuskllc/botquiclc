"""
Test pour vérifier que seul le service ID 1321 est utilisé
"""
import json
from api_service import APIService

print("=" * 60)
print("🔍 VÉRIFICATION: Service ID 1321 uniquement")
print("=" * 60)

# Charger la config
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

smmfollows_config = config.get('smmfollows', {})
service_id_1321 = smmfollows_config.get('service_ids', {}).get('views', 1321)

print(f"\n✅ Service ID configuré dans config.json: {service_id_1321}")

# Tester le service views
views_config = config['services']['views'].copy()
views_config['api_key'] = smmfollows_config.get('api_key', '')
views_config['service_id'] = service_id_1321
views_config['service_type'] = 'views'

print(f"\n📋 Configuration views:")
print(f"   - enabled: {views_config.get('enabled')}")
print(f"   - use_smmfollows: {views_config.get('use_smmfollows')}")
print(f"   - service_id: {views_config.get('service_id')}")
print(f"   - count: {views_config.get('count')}")

# Initialiser le service
service = APIService(views_config)

# Vérifier que le service ID est bien 1321
if hasattr(service, 'smm_service'):
    views_id = service.smm_service._service_ids.get('views')
    print(f"\n🔧 Service ID dans smm_service: {views_id}")
    
    if views_id == 1321:
        print("✅ CORRECT: Service ID 1321 est bien configuré!")
    else:
        print(f"❌ ERREUR: Service ID est {views_id} au lieu de 1321!")
else:
    print("⚠️  smm_service non initialisé")

print("\n" + "=" * 60)
print("✅ Test terminé")

