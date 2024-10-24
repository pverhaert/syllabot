import os
from crewai.tasks import TaskOutput


def callback_function(output: TaskOutput) -> str:
    file_path = "course_latest/course.md"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Check if the file exists, if not, create it
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding='utf-8') as file:
            file.write("# Agent Outputs\n\n")
        print(f"Created new file: {file_path}")

    # Append the output to the file
    with open(file_path, "a", encoding='utf-8') as file:
        # Add a horizontal rule before new content for better separation
        file.write("\n\n___\n\n")

        # If output is a dictionary (common for Markdown output), extract the content
        if isinstance(output, dict) and 'content' in output:
            file.write(output['content'])
        else:
            # If it's a string or any other type, write it directly
            file.write(str(output))

    return f"Output successfully appended to {file_path}"
