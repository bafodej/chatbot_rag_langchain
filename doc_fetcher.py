"""
Module pour recuperer la documentation technique recente
Technologies: Python, LangChain, ChromaDB, Data Analysis, ML, DL, Azure, Web Scraping
"""
import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader
import time

class DocumentationFetcher:
    """Recupere la documentation de differentes sources"""

    def __init__(self):
        self.documentation_sources = {
            "python": [
                "https://docs.python.org/3/tutorial/index.html",
                "https://docs.python.org/3/library/index.html",
            ],
            "langchain": [
                "https://python.langchain.com/docs/get_started/introduction",
                "https://python.langchain.com/docs/tutorials/",
            ],
            "chromadb": [
                "https://docs.trychroma.com/getting-started",
                "https://docs.trychroma.com/guides",
            ],
            "data_analysis": [
                "https://pandas.pydata.org/docs/getting_started/index.html",
                "https://numpy.org/doc/stable/user/index.html",
            ],
            "machine_learning": [
                "https://scikit-learn.org/stable/tutorial/index.html",
                "https://scikit-learn.org/stable/user_guide.html",
            ],
            "deep_learning": [
                "https://pytorch.org/tutorials/",
                "https://www.tensorflow.org/tutorials",
            ],
            "azure": [
                "https://learn.microsoft.com/en-us/azure/",
                "https://learn.microsoft.com/en-us/azure/machine-learning/",
            ],
            "scraping": [
                "https://docs.python-requests.org/en/latest/",
                "https://beautiful-soup-4.readthedocs.io/en/latest/",
                "https://selenium-python.readthedocs.io/",
            ]
        }

    def fetch_documentation(self, topics=None, max_pages_per_topic=2):
        """
        Recupere la documentation pour les topics specifies

        Args:
            topics: Liste des topics (None = tous)
            max_pages_per_topic: Nombre max de pages par topic

        Returns:
            Liste de Documents LangChain
        """
        if topics is None:
            topics = list(self.documentation_sources.keys())

        all_docs = []

        for topic in topics:
            if topic not in self.documentation_sources:
                print(f"Topic '{topic}' non reconnu, ignore")
                continue

            print(f"\nRecuperation documentation: {topic.upper()}")
            urls = self.documentation_sources[topic][:max_pages_per_topic]

            for url in urls:
                try:
                    print(f"  Chargement: {url}")
                    loader = WebBaseLoader(
                        web_paths=[url],
                        header_template={
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                        }
                    )
                    docs = loader.load()

                    for doc in docs:
                        # Ajouter le topic comme metadata
                        doc.metadata["topic"] = topic
                        doc.metadata["source_url"] = url
                        all_docs.append(doc)

                    print(f"    ✓ {len(docs)} document(s) recupere(s)")
                    time.sleep(1)  # Rate limiting

                except Exception as e:
                    print(f"    ✗ Erreur: {e}")
                    continue

        print(f"\nTotal: {len(all_docs)} documents recuperes")
        return all_docs


def fetch_tech_docs(topics=None, max_pages=2):
    """
    Fonction utilitaire pour recuperer la documentation

    Args:
        topics: Liste des topics ('python', 'langchain', 'chromadb', etc.)
        max_pages: Nombre max de pages par topic

    Returns:
        Liste de Documents LangChain
    """
    fetcher = DocumentationFetcher()
    return fetcher.fetch_documentation(topics=topics, max_pages_per_topic=max_pages)


# Topics disponibles
AVAILABLE_TOPICS = [
    "python",
    "langchain",
    "chromadb",
    "data_analysis",
    "machine_learning",
    "deep_learning",
    "azure",
    "scraping"
]
