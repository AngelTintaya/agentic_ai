from phi.agent import Agent
# from phi.model.openai import OpenAIChat
from phi.model.groq import Groq
from phi.storage.agent.sqlite import SqlAgentStorage
from typing import Optional, List
from phi.storage.agent.sqlite import SqlAgentStorage

def get_session_id_from_phone(phone_number:int) -> str:
    session_id: Optional[str] = None

    # return session_id
    return None

def save_credentials_in_db(session_id: str, phone_number:int) -> None:
    return None

#def get_availability(session_id: str) -> bool:
#    return True

def ask_eva(query: str, phone_number:int, rules: List[str] = None) -> str:
    if rules is None:
        rules = []  # Initialize an empty list if none provided
    
    session_id = get_session_id_from_phone(phone_number)
    instructions = ["The answer should be in spanish"]
    instructions.extend(rules)

    # Shared Storage
    storage = SqlAgentStorage(table_name="agent_sessions", db_file="tmp/agent_storage.db")

    scheduler_agent=Agent(
        session_id=session_id,
        # model=OpenAIChat(id="gpt-4o"),
        model=Groq(id="llama-3.3-70b-Versatile"),
        name="Scheduler Agent",
        role="Schedule a car apointment",
        storage=storage,
        description="You are a friendly scheduler for car maintenance appointments.",
        task="Help customers schedule car maintenance appointments in a clear and friendly way.",
        instructions=[
            "Respond in Spanish for all interactions.",
            "When scheduling, always request a specific date.",
            "If the year is missing, assume it is in the year of the next week.",
            "Provide the date in 'dd/mm/YYYY' format and ask for confirmation.",
            "Once the date is confirmed, confirm the appointment warmly, thank the user, and express excitement to see them.",
        ],
        add_history_to_messages=True,
        num_history_responses=5,
        add_datetime_to_instructions=True,
        read_chat_history=True
    )

    faq_agent=Agent(
        session_id=session_id,
        # model=OpenAIChat(id="gpt-4o"),
        model=Groq(id="llama-3.3-70b-Versatile"),
        name="FAQ Agent",
        role="Answer car shop-related questions",
        storage=storage,
        description="You are an expert in answering car shop-related questions.",
        task="Provide clear and helpful answers to customers' questions about the car shop.",
        instructions=[
            "Respond in Spanish for all interactions.",
            "Use friendly and professional language.",
            "If unsure about a specific query, politely ask the user to clarify or provide additional information.",
        ],
        add_history_to_messages=True,
        num_history_responses=5,
        add_datetime_to_instructions=True,
        read_chat_history=True
    )

    main_agent = Agent(
        session_id=session_id,
        model=Groq(id="llama-3.3-70b-Versatile"),
        team=[scheduler_agent, faq_agent],
        storage=storage,
        description="You are a Car Shop Dialer Agent in Connectia.",
        task="Identify the user's needs and activate the appropriate specialized agent.",
        instructions=[
            "Respond in Spanish for all interactions.",
            "When scheduling, always request a specific date.",
            "If the year is missing, assume it is in the year of the next week.",
            "Provide the date in 'dd/mm/YYYY' format and ask for confirmation.",
            "Once the date is confirmed, confirm the appointment warmly, thank the user, and express excitement to see them.",
            "Use friendly and professional language.",
            "If unsure about a specific query, politely ask the user to clarify or provide additional information.",
        ],
        add_history_to_messages=True,
        num_history_responses=5,
        add_datetime_to_instructions=True,
        read_chat_history=True
    )

    if session_id is None:
        session_id = main_agent.session_id
        save_credentials_in_db(session_id, phone_number)
        print(f"Started Session: {session_id}\n")
    else:
        print(f"Continuing Session: {session_id}\n")

    response = main_agent.run(query)
    # print("Pregunta: ",query)
    # print(response.content)
    return response.content, session_id

rpta, session_id = ask_eva(
    'Hola',
    123456
    )
print(rpta)


rpta, session_id = ask_eva(
    'Quisiera agendar una cita',
    123456,
    rules=[
        "When asked to schedule, request for a date"
        ]
    )
print(rpta)

rpta, session_id = ask_eva(
    'Claro, el diez de Marzo',
    123456,
    rules=[
        "If year is missing, consider the year of the next week",
        "If a date is given, return it back in the formad dd/mm/YYYY, and ask to confirm if the date is correct",
        ]
    )
print(rpta)

rpta, session_id = ask_eva(
    'Si, es correcto',
    123456,
    rules=[
        "Only when date was confirmed or correct, always confirmcthat the car maintenance was done, and always end to hope to see them there",
        ]
    )
print(rpta)
