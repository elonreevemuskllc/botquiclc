"""
Module de scraping TikTok avancé utilisant Selenium/Playwright
"""
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TikTokScraperAdvanced:
    """Classe avancée pour scraper TikTok avec Selenium"""
    
    def __init__(self, username: str = None, check_interval: int = 60, headless: bool = True):
        self.username = username
        self.check_interval = check_interval
        self.headless = headless
        self.driver = None
        self.tracked_videos = self._load_tracked_videos()
    
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
    
    def _init_driver(self):
        """Initialise le driver Selenium"""
        if self.driver:
            return
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("Driver Selenium initialisé")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du driver: {e}")
            raise
    
    def _close_driver(self):
        """Ferme le driver Selenium"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("Driver Selenium fermé")
    
    def get_user_videos(self, username: str) -> List[Dict]:
        """
        Récupère les vidéos d'un utilisateur TikTok en utilisant Selenium
        """
        self._init_driver()
        videos = []
        
        try:
            url = f"https://www.tiktok.com/@{username}"
            logger.info(f"Chargement de la page: {url}")
            
            self.driver.get(url)
            time.sleep(5)  # Attendre le chargement de la page
            
            # Attendre que les vidéos se chargent
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-e2e='user-post-item']"))
                )
            except TimeoutException:
                logger.warning("Timeout: Les vidéos n'ont pas été trouvées")
                return videos
            
            # Scroller pour charger plus de vidéos
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            
            # Trouver tous les éléments de vidéo
            video_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-e2e='user-post-item']")
            
            for element in video_elements:
                try:
                    # Extraire l'URL de la vidéo
                    link_element = element.find_element(By.TAG_NAME, "a")
                    video_url = link_element.get_attribute("href")
                    
                    if video_url:
                        # Extraire l'ID de la vidéo depuis l'URL
                        video_id = video_url.split('/')[-1] if '/' in video_url else video_url
                        
                        video_data = {
                            "id": video_id,
                            "url": video_url,
                            "username": username,
                            "timestamp": datetime.now().isoformat(),
                            "description": ""
                        }
                        
                        # Essayer d'extraire la description
                        try:
                            desc_element = element.find_element(By.CSS_SELECTOR, "[data-e2e='user-post-item-desc']")
                            video_data["description"] = desc_element.text
                        except NoSuchElementException:
                            pass
                        
                        videos.append(video_data)
                        
                except Exception as e:
                    logger.warning(f"Erreur lors de l'extraction d'une vidéo: {e}")
                    continue
            
            logger.info(f"✅ {len(videos)} vidéo(s) trouvée(s) pour @{username}")
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des vidéos: {e}")
        
        return videos
    
    def check_new_videos(self, usernames: List[str]) -> List[Dict]:
        """Vérifie les nouvelles vidéos pour une liste d'utilisateurs"""
        new_videos = []
        
        try:
            for username in usernames:
                logger.info(f"🔍 Vérification des vidéos de @{username}")
                videos = self.get_user_videos(username)
                
                for video in videos:
                    video_id = video.get('id')
                    
                    # Vérifier si la vidéo n'a pas déjà été trackée
                    if video_id not in self.tracked_videos:
                        self.tracked_videos[video_id] = {
                            "first_seen": datetime.now().isoformat(),
                            "username": username,
                            "url": video.get('url'),
                            "description": video.get('description', ''),
                            "processed": False
                        }
                        new_videos.append(video)
                        logger.info(f"✨ Nouvelle vidéo détectée: {video.get('url')}")
                
                # Délai entre les utilisateurs
                time.sleep(3)
        
        finally:
            # Sauvegarder les nouvelles vidéos trackées
            if new_videos:
                self._save_tracked_videos()
        
        return new_videos
    
    def mark_video_processed(self, video_id: str):
        """Marque une vidéo comme traitée"""
        if video_id in self.tracked_videos:
            self.tracked_videos[video_id]['processed'] = True
            self._save_tracked_videos()
    
    def __del__(self):
        """Nettoyage à la destruction de l'objet"""
        self._close_driver()

