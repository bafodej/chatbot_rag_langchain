"""
Script de test pour valider le scraping Indeed des offres d'emploi en France
Supporte plusieurs termes de recherche : data analyst, python, IA, alternance, etc.
Le filtrage par localisation sera effectue par le chatbot dans les requetes
"""
from langchain_community.document_loaders import WebBaseLoader
from bs4 import BeautifulSoup
import requests

def test_scraping(query=""):
    """
    Test du scraping des offres d'emploi Indeed France

    Args:
        query: Terme de recherche (ex: 'data analyst', 'python', 'alternance', ou '' pour toutes les offres)
    """

    # Construction de l'URL - TOUTE LA FRANCE (pas de filtre localisation)
    base_url = "https://fr.indeed.com/emplois"
    url = f"{base_url}?q={query}"

    print(f"Scraping: {url}\n")

    # WebBaseLoader avec headers personnalises pour eviter le blocage
    loader = WebBaseLoader(
        web_paths=[url],
        header_template={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    )

    try:
        # Charger les documents
        docs = loader.load()

        print(f"Documents scraped: {len(docs)}")

        if len(docs) > 0:
            print(f"\nFirst document preview:")
            print(f"Length: {len(docs[0].page_content)} characters")
            print(f"Content (first 500 chars):\n{docs[0].page_content[:500]}\n")

            # Extraire les details des offres avec BeautifulSoup
            response = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            soup = BeautifulSoup(response.content, 'html.parser')

            # Trouver les cartes d'offres
            jobs = soup.find_all('div', class_='job_seen_beacon')
            print(f"\nJob cards found: {len(jobs)}")

            if len(jobs) > 0:
                print("\nFirst 3 jobs extracted:")
                for i, job in enumerate(jobs[:3]):
                    title = job.find('h2', class_='jobTitle')
                    company = job.find('span', class_='companyName')
                    location = job.find('div', class_='companyLocation')
                    salary = job.find('div', class_='salary-snippet')
                    snippet = job.find('div', class_='job-snippet')

                    print(f"\nJob {i+1}:")
                    print(f"  Title: {title.get_text(strip=True) if title else 'N/A'}")
                    print(f"  Company: {company.get_text(strip=True) if company else 'N/A'}")
                    print(f"  Location: {location.get_text(strip=True) if location else 'N/A'}")
                    print(f"  Salary: {salary.get_text(strip=True) if salary else 'N/A'}")
                    if snippet:
                        print(f"  Snippet: {snippet.get_text(strip=True)[:100]}...")

                return len(jobs)
            else:
                print("WARNING: No job cards found - check HTML structure")
                return 0
        else:
            print("ERROR: No documents loaded")
            return 0

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 0

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
