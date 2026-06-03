from langchain.agents import tool
from tools import call_emergency
from config import GROQ_API_KEY

from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent


# -----------------------------
# TOOL 1: Mental Health Support
# -----------------------------
@tool
def ask_mental_health_specialist(query: str) -> str:
    """
    Handles emotional or psychological concerns with empathetic support.
    The LLM will generate the response.
    """
    return query


# -----------------------------
# TOOL 2: Emergency Call
# -----------------------------
@tool
def emergency_call_tool() -> str:
    """
    Call emergency helpline if user is in crisis.
    """
    call_emergency()
    return "Emergency services have been contacted to help you."


# -----------------------------
# TOOL 3: Therapist Finder
# -----------------------------
@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """
    Finds therapists near a given location.
    """
    return (
        f"Here are some therapists near {location}:\n"
        "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
        "- Dr. James Patel - +1 (555) 987-6543\n"
        "- MindCare Counseling Center - +1 (555) 222-3333"
    )


# -----------------------------
# Tools List
# -----------------------------
tools = [
    ask_mental_health_specialist,
    emergency_call_tool,
    find_nearby_therapists_by_location
]


# -----------------------------
# Groq LLM
# -----------------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # fastest Groq model
    api_key=GROQ_API_KEY,
    temperature=0.3
)


# -----------------------------
# Create Agent
# -----------------------------
graph = create_react_agent(llm, tools=tools)


# -----------------------------
# System Prompt
# -----------------------------
SYSTEM_PROMPT = """
You are a compassionate AI therapist.

Your goals:
• Listen carefully
• Validate emotions
• Offer gentle guidance
• Ask open-ended questions

If the user expresses:
- suicidal thoughts
- self harm
- crisis

Immediately call `emergency_call_tool`.

If the user asks about therapists near them,
use `find_nearby_therapists_by_location`.

Otherwise respond warmly and supportively.
"""


# -----------------------------
# Parse Response
# -----------------------------
def parse_response(stream):

    tool_called_name = "None"
    final_response = None

    for s in stream:

        # tool calls
        tool_data = s.get("tools")
        if tool_data:
            tool_messages = tool_data.get("messages")

            if tool_messages:
                for msg in tool_messages:
                    tool_called_name = getattr(msg, "name", "None")

        # agent response
        agent_data = s.get("agent")

        if agent_data:
            messages = agent_data.get("messages")

            if messages:
                for msg in messages:
                    if msg.content:
                        final_response = msg.content

    return tool_called_name, final_response