This repository facilitates the creation of a course using [CrewAI](https://crew.ai/), ideally suited for courses on programming languages. The CrewAI generates five essential files for you:

- `course_latest/1_outline.md`: An outline for a specific course chapter (e.g., "Functions in JavaScript").
- `course_latest/2_draft.md`: The first draft of the course, based on the outline.
- `course_latest/3_course_content.md`: The detailed content of the course, based on the draft.
- `course_latest/4_exercises.md`: Exercises to reinforce the subject matter.
- `course_latest/5_quiz.md`: Quiz questions similar to Kahoot, focusing on the subject.

> [!CAUTION]
> - LLMs can hallucinate. Always verify the results before using them.
> - Run the crew multiple times to obtain (slightly) different content.
> - Experiment with different models to find the best fit for your needs.
> - LLMs perform best in English. If you require a different language, first ensure the model supports multilingual capabilities.
> - The generated content may not be perfect but serves as a solid starting point for your course development.

## Requirements

- [Git](https://git-scm.com/)
- [Python](https://www.python.org) `3.10.x` or `3.11.x` (Check your active Python version with `python -V`)

## Getting Started

- Clone this repository: `git clone https://github.com/pverhaert/syllabot`

### On Windows

- Double-click the `install.bat` file to:
  - Create the virtual environment.
  - Install the dependencies.
  - Create a `.env` file.
  - Create a `models.py` file.

### On Linux or macOS

- Create a virtual environment named `.venv`.
- Activate the virtual environment.
- Install the dependencies with `pip install -r requirements.txt`.
- Rename the `.env.example` file to `.env`.
- Rename the `models.example.py` file to `models.py`.

## Configure the API keys in the .env File

You can choose between [Groq](https://groq.com/) or [OpenRouter](https://openrouter.com/).

### Groq

- The [Groq](https://groq.com/) API is fast and free to use.
- Create a [Groq account](https://console.groq.com/).
- Generate an [API key](https://console.groq.com/keys).
- Update the `.env` file with your API key (`GROQ_API_KEY=`).

### OpenRouter (Optional)

- With [OpenRouter](https://openrouter.ai/), you can access almost all frontier models from OpenAI, Anthropic, Google, Cohere, etc.
- Most APIs are not free, but frontier models can generate better results.
- Create an OpenRouter account.
- Generate an [API key](https://openrouter.ai/settings/keys).
- Update the `.env` file with your API key (`OPENROUTER_API_KEY=`).

### Serper

- We use the [Serper API](https://serper.dev/) to search the web for relevant sources about the course you want to create.
- The first 2,500 API calls are free.
- Generate an [API key](https://serper.dev/api-key/).
- Update the `.env` file with your API key (`SERPER_API_KEY=`).

```markdown
GROQ_API_KEY=
OPENROUTER_API_KEY=
SERPER_API_KEY=
```
  
## Run the Crew

### On Windows

- Double-click the `run.bat` file to start the Crew.

### On Linux or macOS

- Activate the virtual environment.
- Run the crew with `streamlit run main.py`.

## Input Fields

- `Language of the course`: The language of the course, e.g., "English".
- `Write a course about`: The name of the course, e.g., "Funcripns in Python".
- `Special needs to take into account`: The topics that must or may need be included in the course (can be left empty).
- `Model`: The model to use for the course creation.
- `Nr of Exercises`: The number of exercises to include in the course.
- `Nr of Quizzes`: The number of quiz questions to include in the course.
- `Temperature`: The temperature for the model to use when generating the course (between `0` and `1`).  
   The higher the temperature, the more diverse the course will be, but also the more hallucination you can expect.

## Previous Generated Courses

After the crew has finished, you can find all the generated courses in the `course_history` folder.   
All the files are in Markdown format.

> [!TIP]
> - Install the [Markdown Viewer](https://chromewebstore.google.com/detail/markdown-viewer/ckkdlimhmcjmikdlpkmbgfkaikojcbjk) extension to view the course files in your browser.
> - Allow the extension to [have access to your local files](https://github.com/simov/markdown-viewer?tab=readme-ov-file#manage-origins).
> - Drag and drop the a file from the `course_history` folder to your browser.
