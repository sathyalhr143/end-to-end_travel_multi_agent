import asyncio
import logging

from src.exception import CustomException
from src.logger import logger
from src.prompt import *

from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.agents.requirement.requirements.conditional import ConditionalRequirement
from beeai_framework.agents.requirement.requirements.ask_permission import AskPermissionRequirement
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.backend import ChatModel, ChatModelParameters
from beeai_framework.tools.search.wikipedia import WikipediaTool
from beeai_framework.tools.weather import OpenMeteoTool
from beeai_framework.tools.think import ThinkTool
from beeai_framework.tools.handoff import HandoffTool
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool

from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

import os

from dotenv import load_dotenv

load_dotenv()



async def multi_agent_travel_planner_with_language(user_query=input_query):
    """
    Advanced Multi-Agent Travel Planning System with Language Expert
    
    This system demonstrates:
    1. Specialized agent roles and coordination
    2. Tool-based inter-agent communication
    3. Requirements-based execution control
    4. Language and cultural expertise integration
    5. Comprehensive travel planning workflow
    """
    
    # Initialize the language model
    llm = ChatModel.from_name(os.getenv("LLM_CHAT_MODEL_NAME", "openai:gpt-4o-mini"),
        ChatModelParameters(temperature=0)
    )
    
    llm.allow_parallel_tool_calls = True
    
    # === AGENT 1: DESTINATION RESEARCH EXPERT ===
    destination_expert = RequirementAgent(
        llm=llm,
        
        tools=[WikipediaTool(), ThinkTool()],
        memory=UnconstrainedMemory(),
        instructions=destination_expert_instruction,
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        requirements=[
            ConditionalRequirement(
                ThinkTool,
                force_at_step=1,
                min_invocations=1,
                max_invocations=5,
                consecutive_allowed=False
            ),
            ConditionalRequirement(
                WikipediaTool,
                only_after=[ThinkTool],
                min_invocations=1,
                max_invocations=4,
                consecutive_allowed=False
            ),
        ]
    )
    
    # === AGENT 2: TRAVEL METEOROLOGIST ===
    travel_meteorologist = RequirementAgent(
        llm=llm,
        tools=[OpenMeteoTool(), ThinkTool()],
        memory=UnconstrainedMemory(),
        instructions=travel_meteorologist_instruction,
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        requirements=[
            ConditionalRequirement(
                ThinkTool,
                force_at_step=1,
                min_invocations=1,
                max_invocations=2
            ),
            ConditionalRequirement(
                OpenMeteoTool,
                only_after=[ThinkTool],
                min_invocations=1,
                max_invocations=1
            )
        ]
    )
    
    # === AGENT 3: LANGUAGE & CULTURAL EXPERT ===
    language_and_culture_expert = RequirementAgent(
        llm=llm,
        tools=[WikipediaTool(), ThinkTool()],
        memory=UnconstrainedMemory(),
        instructions=lang_and_cultural_expert_instruction,
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        requirements=[
            ConditionalRequirement(
                ThinkTool,
                force_at_step=1,
                min_invocations=1,
                max_invocations=3,
                consecutive_allowed=False
            ),
        ]
    )
    
    # === AGENT 4: TRAVEL COORDINATOR (MAIN INTERFACE) ===
    # Create handoff tools for coordination with unique names
    handoff_to_destination = HandoffTool(
        destination_expert,
        name="DestinationResearch",
        description="Consult our Destination Research Expert for comprehensive information about travel destinations, attractions, and practical travel guidance."
    )
    handoff_to_weather = HandoffTool(
        travel_meteorologist,
        name="WeatherPlanning", 
        description="Consult our Travel Meteorologist for weather forecasts, climate analysis, and weather-appropriate travel recommendations."
    )
    handoff_to_language = HandoffTool(
        language_and_culture_expert,
        name="LanguageCulturalGuidance",
        description="Consult our Language & Cultural Expert for essential phrases, cultural etiquette, and communication guidance for respectful travel."
    )
    
    travel_coordinator = RequirementAgent(
        llm=llm,
        tools=[handoff_to_destination, handoff_to_weather, handoff_to_language, ThinkTool()],
        memory=UnconstrainedMemory(),
        instructions=travel_coordinator_instruction,
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        requirements=[
            ConditionalRequirement(ThinkTool, consecutive_allowed=False),
            # AskPermissionRequirement([handoff_to_destination, handoff_to_weather, handoff_to_language])
        ]
    )
    

    query = user_query
    # """I'm planning a 2-week cultural immersion trip to Japan (Tokyo and Osaka) as a first-time visitor. 
    # I want to experience traditional culture, visit historical sites, and interact with locals. 
    # I speak only English and want to be respectful of Japanese customs. 
    # What should I know about the destination, weather expectations, and language/cultural tips?"""
    
    # result = await travel_coordinator.run(query)
    # # print(f"\n📋 Comprehensive Travel Plan:\n{result.answer.text}")cle
    
    

    try:
        result = await travel_coordinator.run(query)
        print(f"full result dict: \n{result.model_dump()}")
        print(f"\n📋 Comprehensive Travel Plan:\n{result.output_structured.response}")
        
        return result.output_structured.response
    
    except Exception as e:
        print("\n" + "---" * 10)
        print("🔴 A SPECIFIC ERROR OCCURRED 🔴")
        print(f"Error Type: {type(e)}")
        print(f"Error Details: {CustomException(e,sys)}")
        
        # This will often show the *original* Google API error
        if e.__cause__:
            print(f"\nOriginal Cause: {e.__cause__}")
        print("---" * 10 + "\n")

async def main(input_query) -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL)
    
    await multi_agent_travel_planner_with_language(input_query)

if __name__ == "__main__":
    input_q= input('enter')
    response = asyncio.run(main(input_query(input_q)))
    print(response)