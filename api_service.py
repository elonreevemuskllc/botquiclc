"""
Module pour interagir avec les services API (likes, commentaires, vues)
Supporte smmfollows.com et autres APIs personnalisées
"""
import requests
import random
import logging
from typing import Dict, List, Optional
from smmfollows_api import TikTokSMMService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIService:
    """Classe pour gérer les interactions avec les services API externes"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.session = requests.Session()
        self.use_smmfollows = config.get('use_smmfollows', False)
        
        # Initialiser smmfollows si activé
        if self.use_smmfollows:
            api_key = config.get('api_key')
            if api_key:
                self.smm_service = TikTokSMMService(api_key)
                # FORCER l'utilisation du service_id depuis la config
                # On détermine le type de service depuis le contexte (likes, comments, views)
                service_type = config.get('service_type', 'views')  # Par défaut views car c'est le seul activé
                
                # Si service_id est défini dans la config, l'utiliser
                if 'service_id' in config and config['service_id']:
                    self.smm_service.set_service_id(service_type, config['service_id'])
                    logger.info(f"🔧 Service {service_type} FORCÉ avec ID: {config['service_id']}")
                else:
                    # Sinon, essayer de le déduire du nom de la méthode appelée
                    # Mais on préfère toujours utiliser celui de la config
                    logger.warning(f"⚠️ service_id non défini pour {service_type}, utilisation de la config smmfollows")
            else:
                logger.warning("⚠️ smmfollows activé mais clé API manquante")
                self.use_smmfollows = False
    
    def send_likes(self, video_url: str, count: int = 10) -> bool:
        """
        Envoie une requête pour ajouter des likes à une vidéo
        """
        if not self.config.get('enabled', False):
            logger.info("Service de likes désactivé")
            return False
        
        # Utiliser smmfollows si activé
        if self.use_smmfollows and hasattr(self, 'smm_service'):
            try:
                order_id = self.smm_service.add_likes(video_url, count)
                if order_id:
                    logger.info(f"✅ Commande de {count} likes créée (Order ID: {order_id})")
                    return True
                return False
            except Exception as e:
                logger.error(f"Erreur smmfollows lors de l'envoi des likes: {e}")
                return False
        
        # API personnalisée (ancien code)
        api_url = self.config.get('api_url')
        api_key = self.config.get('api_key')
        
        if not api_url:
            logger.warning("URL API non configurée pour les likes")
            return False
        
        try:
            payload = {
                "video_url": video_url,
                "count": count,
                "api_key": api_key
            }
            
            response = self.session.post(
                api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info(f"✅ {count} likes envoyés pour {video_url}")
                return True
            else:
                logger.error(f"Erreur API likes: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi des likes: {e}")
            return False
    
    def send_comments(self, video_url: str, count: int = 5, templates: List[str] = None) -> bool:
        """
        Envoie une requête pour ajouter des commentaires à une vidéo
        """
        if not self.config.get('enabled', False):
            logger.info("Service de commentaires désactivé")
            return False
        
        # Utiliser smmfollows si activé
        if self.use_smmfollows and hasattr(self, 'smm_service'):
            try:
                order_id = self.smm_service.add_comments(video_url, count)
                if order_id:
                    logger.info(f"✅ Commande de {count} commentaires créée (Order ID: {order_id})")
                    logger.info(f"   Note: Les commentaires seront générés automatiquement par smmfollows")
                    return True
                return False
            except Exception as e:
                logger.error(f"Erreur smmfollows lors de l'envoi des commentaires: {e}")
                return False
        
        # API personnalisée (ancien code)
        api_url = self.config.get('api_url')
        api_key = self.config.get('api_key')
        
        if not api_url:
            logger.warning("URL API non configurée pour les commentaires")
            return False
        
        if templates is None:
            templates = ["Super vidéo ! 🔥", "J'adore ! ❤️"]
        
        try:
            # Sélectionner des commentaires aléatoires
            selected_comments = random.sample(templates, min(count, len(templates)))
            
            payload = {
                "video_url": video_url,
                "comments": selected_comments,
                "api_key": api_key
            }
            
            response = self.session.post(
                api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info(f"✅ {len(selected_comments)} commentaires envoyés pour {video_url}")
                return True
            else:
                logger.error(f"Erreur API commentaires: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi des commentaires: {e}")
            return False
    
    def send_views(self, video_url: str, count: int = 100) -> bool:
        """
        Envoie une requête pour ajouter des vues à une vidéo
        """
        if not self.config.get('enabled', False):
            logger.info("Service de vues désactivé")
            return False
        
        # Utiliser smmfollows si activé
        if self.use_smmfollows and hasattr(self, 'smm_service'):
            try:
                # FORCER l'utilisation du service_id depuis la config
                service_id = self.config.get('service_id')
                if service_id:
                    # Forcer le service ID pour views
                    self.smm_service.set_service_id('views', service_id)
                    logger.info(f"🔧 Service ID FORCÉ pour views: {service_id}")
                
                order_id = self.smm_service.add_views(video_url, count)
                if order_id:
                    logger.info(f"✅ Commande de {count} vues créée (Order ID: {order_id}) avec Service ID: {service_id or 'config'}")
                    return True
                return False
            except Exception as e:
                logger.error(f"Erreur smmfollows lors de l'envoi des vues: {e}")
                return False
        
        # API personnalisée (ancien code)
        api_url = self.config.get('api_url')
        api_key = self.config.get('api_key')
        
        if not api_url:
            logger.warning("URL API non configurée pour les vues")
            return False
        
        try:
            payload = {
                "video_url": video_url,
                "count": count,
                "api_key": api_key
            }
            
            response = self.session.post(
                api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info(f"✅ {count} vues envoyées pour {video_url}")
                return True
            else:
                logger.error(f"Erreur API vues: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi des vues: {e}")
            return False

