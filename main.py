import os
import GUI as gui

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

window = gui.Window()

@tool
def set_buttion_color(button_index: int, new_color: str) -> None:
    """Set the background color of a button. There are 2 buttons, 1 and 2"""
    button = [None, window.button1, window.button2][button_index]
    button.config(bg=new_color)

tools = [set_buttion_color]

# Construct the tool calling agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

window.set_agent_executor(agent_executor)
window.run()
