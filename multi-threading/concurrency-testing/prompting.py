from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from json_prompt import load_prompts

llm = ChatGroq(model = 'llama-3.1-70b-versatile', temperature = 0.5)


extract_json_prompt = load_prompts(
    'multi-threading/concurrency-testing/prompts/extract-info.txt'
    )



parser = StrOutputParser()
prompt_template = ChatPromptTemplate.from_messages(
    [("user", extract_json_prompt)]
)

def get_output(content):
    try:
        llmchain = prompt_template | llm | parser
        return llmchain.invoke({"context": content})
    except Exception as e:
        return e
