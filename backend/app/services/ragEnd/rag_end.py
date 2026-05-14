from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
import chromadb
import json
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
from llama_index.llms.ollama import Ollama
from app.utils.json_utils import safe_json_load2

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


llm = Ollama(
    model="llama3",
    request_timeout=300.0,
    temperature=0.0
)

INDEX_DIR = "chroma_db"

chroma_client = chromadb.PersistentClient(path=INDEX_DIR)

collection = chroma_client.get_or_create_collection(
    "pdf_chunks"
)

vector_store = ChromaVectorStore(
    chroma_collection=collection
)

storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)

index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store
)


def analyse_chunks(query: str, chunk: list[str]):
    
    all_chunks = "\n\n".join(
        [f"[Page {c['page']}] {c['text']}" for c in chunk]
    )

    prompt = f"""
    Tu es un système d'extraction d'information STRICT et d'explication intelligent.

    MISSION:
    Tu dois trouver le passage EXACT du document qui répond à la question.

    REQUÊTE:
    {query}

    DOCUMENT (avec pages):
    {all_chunks}

    RÈGLES IMPORTANTES:
    - Tu dois choisir UN SEUL passage du document.
    - Le passage doit être copié EXACTEMENT (aucune modification).
    - Tu peux choisir une phrase ou une portion de phrase, mais uniquement présente dans le texte.
    - Si plusieurs passages sont possibles, choisis le plus précis.
    - Si rien ne répond, retourne une chaîne vide pour "extrait".
    - Ne fusionne jamais plusieurs chunks.
    - Ne reformule jamais.
    - si la requête ressemble à un passage alors donne tout le passage dans "extrait" sans le reduire

    SORTIE OBLIGATOIRE (JSON strict):

    {{
        "extrait": "texte exact copié du document",
        "page": numéro_de_page_du_passage,
        "explication": "explication simple de pourquoi ce passage répond à la question"
    }}

    CONTRAINTE:
    - JSON uniquement
    - Aucun texte hors JSON
    """

    try:

        response = llm.complete(
            prompt,
            format="json"
        )
        data = safe_json_load2(response.text)

        return {
            "extrait": data.get("extrait", ""),
            "page": data.get("page") + 1,
            "explication": data.get("explication", "")
        }

    except Exception as e:

        print(e)

        return {
            "extrait": "",
            "page": None,
            "explication": "Erreur analyse"
        }


def search_in_pdf(user_query: str, file_id: str):

    filters = MetadataFilters(
        filters=[
            ExactMatchFilter(key="file_id", value=file_id)
        ]
    )

    retriever = index.as_retriever(
        similarity_top_k=3,
        filters=filters
    )

    nodes = retriever.retrieve(user_query)
    for node in nodes:
        print(node.text)
        print(node.metadata)
        
    if not nodes:
        return {"message": "Aucune correspondance"}

    chunks = [
        {
            "text": node.text,
            "page": node.metadata.get("page"),
        }
        for node in nodes
    ]

    result = analyse_chunks(
        user_query,
        chunks
    )

    return result