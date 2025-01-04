from phi.agent import Agent
from phi.model.groq import Groq
# from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

load_dotenv()

web_agent = Agent(
    name="Web Agent",
    model=Groq(id="llama-3.3-70b-Versatile"),
    # model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True
)

# If we use only the model, it will contains only static knowledge.
# If we want to get more current data, we need to give them tools.
# So agents use tools to fetch the latest information.
finance_agent = Agent(
    name="Finance Agent",
    role="Get Financial Data",
    model=Groq(id="llama-3.3-70b-Versatile"),
    # model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=True,
    markdown=True
)

agent_team = Agent(
    model=Groq(id="llama-3.3-70b-Versatile"),
    team=[web_agent, finance_agent],
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True
)

query = "Summarize analyst recommendations and share the latest news for NVDA"
agent_team.print_response(query, stream=True)
