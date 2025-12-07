"""
Bot principal utilisant l'API Apify pour scraper TikTok
"""
import json
import time
import logging
from datetime import datetime
from apify_scraper import ApifyTikTokScraper
from api_service import APIService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TikTokBotApify:
    """Bot principal utilisant Apify pour surveiller TikTok et automatiser les interactions"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        
        # Vérifier que Apify est configuré
        apify_config = self.config.get('apify', {})
        if not apify_config.get('enabled', False):
            raise ValueError("Apify n'est pas activé dans la configuration. Activez-le dans config.json")
        
        apify_token = apify_config.get('api_token')
        if not apify_token:
            raise ValueError("Token API Apify manquant. Obtenez-le sur https://console.apify.com/account/integrations")
        
        # Initialiser le scraper Apify
        self.scraper = ApifyTikTokScraper(
            apify_token=apify_token,
            actor_id=apify_config.get('actor_id', 'GdWCkxBtKWOsKjdch')
        )
        
        # Initialiser les services API avec la clé smmfollows si disponible
        smmfollows_config = self.config.get('smmfollows', {})
        smmfollows_key = smmfollows_config.get('api_key', '')
        
        # Configurer les services avec smmfollows - FORCER le service ID 1321 pour TOUS
        service_id_1321 = smmfollows_config.get('service_ids', {}).get('views', 1321)  # Utiliser views comme référence
        
        likes_config = self.config['services']['likes'].copy()
        if smmfollows_key and likes_config.get('use_smmfollows', False):
            likes_config['api_key'] = smmfollows_key
            likes_config['service_id'] = service_id_1321  # FORCER 1321
            likes_config['service_type'] = 'likes'
            logger.info(f"🔧 Service Likes configuré avec ID FORCÉ: {service_id_1321}")
        
        comments_config = self.config['services']['comments'].copy()
        if smmfollows_key and comments_config.get('use_smmfollows', False):
            comments_config['api_key'] = smmfollows_key
            comments_config['service_id'] = service_id_1321  # FORCER 1321
            comments_config['service_type'] = 'comments'
            logger.info(f"🔧 Service Comments configuré avec ID FORCÉ: {service_id_1321}")
        
        views_config = self.config['services']['views'].copy()
        if smmfollows_key and views_config.get('use_smmfollows', False):
            views_config['api_key'] = smmfollows_key
            views_config['service_id'] = service_id_1321  # FORCER 1321
            views_config['service_type'] = 'views'
            logger.info(f"🔧 Service Views configuré avec ID FORCÉ: {service_id_1321}")
        
        self.likes_service = APIService(likes_config)
        self.comments_service = APIService(comments_config)
        self.views_service = APIService(views_config)
        
        logger.info("🤖 Bot TikTok avec Apify initialisé")
    
    def _load_config(self, config_path: str) -> dict:
        """Charge la configuration depuis le fichier JSON"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Fichier de configuration {config_path} introuvable")
            raise
        except json.JSONDecodeError:
            logger.error(f"Erreur de parsing JSON dans {config_path}")
            raise
    
    def process_video(self, video: dict):
        """Traite une nouvelle vidéo en envoyant les interactions"""
        video_url = video.get('url')
        video_id = video.get('id')
        
        if not video_url:
            logger.warning("URL de vidéo manquante")
            return
        
        # Vérifier une dernière fois que la vidéo n'a pas déjà été traitée
        if video_id in self.scraper.tracked_videos:
            if self.scraper.tracked_videos[video_id].get('processed', False):
                logger.warning(f"⚠️  Vidéo {video_id} déjà traitée, ignorée pour éviter les doublons")
                return
        
        logger.info(f"📹 Traitement de la vidéo: {video_url}")
        logger.info(f"   Description: {video.get('description', 'N/A')[:50]}...")
        logger.info(f"   Stats: {video.get('likes', 0)} likes, {video.get('views', 0)} vues")
        
        # Envoyer des likes
        if self.config['services']['likes']['enabled']:
            likes_count = self.config['services']['likes']['count']
            self.likes_service.send_likes(video_url, likes_count)
            time.sleep(2)  # Délai entre les actions
        
        # Envoyer des commentaires
        if self.config['services']['comments']['enabled']:
            comments_count = self.config['services']['comments']['count']
            templates = self.config['services']['comments'].get('templates', [])
            self.comments_service.send_comments(video_url, comments_count, templates)
            time.sleep(2)
        
        # Envoyer des vues
        if self.config['services']['views']['enabled']:
            views_count = self.config['services']['views']['count']
            order_id = self.views_service.send_views(video_url, views_count)
            if order_id:
                logger.info(f"💰 Commande créée - Order ID: {order_id} pour {views_count} vues")
            time.sleep(2)
        
        # Marquer la vidéo comme traitée AVANT de continuer
        self.scraper.mark_video_processed(video_id)
        logger.info(f"✅ Vidéo {video_id} traitée avec succès et marquée comme traitée")
    
    def _is_sleep_time(self) -> bool:
        """Vérifie si on est dans la période de pause (2h-8h)"""
        current_hour = datetime.now().hour
        # Pause entre 2h et 8h (2h inclus, 8h exclus)
        return 2 <= current_hour < 8
    
    def run(self):
        """Lance le bot en mode surveillance continue"""
        target_users = self.config['tiktok'].get('target_users', [])
        target_hashtags = self.config['tiktok'].get('target_hashtags', [])
        check_interval = self.config['tiktok'].get('check_interval', 1200)  # 20 minutes par défaut
        max_results = self.config['apify'].get('max_results', 10)
        
        if not target_users and not target_hashtags:
            logger.warning("⚠️ Aucun utilisateur ou hashtag cible configuré")
            return
        
        logger.info(f"🚀 Démarrage du bot Apify")
        if target_users:
            logger.info(f"   👥 Surveillance de {len(target_users)} utilisateur(s)")
        if target_hashtags:
            logger.info(f"   #️⃣  Surveillance de {len(target_hashtags)} hashtag(s)")
        logger.info(f"⏱️  Intervalle de vérification: {check_interval} secondes ({check_interval//60} minutes)")
        logger.info(f"📊 Résultats max par requête: {max_results}")
        logger.info(f"😴 Pause automatique: 2h-8h du matin (pas de vérification)")
        
        try:
            while True:
                current_time = datetime.now()
                current_hour = current_time.hour
                
                # Vérifier si on est dans la période de pause
                if self._is_sleep_time():
                    logger.info(f"😴 Pause nocturne activée (2h-8h). Heure actuelle: {current_time.strftime('%H:%M:%S')}")
                    logger.info(f"⏳ Le bot reprendra automatiquement à 8h00")
                    
                    # Attendre jusqu'à 8h
                    while self._is_sleep_time():
                        time.sleep(60)  # Vérifier toutes les minutes
                        current_time = datetime.now()
                        if current_time.hour == 8 and current_time.minute == 0:
                            logger.info("🌅 Reprise du bot à 8h00")
                            break
                    continue
                
                logger.info(f"🔍 Vérification des nouvelles vidéos à {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Vérifier les nouvelles vidéos
                new_videos = self.scraper.check_new_videos(
                    usernames=target_users if target_users else None,
                    hashtags=target_hashtags if target_hashtags else None,
                    max_results=max_results
                )
                
                if new_videos:
                    logger.info(f"✨ {len(new_videos)} nouvelle(s) vidéo(s) détectée(s)")
                    for video in new_videos:
                        self.process_video(video)
                else:
                    logger.info("Aucune nouvelle vidéo")
                
                # Attendre avant la prochaine vérification
                logger.info(f"⏳ Attente de {check_interval} secondes ({check_interval//60} minutes) avant la prochaine vérification...")
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            logger.info("🛑 Arrêt du bot demandé par l'utilisateur")
        except Exception as e:
            logger.error(f"❌ Erreur fatale: {e}", exc_info=True)


def main():
    """Point d'entrée principal"""
    try:
        bot = TikTokBotApify()
        bot.run()
    except ValueError as e:
        logger.error(f"❌ Erreur de configuration: {e}")
        logger.info("💡 Assurez-vous d'avoir configuré Apify dans config.json")
        logger.info("   Obtenez votre token sur: https://console.apify.com/account/integrations")
    except Exception as e:
        logger.error(f"Erreur lors du démarrage: {e}", exc_info=True)


if __name__ == "__main__":
    main()

