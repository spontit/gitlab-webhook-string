from get_gitlab_webhook_body import get_gitlab_webhook_body
import json


class Example:

    def __init__(self, example_title, example_file_name):
        self.example_title = example_title
        self.example_file_name = example_file_name

    def print_separator(self):
        print(f"-------------------- {self.example_title} --------------------\n")

    def print_body_for_file_name(self):
        with open(f'examples/{self.example_file_name}.json', 'r') as json_file:
            payload = json.load(json_file)
            print(get_gitlab_webhook_body(payload))


if __name__ == "__main__":
    examples = [
        Example("Push Example", "push_example"),
        Example("Push Tag Example", "push_tag_example"),
        Example("Issue Example", "issue_example"),
        Example("Note Example", "note_example"),
        Example("Merge Request Example", "merge_request_example"),
        Example("Job Example", "job_example"),
        Example("Pipeline Example", "pipeline_example"),
        Example("Wiki Example", "wiki_example")
    ]
    for example in examples:
        example.print_separator()
        example.print_body_for_file_name()
