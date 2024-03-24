import json
import random
import gradio as gr

USER_ROLES = {
    1: "Employee",
    2: "CXO (Chief Experience Officer)",
    3: "Service Line Head",
    4: "Corporate Strategy",
}

INFO_CLASSIFICATIONS = {
    "Public": ["Employee", "CXO (Chief Experience Officer)"],
    "Confidential": ["Service Line Head", "Corporate Strategy"],
}

ACCESS_CONTROL = {
    role: classifications for role, classifications in INFO_CLASSIFICATIONS.items()
    if role in classifications
}

def load_chatbot_data(filename):
    """Loads chatbot data (intents and responses) from a JSON file."""
    try:
        with open(filename, "r") as data_file:
            return json.load(data_file)
    except FileNotFoundError:
        print(f"Error: Could not find data file '{filename}'.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{filename}'.")
        return {}

def validate_user_role(username, password, user_role):
    """Validates the user role with a fake username and password."""
    # Replace this with your actual validation logic
    fake_credentials = {
        "Employee": ("employee_username", "employee_password"),
        "CXO (Chief Experience Officer)": ("cxo_username", "cxo_password"),
        "Service Line Head": ("service_username", "service_password"),
        "Corporate Strategy": ("strategy_username", "strategy_password")
    }
    if (username, password) == fake_credentials.get(user_role):
        return True
    else:
        return False

def process_message(message, user_role, username, password):
    """Processes a user message based on access control and loaded chatbot data."""
    allowed_classifications = ACCESS_CONTROL.get(user_role, [])
    chatbot_data = load_chatbot_data("infosys.json")

    if not chatbot_data:
        return "Sorry, I'm having trouble accessing my knowledge base. Please try again later."

    intents = chatbot_data.get("intents", [])
    response = "I apologize, I didn't quite understand that."

    for intent in intents:
        patterns = intent.get("patterns", [])
        for pattern in patterns:
            if message.lower() == pattern.lower():
                classification = intent.get("classification")
                if classification:
                    if classification in allowed_classifications:
                        response = random.choice(intent["responses"])
                        break
                    else:
                        return (
                            f"Sorry, you don't have permission to access "
                            f"'{classification}' information."
                        )
                else:
                    response = random.choice(intent["responses"])
                    break

    return response

# Gradio interface with text input and output
interface = gr.Interface(
    fn=process_message,
    inputs=[
        gr.Textbox(label="Your message"),
        gr.Dropdown(label="Your role", choices=list(USER_ROLES.values())),
        gr.Textbox(label="Username"),
        gr.Textbox(label="Password", type="password", placeholder="Password")
    ],
    outputs="text",
    title="Infosys Chatbot",
    description="Ask your questions here!",
)

# Launch the Gradio interface
interface.launch()
