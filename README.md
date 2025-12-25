# Chatbot RAG - Offres d'emploi Indeed France

Application de chatbot RAG (Retrieval-Augmented Generation) pour analyser les offres d'emploi Indeed en France.

## Caracteristiques

- **Scraping Indeed** avec Selenium (contourne les protections JavaScript)
- **RAG Pipeline** avec LangChain et ChromaDB
- **IA locale gratuite** avec Ollama (llama3.2)
- **Interface Streamlit** interactive
- **Recherche flexible** : Data Analyst, Python, Alternance, etc.
- **Acces aux liens** pour postuler directement

## Technologies

- **Python 3.12**
- **Selenium** - Web scraping
- **LangChain** - Framework RAG
- **Ollama** - Modele IA local (gratuit)
- **ChromaDB** - Base vectorielle
- **Streamlit** - Interface utilisateur
- **BeautifulSoup** - Parsing HTML

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

## Utilisation

### Tester le scraping

```bash
python test_scraping.py
```

Cela va scraper Indeed pour 3 types de recherches (Data Analyst, Python, Alternance) et afficher les resultats.

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

## Fonctionnement

1. **Scraping** : Selenium charge Indeed avec JavaScript et extrait les offres
2. **Chunking** : Les offres sont decoupees en morceaux de 1000 caracteres
3. **Vectorisation** : Ollama cree des embeddings pour chaque chunk
4. **Stockage** : ChromaDB sauvegarde les vecteurs localement
5. **Requete** : L'utilisateur pose une question
6. **Recherche** : ChromaDB trouve les chunks pertinents
7. **Reponse** : Ollama genere une reponse basee sur le contexte

## Exemples de questions

- "Combien d'offres data analyst ?"
- "Quelles offres a Lille ?"
- "Top 5 entreprises qui recrutent ?"
- "Quels sont les salaires proposes ?"
- "Quelles competences sont demandees ?"

## Structure du projet

```
chatbot/
├── app.py                  # Application Streamlit
├── rag_chatbot.ipynb       # Notebook de test
├── test_scraping.py        # Script de test scraping
├── requirements.txt        # Dependances Python
├── .env                    # Configuration (optionnel avec Ollama)
├── .gitignore             # Fichiers ignores par Git
├── chroma_db/             # Base vectorielle (generee)
└── venv/                  # Environnement virtuel (ignore)
```

## Limitations

- **Scraping lent** : Selenium prend ~5 secondes par recherche
- **Donnees limitees** : Indeed affiche max 16 offres par page
- **Pas d'API officielle** : Indeed a ferme son API publique en 2021
- **Modele local** : Reponses parfois moins precises que GPT-4

## Solutions alternatives

Si le scraping Indeed est bloque :
- **API France Travail** (ex-Pole Emploi) - gratuite et officielle
- **API Adzuna** - 5000 requetes/mois gratuites
- **Autres sites** - Welcome to the Jungle, LinkedIn

## Contribution

Ameliorations possibles :
- [ ] Support multi-pages Indeed
- [ ] Extraction amelioree (entreprise, lieu, salaire)
- [ ] Cache des resultats
- [ ] Export CSV des offres
- [ ] Filtres avances (salaire, contrat, etc.)

## Licence

Projet educatif - Libre d'utilisation

## Auteur

Bafode Jaiteh - https://github.com/bafodej
