"""
Application Streamlit - Assistant Technique IA
Chatbot RAG sur Python, LangChain, ChromaDB, ML, DL, Azure, Scraping, Data Analysis
"""
import streamlit as st
from dotenv import load_dotenv
from doc_fetcher import fetch_tech_docs, AVAILABLE_TOPICS
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
    page_title="Assistant Technique IA",
    page_icon="🤖",
    layout="wide"
)

# Initialiser session state
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'rag_chain' not in st.session_state:
    st.session_state.rag_chain = None
if 'docs_loaded' not in st.session_state:
    st.session_state.docs_loaded = False

# Fonctions
def fetch_docs(topics, max_pages=2):
    """Recupere la documentation pour les topics selectionnes"""
    try:
        with st.spinner(f"Recuperation de la documentation pour {len(topics)} topic(s)..."):
            docs = fetch_tech_docs(topics=topics, max_pages=max_pages)
        return docs

    except Exception as e:
        st.error(f"Erreur lors de la recuperation: {e}")
        return []

def create_rag_chain(docs):
    """Cree la chaine RAG avec Ollama"""

    # Division des documents
    with st.spinner("Division des documents..."):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=300
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
    template = """Tu es un assistant technique expert en Python, Machine Learning, Deep Learning, Azure et technologies de donnees.

CONTEXTE (Documentation technique):
{context}

QUESTION: {question}

Instructions:
1. Reponds de maniere precise et technique
2. Cite les sources de documentation quand disponible
3. Donne des exemples de code quand pertinent
4. Sois concis mais complet (3-5 phrases)
5. Si tu ne sais pas, dis-le clairement

Reponse:"""

    prompt = ChatPromptTemplate.from_template(template)

    # Creation de la chaine RAG avec Ollama
    with st.spinner("Configuration du modele Ollama..."):
        llm = Ollama(model="llama3.2", temperature=0.3)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 8})

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    return vectorstore, rag_chain, len(splits)

# Interface utilisateur
st.title("🤖 Assistant Technique IA")
st.markdown("Posez vos questions sur Python, ML, DL, Azure, LangChain, ChromaDB, Scraping, Data Analysis")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")

    # Selection des topics
    st.markdown("### Topics de documentation")
    selected_topics = st.multiselect(
        "Selectionnez les technologies",
        options=AVAILABLE_TOPICS,
        default=["python", "langchain"],
        help="Choisissez les technologies dont vous voulez charger la documentation"
    )

    # Nombre de pages
    max_pages = st.slider(
        "Pages par topic",
        min_value=1,
        max_value=5,
        value=2,
        help="Plus de pages = plus de documentation mais temps de chargement plus long"
    )

    # Bouton pour charger
    load_button = st.button("📚 Charger Documentation", type="primary")

    st.divider()

    # Informations
    st.markdown("### 📖 A propos")
    st.markdown("""
    Cet assistant technique utilise :
    - **WebBaseLoader** pour recuperer la doc
    - **LangChain** pour le RAG
    - **ChromaDB** pour le stockage vectoriel
    - **Ollama llama3.2** pour l'IA (gratuit, local)
    - **Streamlit** pour l'interface

    100% gratuit et open-source
    """)

    st.divider()

    st.markdown("### 🎯 Topics disponibles")
    for topic in AVAILABLE_TOPICS:
        st.markdown(f"- {topic.replace('_', ' ').title()}")

# Chargement de la documentation
if load_button:
    if not selected_topics:
        st.warning("Veuillez selectionner au moins un topic")
    else:
        try:
            docs = fetch_docs(selected_topics, max_pages)

            if docs:
                st.success(f"✓ {len(docs)} documents recuperes")
                vectorstore, rag_chain, num_chunks = create_rag_chain(docs)
                st.session_state.vectorstore = vectorstore
                st.session_state.rag_chain = rag_chain
                st.session_state.docs_loaded = True
                st.success(f"✓ RAG pret ! {num_chunks} chunks vectorises")
            else:
                st.error("Aucun document recupere")

        except Exception as e:
            st.error(f"Erreur : {e}")
            import traceback
            st.code(traceback.format_exc())

# Zone de chat
st.divider()

if st.session_state.docs_loaded and st.session_state.rag_chain is not None:
    st.header("💬 Posez vos questions")

    # Exemples
    with st.expander("💡 Exemples de questions"):
        st.markdown("""
        **Python:**
        - Comment utiliser les decorateurs en Python ?
        - Quelle est la difference entre list et tuple ?

        **Machine Learning:**
        - Comment preparer des donnees pour un modele ML ?
        - Explique-moi le RandomForest

        **Deep Learning:**
        - Comment creer un reseau de neurones avec PyTorch ?
        - Qu'est-ce que le backpropagation ?

        **LangChain:**
        - Comment creer une chaine RAG avec LangChain ?
        - Qu'est-ce qu'un retriever ?

        **Azure:**
        - Comment deployer un modele ML sur Azure ?
        - Qu'est-ce qu'Azure Machine Learning ?

        **Data Analysis:**
        - Comment utiliser Pandas pour analyser des donnees ?
        - Comment visualiser des donnees avec Matplotlib ?

        **Web Scraping:**
        - Comment scraper un site web avec BeautifulSoup ?
        - Quelle est la difference entre Requests et Selenium ?
        """)

    # Input utilisateur
    user_question = st.text_input(
        "Votre question :",
        placeholder="Ex: Comment creer un modele de classification avec scikit-learn ?"
    )

    if user_question:
        try:
            with st.spinner("Recherche dans la documentation..."):
                reponse = st.session_state.rag_chain.invoke(user_question)
                st.markdown("### 🎯 Reponse :")
                st.write(reponse)
        except Exception as e:
            st.error(f"Erreur RAG : {e}")
else:
    st.info("👆 Selectionnez des topics dans la sidebar et cliquez sur 'Charger Documentation' pour commencer")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    Assistant Technique IA - Powered by Ollama (100% gratuit) | Chatbot RAG
</div>
""", unsafe_allow_html=True)
