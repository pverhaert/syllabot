from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

from callbacks.callback import callback_function


@CrewBase
class CourseBuilderCrew():
    """CourseBuilder crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, inputs) -> None:
        self.llm = LLM(
            api_key=inputs['llm_api_key'],
            model=inputs['model'],
            temperature=inputs['temperature'],
        )
        self.search_tool = SerperDevTool()
        self.callback_function = callback_function

    # Create outline
    # ------------------------------------------------------------

    @agent
    def outline_creator(self) -> Agent:
        return Agent(
            llm=self.llm,
            config=self.agents_config['outline_creator'],
            allow_delegation=False,
            tools=[],
            verbose=True
        )

    @task
    def outline_task(self) -> Task:
        return Task(
            config=self.tasks_config['outline_task'],
            callback=self.callback_function,
            output_file='course_latest/1_outline.md'
        )

    # Create draft
    # ------------------------------------------------------------

    @agent
    def draft_creator(self) -> Agent:
        return Agent(
            llm=self.llm,
            config=self.agents_config['draft_creator'],
            allow_delegation=False,
            tools=[self.search_tool],
            max_iter=3,
            verbose=True
        )

    @task
    def draft_task(self) -> Task:
        return Task(
            config=self.tasks_config['draft_task'],
            output_file='course_latest/2_draft.md'
        )

    # Course enhancer
    # ------------------------------------------------------------

    @agent
    def course_enhancer(self) -> Agent:
        return Agent(
            llm=self.llm,
            config=self.agents_config['course_enhancer'],
            allow_delegation=False,
            tools=[],
            verbose=True
        )

    @task
    def enhancer_task(self) -> Task:
        return Task(
            config=self.tasks_config['enhancer_task'],
            callback=self.callback_function,
            output_file='course_latest/3_course_content.md'
        )

    # Exercises
    # ------------------------------------------------------------

    @agent
    def exercise_creator(self) -> Agent:
        return Agent(
            llm=self.llm,
            config=self.agents_config['exercise_creator'],
            allow_delegation=False,
            tools=[],
            verbose=True
        )

    @task
    def exercise_task(self) -> Task:
        return Task(
            config=self.tasks_config['exercise_task'],
            callback=self.callback_function,
            output_file='course_latest/4_exercises.md'
    )

    # Quiz
    # ------------------------------------------------------------

    @agent
    def quiz_creator(self) -> Agent:
        return Agent(
            llm=self.llm,
            config=self.agents_config['quiz_creator'],
            allow_delegation=False,
            tools=[],
            verbose=True
        )

    @task
    def quiz_task(self) -> Task:
        return Task(
            config=self.tasks_config['quiz_task'],
            callback=self.callback_function,
            output_file='course_latest/5_quiz.md'
    )

    #  Find resources
    # ------------------------------------------------------------

    # @agent
    # def research_creator(self) -> Agent:
    #     return Agent(
    #         llm=self.llm,
    #         config=self.agents_config['research_creator'],
    #         allow_delegation=False,
    #         tools=[self.search_tool],
    #         verbose=True
    #     )

    # @task
    # def research_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['research_task'],
    #         callback=self.callback_function,
    #         output_file='course_latest/6_resources.md'
    # )

    @crew
    def crew(self) -> Crew:
        """Creates the CourseBuilder crew"""
        print("Creating the CourseBuilder crew...")
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            # max_rpm= 10,
            # task_callback=self.callback_function,
            verbose=True,
        )
