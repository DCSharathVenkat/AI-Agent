from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

@tool
def calculator(a: float, b: float) -> str:
    """Perform basic arithmetic operations."""
    return f"Sum: {a + b}, Difference: {a - b}, Product: {a * b}, Quotient: {a / b if b != 0 else 'undefined'}"

def main():
    model = ChatOpenAI(temperature=0)
    
    tools = [calculator]
    agent_executor = create_react_agent(model,tools)
    print("Welcome! I'm your AI assistant. Type 'quit' to exit.")
    print("You can ask me to perform calculations or chat with me.")
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input == 'quit':
            print("Goodbye!")
            break
        
        print("\nAssistant: ", end="")
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        print()
        
if __name__ == "__main__":
    main()