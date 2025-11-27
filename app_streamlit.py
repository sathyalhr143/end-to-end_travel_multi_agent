# import streamlit as st
# from agent import multi_agent_travel_planner_with_language, main
# import asyncio 

# from src.exception import CustomException

# from src.prompt import *



# st.set_page_config(
#     page_title="Travel multi-agent",
#     page_icon="🤖",
#     layout="centered"
# )

# st.title("A Multi-agent Travel Agent")
# st.markdown("Provide a query to the agent and look at it give you an excellent travel itinerary for your travel plans ")

# query = st.chat_input("Provide a query about your travel plans")

# async def get_agent_response(user_input):
#     try:
#         response = await multi_agent_travel_planner_with_language(query)
#         return response
#     except Exception as e:
#         return f"An error occurred: {CustomException(e, sys)} "



# import streamlit as st
# import asyncio
# import sys
# import os
# import logging
# from dotenv import load_dotenv
# from src.exception import CustomException
# from agent import multi_agent_travel_planner_with_language


# # --- Page Configuration ---
# st.set_page_config(
#     page_title="AI Travel Planner",
#     page_icon="✈️",
#     layout="centered"
# )

# # --- Environment & Logging ---
# load_dotenv()
# logging.getLogger('asyncio').setLevel(logging.CRITICAL)

# # --- Import Agent Logic ---
# # Add current directory to path so we can import agent.py
# sys.path.append(os.getcwd())

# try:
#     # We import the specific function from your agent.py file
#     from agent import multi_agent_travel_planner_with_language
# except ImportError:
#     st.error("⚠️ Could not find 'agent.py'. Please ensure it is in the same directory as this script.")
#     st.stop()

# # --- Helper to Run Agent ---
# async def get_agent_response(user_input):
#     """
#     Runs the agent with the user's input.
#     """
#     try:
#         # We call the function from agent.py, passing the user_input
#         # NOTE: Ensure your agent.py function accepts an argument: 
#         # async def multi_agent_travel_planner_with_language(query):
#         response = await multi_agent_travel_planner_with_language(user_input)
#         return response
#     except TypeError as e:
#         return (
#             f"❌ **Integration Error**: The agent function in `agent.py` does not accept arguments.\n\n"
#             f"Please update `agent.py` to accept the query:\n"
#             f"`async def multi_agent_travel_planner_with_language(query):`"
#         )
#     except Exception as e:
#         return f"An error occurred: {CustomException(e, sys)} "

# # --- Sidebar ---
# with st.sidebar:
#     st.header("Agent Settings")
#     st.info("This app connects to your local AI Multi-Agent Travel Assistant developed using the BeeAI Framework.")
    
#     if st.button("Clear Chat History", type="primary"):
#         st.session_state.messages = []
#         st.rerun()

# # --- Main Interface ---
# st.title("✈️ AI Multi-Agent Travel Planner")
# st.caption("Developed using **BeeAI Framework** | Destination • Weather • Culture")
# st.caption("-by Sathyaraj Medipalli")

# # 1. Initialize Chat History
# if "messages" not in st.session_state:
#     st.session_state.messages = []
#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": "Hello! I am your Multi-Agent Travel Assistant. I can help with destinations, weather, and cultural tips. Where would you like to go?"
#     })

# # 2. Display Chat History
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # 3. Handle User Input
# if prompt := st.chat_input("E.g., Plan a 5-day trip to Tokyo..."):
    
#     # Display user message
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     # Generate Response
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
        
#         with st.spinner("Agents are coordinating (Researching destination 🗺️, Checking weather 🌤️, Analyzing culture ⛩️)..."):
#             # Run the async agent function
#             full_response = asyncio.run(get_agent_response(prompt))
            
#         message_placeholder.markdown(full_response)
    
#     # Save assistant response
#     st.session_state.messages.append({"role": "assistant", "content": full_response})
    
# print



