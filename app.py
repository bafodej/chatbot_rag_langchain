"""
Application Streamlit pour le chatbot RAG France Travail
Utilise l'API France Travail (ex-Pole Emploi) et Ollama pour l'IA (100% gratuit)
"""
import streamlit as st
from dotenv import load_dotenv
from france_travail_api import fetch_france_travail_jobs
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Chatbot RAG France Travail",
    layout="wide"
)

# Initialiser session state avant utilisation
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'rag_chain' not in st.session_state:
    st.session_state.rag_chain = None
if 'scraped' not in st.session_state:
    st.session_state.scraped = False

# Fonctions
def fetch_jobs(query="", departement=""):
    """Recupere les offres d'emploi via l'API France Travail"""
    try:
        with st.spinner(f"Recherche d'offres pour '{query}'..."):
            docs = fetch_france_travail_jobs(
                query=query,
                departement=departement,
                max_results=150
            )
        return docs

    except ValueError as e:
        st.error(f"Erreur de configuration: {e}")
        st.info("""
        Pour utiliser l'API France Travail:
        1. Allez sur https://francetravail.io
        2. Creez un compte
        3. Creez une application dans 'Espace Partenaire'
        4. Ajoutez vos credentials dans le fichier .env
        """)
        return []

    except Exception as e:
        st.error(f"Erreur API: {e}")
        return []

def create_rag_chain(docs):
    """Cree la chaine RAG avec Ollama"""

    # Division des documents
    with st.spinner("Division des documents..."):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)

    # Creation du vector store
    with st.spinner("Creation de la base vectorielle..."):
        embeddings = OllamaEmbeddings(model="llama3.2")
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )

    # Configuration du prompt
    template = """Tu es un analyste offres d'emploi en France.

CONTEXTE (France Travail API):
{context}

QUESTION: {question}

Instructions:
1. Reponds precisement avec chiffres exacts
2. Cite les entreprises et lieux quand disponible
3. Maximum 3-4 phrases concises
4. Francais uniquement

Reponse:"""

    prompt = ChatPromptTemplate.from_template(template)

    # Creation de la chaine RAG avec Ollama
    with st.spinner("Configuration du modele Ollama..."):
        llm = Ollama(model="llama3.2", temperature=0)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    return vectorstore, rag_chain, len(splits)

# Note: Scraping automatique desactive pour ameliorer les performances
# Utilisez le bouton dans la sidebar pour charger les donnees

# Interface utilisateur
st.title("Chatbot RAG - Offres d'emploi France Travail")
st.markdown("Analysez les offres d'emploi officielles France Travail avec Ollama (100% gratuit)")

# Sidebar
with st.sidebar:
    st.header("Configuration")

    # Requete de recherche
    search_query = st.text_input(
        "Terme de recherche",
        value="alternance",
        help="Ex: 'alternance', 'data analyst', 'python', 'developpeur'"
    )

    # Departement (optionnel)
    departement = st.text_input(
        "Code departement (optionnel)",
        value="",
        help="Ex: '75' pour Paris, '59' pour Nord, '69' pour Rhone"
    )

    # Bouton pour rechercher
    search_button = st.button("Rechercher offres", type="primary")

    st.divider()

    # Informations
    st.markdown("### A propos")
    st.markdown("""
    Ce chatbot utilise :
    - **France Travail API** pour les offres (gratuit, officiel)
    - **LangChain** pour le RAG
    - **ChromaDB** pour le stockage vectoriel
    - **Ollama llama3.2** pour l'IA (gratuit, local)
    - **Streamlit** pour l'interface

    100% gratuit et open-source
    """)

# Recherche au clic du bouton
if search_button:
    try:
        docs = fetch_jobs(search_query, departement)

        if docs:
            st.success(f"{len(docs)} offres trouvees")
            vectorstore, rag_chain, num_chunks = create_rag_chain(docs)
            st.session_state.vectorstore = vectorstore
            st.session_state.rag_chain = rag_chain
            st.session_state.scraped = True
            st.success(f"RAG pret ! {num_chunks} chunks vectorises")
        else:
            st.warning("Aucune offre trouvee pour cette recherche")

    except Exception as e:
        st.error(f"Erreur : {e}")

# Zone de chat
st.divider()

if st.session_state.scraped and st.session_state.rag_chain is not None:
    st.header("Posez vos questions")

    # Exemples
    with st.expander("Exemples de questions"):
        st.markdown("""
        - Combien d'offres d'alternance ?
        - Quelles offres a Paris ?
        - Top 5 entreprises qui recrutent ?
        - Quels sont les salaires proposes ?
        - Quels types de contrats sont proposes ?
        - Quelles competences sont demandees ?
        """)

    # Input utilisateur
    user_question = st.text_input("Votre question :", placeholder="Ex: Combien d'offres a Paris ?")

    if user_question:
        try:
            with st.spinner("Recherche RAG en cours..."):
                reponse = st.session_state.rag_chain.invoke(user_question)
                st.markdown("### Reponse :")
                st.write(reponse)
        except Exception as e:
            st.error(f"Erreur RAG : {e}")
else:
    st.info("Chargement en cours...")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    Chatbot RAG France Travail - Powered by Ollama (100% gratuit)
</div>
""", unsafe_allow_html=True)
