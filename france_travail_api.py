"""
Module pour interagir avec l'API France Travail (ex-Pole Emploi)
Documentation: https://francetravail.io/data/api/offres-emploi
"""
import os
import requests
from dotenv import load_dotenv
from langchain_core.documents import Document

# Charger les variables d'environnement
load_dotenv()

class FranceTravailAPI:
    """Client pour l'API Offres d'emploi France Travail"""

    def __init__(self):
        self.client_id = os.getenv("FRANCE_TRAVAIL_CLIENT_ID")
        self.client_secret = os.getenv("FRANCE_TRAVAIL_CLIENT_SECRET")
        self.token_url = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire"
        self.api_base_url = "https://api.francetravail.io/partenaire/offresdemploi/v2"
        self.access_token = None

        if not self.client_id or not self.client_secret:
            raise ValueError(
                "Credentials manquants. Veuillez configurer FRANCE_TRAVAIL_CLIENT_ID "
                "et FRANCE_TRAVAIL_CLIENT_SECRET dans le fichier .env"
            )

    def get_access_token(self):
        """Obtenir un token d'acces OAuth2"""

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "api_offresdemploiv2 o2dsoffre"
        }

        try:
            response = requests.post(self.token_url, headers=headers, data=data)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data["access_token"]
            return self.access_token
        except Exception as e:
            raise Exception(f"Erreur lors de l'obtention du token: {e}")

    def search_jobs(self, motsCles="", departement="", commune="", range_limit=150):
        """
        Rechercher des offres d'emploi

        Args:
            motsCles: Mots-cles de recherche (ex: 'python', 'data analyst', 'alternance')
            departement: Code departement (ex: '75' pour Paris, '59' pour Nord)
            commune: Code INSEE de la commune
            range_limit: Nombre maximum de resultats (max 150 par requete)

        Returns:
            Liste de Documents LangChain
        """

        if not self.access_token:
            self.get_access_token()

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        params = {
            "motsCles": motsCles,
            "range": f"0-{range_limit}"
        }

        if departement:
            params["departement"] = departement
        if commune:
            params["commune"] = commune

        url = f"{self.api_base_url}/offres/search"

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            # Convertir les offres en Documents
            documents = []
            offres = data.get("resultats", [])

            for offre in offres:
                # Extraire les informations
                titre = offre.get("intitule", "N/A")
                entreprise = offre.get("entreprise", {}).get("nom", "N/A")
                lieu_travail = offre.get("lieuTravail", {})
                ville = lieu_travail.get("libelle", "N/A")
                code_postal = lieu_travail.get("codePostal", "")

                salaire_libelle = offre.get("salaire", {}).get("libelle", "Non specifie")
                description = offre.get("description", "")

                # Lien pour postuler
                offre_id = offre.get("id", "")
                lien = f"https://candidat.francetravail.fr/offres/recherche/detail/{offre_id}"

                # Type de contrat
                type_contrat = offre.get("typeContrat", "N/A")

                # Formatage du contenu
                content = f"""Titre: {titre}
Entreprise: {entreprise}
Lieu: {ville} ({code_postal})
Type de contrat: {type_contrat}
Salaire: {salaire_libelle}
Description: {description[:500]}...
Lien: {lien}"""

                metadata = {
                    "source": "France Travail API",
                    "title": titre,
                    "link": lien,
                    "location": ville,
                    "company": entreprise
                }

                documents.append(Document(page_content=content, metadata=metadata))

            return documents

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                # Token expire, renouveler et reessayer
                self.get_access_token()
                return self.search_jobs(motsCles, departement, commune, range_limit)
            else:
                raise Exception(f"Erreur HTTP {e.response.status_code}: {e}")
        except Exception as e:
            raise Exception(f"Erreur lors de la recherche: {e}")


def fetch_france_travail_jobs(query="", departement="", max_results=150):
    """
    Fonction utilitaire pour recuperer des offres d'emploi

    Args:
        query: Termes de recherche
        departement: Code departement (optionnel)
        max_results: Nombre max de resultats

    Returns:
        Liste de Documents LangChain
    """
    api = FranceTravailAPI()
    return api.search_jobs(motsCles=query, departement=departement, range_limit=max_results)