############################################################
# import streamlit as st
# import asyncio
# import sys
# import os
# import logging
# import threading
# import queue
# import builtins
# from unittest.mock import patch
# from dotenv import load_dotenv
# from src.exception import CustomException
# import importlib

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="AI Travel Planner",
#     page_icon="✈️",
#     layout="centered"
# )

# # --- Environment & Logging ---
# load_dotenv()
# logging.getLogger('asyncio').setLevel(logging.CRITICAL)

# # --- Import Agent Logic ---
# sys.path.append(os.getcwd())

# try:
    
#     import agent
#     importlib.reload(agent)
#     from agent import multi_agent_travel_planner_with_language
    
# except ImportError:
#     st.error("⚠️ Could not find 'agent.py'. Please ensure it is in the same directory.")
#     st.stop()

# # --- Custom Agent Runner (Handles Background Thread & Input) ---
# class AgentRunner:
#     def __init__(self):
#         self.input_queue = queue.Queue()  # Request from Agent -> UI
#         self.output_queue = queue.Queue() # Response from UI -> Agent
#         self.result_queue = queue.Queue() # Final result
#         self.error_queue = queue.Queue()
#         self.thread = None
#         self.is_running = False
#         self.waiting_for_input = False

#     def start(self, user_prompt):
#         """Starts the agent in a separate thread."""
#         self.is_running = True
#         self.thread = threading.Thread(target=self._run_agent_thread, args=(user_prompt,),daemon=True)
#         self.thread.start()
        

#     def _custom_input(self, prompt=""):
#         """Intercepts input() calls from the agent."""
#         # Send the prompt (e.g., "Allow tool X?") to the UI
#         self.input_queue.put(prompt)
#         self.waiting_for_input = True
        
#         # Block and wait for UI response
#         user_response = self.output_queue.get()
        
#         self.waiting_for_input = False
#         return user_response

#     def _run_agent_thread(self, user_prompt):
#         """Runs the async agent logic with patched input."""
#         try:
#             # Patch 'input' so when BeeAI asks for permission, it calls _custom_input
#             with patch('builtins.input', side_effect=self._custom_input):
#                 response = asyncio.run(multi_agent_travel_planner_with_language(user_prompt))
#                 self.result_queue.put(response)
#         except Exception as e:
#             self.error_queue.put(CustomException(e, sys))
#         finally:
#             self.is_running = False

#     def send_approval(self, approved: bool):
#         """Sends Yes/No back to the agent."""
#         response = "yes" if approved else "no"
#         self.output_queue.put(response)

# # --- Initialize Session State ---
# if "runner" not in st.session_state:
#     st.session_state.runner = AgentRunner()
# if "messages" not in st.session_state:
#     st.session_state.messages = [{
#         "role": "assistant",
#         "content": "Hello! I am your Multi-Agent Travel Assistant. I need your approval to use specific tools. Where would you like to go?"
#     }]

# # --- Sidebar ---
# with st.sidebar:
#     st.header("Agent Settings")
#     st.info("Human-in-the-loop enabled. You will be asked to approve tool usage.")
#     if st.button("Clear Chat History", type="primary"):
#         st.session_state.messages = []
#         st.session_state.runner = AgentRunner() # Reset runner
#         st.rerun()

# # --- Main Interface ---
# st.title("✈️ AI Travel Planner (HITL)")
# st.caption("Powered by **BeeAI Framework** | Human-in-the-Loop Enabled")

# # 1. Display Chat History
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # 2. Handle Agent State & Updates
# runner = st.session_state.runner

# # If agent is running, check for updates
# if runner.is_running:
    
#     # A. Check if Agent is waiting for Human Approval
#     if not runner.input_queue.empty():
#         request_text = runner.input_queue.get() # Get the specific request (e.g. "Allow WeatherTool?")
        
#         with st.chat_message("assistant"):
#             st.warning(f"✋ **Permission Requested**\n\nThe agent wants to: `{request_text}`")
#             col1, col2 = st.columns(2)
#             with col1:
#                 if st.button("✅ Approve", key="approve_btn"):
#                     runner.send_approval(True)
#                     st.rerun()
#             with col2:
#                 if st.button("❌ Deny", key="deny_btn"):
#                     runner.send_approval(False)
#                     st.rerun()
#         st.stop() # Stop script here to wait for button click

