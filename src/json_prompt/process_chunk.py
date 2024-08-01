from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser



def process_chunk_with_llm(chunk, llm, prompt):
    parser = StrOutputParser()
    prompt_template = ChatPromptTemplate.from_messages(
        [("user", prompt)]
    )
    llmchain = prompt_template | llm | parser
    return llmchain.invoke(chunk)


def refine(chunk, context, llm, prompt):
    """
    Refines and merges important details from a given context and a new chunk 
    of information to create a comprehensive and coherent summary.
    The function processes the context and the new chunk of information using a
    language model (LLM) and returns a detailed and accurate summary that 
    includes all critical points.

    Parameters:
    chunk (str): New chunk of information to be integrated with the context.
    context (str): Existing context that provides background or previous
    information.

    Returns:
    str: A refined summary that integrates information from both the context 
    and the new chunk.
    """
    parser = StrOutputParser()
    prompt_template = ChatPromptTemplate.from_messages(
        [("user", prompt)]
    )
    llmchain = prompt_template | llm | parser
    return llmchain.invoke({"context": context, "chunk": chunk})


def extract_json(context, llm, prompt):
    parser = StrOutputParser()
    prompt_template = ChatPromptTemplate.from_messages(
        [("user", prompt)]
    )
    llmchain = prompt_template | llm | parser
    return llmchain.invoke({"context": context})