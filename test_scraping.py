"""
Script de test pour valider le scraping Indeed avec Selenium
Contourne les protections JavaScript d'Indeed
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def test_scraping(query=""):
    """
    Test du scraping des offres d'emploi Indeed France avec Selenium

    Args:
        query: Terme de recherche (ex: 'data analyst', 'python', 'alternance')
    """

    # Construction de l'URL
    base_url = "https://fr.indeed.com/emplois"
    url = f"{base_url}?q={query}"

    print(f"Scraping avec Selenium: {url}\n")

    # Configuration Chrome en mode headless (sans interface)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")

    driver = None
    try:
        # Initialiser le driver Chrome
        print("Initialisation du navigateur Chrome...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Charger la page
        print("Chargement de la page Indeed...")
        driver.get(url)

        # Attendre que la page charge (JavaScript)
        time.sleep(5)

        # Recuperer le HTML
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extraire les offres
        jobs = soup.find_all('div', class_='job_seen_beacon')
        print(f"Offres trouvees: {len(jobs)}\n")

        if len(jobs) > 0:
            print("Premieres 3 offres:\n")
            for i, job in enumerate(jobs[:3]):
                # Extraire les details
                title_elem = job.find('h2', class_='jobTitle')
                company_elem = job.find('span', class_='companyName')
                location_elem = job.find('div', class_='companyLocation')
                salary_elem = job.find('div', class_='salary-snippet')
                snippet_elem = job.find('div', class_='job-snippet')

                # Extraire le lien
                link_elem = job.find('a', class_='jcs-JobTitle')
                job_link = f"https://fr.indeed.com{link_elem['href']}" if link_elem and 'href' in link_elem.attrs else 'N/A'

                print(f"Offre {i+1}:")
                print(f"  Titre: {title_elem.get_text(strip=True) if title_elem else 'N/A'}")
                print(f"  Entreprise: {company_elem.get_text(strip=True) if company_elem else 'N/A'}")
                print(f"  Lieu: {location_elem.get_text(strip=True) if location_elem else 'N/A'}")
                print(f"  Salaire: {salary_elem.get_text(strip=True) if salary_elem else 'N/A'}")
                print(f"  Lien: {job_link}")
                if snippet_elem:
                    print(f"  Description: {snippet_elem.get_text(strip=True)[:100]}...")
                print()

            return len(jobs)
        else:
            print("ATTENTION: Aucune offre trouvee")
            print(f"Contenu de la page (500 premiers caracteres):\n{page_source[:500]}")
            return 0

    except Exception as e:
        print(f"ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return 0

    finally:
        # Fermer le navigateur
        if driver:
            print("Fermeture du navigateur...")
            driver.quit()

if __name__ == "__main__":
    # Test avec differentes requetes
    print("="*60)
    print("TEST 1: Offres Data Analyst en France")
    print("="*60)
    test_scraping("data analyst")

    print("\n" + "="*60)
    print("TEST 2: Offres developpeur Python en France")
    print("="*60)
    test_scraping("python")

    print("\n" + "="*60)
    print("TEST 3: Offres alternance en France")
    print("="*60)
    test_scraping("alternance")
