
from dotenv import load_dotenv
from json_prompt import fetch_wikipedia_page_by_url
import concurrent.futures
import logging.config
from prompting import get_output

load_dotenv()

# Load the logging configuration
logging.config.fileConfig('multi-threading/concurrency-testing/logging.conf')
logger = logging.getLogger(__name__)



url = input("Please enter the URL of the Wikipedia page: ")

# Fetch the HTML content of the page
html_content = fetch_wikipedia_page_by_url(url)

# Check if the content was fetched successfully and print it
if isinstance(html_content, Exception):
    logger.error(f"Failed to fetch content from '{url}'")
    exit(1)
else:
    logger.info("Content fetched successfully")







contents = [html_content[:20000]] * 5



with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(get_output, content) for content in contents]
    timeout = 5

    for i, future in enumerate(futures):
        try:
            response = future.result(timeout = timeout)
            logger.info(f"\nResponse Number {i}: \n{response}")
        except concurrent.futures.TimeoutError:
            logger.error(f"Timeout occured for response number {i}")
        except Exception as e:
            logger.error(f"Error occured for response number {i}: {e}")


