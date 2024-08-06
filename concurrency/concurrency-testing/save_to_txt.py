def save_responses_to_file(
    responses,
    filename="/home/prashjeev/tasks/json_extraction_prompt_engineering/concurrency/concurrency-testing/responses.txt",
):
    with open(filename, "w") as file:
        for i, response in enumerate(responses):
            file.write(f"Response Number {i}:\n")
            file.write(response + "\n\n")
