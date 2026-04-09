import os
from langfuse import Langfuse
from dotenv import load_dotenv

load_dotenv()

# On initialise le client ici
langfuse_client = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com"),
)
