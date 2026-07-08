from agent import agent_ask
from config.messages import messages

GOODBYE = "Goodbye!"


def run_chat():
    print("AgentCalib chat. Type 'exit' or 'quit' to leave.")

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

        messages.append({"role": "user", "content": user_input})

        try:
            response = agent_ask(messages)
        except Exception as error:
            messages.pop()
            print(f"Error: {error}. Please try again.")
            continue

        messages.append({"role": "assistant", "content": response})
        print(f"Assistant: {response}")
