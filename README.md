# 🤖 Assistant Technique IA - Chatbot RAG

Assistant technique intelligent utilisant RAG (Retrieval-Augmented Generation) pour répondre à vos questions sur Python, Machine Learning, Deep Learning, Azure, LangChain, ChromaDB, Web Scraping et Data Analysis.

## 🎯 Caracteristiques

- **8 domaines techniques** : Python, LangChain, ChromaDB, Data Analysis, ML, DL, Azure, Web Scraping
- **Documentation officielle** recuperee automatiquement depuis les sources officielles
- **RAG Pipeline** avec LangChain et ChromaDB pour reponses precises
- **IA locale gratuite** avec Ollama (llama3.2)
- **Interface interactive** avec Streamlit
- **Recherche semantique** dans la documentation
- **Exemples de code** dans les reponses
- **100% gratuit** et open-source

## 🚀 Technologies

- **Python 3.12**
- **LangChain** - Framework RAG
- **Ollama** - Modele IA local (gratuit)
- **ChromaDB** - Base vectorielle
- **Streamlit** - Interface utilisateur
- **BeautifulSoup** - Parsing HTML
- **Requests** - HTTP client

## 📚 Topics disponibles

1. **Python** - Tutoriels et librairie standard
2. **LangChain** - Framework RAG et agents IA
3. **ChromaDB** - Base de donnees vectorielle
4. **Data Analysis** - Pandas, NumPy
5. **Machine Learning** - scikit-learn
6. **Deep Learning** - PyTorch, TensorFlow
7. **Azure** - Cloud Microsoft, Azure ML
8. **Web Scraping** - Requests, BeautifulSoup, Selenium

## 🛠️ Installation

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

## 📖 Utilisation

### Tester la recuperation de documentation

```bash
python test_doc_fetch.py
```

Cela va tester la recuperation de documentation pour differents topics.

### Lancer l'application Streamlit

```bash
streamlit run app.py
```

L'application s'ouvre sur http://localhost:8501

### Dans l'interface :

1. **Selectionnez les topics** de documentation dans la sidebar (ex: python, machine_learning)
2. **Choisissez le nombre de pages** par topic (1-5)
3. **Cliquez sur "Charger Documentation"**
4. **Attendez** que le RAG soit pret
5. **Posez vos questions** dans le chat

## 💬 Exemples de questions

### Python
- Comment utiliser les decorateurs en Python ?
- Quelle est la difference entre list et tuple ?
- Comment gerer les exceptions en Python ?

### Machine Learning
- Comment preparer des donnees pour un modele ML ?
- Explique-moi le RandomForest
- Comment faire de la validation croisee ?

### Deep Learning
- Comment creer un reseau de neurones avec PyTorch ?
- Qu'est-ce que le backpropagation ?
- Comment eviter l'overfitting ?

### LangChain
- Comment creer une chaine RAG avec LangChain ?
- Qu'est-ce qu'un retriever ?
- Comment utiliser les agents LangChain ?

### Azure
- Comment deployer un modele ML sur Azure ?
- Qu'est-ce qu'Azure Machine Learning ?
- Comment utiliser Azure pour le traitement de donnees ?

### Data Analysis
- Comment utiliser Pandas pour analyser des donnees ?
- Comment visualiser des donnees avec Matplotlib ?
- Comment nettoyer des donnees manquantes ?

### Web Scraping
- Comment scraper un site web avec BeautifulSoup ?
- Quelle est la difference entre Requests et Selenium ?
- Comment respecter robots.txt ?

### ChromaDB
- Comment creer une collection dans ChromaDB ?
- Comment faire une recherche semantique ?
- Comment persister les donnees ?

## 🔧 Fonctionnement technique

1. **Recuperation** : WebBaseLoader recupere la documentation depuis les sources officielles
2. **Chunking** : Les documents sont decoupes en morceaux de 1500 caracteres (overlap 300)
3. **Vectorisation** : Ollama cree des embeddings pour chaque chunk
4. **Stockage** : ChromaDB sauvegarde les vecteurs localement
5. **Requete** : L'utilisateur pose une question
6. **Recherche** : ChromaDB trouve les 8 chunks les plus pertinents
7. **Reponse** : Ollama genere une reponse basee sur le contexte

## 📁 Structure du projet

```
chatbot/
├── app.py                      # Application Streamlit
├── doc_fetcher.py              # Module recuperation documentation
├── test_doc_fetch.py           # Script de test
├── rag_chatbot.ipynb           # Notebook de test
├── requirements.txt            # Dependances Python
├── .env                        # Configuration (optionnel)
├── .gitignore                  # Fichiers ignores par Git
├── chroma_db/                  # Base vectorielle (generee)
└── venv/                       # Environnement virtuel (ignore)
```

## 🌐 Sources de documentation

| Topic | Sources officielles |
|-------|-------------------|
| **Python** | https://docs.python.org |
| **LangChain** | https://python.langchain.com/docs |
| **ChromaDB** | https://docs.trychroma.com |
| **Data Analysis** | https://pandas.pydata.org, https://numpy.org |
| **ML** | https://scikit-learn.org |
| **DL** | https://pytorch.org, https://tensorflow.org |
| **Azure** | https://learn.microsoft.com/azure |
| **Scraping** | https://docs.python-requests.org, https://beautiful-soup-4.readthedocs.io |

## ⚙️ Configuration avancee

### Personnaliser les sources

Editez `doc_fetcher.py` pour ajouter/modifier les URLs de documentation :

```python
self.documentation_sources = {
    "python": [
        "https://docs.python.org/3/tutorial/index.html",
        # Ajoutez vos URLs ici
    ],
}
```

### Modifier le modele Ollama

Dans `app.py`, ligne 87 :

```python
llm = Ollama(model="llama3.2", temperature=0.3)
# Changez pour: "llama3", "mistral", "codellama", etc.
```

### Ajuster les parametres RAG

- **Chunk size** : ligne 52 de `app.py` (default: 1500)
- **Chunk overlap** : ligne 53 de `app.py` (default: 300)
- **Nombre de chunks** : ligne 88 de `app.py` (default: k=8)
- **Temperature** : ligne 87 de `app.py` (default: 0.3)

## 🚧 Limitations

- **Temps de chargement** : La recuperation de documentation peut prendre 1-2 minutes
- **Qualite des reponses** : Depend de la documentation recuperee
- **Modele local** : Moins precis que GPT-4 mais 100% gratuit
- **Connexion internet** : Necessaire pour recuperer la documentation

## 🔄 Evolution du projet

Ce projet a evolue :
1. **v1** : Scraping Indeed (bloque par Cloudflare)
2. **v2** : API France Travail pour offres d'emploi
3. **v3** : Assistant technique avec documentation IA/ML/Azure

## 🤝 Contribution

Ameliorations possibles :
- [ ] Cache de la documentation
- [ ] Support de plus de technologies (React, Django, etc.)
- [ ] Export des conversations
- [ ] Historique des questions
- [ ] Mode hors-ligne avec doc pre-telechargee
- [ ] Support PDF/Markdown locaux
- [ ] Multi-langues (anglais/francais)

## 📄 Licence

Projet educatif - Libre d'utilisation

## 👨‍💻 Auteur

Bafode Jaiteh - https://github.com/bafodej

---

**Note** : Parfait pour apprendre Python, ML, DL, Azure et technologies de donnees avec un assistant IA local et gratuit !