#     # B. Show Spinner while working (if not waiting)
#     elif not runner.waiting_for_input:
#         with st.chat_message("assistant"):
#             with st.spinner("Agents are thinking & coordinating..."):
#                 try:
#                     # Non-blocking wait to allow Streamlit loop to refresh
#                     # This effectively polls the thread status
#                     import time
#                     time.sleep(1) 
#                     st.rerun() 
#                 except Exception:
#                     pass

# # C. Check for Final Results
# if not runner.result_queue.empty():
#     result = runner.result_queue.get()
#     st.session_state.messages.append({"role": "assistant", "content": result})
#     st.rerun()

# # D. Check for Errors
# if not runner.error_queue.empty():
#     error_msg = runner.error_queue.get()
#     st.error(f"Agent Error: {error_msg}")
#     st.session_state.messages.append({"role": "assistant", "content": f"Error: {error_msg}"})

# # 3. Handle User Input (Only if agent is NOT running)
# if not runner.is_running and (prompt := st.chat_input("E.g., Plan a 5-day trip to Tokyo...")):
#     # Display user message
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     st.session_state.messages.append({"role": "user", "content": prompt})
    
#     # Start Agent
#     runner.start(prompt)
#     st.rerun()
    
    
    ###################################################
import streamlit as st
import asyncio
import sys
import os
import logging
import threading
import queue
import builtins
import importlib
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="centered"
)

# --- Environment & Logging ---
load_dotenv()
logging.getLogger('asyncio').setLevel(logging.CRITICAL)
logging.getLogger('wikipediaapi').setLevel(logging.WARNING)

# --- Import Agent Logic & Logger ---
sys.path.append(os.getcwd())

# 1. Setup Logger (Force File Handler to bypass Streamlit defaults)
try:
    from src.logger import logger, LOG_FILE_PATH
    
    # Check if we need to add a file handler (Streamlit sometimes blocks basicConfig)
    has_file_handler = any(isinstance(h, logging.FileHandler) for h in logger.handlers)
    if not has_file_handler:
        file_handler = logging.FileHandler(LOG_FILE_PATH)
        formatter = logging.Formatter('[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        
except ImportError:
    logger = logging.getLogger(__name__)

# 2. Hard Reload of Agent Module
try:
    # Explicitly remove 'agent' from sys.modules to force a fresh load from disk
    if 'agent' in sys.modules:
        del sys.modules['agent']
    
    import agent
    from agent import multi_agent_travel_planner_with_language
    logger.info("Successfully reloaded agent module.")
except ImportError:
    st.error("⚠️ Could not find 'agent.py'. Please ensure it is in the same directory.")
    st.stop()

# --- Custom Agent Runner ---
class AgentRunner:
    def __init__(self):
        self.output_queue = queue.Queue() # Response from UI -> Agent
        self.result_queue = queue.Queue() # Final result from Agent
        self.error_queue = queue.Queue()  # Errors
        
        # State flags
        self.thread = None
        self.is_running = False
        self.waiting_for_input = False
        self.pending_request = None # Stores the prompt text (e.g., "Allow tool X?")

    def start(self, user_prompt):
        """Starts the agent in a separate daemon thread."""
        if self.is_running:
            return
        
        logger.info(f"Starting AgentRunner with prompt: {user_prompt}")
            
        self.is_running = True
        self.waiting_for_input = False
        self.pending_request = None
        
        self.thread = threading.Thread(
            target=self._run_agent_thread, 
            args=(user_prompt,),
            daemon=True # Critical: Ensures thread dies if script stops
        )
        self.thread.start()

    def _custom_input(self, prompt=""):
        """
        Intercepts input() calls. 
        This runs inside the background thread.
        """
        # 1. Signal UI that we need input
        logger.info(f"Agent requested input: {prompt}")
        self.pending_request = prompt if prompt else "Agent requested permission."
        self.waiting_for_input = True
        
        # 2. Block and wait for response from UI
        # This blocks the agent thread until the user clicks a button
        user_response = self.output_queue.get()
        logger.info(f"User responded: {user_response}")
        
        # 3. Reset state and return answer to agent
        self.waiting_for_input = False
        self.pending_request = None
        return user_response

    def _run_agent_thread(self, user_prompt):
        """Runs the async agent logic with patched inputs."""
        try:
            # Patch both input() and sys.stdin to be safe
            with patch('builtins.input', side_effect=self._custom_input):
                with patch('sys.stdin', new=MagicMock()) as mock_stdin:
                    mock_stdin.read.side_effect = self._custom_input
                    mock_stdin.readline.side_effect = self._custom_input
                    
                    # Run the agent
                    response = asyncio.run(multi_agent_travel_planner_with_language(user_prompt))
                    
                    if response is None:
                        msg = "⚠️ Agent returned `None`. Did you add `return` to the end of `agent.py`?"
                        logger.error(msg)
                        response = msg
                    else:
                        logger.info("Agent finished successfully.")
                    
                    self.result_queue.put(response)
                    
        except Exception as e:
            logger.error(f"Agent thread failed: {str(e)}")
            self.error_queue.put(str(e))
        finally:
            self.is_running = False

    def send_approval(self, approved: bool):
        """Called by UI to send answer to agent."""
        response = "y" if approved else "n"
        self.output_queue.put(response)

# --- Initialize Session State ---
if "runner" not in st.session_state:
    st.session_state.runner = AgentRunner()
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! I am Atlas your Multi-Agent Travel Assistant. Where would you like to go?"
    }]

