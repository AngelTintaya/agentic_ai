from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    model=Groq(id="llama-3.3-70b-Versatile"),

    # Set add_history_to_messages=true to add the previous chat history to the messages sent to the Model.
    add_history_to_messages=True,
    # Number of historical responses to add to the messages.
    num_history_responses=5,

    # description="You are an Car Shop Agent that will help customer to schedule car maintenance or answer doubtd related to the carshop.",
    description="You are an Car Shop Agent",
    task="You should help customer to schedule car maintenance or answer doubts related to the carshop",
    instructions=[
        "The answer should be in spanish"
        "If there is a typo, correct it to infer the date",
        "If year is missing, consider the year for next_week",
        "The answer should ask for confirmation if the infered date (format dd/mm/YYYY) for the car maintenance is correct",
        ],
    add_datetime_to_instructions=True,
    read_chat_history=True
)

print("Pregunta 1", "="*100)
query = "Quisiera reservar para el 10 de Enero"
response = agent.run(query)
print("Pregunta: ",query)
print(response.content)

print("Pregunta 2", "="*100)
query = 'What was my last question?'
response = agent.run(query)
print("Pregunta: ",query)
print(response.content)

print("Pregunta 3", "="*100)
query = 'Tienes disponibilidad para el cinco de Marzo'
response = agent.run(query)
print("Pregunta: ",query)
print(response.content)

print("Pregunta 4", "="*100)
query = 'What was my last question?'
response = agent.run(query)
print("Pregunta: ",query)
print(response.content)

print("Pregunta 5", "="*100)
query = 'Cuantas preguntas te hice?'
response = agent.run(query)
print("Pregunta: ",query)
print(response.content)