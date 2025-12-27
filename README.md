# Chatbot RAG - Offres d'emploi France Travail

Application de chatbot RAG (Retrieval-Augmented Generation) pour analyser les offres d'emploi officielles France Travail (ex-Pôle Emploi) en France.

## Caracteristiques

- **API France Travail** officielle et gratuite (remplace le scraping Indeed bloqué par Cloudflare)
- **RAG Pipeline** avec LangChain et ChromaDB
- **IA locale gratuite** avec Ollama (llama3.2)
- **Interface Streamlit** interactive
- **Recherche flexible** : Alternance, Data Analyst, Python, Developpeur, etc.
- **Filtre par departement** : Paris (75), Nord (59), Rhone (69), etc.
- **Acces aux liens** pour postuler directement sur France Travail
- **100% gratuit** et open-source

## Technologies

- **Python 3.12**
- **France Travail API** - API officielle offres d'emploi
- **LangChain** - Framework RAG
- **Ollama** - Modele IA local (gratuit)
- **ChromaDB** - Base vectorielle
- **Streamlit** - Interface utilisateur
- **Requests** - HTTP client

## Installation

### 1. Cloner le repository

```bash
git clone https://github.com/bafodej/chatbot_rag_langchain.git
cd chatbot_rag_langchain
```

### 2. Creer un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate  # Sur Mac/Linux
# venv\Scripts\activate  # Sur Windows
```

### 3. Installer les dependances

```bash
pip install -r requirements.txt
```

### 4. Installer Ollama

```bash
brew install ollama  # Sur Mac
brew services start ollama
ollama pull llama3.2
```

Pour les autres systemes : https://ollama.com/download

### 5. Configurer l'API France Travail

**IMPORTANT** : Vous devez obtenir des credentials API pour utiliser l'application.

#### Etape par etape :

1. **Creer un compte** sur https://francetravail.io

2. **Creer une application** :
   - Connectez-vous a votre espace partenaire
   - Allez dans "Mes applications"
   - Cliquez sur "Ajouter une application"
   - Selectionnez l'API "Offres d'emploi v2"
   - Remplissez les informations de votre application

3. **Recuperer les credentials** :
   - Une fois l'application creee, vous obtiendrez :
     - `Client ID` (identifiant client)
     - `Client Secret` (cle secrete)

4. **Configurer le fichier .env** :
   ```bash
   cp .env.example .env
   ```

5. **Editer le fichier .env** et ajouter vos credentials :
   ```
   FRANCE_TRAVAIL_CLIENT_ID=votre_client_id_ici
   FRANCE_TRAVAIL_CLIENT_SECRET=votre_client_secret_ici
   ```

## Utilisation

### Tester l'API

```bash
python test_scraping.py
```

Cela va rechercher des offres pour 4 types de recherches (Data Analyst, Python, Alternance, Alternance a Paris) et afficher les resultats.

### Lancer le notebook

```bash
jupyter notebook rag_chatbot.ipynb
```

Executez les cellules pour tester le pipeline RAG complet.

### Lancer l'application Streamlit

```bash
streamlit run app.py
```

L'application s'ouvre sur http://localhost:8501

**Dans l'interface** :
1. Entrez votre terme de recherche (ex: "alternance", "python", "developpeur")
2. (Optionnel) Entrez un code departement (ex: "75" pour Paris)
3. Cliquez sur "Rechercher offres"
4. Attendez que le RAG soit pret
5. Posez vos questions dans le chat

## Fonctionnement

1. **API Call** : L'application interroge l'API France Travail avec vos criteres
2. **Chunking** : Les offres sont decoupees en morceaux de 1000 caracteres
3. **Vectorisation** : Ollama cree des embeddings pour chaque chunk
4. **Stockage** : ChromaDB sauvegarde les vecteurs localement
5. **Requete** : L'utilisateur pose une question
6. **Recherche** : ChromaDB trouve les chunks pertinents
7. **Reponse** : Ollama genere une reponse basee sur le contexte

## Exemples de questions

- "Combien d'offres d'alternance ?"
- "Quelles offres a Paris ?"
- "Top 5 entreprises qui recrutent ?"
- "Quels sont les salaires proposes ?"
- "Quels types de contrats sont proposes ?"
- "Quelles competences sont demandees ?"

## Structure du projet

```
chatbot/
├── app.py                      # Application Streamlit
├── france_travail_api.py       # Module API France Travail
├── rag_chatbot.ipynb           # Notebook de test
├── test_scraping.py            # Script de test API
├── requirements.txt            # Dependances Python
├── .env.example                # Template configuration
├── .env                        # Configuration (a creer avec vos credentials)
├── .gitignore                  # Fichiers ignores par Git
├── chroma_db/                  # Base vectorielle (generee)
└── venv/                       # Environnement virtuel (ignore)
```

## Codes departement France

Quelques exemples de codes departement :
- **75** : Paris
- **59** : Nord (Lille)
- **69** : Rhone (Lyon)
- **13** : Bouches-du-Rhone (Marseille)
- **31** : Haute-Garonne (Toulouse)
- **33** : Gironde (Bordeaux)
- **44** : Loire-Atlantique (Nantes)
- **67** : Bas-Rhin (Strasbourg)

Liste complete : https://www.data.gouv.fr/fr/datasets/departements-de-france/

## Avantages vs Indeed

| Critere | France Travail API | Indeed (scraping) |
|---------|-------------------|-------------------|
| **Gratuit** | ✅ Oui | ✅ Oui |
| **Legal** | ✅ API officielle | ⚠️ Scraping = zone grise |
| **Fiable** | ✅ Stable | ❌ Bloque par Cloudflare |
| **Donnees** | ✅ Completes | ⚠️ Limitees |
| **Maintenance** | ✅ Aucune | ❌ Casse regulierement |
| **Rapidite** | ✅ Rapide (API) | ❌ Lent (Selenium) |
| **Offres alternance** | ✅ Excellent | ⚠️ Variable |

## Limitations

- **Limite API** : 10 requetes/seconde (largement suffisant)
- **Max resultats** : 150 offres par requete API
- **Modele local** : Reponses parfois moins precises que GPT-4
- **Credentials requis** : Necessite creation compte France Travail

## Contribution

Ameliorations possibles :
- [ ] Support multi-pages API (pagination)
- [ ] Cache des resultats
- [ ] Export CSV des offres
- [ ] Filtres avances (salaire, contrat, experience)
- [ ] Integration d'autres APIs (Adzuna, etc.)
- [ ] Mode hors-ligne avec cache

## Ressources

- **API France Travail** : https://francetravail.io
- **Documentation API** : https://francetravail.io/data/api/offres-emploi
- **Ollama** : https://ollama.com
- **LangChain** : https://langchain.com

## Licence

Projet educatif - Libre d'utilisation

## Auteur

Bafode Jaiteh - https://github.com/bafodej

---

**Note** : Ce projet utilisait initialement le scraping Indeed avec Selenium, mais Indeed a bloque l'acces avec Cloudflare. L'API France Travail est une solution 100% legale, gratuite et plus fiable.
