from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from app.models.comprehension_schema import AnalysePedagogique
import os

load_dotenv()

GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
]

parser = PydanticOutputParser(pydantic_object=AnalysePedagogique)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Tu es un expert pédagogique qui aide à résoudre des exercices."),
        (
            "human",
            """
Analyse le document suivant et retourne une aide pédagogique.

Valeur obligatoire de warning est "warning": ["LangChain"]

{format_instructions}

DOCUMENT:
{document}
""",
        ),
    ]
).partial(format_instructions=parser.get_format_instructions())


def build_chain(model_name: str):
    llm = ChatGroq(
        temperature=0.2, model_name=model_name, groq_api_key=os.getenv("GROQ_API_KEY")
    )
    return prompt | llm | parser


def run_chain_with_fallback(document: str):
    last_error = None

    for model_name in GROQ_MODELS:
        try:
            chain = build_chain(model_name)

            result = chain.invoke({"document": document})

            return {"result": result.dict(), "source": f"groq:{model_name}"}

        except Exception as e:
            last_error = str(e)

    return {
        "result": {"erreur": "All Groq models failed", "detail": last_error},
        "source": "groq_failed",
    }
