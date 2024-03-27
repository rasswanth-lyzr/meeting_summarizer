from dotenv import load_dotenv
import os
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent
from lyzr_automata import Task
from lyzr_automata.tasks.task_literals import InputType, OutputType
from lyzr_automata.tools.prebuilt_tools import send_email_by_smtp_tool

from helpers import get_attendees_list, get_transcript_content

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL = os.getenv("EMAIL") # Email ID to send emails from
PASSWORD = os.getenv("PASSWORD") # App password of the email

# GPT 4 Text Model
open_ai_model_text = OpenAIModel(
    api_key= OPENAI_API_KEY,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)

# Intructions for our Agent
summarizer_agent = Agent(
        prompt_persona="You are an intelligent agent that can summarize WebVTT content into a meaninful summary",
        role="WebVTT summarizer",
    )

### ASSUMING YOU HAVE ALL THE BELOW PARAMS
### IF NOT, FOLLOW - https://registeredapps.hosting.portal.azure.net/registeredapps/Content/1.0.2622.777/Quickstarts/en/PythonQuickstartPage.html?clientOptimizations=undefined&l=en.en-gb&trustedAuthority=https%3A%2F%2Fportal.azure.com&shellVersion=undefined
input_transcript = get_transcript_content(meeting_ID, transcript_ID, token)
input_email_list = get_attendees_list(meeting_ID, report_ID, token)

def email_draft_function(input_transcript):
    # Draft a summary Task
    summarize_content_task = Task(
        name="Transcript summarizer",
        agent=summarizer_agent,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=open_ai_model_text,
        instructions="Summarize the WebVTT input into a meaningful Minutes of Meeting that captures immportant details and speakers. Return only the speaker name and their corresponding suammary [!IMPORTANT] Use HTML table to revise the email and beautify it", # Prompt Engineering
        log_output=True,
        enhance_prompt=False,
        default_input=input_transcript # Input for the task
    ).execute()

    return summarize_content_task # Return Output

# Email config
def email_sender_function(summarize_content_task, input_email_list):
    email_sender = send_email_by_smtp_tool(
        username=EMAIL,
        password=PASSWORD,
        host="smtp.gmail.com",
        port=587,
        sender_email=EMAIL
    )

    # Send email Task
    send_email_task = Task(
        name = "Send Email Task",
        tool = email_sender,
        instructions="Send Email",
        model=open_ai_model_text,
        input_tasks = [summarize_content_task],
        default_input = input_email_list,
        previous_output = summarize_content_task
    ).execute()

# ALTERNATIVELY, you can add these 2 Tasks into a LinearSyncPipleline too!