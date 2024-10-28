import datetime
import os
import shutil
import time

import pandas as pd
import pypandoc
import streamlit as st
from groq import Groq

from crew import CourseBuilderCrew
from models import Models

# Page layout
st.set_page_config(page_title="ITF SyllaBot", page_icon="assets/logo-tm.svg", layout="wide")
with open('./assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def create_folders():
    folders = ['course_latest', 'course_history']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)


def create_new_course_file(inputs):
    if os.path.exists('course_latest/course.md'):
        os.remove('course_latest/course.md')

    with open('course_latest/course.md', 'w', encoding='utf-8') as f:
        f.write(f"___\n")
        f.write(f"- **Prompt:** {inputs['course']}\n")
        f.write(f"- **Special needs:** {inputs['special_needs']}\n")
        f.write(f"- **Target audience:** {inputs['target_audience']}\n")
        f.write(f"- **Language:** {inputs['language']}\n")
        f.write(f"- **Model:** {inputs['model']}\n")
        f.write(f"- **Temperature:** {inputs['temperature']}\n")
        f.write(f"- **Total Tokens:** %%total_tokens%%\n")
        f.write(f"   - **Prompt Tokens:** %%prompt_tokens%%\n")
        f.write(f"   - **Completion Tokens:** %%completion_tokens%%\n")
        f.write(f"   - **Successful Requests:** %%successful_requests%%\n")
        f.write(f"- **Elapsed Time:** %%elapsed_time%%\n")
        f.write(f"- **Date Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def run_crew(inputs):
    #  Start the timer
    start_time = time.time()

    create_new_course_file(inputs)
    my_crew = CourseBuilderCrew(inputs=inputs).crew()
    # with st.expander("Live Info", expanded=True):
    #     st.write("Starting the course generation process...")
    my_crew.kickoff(inputs=inputs)
    # Create a filename for the final output Markdown file
    client = Groq()
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": f"""Generate a filename for a markdown document. 
                    The filename should be a descriptive name based on the users input. 
                    **ONLY RESPOND WITH THE FILENAME**, replace whitespace with underscores and don't add any extension.""",
            },
            {
                "role": "user",
                "content": inputs['course']
            }
        ],
        temperature=1,
        max_tokens=60,
        stream=False,
        stop=None,
    )
    # Get suggested filename
    filename = completion.choices[0].message.content
    # Timestamp prefix from datetime: eg 202401-081236
    prefix = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    # Stop the timer
    end_time = time.time()
    # Calculate the difference and format the time in mm:ss
    elapsed_time = end_time - start_time
    formatted_elapsed_time = f'{elapsed_time // 60:.0f}:{elapsed_time % 60:02.0f}'
    st.write(f"Elapsed time: {elapsed_time:.2f} seconds")
    # Replace placeholders with actual content
    with open('course_latest/course.md', 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('%%total_tokens%%', str(my_crew.usage_metrics.total_tokens))
    content = content.replace('%%completion_tokens%%', str(my_crew.usage_metrics.completion_tokens))
    content = content.replace('%%prompt_tokens%%', str(my_crew.usage_metrics.prompt_tokens))
    content = content.replace('%%successful_requests%%', str(my_crew.usage_metrics.successful_requests))
    content = content.replace('%%elapsed_time%%', formatted_elapsed_time)
    # Save the updated file
    with open('course_latest/course.md', 'w', encoding='utf-8') as f:
        f.write(content)
    # Make a copy of the final.md file in course_backup folder
    shutil.copy('course_latest/course.md', f'course_history/{prefix}_{filename}.md')
    # Convert the markdown file to a docx file and save it also in course_backup folder
    pypandoc.convert_file('course_latest/course.md', 'docx',
                          outputfile=f'course_history/{prefix}_{filename}.docx')
    # Convert the markdown file to a docx file with the template "course_templates/Thomas_More.docx"
    pypandoc.convert_file('course_latest/course.md', 'docx',
                          outputfile=f'course_history/{prefix}_{filename}_tm.docx',
                          extra_args=['--reference-doc', './course_templates/ThomasMore.docx'])


def main():
    create_folders()
    # Streamlit app
    with open('assets/logo-tm.svg') as f:
        st.markdown(f'<div id="main_header">{f.read()}<p>ITF SyllaBot <span>(v0.1.2)</span></p></div>',
                    unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("Input Parameters")
        # Input parameters
        language = st.text_input("Language for this course", value="English")
        course = st.text_input("Write a course about", value="", placeholder="Short description of the topic")
        special_needs = st.text_input("Special needs to take into account?", value="", placeholder="Optional")
        target_audience = st.text_input("Target audience", value="", placeholder="Optional")
        model = st.selectbox("Model", options=[m['model'] for m in Models])
        col1, col2 = st.columns(2)
        with col1:
            num_exercises = st.number_input("Nr of Exercises", value=20, min_value=0)
        with col2:
            num_quizzes = st.number_input("Nr of Quizzes", value=20, min_value=0)
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.05)

        if st.button("Generate New Content"):
            if target_audience == "":
                target_audience = "not specified"
            inputs = {
                'language': language,
                'course': course,
                'special_needs': special_needs,
                'target_audience': target_audience,
                'model': model,
                'num_exercises': num_exercises,
                'num_quizzes': num_quizzes,  # Using the same value as exercises for quiz
                'temperature': temperature,
                'serper_api_key': os.environ.get('SERPER_API_KEY', None)
            }

            inputs['llm_api_key'] = os.environ.get('GROQ_API_KEY', None) if inputs['model'].startswith(
                'groq/') else os.environ.get('OPENROUTER_API_KEY', None)

            # st.write("Inputs:", inputs)
            run_crew(inputs)

    # Main content
    new_course, model_details, all_courses = st.tabs(["New Course", "Model details", "Previously Generated Courses"])

    with new_course:
        if os.path.exists('course_latest/course.md'):
            with open('course_latest/course.md', 'r') as f:
                st.markdown(f.read(), unsafe_allow_html=True)
        else:
            st.write("No final output available yet. Generate a course to see the results.")

    with model_details:
        # Info about add/remove models
        with st.expander("📚 How to Add/Remove Models"):
            st.markdown("""
                        ##### Open the `models.py` and add or remove models as needed.

                        1. **Open** the `models.py` file in your editor
                        2. **Follow** this format to add new models:
                        ```
                        {
                            "model": "openrouter/nvidia/llama-3.1-nemotron-70b-instruct",
                            "max_output_tokens": 131.072,
                            "price_input": 0.35,
                            "price_output": 0.4
                        }
                        ```

                        - For [Groq models](https://console.groq.com/docs/models)
                        - For [OpenRouter models](https://openrouter.ai/models)

                        ⚠️ **Important:** always add the provider name (`groq/` or `openrouter/`) before the model name!  
                        For example, for the [inflection-3-pi](https://openrouter.ai/inflection/inflection-3-pi) model on OpenRouter, 
                        the `model` key should be `openrouter/inflection/inflection-3-pi` instead of just `inflection/inflection-3-pi`.
                """)
        # Show all model details in a table (column names are Model, Max Output Tokens, Input Price, Output Price)
        table = []
        for i, model in enumerate(Models, start=1):
            table.append([model['model'], model['max_output_tokens'], f"$ {model['price_input']}",
                          f"$ {model['price_output']}"])
        # Convert the list of lists to a DataFrame
        df = pd.DataFrame(table, columns=["Model", "Max Tokens", "Input Price", "Output Price"])
        # Display the DataFrame as a table
        st.table(df)

    with all_courses:
        # Read all files in course_history folder and display them in a dropdown
        course_files = [f for f in os.listdir('course_history') if os.path.isfile(os.path.join('course_history', f))]
        if len(course_files) == 0:
            st.write("No courses generated yet.")
        else:
            # Filter only .md files (.docx must not be visible in the dropdown)
            course_files = [f for f in course_files if f.endswith('.md')]
            # show all files in a reverse order
            course_files = sorted(course_files, reverse=True)
            # Get the selected md file and docx files
            selected_file_md = st.selectbox("Select a course", course_files)
            selected_file_default_docx = selected_file_md.split(".")[0] + ".docx"
            selected_file_tm_docx = selected_file_md.rsplit(".", 1)[0] + "_tm.docx"
            st.markdown("<b>Download selected file</b>", unsafe_allow_html=True)
            word, tm_word, md = st.columns(3)
            with word:
                # if the file exists, download the file in docx format
                if os.path.exists(os.path.join('course_history', selected_file_default_docx)):
                    with open(os.path.join('course_history', selected_file_default_docx), 'rb') as docx_file:
                        st.download_button('DOCX (default template)', docx_file,
                                           file_name=selected_file_default_docx,
                                           use_container_width=True,
                                           )
            with tm_word:
                # if the file exists, download the file in docx format
                if os.path.exists(os.path.join('course_history', selected_file_tm_docx)):
                    with open(os.path.join('course_history', selected_file_tm_docx), 'rb') as docx_file:
                        st.download_button('DOCX (Thomas More template)', docx_file,
                                           file_name=selected_file_tm_docx,
                                           use_container_width=True,
                                           type="primary"
                                           )
            with md:
                # download the file in Markdown format
                with open(os.path.join('course_history', selected_file_md), 'r') as md_file:
                    st.download_button('Markdown',md_file,file_name=selected_file_md, use_container_width=True)
            # display the file content in markdown
            with open(os.path.join('course_history', selected_file_md), 'r') as md_file:
                st.markdown(md_file.read(), unsafe_allow_html=True)


if __name__ == '__main__':
    main()
