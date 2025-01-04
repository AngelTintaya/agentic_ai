from phi.agent import Agent
from phi.model.groq import Groq
# from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

load_dotenv()

def get_company_symbol(company: str) -> str:
    """Use this function to get the symbol for a company.

    Args:
        company (str): The name of the company.

    Returns:
        str: The symbol of the company.
    """
    symbols = {
        "Phidata": "MSFT",
        "Infosys": "INFY",
        "Tesla": "TSLA",
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Amazon": "AMZN",
        "Google": "GOOGL",
    }

    return symbols.get(company, "Unknown")

# If we use only the model, it will contains only static knowledge.
# If we want to get more current data, we need to give them tools.
# So agents use tools to fetch the latest information.
agent = Agent(
    model=Groq(id="llama-3.3-70b-Versatile"),
    # model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True), get_company_symbol],
    instructions=[
        "Use tables to display data.",
        "If you do not know the company symbol, please use get_company_symbol, even if it is not a public company"
        ],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True
)

query = "Summarize and compare analyst recommendations and fundamentals for TSLA and Phidata"
agent.print_response(query)
