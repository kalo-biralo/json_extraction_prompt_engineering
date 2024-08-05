import os
import logging.config
from IPython.display import display, Markdown
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from wiki_extract import fetch_wikipedia_page_by_url
from process_chunk import process_chunk_with_llm, refine, extract_json
from load_prompt import load_prompt
from check_json import is_valid_json

# Load the logging configuration
logging.config.fileConfig('src/json_prompt/logging.conf')
logger = logging.getLogger(__name__)

load_dotenv()

llm = ChatGroq(model='llama-3.1-70b-versatile')

url = input("Please enter the URL of the Wikipedia page: ")

# Fetch the HTML content of the page
html_content = fetch_wikipedia_page_by_url(url)

# Check if the content was fetched successfully and log it
if html_content:
    logger.info("Content fetched successfully.")
else:
    logger.error(f"Page at '{url}' not found or could not be fetched.")

# Create an instance of RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=10000,
    chunk_overlap=2000
)

# Split the text into chunks and store the output
doc_split = splitter.create_documents([html_content])
logger.info("Text split into chunks.")

# Load the prompt
summarize_chunk_prompt = load_prompt(
    'src/json_prompt/prompts/summarize_chunk_prompt.txt'
)

chunk_sums = []
for chunk in doc_split:
    chunk_sums.append(process_chunk_with_llm(
        chunk, llm, summarize_chunk_prompt
    ))
logger.info(f"First chunk processed: \n{chunk_sums[0]}")

refine_prompt = load_prompt('src/json_prompt/prompts/refine_prompt.txt')
context = chunk_sums[0]
for i, response in enumerate(chunk_sums):
    if i == 0:
        continue
    context = refine(response, context, llm, refine_prompt)

logger.info(f"\nContext refined: \n{context}")

extract_json_prompt = load_prompt(
    'src/json_prompt/prompts/json_extract_prompt.txt'
)

extracted_json = extract_json(context, llm, extract_json_prompt)
logger.info(f"\nExtracted JSON: \n{extracted_json}")
