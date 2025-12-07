"""
Bot principal avec scraping avancé utilisant Selenium
"""
import json
import time
import logging
from datetime import datetime
from tiktok_scraper_advanced import TikTokScraperAdvanced
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


class TikTokBotAdvanced:
    """Bot principal avec scraping avancé pour surveiller TikTok et automatiser les interactions"""
    
    def __init__(self, config_path: str = "config.json", headless: bool = True):
        self.config = self._load_config(config_path)
        self.scraper = TikTokScraperAdvanced(
            username=self.config['tiktok'].get('username'),
            check_interval=self.config['tiktok'].get('check_interval', 60),
            headless=headless
        )
        
        # Initialiser les services API avec la clé smmfollows si disponible
        smmfollows_config = self.config.get('smmfollows', {})
        smmfollows_key = smmfollows_config.get('api_key', '')
        
        # Configurer les services avec smmfollows
        likes_config = self.config['services']['likes'].copy()
        if smmfollows_key and likes_config.get('use_smmfollows', False):
            likes_config['api_key'] = smmfollows_key
            if smmfollows_config.get('service_ids', {}).get('likes'):
                likes_config['service_id'] = smmfollows_config['service_ids']['likes']
        
        comments_config = self.config['services']['comments'].copy()
        if smmfollows_key and comments_config.get('use_smmfollows', False):
            comments_config['api_key'] = smmfollows_key
            if smmfollows_config.get('service_ids', {}).get('comments'):
                comments_config['service_id'] = smmfollows_config['service_ids']['comments']
        
        views_config = self.config['services']['views'].copy()
        if smmfollows_key and views_config.get('use_smmfollows', False):
            views_config['api_key'] = smmfollows_key
            if smmfollows_config.get('service_ids', {}).get('views'):
                views_config['service_id'] = smmfollows_config['service_ids']['views']
        
        self.likes_service = APIService(likes_config)
        self.comments_service = APIService(comments_config)
        self.views_service = APIService(views_config)
        
        logger.info("🤖 Bot TikTok Avancé initialisé")
    
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
        
        logger.info(f"📹 Traitement de la vidéo: {video_url}")
        
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
            self.views_service.send_views(video_url, views_count)
            time.sleep(2)
        
        # Marquer la vidéo comme traitée
        self.scraper.mark_video_processed(video_id)
        logger.info(f"✅ Vidéo {video_id} traitée avec succès")
    
    def run(self):
        """Lance le bot en mode surveillance continue"""
        target_users = self.config['tiktok'].get('target_users', [])
        check_interval = self.config['tiktok'].get('check_interval', 60)
        
        if not target_users:
            logger.warning("⚠️ Aucun utilisateur cible configuré")
            return
        
        logger.info(f"🚀 Démarrage du bot avancé - Surveillance de {len(target_users)} utilisateur(s)")
        logger.info(f"⏱️  Intervalle de vérification: {check_interval} secondes")
        
        try:
            while True:
                logger.info(f"🔍 Vérification des nouvelles vidéos à {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Vérifier les nouvelles vidéos
                new_videos = self.scraper.check_new_videos(target_users)
                
                if new_videos:
                    logger.info(f"✨ {len(new_videos)} nouvelle(s) vidéo(s) détectée(s)")
                    for video in new_videos:
                        self.process_video(video)
                else:
                    logger.info("Aucune nouvelle vidéo")
                
                # Attendre avant la prochaine vérification
                logger.info(f"⏳ Attente de {check_interval} secondes avant la prochaine vérification...")
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            logger.info("🛑 Arrêt du bot demandé par l'utilisateur")
        except Exception as e:
            logger.error(f"❌ Erreur fatale: {e}", exc_info=True)
        finally:
            # Nettoyer le driver Selenium
            self.scraper._close_driver()


def main():
    """Point d'entrée principal"""
    import sys
    
    # Mode headless par défaut, peut être désactivé avec --no-headless
    headless = '--no-headless' not in sys.argv
    
    try:
        bot = TikTokBotAdvanced(headless=headless)
        bot.run()
    except Exception as e:
        logger.error(f"Erreur lors du démarrage: {e}", exc_info=True)


if __name__ == "__main__":
    main()

