"""
Script de test pour valider la recuperation de documentation
Technologies: Python, LangChain, ChromaDB, ML, DL, Azure, Scraping, Data Analysis
"""
from doc_fetcher import fetch_tech_docs, AVAILABLE_TOPICS

def test_fetch(topics, max_pages=1):
    """
    Test de la recuperation de documentation

    Args:
        topics: Liste de topics a tester
        max_pages: Nombre de pages par topic
    """
    print(f"Test recuperation documentation: {', '.join(topics)}")
    print(f"Pages par topic: {max_pages}\n")

    try:
        docs = fetch_tech_docs(topics=topics, max_pages=max_pages)

        if docs:
            print(f"\n{'='*60}")
            print(f"RESULTAT: {len(docs)} documents recuperes")
            print(f"{'='*60}\n")

            # Afficher un apercu de chaque topic
            for topic in topics:
                topic_docs = [d for d in docs if d.metadata.get("topic") == topic]
                if topic_docs:
                    print(f"\n--- {topic.upper()} ({len(topic_docs)} docs) ---")
                    sample = topic_docs[0]
                    print(f"Source: {sample.metadata.get('source_url', 'N/A')}")
                    print(f"Contenu (200 premiers caracteres):")
                    print(f"{sample.page_content[:200]}...\n")

            return len(docs)
        else:
            print("Aucune documentation recuperee")
            return 0

    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
        return 0


if __name__ == "__main__":
    print("="*60)
    print("TEST RECUPERATION DOCUMENTATION TECHNIQUE")
    print("="*60)
    print(f"\nTopics disponibles: {', '.join(AVAILABLE_TOPICS)}\n")

    print("="*60)
    print("Test 1: Python + LangChain")
    print("="*60)
    test_fetch(["python", "langchain"], max_pages=1)

    print("\n" + "="*60)
    print("Test 2: Machine Learning + Deep Learning")
    print("="*60)
    test_fetch(["machine_learning", "deep_learning"], max_pages=1)

    print("\n" + "="*60)
    print("Test 3: Data Analysis + ChromaDB")
    print("="*60)
    test_fetch(["data_analysis", "chromadb"], max_pages=1)

    print("\n" + "="*60)
    print("Test 4: Azure + Web Scraping")
    print("="*60)
    test_fetch(["azure", "scraping"], max_pages=1)

    print("\n" + "="*60)
    print("TOUS LES TESTS TERMINES")
    print("="*60)
