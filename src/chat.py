from core.agent import agent_run
from config.messages import messages

GOODBYE = "Goodbye!"

def run_chat():
    print("Mosfet chat. Type 'exit' or 'quit' to leave.")

    while True:
        try:
            user_input = input("You: ")
        except (KeyboardInterrupt, EOFError):
            print(f"\n{GOODBYE}")
            break

        user_input = user_input.strip()

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print(GOODBYE)
            break

        try:
            response = agent_run(messages, user_input)
        except Exception as error:
            print(f"Error: {error}. Please try again.")
            continue

        print(f"Assistant: {response}")
