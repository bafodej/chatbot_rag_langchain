"""
Application Streamlit pour le chatbot RAG Indeed
Utilise Selenium pour scraper Indeed et Ollama pour l'IA (100% gratuit, local)
"""
import streamlit as st
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
import time

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Chatbot RAG Indeed",
    layout="wide"
)

st.title("Chatbot RAG - Offres d'emploi Indeed France")
st.markdown("Analysez les offres d'emploi Indeed en France avec Ollama (100% gratuit)")

# Sidebar pour la configuration
with st.sidebar:
    st.header("Configuration")

    # Requete de recherche
    search_query = st.text_input(
        "Terme de recherche Indeed",
        value="data analyst",
        help="Ex: 'data analyst', 'python', 'alternance', ou vide pour toutes les offres"
    )

    # Bouton pour scraper
    scrape_button = st.button("Scraper Indeed", type="primary")

    st.divider()

    # Informations
    st.markdown("### A propos")
    st.markdown("""
    Ce chatbot utilise :
    - **LangChain** pour le RAG
    - **ChromaDB** pour le stockage vectoriel
    - **Ollama llama3.2** pour l'IA (gratuit, local)
    - **Streamlit** pour l'interface
    """)

# Initialiser session state
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'rag_chain' not in st.session_state:
    st.session_state.rag_chain = None
if 'scraped' not in st.session_state:
    st.session_state.scraped = False

def scrape_indeed(query=""):
    """Scrappe les offres d'emploi Indeed France avec Selenium"""
    url = f"https://fr.indeed.com/emplois?q={query}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)")

    driver = None
    try:
        with st.spinner("Initialisation du navigateur..."):
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)

        with st.spinner(f"Scraping : {url}"):
            driver.get(url)
            time.sleep(5)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        jobs = soup.find_all('div', class_='job_seen_beacon')

        docs = []
        for job in jobs:
            title_elem = job.find('h2', class_='jobTitle')
            company_elem = job.find('span', class_='companyName')
            location_elem = job.find('div', class_='companyLocation')
            salary_elem = job.find('div', class_='salary-snippet')
            snippet_elem = job.find('div', class_='job-snippet')
            link_elem = job.find('a', class_='jcs-JobTitle')

            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            location = location_elem.get_text(strip=True) if location_elem else "N/A"
            salary = salary_elem.get_text(strip=True) if salary_elem else "Non specifie"
            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
            job_link = f"https://fr.indeed.com{link_elem['href']}" if link_elem and 'href' in link_elem.attrs else ""

            content = f"""Titre: {title}
Entreprise: {company}
Lieu: {location}
Salaire: {salary}
Description: {snippet}
Lien: {job_link}"""

            docs.append(Document(page_content=content, metadata={"source": url, "title": title, "link": job_link}))

        return docs

    except Exception as e:
        st.error(f"Erreur de scraping: {e}")
        return []

    finally:
        if driver:
            driver.quit()

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

CONTEXTE SCRAPE (Indeed France):
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

# Scraping au clic du bouton
if scrape_button:
    try:
        # Scraping
        docs = scrape_indeed(search_query)

        if docs:
            st.success(f"{len(docs)} documents scrapes")

            # Creation de la chaine RAG
            vectorstore, rag_chain, num_chunks = create_rag_chain(docs)

            # Sauvegarder dans session state
            st.session_state.vectorstore = vectorstore
            st.session_state.rag_chain = rag_chain
            st.session_state.scraped = True

            st.success(f"RAG pret ! {num_chunks} chunks vectorises")
        else:
            st.error("Aucun document scrape")

    except Exception as e:
        st.error(f"Erreur : {e}")

# Zone de chat
st.divider()

if st.session_state.scraped and st.session_state.rag_chain is not None:
    st.header("Posez vos questions")
    
    # Exemples
    with st.expander("Exemples de questions"):
        st.markdown("""
        - Combien d'offres data analyst ?
        - Quelles offres à Lille ?
        - Top 5 entreprises qui recrutent ?
        """)
    
    # Input utilisateur
    user_question = st.text_input("Votre question :", placeholder="Ex: Combien d'offres à Paris ?")
    
    if user_question:
        try:
            with st.spinner("Recherche RAG en cours..."):
                reponse = st.session_state.rag_chain.invoke(user_question)
                st.markdown("### Reponse :")
                st.write(reponse)
        except Exception as e:
            st.error(f"Erreur RAG : {e}")
else:
    st.info("Cliquez 'Scraper Indeed' dans la sidebar d'abord")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    Chatbot RAG Indeed - Powered by Ollama (100% gratuit)
</div>
""", unsafe_allow_html=True)

