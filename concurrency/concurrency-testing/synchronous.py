import logging.config
from json_prompt import fetch_wikipedia_page_by_url
from prompting import get_output, self_consistency
import time

# Load the logging configuration
logging.config.fileConfig("concurrency/concurrency-testing/logging-sync.conf")
logger = logging.getLogger(__name__)


def main():
    url = input("Please enter the URL of the Wikipedia page: ")

    try:
        html_content = fetch_wikipedia_page_by_url(url)
    except Exception as e:
        logger.error(f"Failed to fetch content from '{url}': {e}")
        return

    logger.info("Content fetched successfully")

    contents = [html_content[:20000]] * 10

    responses = []
    start_time = time.time()
    timeout = 5  # Timeout in seconds for each get_output call

    for i, content in enumerate(contents):
        try:
            start_single_time = time.time()
            response = get_output(content)
            end_single_time = time.time()

            if (end_single_time - start_single_time) > timeout:
                raise TimeoutError("Operation timed out")

            logger.info(f"\nResponse Number {i} saved")
            responses.append(response)
        except TimeoutError:
            logger.error(f"Timeout occurred for response number {i}")
        except Exception as e:
            logger.error(f"Error occurred for response number {i}: {e}")

    end_time = time.time()
    execution_time = end_time - start_time
    logger.info(f"Total execution time: {execution_time:.2f} seconds")

    final_output = self_consistency(responses)
    if isinstance(final_output, Exception):
        logger.error(f"Error encountered: {final_output}")
    else:
        logger.info(f"\nFinal Output:\n{final_output}")


if __name__ == "__main__":
    main()
