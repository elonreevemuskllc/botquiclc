"""
Module pour interagir avec l'API smmfollows.com
API pour commander des likes, commentaires, vues, etc. sur TikTok
"""
import requests
import logging
import time
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SMMFollowsAPI:
    """Classe pour interagir avec l'API smmfollows.com"""
    
    BASE_URL = "https://smmfollows.com/api/v2"
    
    def __init__(self, api_key: str):
        """
        Initialise l'API smmfollows
        
        Args:
            api_key: Clé API obtenue sur la page Account de smmfollows.com
        """
        self.api_key = api_key
        self.session = requests.Session()
        self._services_cache = None
        logger.info("✅ API smmfollows initialisée")
    
    def _make_request(self, action: str, **params) -> Optional[Dict]:
        """
        Effectue une requête à l'API
        
        Args:
            action: Action à effectuer (services, add, status, balance, etc.)
            **params: Paramètres additionnels
            
        Returns:
            Réponse JSON de l'API ou None en cas d'erreur
        """
        payload = {
            "key": self.api_key,
            "action": action,
            **params
        }
        
        try:
            response = self.session.post(
                self.BASE_URL,
                data=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Erreur API smmfollows: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors de la requête API: {e}")
            return None
    
    def get_balance(self) -> Optional[float]:
        """
        Récupère le solde du compte
        
        Returns:
            Solde en USD ou None en cas d'erreur
        """
        result = self._make_request("balance")
        if result and "balance" in result:
            balance = float(result["balance"])
            logger.info(f"💰 Solde disponible: {balance} {result.get('currency', 'USD')}")
            return balance
        return None
    
    def get_services(self, force_refresh: bool = False) -> List[Dict]:
        """
        Récupère la liste des services disponibles
        
        Args:
            force_refresh: Force le rafraîchissement du cache
            
        Returns:
            Liste des services disponibles
        """
        if self._services_cache is None or force_refresh:
            result = self._make_request("services")
            if result and isinstance(result, list):
                self._services_cache = result
                logger.info(f"📋 {len(result)} service(s) disponible(s)")
            else:
                self._services_cache = []
        
        return self._services_cache or []
    
    def find_service(self, name_keywords: List[str], service_type: str = None) -> Optional[Dict]:
        """
        Trouve un service par mots-clés dans le nom
        
        Args:
            name_keywords: Mots-clés à rechercher dans le nom du service
            service_type: Type de service (optionnel)
            
        Returns:
            Service trouvé ou None
        """
        services = self.get_services()
        
        for service in services:
            service_name = service.get("name", "").lower()
            service_type_val = service.get("type", "").lower()
            
            # Vérifier les mots-clés
            matches = all(keyword.lower() in service_name for keyword in name_keywords)
            
            # Vérifier le type si spécifié
            if service_type and service_type.lower() not in service_type_val:
                continue
            
            if matches:
                return service
        
        return None
    
    def create_order(
        self,
        service_id: int,
        link: str,
        quantity: int,
        runs: Optional[int] = None,
        interval: Optional[int] = None
    ) -> Optional[int]:
        """
        Crée une commande (order)
        
        Args:
            service_id: ID du service
            link: Lien vers la page/vidéo TikTok
            quantity: Quantité souhaitée
            runs: Nombre d'exécutions (optionnel)
            interval: Intervalle en minutes (optionnel)
            
        Returns:
            ID de la commande créée ou None en cas d'erreur
        """
        params = {
            "service": service_id,
            "link": link,
            "quantity": quantity
        }
        
        if runs is not None:
            params["runs"] = runs
        if interval is not None:
            params["interval"] = interval
        
        result = self._make_request("add", **params)
        
        if result and "order" in result:
            order_id = result["order"]
            logger.info(f"✅ Commande créée: Order ID {order_id} (Service: {service_id}, Quantité: {quantity})")
            return order_id
        
        logger.error(f"❌ Échec de la création de la commande: {result}")
        return None
    
    def get_order_status(self, order_id: int) -> Optional[Dict]:
        """
        Récupère le statut d'une commande
        
        Args:
            order_id: ID de la commande
            
        Returns:
            Statut de la commande ou None
        """
        result = self._make_request("status", order=order_id)
        if result:
            return result
        return None
    
    def get_multiple_orders_status(self, order_ids: List[int]) -> Optional[Dict]:
        """
        Récupère le statut de plusieurs commandes
        
        Args:
            order_ids: Liste des IDs de commandes (max 100)
            
        Returns:
            Dictionnaire avec les statuts ou None
        """
        if len(order_ids) > 100:
            logger.warning("Maximum 100 commandes par requête")
            order_ids = order_ids[:100]
        
        orders_str = ",".join(str(order_id) for order_id in order_ids)
        result = self._make_request("status", orders=orders_str)
        return result
    
    def create_refill(self, order_id: int) -> Optional[int]:
        """
        Crée un refill pour une commande
        
        Args:
            order_id: ID de la commande
            
        Returns:
            ID du refill ou None
        """
        result = self._make_request("refill", order=order_id)
        if result and "refill" in result:
            refill_id = result["refill"]
            logger.info(f"✅ Refill créé: {refill_id} pour la commande {order_id}")
            return refill_id
        return None
    
    def cancel_order(self, order_id: int) -> bool:
        """
        Annule une commande
        
        Args:
            order_id: ID de la commande
            
        Returns:
            True si l'annulation a réussi
        """
        result = self._make_request("cancel", orders=str(order_id))
        if result and isinstance(result, list):
            for item in result:
                if item.get("order") == order_id and "cancel" in item:
                    cancel_result = item["cancel"]
                    if isinstance(cancel_result, int) or cancel_result == 1:
                        logger.info(f"✅ Commande {order_id} annulée")
                        return True
                    else:
                        logger.error(f"❌ Erreur lors de l'annulation: {cancel_result}")
        return False


class TikTokSMMService:
    """Classe simplifiée pour utiliser smmfollows avec TikTok"""
    
    def __init__(self, api_key: str):
        self.api = SMMFollowsAPI(api_key)
        self._service_ids = {}
        self._load_service_ids()
    
    def _load_service_ids(self):
        """Charge les IDs des services TikTok"""
        # NE PAS chercher automatiquement - on utilisera uniquement les IDs définis manuellement
        # via set_service_id() depuis la configuration
        logger.info("📋 Services TikTok - Utilisation des IDs définis manuellement dans config.json")
    
    def set_service_id(self, service_type: str, service_id: int):
        """Définit manuellement un ID de service"""
        self._service_ids[service_type] = service_id
        logger.info(f"🔧 Service {service_type} défini manuellement: ID {service_id}")
    
    def add_likes(self, video_url: str, quantity: int) -> Optional[int]:
        """Ajoute des likes à une vidéo TikTok"""
        service_id = self._service_ids.get("likes")
        if not service_id:
            logger.error("❌ Service Likes non trouvé. Définissez-le manuellement avec set_service_id('likes', ID)")
            return None
        
        return self.api.create_order(service_id, video_url, quantity)
    
    def add_comments(self, video_url: str, quantity: int) -> Optional[int]:
        """Ajoute des commentaires à une vidéo TikTok"""
        service_id = self._service_ids.get("comments")
        if not service_id:
            logger.error("❌ Service Comments non trouvé. Définissez-le manuellement avec set_service_id('comments', ID)")
            return None
        
        return self.api.create_order(service_id, video_url, quantity)
    
    def add_views(self, video_url: str, quantity: int) -> Optional[int]:
        """Ajoute des vues à une vidéo TikTok"""
        service_id = self._service_ids.get("views")
        if not service_id:
            logger.error("❌ Service Views non trouvé. Définissez-le manuellement avec set_service_id('views', ID)")
            return None
        
        logger.info(f"📤 Création commande: Service ID {service_id}, URL: {video_url}, Quantité: {quantity}")
        return self.api.create_order(service_id, video_url, quantity)
    
    def add_followers(self, profile_url: str, quantity: int) -> Optional[int]:
        """Ajoute des followers à un profil TikTok"""
        service_id = self._service_ids.get("followers")
        if not service_id:
            logger.error("❌ Service Followers non trouvé. Définissez-le manuellement avec set_service_id('followers', ID)")
            return None
        
        return self.api.create_order(service_id, profile_url, quantity)

