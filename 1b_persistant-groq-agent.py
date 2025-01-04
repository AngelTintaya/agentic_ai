import json
from rich.console import Console
from rich.panel import Panel
from rich.json import JSON

from phi.agent import Agent
# from phi.model.openai import OpenAIChat
from phi.model.groq import Groq
from phi.storage.agent.sqlite import SqlAgentStorage
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    # model=OpenAIChat(id="gpt-4o"),
    model=Groq(id="llama-3.3-70b-Versatile"),
    # Store agent sessions in a database
    storage=SqlAgentStorage(table_name="agent_sessions", db_file="tmp/agent_storage.db"),
    # Set add_history_to_messages=true to add the previous chat history to the messages sent to the Model.
    add_history_to_messages=True,
    # Number of historical responses to add to the messages.
    num_history_responses=5,
    # The session_id is used to identify the session in the database
    # You can resume any session by providing a session_id
    # session_id="xxxx-xxxx-xxxx-xxxx",
    # Description creates a system prompt for the agent
    description="You are a helpful Car Shop Agent that always responds in a polite, upbeat and positive manner.",
    task="You should help customer to schedule car maintenance or answer doubts related to the carshop",
    instructions=[
        "The answer should be in spanish"
        "If there is a typo, correct it to infer the date",
        "If year is missing, consider the year for next_week",
        "The answer should ask for confirmation if the infered date (format dd/mm/YYYY) for the car maintenance is correct",
        ],
    # add_datetime_to_instructions=True,
    # read_chat_history=True
)

console = Console()


def print_chat_history(agent):
    # -*- Print history
    console.print(
        Panel(
            JSON(json.dumps([m.model_dump(include={"role", "content"}) for m in agent.memory.messages]), indent=4),
            title=f"Chat History for session_id: {agent.session_id}",
            expand=True,
        )
    )


# -*- Create a run
agent.print_response("Share a 5 sentence horror story", stream=True)
# -*- Print the chat history
print_chat_history(agent)

# -*- Ask a follow up question that continues the conversation
agent.print_response("What was my first message?", stream=True)
# -*- Print the chat history
print_chat_history(agent)