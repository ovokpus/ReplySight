"""
LLM Agent with Direct Tool Binding for ReplySight.

This module demonstrates how to bind tools directly to an LLM,
allowing the model to autonomously decide which tools to call
and when to call them (including in parallel).
"""

import os
from typing import Dict, Any, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langsmith import traceable

from backend.tools import ArxivInsightsTool, TavilyExamplesTool, ResponseComposerTool


class ReplySightAgent:
    """
    LLM Agent that can autonomously call tools to generate responses.
    
    This agent binds tools directly to the LLM, allowing it to:
    - Decide which tools to call based on the complaint
    - Call multiple tools in parallel when possible
    - Chain tool calls based on intermediate results
    """

    def __init__(self, tavily_api_key: Optional[str] = None):
        """
        Initialize the ReplySight agent with tool-bound LLM.
        
        Args:
            tavily_api_key: API key for Tavily search service
        """
        # Initialize tools
        self.arxiv_tool = ArxivInsightsTool()
        self.tavily_tool = TavilyExamplesTool(api_key=tavily_api_key)
        self.composer_tool = ResponseComposerTool()
        
        # Create tool list for LLM binding
        self.tools = [self.arxiv_tool, self.tavily_tool]
        
        # Initialize LLM with tools bound
        self.llm = ChatOpenAI(
            model="gpt-4o",  # Using GPT-4 for better tool calling
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Bind tools to LLM for autonomous calling
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Create agent with tools
        self.agent = self._create_agent()

    def _create_agent(self) -> AgentExecutor:
        """
        Create an OpenAI tools agent that can call tools autonomously.
        
        Returns:
            Configured AgentExecutor
        """
        # Define agent prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert customer service AI assistant with access to research tools.

                Your goal is to help craft empathetic, research-backed responses to customer complaints.

                Available tools:
                - arxiv_insights: Fetch academic research on customer service topics
                - tavily_examples: Search for customer service best practices and examples

                When given a customer complaint:
                1. Use BOTH tools to gather insights and examples (you can call them in parallel)
                2. Analyze the research and examples to understand best practices
                3. Provide a comprehensive summary of findings that can be used to craft an empathetic response

                Be thorough in your research gathering, but efficient in your tool usage."""
                ),
            ("user", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

        # Create the agent
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5
        )

    @traceable(name="agent_research")
    async def research_complaint(self, complaint: str) -> Dict[str, Any]:
        """
        Use the LLM agent to research a complaint and gather insights.
        
        The LLM will autonomously decide which tools to call and when.
        
        Args:
            complaint: Customer complaint text
            
        Returns:
            Dictionary with research findings
        """
        result = await self.agent.ainvoke({
            "input": f"""Analyze this customer complaint and gather research to help craft an empathetic response:

COMPLAINT: {complaint}

Please use your available tools to:
1. Find academic research relevant to this type of complaint
2. Search for best practice examples for similar situations
3. Provide a summary of key insights for crafting an empathetic response"""
        })
        
        return {
            "research_summary": result["output"],
            "tool_calls": result.get("intermediate_steps", [])
        }

    @traceable(name="agent_full_response")
    async def generate_full_response(self, complaint: str) -> Dict[str, Any]:
        """
        Generate a complete response using agent research + composer tool.
        
        Args:
            complaint: Customer complaint text
            
        Returns:
            Dictionary with final response and citations
        """
        # Step 1: Agent researches the complaint
        research = await self.research_complaint(complaint)
        
        # Step 2: Extract insights and examples from research
        # This would need parsing logic based on agent output
        insights = {"summary": research["research_summary"]}
        examples = {"summary": research["research_summary"]}
        
        # Step 3: Use composer tool to create final response
        response = await self.composer_tool._arun(complaint, insights, examples)
        
        return {
            "reply": response["response"],
            "citations": response.get("citations", []),
            "research_details": research["research_summary"]
        }


class ParallelToolLLM:
    """
    Simplified example showing direct parallel tool calling with LLM.
    """

    def __init__(self, tavily_api_key: Optional[str] = None):
        """Initialize LLM with bound tools."""
        self.arxiv_tool = ArxivInsightsTool()
        self.tavily_tool = TavilyExamplesTool(api_key=tavily_api_key)
        
        # Create LLM with tools bound
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY")
        ).bind_tools([self.arxiv_tool, self.tavily_tool])

    @traceable(name="parallel_tool_calling")
    async def call_tools_parallel(self, complaint: str) -> Dict[str, Any]:
        """
        Example of LLM calling tools autonomously.
        
        Args:
            complaint: Customer complaint
            
        Returns:
            LLM response with potential tool calls
        """
        messages = [
            HumanMessage(content=f"""I need to research this customer complaint to craft an empathetic response. 
            Please use your available tools to gather relevant academic insights and best practice examples.

            Complaint: {complaint}
            
            Use both tools to gather comprehensive research.""")
        ]
        
        # LLM will decide which tools to call
        response = await self.llm.ainvoke(messages)
        
        return {
            "response": response.content,
            "tool_calls": response.tool_calls if hasattr(response, 'tool_calls') else []
        }


# Factory functions
def create_replysight_agent(tavily_api_key: Optional[str] = None) -> ReplySightAgent:
    """Create a ReplySight agent with tool-bound LLM."""
    return ReplySightAgent(tavily_api_key=tavily_api_key)

def create_parallel_tool_llm(tavily_api_key: Optional[str] = None) -> ParallelToolLLM:
    """Create a simple parallel tool calling LLM."""
    return ParallelToolLLM(tavily_api_key=tavily_api_key) 