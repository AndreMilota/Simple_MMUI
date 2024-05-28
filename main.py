
import random
import os
import GUI as gui

# gestures = ""
# # the GUI stuff --------------------------------------------------------------------------
# def change_color(button):
#     # Generate random RGB color values
#     r = random.randint(0, 255)
#     g = random.randint(0, 255)
#     b = random.randint(0, 255)
#
#     # Convert RGB values to hexadecimal color code
#     color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
#
#     # Change the background color of the button
#     button.config(bg=color)
# def run_callback():
#     global gestures
#     # get the text from the text entry box
#     command = text_entry.get("1.0", "end-1c")
#     print("command", command)
#     if gestures != "":
#         command += ". The user clicked on " + gestures
#     r = agent_executor.invoke(
#         {
#             "input": command,
#         }
#     )
#     gestures = ""
#     print(r)
#
#
# def button1_clicked():
#     # Placeholder function for the first button click event
#     global gestures
#     gestures = "button 1"
#     print("Button 1 clicked")
#
# def button2_clicked():
#     # Placeholder function for the second button click event
#     global gestures
#     gestures = "button 2"
#     print("Button 2 clicked")

# Create main window
# root = tk.Tk()
# root.title("GUI Example")

# Create text entry box
# text_entry = tk.Text(root, width=50, height=20)
# text_entry.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
#
# # Create Button 1
# button1 = tk.Button(root, text="Button 1", command=button1_clicked)
# button1.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ne")
#
# # Create Button 2
# button2 = tk.Button(root, text="Button 2", command=button2_clicked)
# button2.grid(row=0, column=1, padx=(0, 10), pady=40, sticky="ne")
#
# # Create "Run" button
# run_button = tk.Button(root, text="Run", command=run_callback)
# run_button.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
#
# # Configure grid row and column weights
# root.grid_rowconfigure(0, weight=1)
# root.grid_rowconfigure(1, weight=1)
# root.grid_rowconfigure(2, weight=0)
# root.grid_columnconfigure(0, weight=1)
# root.grid_columnconfigure(1, weight=0)
#
# print("the GUI is up and running")

# load the lange chain stuff
open_ai_key = os.environ.get('OPENAI_API_KEY')
print("len(OPENAI_API_KEY)", len(open_ai_key))
hugging_face_key = os.environ.get('HUGGING_FACE_API_KEY')
print("len(HUGGING_FACE_API_KEY)", len(hugging_face_key))

langchain_api_key = os.environ.get('LANG_CHAIN_KEY')
print("len(LANG_CHAIN_KEY)", len(langchain_api_key))

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(api_key=open_ai_key)

from langchain_core.tools import tool

@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    out = first_int * second_int
    return out

from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import PromptTemplate
# for memory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory



# Get the prompt to use - can be replaced with any prompt that includes variables "agent_scratchpad" and "input"!
prompt = hub.pull("hwchase17/openai-tools-agent")
prompt.pretty_print()
print(type(prompt))
print(dir(prompt))
for e in prompt.messages:
    print(e)


#
# template = """You are a multimodal agent. You can control the colors of widgets in a GUI and perform. You will get descriptions of the widgets the user clicked on and the user's commands.
# New_Question: {command}
# Description_of_gesture: {gesture}
# """
# prompt = PromptTemplate.from_template(template)

@tool
def add(first_int: int, second_int: int) -> int:
    "Add two integers."
    return first_int + second_int

@tool
def exponentiate(base: int, exponent: int) -> int:
    "Exponentiate the base to the exponent power."
    return base**exponent

window = gui.Window()

@tool
def set_buttion_color(button_index: int, new_color: str) -> None:
    """Set the background color of a button. There are 2 buttons, 1 and 2"""
    button = [None, window.button1, window.button2][button_index]
    button.config(bg=new_color)

tools = [multiply, add, exponentiate, set_buttion_color]

# Construct the tool calling agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

window.set_agent_executor(agent_executor)
window.run()


