from .json_extractor import load_prompt, process_chunk, wiki_extract

load_prompts = load_prompt.load_prompt
fetch_wikipedia_page_by_url = wiki_extract.fetch_wikipedia_page_by_url
process_chunk_with_llm = process_chunk.process_chunk_with_llm

