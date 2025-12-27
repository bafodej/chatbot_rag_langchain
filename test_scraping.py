"""
Script de test pour valider l'API France Travail
Remplace le scraping Indeed par l'API officielle (100% gratuite)
"""
from france_travail_api import fetch_france_travail_jobs

def test_api(query="", departement=""):
    """
    Test de l'API France Travail

    Args:
        query: Terme de recherche (ex: 'data analyst', 'python', 'alternance')
        departement: Code departement optionnel (ex: '75' pour Paris, '59' pour Nord)
    """

    print(f"Recherche: {query}")
    if departement:
        print(f"Departement: {departement}")
    print()

    try:
        # Recuperer les offres via l'API
        docs = fetch_france_travail_jobs(query=query, departement=departement, max_results=10)

        print(f"Offres trouvees: {len(docs)}\n")

        if docs:
            print("Premieres 3 offres:\n")
            for i, doc in enumerate(docs[:3]):
                print(f"Offre {i+1}:")
                print(doc.page_content)
                print()

            return len(docs)
        else:
            print("Aucune offre trouvee pour cette recherche")
            return 0

    except ValueError as e:
        print(f"Erreur de configuration: {e}")
        print("\nPour utiliser l'API France Travail:")
        print("1. Allez sur https://francetravail.io")
        print("2. Creez un compte")
        print("3. Creez une application dans 'Espace Partenaire'")
        print("4. Copiez le fichier .env.example en .env")
        print("5. Ajoutez vos credentials (CLIENT_ID et CLIENT_SECRET) dans .env")
        return 0

    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
        return 0


if __name__ == "__main__":
    # Test avec differentes requetes
    print("="*60)
    print("Test 1: Offres Data Analyst en France")
    print("="*60)
    test_api("data analyst")

    print("\n" + "="*60)
    print("Test 2: Offres developpeur Python en France")
    print("="*60)
    test_api("python")

    print("\n" + "="*60)
    print("Test 3: Offres alternance en France")
    print("="*60)
    test_api("alternance")

    print("\n" + "="*60)
    print("Test 4: Offres alternance a Paris (75)")
    print("="*60)
    test_api("alternance", departement="75")
