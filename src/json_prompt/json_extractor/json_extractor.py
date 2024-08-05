from IPython.display import display, Markdown
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from wiki_extract import fetch_wikipedia_page_by_url
from process_chunk import process_chunk_with_llm, refine, extract_json
from load_prompt import load_prompt
from check_json import is_valid_json




load_dotenv()


llm = ChatGroq(model = 'llama-3.1-70b-versatile')


url = input("Please enter the URL of the Wikipedia page: ")

# Fetch the HTML content of the page
html_content = fetch_wikipedia_page_by_url(url)

# Check if the content was fetched successfully and print it
if html_content:
    print("Content fetched!")
else:
    print(f"Page at '{url}' not found or could not be fetched.")


# Create an instance of RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=10000,
    chunk_overlap=2000
)

# Split the text into chunks and store the output
doc_split = splitter.create_documents([html_content])

# Load the prompt
summarize_chunk_prompt = load_prompt(
    'src/json_prompt/json_extractor/prompts/summarize_chunk_prompt.txt'
    )


chunk_sums = []
for chunk in doc_split:
    chunk_sums.append(process_chunk_with_llm(
        chunk, llm, summarize_chunk_prompt 
        ))
print(f"First chunk: \n{chunk_sums[0]}")



refine_prompt = load_prompt('src/json_prompt/json_extractor/prompts/refine_prompt.txt')
context = chunk_sums[0]
for i, response in enumerate(chunk_sums):
    if i == 0:
        continue
    context = refine(response, context, llm, refine_prompt)

print(f"\nContext: \n{context}")

extract_json_prompt = load_prompt(
    'src/json_prompt/json_extractor/prompts/json_extract_prompt.txt'
    )

extracted_json = extract_json(context, llm, extract_json_prompt)
print(f"\nJSON: \n{extracted_json}")


