from phi.agent import Agent
# from phi.model.openai import OpenAIChat
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
# from phi.storage.agent.postgres import PgAgentStorage
from phi.storage.agent.sqlite import SqlAgentStorage

session_id = "5c8f799c-79fd-4ad7-ab23-678893a7426e"

agent = Agent(
    model=Groq(id="llama-3.3-70b-Versatile"),
    # storage=PgAgentStorage(table_name="agent_sessions", db_url="postgresql+psycopg://ai:ai@localhost:5532/ai"),
    storage=SqlAgentStorage(table_name="agent_sessions", db_file="tmp/agent_storage.db"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    add_history_to_messages=True,
    session_id=session_id,
)
# response = agent.run("How many people live in Canada?")
# print(response.content)

# INITAL QUESTIONS!!!!
# ================
# agent.print_response("How many people live in Lima - Peru?")
# agent.print_response("My name is Pepe")

# SECONDD QUESTION
# ================
# agent.print_response("What is their original language?")
# agent.print_response("Which country are we speaking about?")

# THIRD QUESTION
# ================
agent.print_response("What is my name?")

# all_messages = [m.model_dump(include={"role", "content"}) for m in agent.memory.messages]
# print("="*100)
# for messages in all_messages:
#     print(messages)
