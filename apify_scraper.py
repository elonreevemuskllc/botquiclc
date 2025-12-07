"""
Module de scraping TikTok utilisant l'API Apify
Utilise l'acteur Apify pour scraper TikTok de manière fiable
"""
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional
from apify_client import ApifyClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ApifyTikTokScraper:
    """Classe pour scraper TikTok en utilisant l'API Apify"""
    
    def __init__(self, apify_token: str, actor_id: str = "GdWCkxBtKWOsKjdch"):
        """
        Initialise le scraper Apify
        
        Args:
            apify_token: Token API Apify (obtenu depuis https://console.apify.com/account/integrations)
            actor_id: ID de l'acteur Apify pour TikTok (défaut: GdWCkxBtKWOsKjdch)
        """
        self.client = ApifyClient(apify_token)
        self.actor_id = actor_id
        self.tracked_videos = self._load_tracked_videos()
        logger.info("✅ Scraper Apify initialisé")
    
    def _load_tracked_videos(self) -> Dict:
        """Charge les vidéos déjà trackées depuis le fichier"""
        try:
            with open('videos_tracked.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _save_tracked_videos(self):
        """Sauvegarde les vidéos trackées dans le fichier"""
        with open('videos_tracked.json', 'w', encoding='utf-8') as f:
            json.dump(self.tracked_videos, f, indent=2, ensure_ascii=False)
    
    def scrape_user_videos(self, username: str, max_results: int = 10) -> List[Dict]:
        """
        Scrape les vidéos d'un utilisateur TikTok via Apify
        
        Args:
            username: Nom d'utilisateur TikTok (sans le @)
            max_results: Nombre maximum de vidéos à récupérer
            
        Returns:
            Liste des vidéos avec leurs informations
        """
        try:
            logger.info(f"🔍 Scraping des vidéos de @{username} via Apify...")
            
            # Configuration de l'acteur Apify
            run_input = {
                "profiles": [f"https://www.tiktok.com/@{username}"],
                "resultsLimit": max_results,
                "shouldDownloadVideos": False,
                "shouldDownloadCovers": False,
            }
            
            # Lancer l'acteur
            run = self.client.actor(self.actor_id).call(run_input=run_input)
            
            # Attendre la fin de l'exécution
            logger.info(f"⏳ Attente de la fin du scraping (run ID: {run['id']})...")
            
            # Récupérer les résultats
            videos = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                video_data = {
                    "id": item.get("id") or item.get("videoId") or item.get("awemeId", ""),
                    "url": item.get("webVideoUrl") or item.get("url") or f"https://www.tiktok.com/@{username}/video/{item.get('id', '')}",
                    "username": username,
                    "timestamp": datetime.now().isoformat(),
                    "description": item.get("text") or item.get("description") or "",
                    "likes": item.get("diggCount") or item.get("likeCount") or 0,
                    "comments": item.get("commentCount") or 0,
                    "shares": item.get("shareCount") or 0,
                    "views": item.get("playCount") or item.get("viewCount") or 0,
                    "created_at": item.get("createTime") or item.get("timestamp") or None
                }
                videos.append(video_data)
            
            logger.info(f"✅ {len(videos)} vidéo(s) récupérée(s) pour @{username}")
            return videos
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du scraping Apify: {e}")
            return []
    
    def scrape_hashtag_videos(self, hashtag: str, max_results: int = 10) -> List[Dict]:
        """
        Scrape les vidéos d'un hashtag TikTok via Apify
        
        Args:
            hashtag: Hashtag à scraper (sans le #)
            max_results: Nombre maximum de vidéos à récupérer
            
        Returns:
            Liste des vidéos avec leurs informations
        """
        try:
            logger.info(f"🔍 Scraping des vidéos du hashtag #{hashtag} via Apify...")
            
            # Configuration de l'acteur Apify pour hashtag
            run_input = {
                "hashtags": [hashtag],
                "resultsLimit": max_results,
                "shouldDownloadVideos": False,
                "shouldDownloadCovers": False,
            }
            
            # Lancer l'acteur
            run = self.client.actor(self.actor_id).call(run_input=run_input)
            
            # Attendre la fin de l'exécution
            logger.info(f"⏳ Attente de la fin du scraping (run ID: {run['id']})...")
            
            # Récupérer les résultats
            videos = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                username = item.get("authorMeta", {}).get("name") or item.get("author") or "unknown"
                video_data = {
                    "id": item.get("id") or item.get("videoId") or item.get("awemeId", ""),
                    "url": item.get("webVideoUrl") or item.get("url") or "",
                    "username": username,
                    "timestamp": datetime.now().isoformat(),
                    "description": item.get("text") or item.get("description") or "",
                    "likes": item.get("diggCount") or item.get("likeCount") or 0,
                    "comments": item.get("commentCount") or 0,
                    "shares": item.get("shareCount") or 0,
                    "views": item.get("playCount") or item.get("viewCount") or 0,
                    "hashtag": hashtag
                }
                videos.append(video_data)
            
            logger.info(f"✅ {len(videos)} vidéo(s) récupérée(s) pour #{hashtag}")
            return videos
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du scraping Apify: {e}")
            return []
    
    def check_new_videos(self, usernames: List[str] = None, hashtags: List[str] = None, max_results: int = 10) -> List[Dict]:
        """
        Vérifie les nouvelles vidéos pour une liste d'utilisateurs ou hashtags
        
        Args:
            usernames: Liste des utilisateurs à surveiller
            hashtags: Liste des hashtags à surveiller
            max_results: Nombre maximum de résultats par requête
            
        Returns:
            Liste des nouvelles vidéos détectées
        """
        new_videos = []
        
        # Scraper les utilisateurs
        if usernames:
            for username in usernames:
                videos = self.scrape_user_videos(username, max_results)
                
                for video in videos:
                    video_id = video.get('id')
                    
                    # Vérifier si la vidéo est nouvelle ET n'a pas déjà été traitée
                    if video_id:
                        if video_id not in self.tracked_videos:
                            # Nouvelle vidéo jamais vue
                            self.tracked_videos[video_id] = {
                                "first_seen": datetime.now().isoformat(),
                                "username": video.get('username'),
                                "url": video.get('url'),
                                "description": video.get('description', ''),
                                "processed": False
                            }
                            new_videos.append(video)
                            logger.info(f"✨ Nouvelle vidéo détectée: {video.get('url')}")
                        elif not self.tracked_videos.get(video_id, {}).get('processed', False):
                            # Vidéo déjà trackée mais pas encore traitée (au cas où)
                            new_videos.append(video)
                            logger.info(f"🔄 Vidéo non traitée détectée: {video.get('url')}")
                        else:
                            # Vidéo déjà traitée, on l'ignore
                            logger.debug(f"⏭️  Vidéo déjà traitée, ignorée: {video.get('url')}")
                
                # Délai entre les requêtes pour éviter la surcharge
                time.sleep(2)
        
        # Scraper les hashtags
        if hashtags:
            for hashtag in hashtags:
                videos = self.scrape_hashtag_videos(hashtag, max_results)
                
                for video in videos:
                    video_id = video.get('id')
                    
                    if video_id and video_id not in self.tracked_videos:
                        self.tracked_videos[video_id] = {
                            "first_seen": datetime.now().isoformat(),
                            "username": video.get('username'),
                            "url": video.get('url'),
                            "description": video.get('description', ''),
                            "hashtag": video.get('hashtag'),
                            "processed": False
                        }
                        new_videos.append(video)
                        logger.info(f"✨ Nouvelle vidéo détectée: {video.get('url')}")
                
                # Délai entre les requêtes
                time.sleep(2)
        
        # Sauvegarder les nouvelles vidéos trackées
        if new_videos:
            self._save_tracked_videos()
        
        return new_videos
    
    def mark_video_processed(self, video_id: str):
        """Marque une vidéo comme traitée"""
        if video_id in self.tracked_videos:
            self.tracked_videos[video_id]['processed'] = True
            self._save_tracked_videos()

