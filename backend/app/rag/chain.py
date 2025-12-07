from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from app.rag.vectordb import get_vector_db
from app.rag.prompts import prompt
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)



def augment_context(input_dict):
    query = input_dict['query']
    docs = input_dict['docs']

    context = ""
    for i, doc in enumerate(docs, start=1):
        context += f"Snippet {i}: {doc.page_content}\n<end of snippet>\n\n"
    

    return {
        'query' :query,
        'context' : context
    }

def build_rag_chain(collection_name='default'):

    logger.info(f"Collection Name: {collection_name}")

    vector_db = get_vector_db()
    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs = {
            'k' : 5,
            # "filter": {"collection_name": collection_name}
        }
    )

    llm = ChatGroq(
        model = "openai/gpt-oss-20b",
        api_key = settings.GROQ_API_KEY
    )

    chain = { 'query' :RunnablePassthrough(), 'docs': retriever} | RunnableLambda(augment_context) | prompt | llm | StrOutputParser()

    return chain