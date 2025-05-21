from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote
import time
import logging
from datetime import datetime
from .base import BaseScraper

class NewsroomScraper(BaseScraper):
    """뉴스룸 스크래퍼 기본 클래스"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.articles = []
        self._setup_driver()
    
    def _setup_driver(self):
        """웹드라이버 설정"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.wait = WebDriverWait(self.driver, 20)
    
    def cleanup(self):
        """리소스 정리"""
        if self.driver:
            self.driver.quit()
            self.driver = None

class SKHynixNewsScraper(NewsroomScraper):
    """SK하이닉스 뉴스룸 스크래퍼"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://news.skhynix.co.kr"
    
    def search(self, keyword: str, num_results: int = 10, date_range: Optional[str] = None) -> List[Dict]:
        try:
            current_page = 1
            encoded_keyword = quote(keyword)
            
            while len(self.articles) < num_results:
                if current_page == 1:
                    url = f"{self.base_url}/all/"
                else:
                    url = f"{self.base_url}/all/page/{current_page}/"
                
                self.driver.get(url)
                time.sleep(3)
                
                articles = self.driver.find_elements(By.TAG_NAME, "article")
                if not articles:
                    break
                
                for article in articles:
                    if len(self.articles) >= num_results:
                        break
                    
                    try:
                        title_element = article.find_element(By.CSS_SELECTOR, "h2.tit a")
                        title = title_element.text.strip()
                        url = title_element.get_attribute("href")
                        
                        # 기사 내용 가져오기
                        content = self._get_article_content(url)
                        
                        # 날짜 정보 가져오기
                        try:
                            date_element = article.find_element(By.CSS_SELECTOR, "span.date")
                            date = date_element.text.strip()
                        except:
                            date = ""
                        
                        self.articles.append({
                            'title': title,
                            'url': url,
                            'content': content,
                            'date': date,
                            'source': 'sk_hynix'
                        })
                        
                    except Exception as e:
                        logging.error(f"기사 처리 중 오류: {str(e)}")
                        continue
                
                current_page += 1
            
            return self.articles
            
        except Exception as e:
            logging.error(f"검색 중 오류: {str(e)}")
            return []
    
    def _get_article_content(self, url: str) -> str:
        """기사 내용 추출"""
        try:
            main_window = self.driver.current_window_handle
            self.driver.execute_script(f"window.open('{url}', '_blank');")
            time.sleep(2)
            
            new_window = [handle for handle in self.driver.window_handles if handle != main_window][0]
            self.driver.switch_to.window(new_window)
            
            content_container = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.post-contents"))
            )
            
            paragraphs = content_container.find_elements(By.TAG_NAME, "p")
            content_texts = []
            
            for p in paragraphs:
                text = p.text.strip()
                if text and not text.startswith('* '):
                    content_texts.append(text)
            
            content = '\n'.join(content_texts)
            
            self.driver.close()
            self.driver.switch_to.window(main_window)
            
            return content if content else "내용 추출 실패"
            
        except Exception as e:
            logging.error(f"본문 추출 중 오류: {str(e)}")
            try:
                self.driver.switch_to.window(main_window)
            except:
                pass
            return "내용 추출 실패"

class SamsungSemiconNewsScraper(NewsroomScraper):
    """삼성반도체 뉴스룸 스크래퍼"""
    
    def __init__(self):
        super().__init__()
        self.categories = [
            {
                "name": "프레스센터",
                "url": "https://news.samsungsemiconductor.com/kr/category/%eb%89%b4%ec%8a%a4/"
            },
            {
                "name": "문화",
                "url": "https://news.samsungsemiconductor.com/kr/category/%eb%ac%b8%ed%99%94/"
            },
            {
                "name": "ESG",
                "url": "https://news.samsungsemiconductor.com/kr/category/esg/"
            }
        ]
    
    def search(self, keyword: str, num_results: int = 10, date_range: Optional[str] = None) -> List[Dict]:
        try:
            for category in self.categories:
                if len(self.articles) >= num_results:
                    break
                
                self._collect_articles_from_category(
                    category["name"],
                    category["url"],
                    keyword,
                    num_results - len(self.articles)
                )
            
            return self.articles
            
        except Exception as e:
            logging.error(f"검색 중 오류: {str(e)}")
            return []
    
    def _collect_articles_from_category(self, category_name: str, category_url: str, keyword: str, remaining_count: int):
        """카테고리별 기사 수집"""
        current_page = 1
        
        while len(self.articles) < remaining_count:
            if current_page == 1:
                page_url = category_url
            else:
                page_url = f"{category_url}page/{current_page}/"
            
            self.driver.get(page_url)
            time.sleep(2)
            
            try:
                articles = self.driver.find_elements(By.CSS_SELECTOR, "ul.article_list > li.article_item")
                if not articles:
                    break
                
                for article in articles:
                    if len(self.articles) >= remaining_count:
                        break
                    
                    try:
                        title = article.find_element(By.CSS_SELECTOR, "p.title").text.strip()
                        
                        # 키워드 필터링
                        if keyword.lower() not in title.lower():
                            continue
                        
                        link_element = article.find_element(By.TAG_NAME, "a")
                        url = link_element.get_attribute("href")
                        date = article.find_element(By.CSS_SELECTOR, "span.date").text.strip()
                        
                        try:
                            category = article.find_element(By.CSS_SELECTOR, "span.category").text.strip()
                        except:
                            category = ""
                        
                        try:
                            desc = article.find_element(By.CSS_SELECTOR, "p.desc").text.strip()
                        except:
                            desc = ""
                        
                        content = self._get_article_content(url)
                        
                        self.articles.append({
                            'title': title,
                            'url': url,
                            'content': content,
                            'date': date,
                            'category': category,
                            'description': desc,
                            'source': 'samsung_semiconductor'
                        })
                        
                    except Exception as e:
                        logging.error(f"기사 처리 중 오류: {str(e)}")
                        continue
                
                current_page += 1
                
            except Exception as e:
                logging.error(f"페이지 처리 중 오류: {str(e)}")
                break
    
    def _get_article_content(self, url: str) -> str:
        """기사 내용 추출"""
        try:
            self.driver.get(url)
            time.sleep(2)
            
            content_container = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.content_view > div.content_desc"))
            )
            
            paragraphs = content_container.find_elements(By.TAG_NAME, "p")
            content_texts = [p.text.strip() for p in paragraphs if p.text.strip()]
            
            return '\n'.join(content_texts) if content_texts else "내용 추출 실패"
            
        except Exception as e:
            logging.error(f"본문 추출 중 오류: {str(e)}")
            return "내용 추출 실패" 