# --- Sidebar ---
with st.sidebar:
    st.header("Agent Settings")
    # st.info("Human-in-the-loop disabled.")
    
    # Status Indicator
    runner = st.session_state.runner
    if runner.is_running:
        if runner.waiting_for_input:
            st.warning("⚠️ Waiting for your input")
        else:
            st.success("🔄 Agent is running...")
    else:
        st.write("💤 Agent is idle")

    if st.button("Clear Chat History", type="primary"):
        st.session_state.messages = []
        st.session_state.runner = AgentRunner()
        st.rerun()

# --- Main Interface ---
st.title("✈️ AI Travel Planner (HITL)")
st.caption("Powered by **BeeAI Framework**")

# 1. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. Handle Agent Interaction
runner = st.session_state.runner

if runner.is_running:
    
    # CASE A: Agent is waiting for user permission
    if runner.waiting_for_input and runner.pending_request:
        with st.chat_message("assistant"):
            st.warning(f"✋ **Permission Requested**\n\nAgent asking: `{runner.pending_request}`")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Approve", key="btn_yes"):
                    runner.send_approval(True)
                    st.rerun()
            with col2:
                if st.button("❌ Deny", key="btn_no"):
                    runner.send_approval(False)
                    st.rerun()
        st.stop() # Halt execution so buttons stay visible

    # CASE B: Agent is working (show spinner)
    else:
        with st.chat_message("assistant"):
            with st.spinner("Agents are extracting weather, cultural and information about vietnam from web while thninking and coordinating with each other..."):
                import time
                time.sleep(5) # Slight delay to allow thread updates
                st.rerun()    # Poll for updates

# CASE C: Agent finished successfully
if not runner.result_queue.empty():
    result = runner.result_queue.get()
    st.session_state.messages.append({"role": "assistant", "content": result})
    st.rerun()

# CASE D: Agent crashed
if not runner.error_queue.empty():
    error_msg = runner.error_queue.get()
    st.session_state.messages.append({"role": "assistant", "content": f"❌ Error: {error_msg}"})
    st.rerun()

# 3. Handle New User Input
if not runner.is_running and (prompt := st.chat_input("E.g., Plan a 5-day trip to India...")):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    runner.start(prompt)
    st.rerun()