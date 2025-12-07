"""
Script pour vérifier les commandes créées et le solde smmfollows
"""
from smmfollows_api import SMMFollowsAPI
import json

# Charger la config
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

api_key = config['smmfollows']['api_key']
api = SMMFollowsAPI(api_key)

print("=" * 60)
print("💰 VÉRIFICATION DU SOLDE ET DES COMMANDES")
print("=" * 60)

# Vérifier le solde
balance = api.get_balance()
print(f"\n💵 Solde actuel: ${balance:.2f} USD")

# Note: smmfollows ne permet pas de lister toutes les commandes via l'API
# Vous devez vérifier sur le site web smmfollows.com
print("\n📋 Pour voir toutes vos commandes:")
print("   1. Allez sur https://smmfollows.com")
print("   2. Connectez-vous")
print("   3. Allez dans 'Orders' pour voir toutes les commandes")
print("\n⚠️  Vérifiez que vous n'avez pas de commandes en double!")

