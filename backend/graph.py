"""
LangGraph implementation for the ReplySight response generation workflow.

This module defines an agent-based graph structure using LangGraph's prebuilt ToolNode 
that orchestrates intelligent tool calling for research insights and examples, 
then composes them into empathetic customer service responses with full LangSmith 
tracing and visualization.
"""

import asyncio
import time
import os
from typing import Dict, Any, List, Optional, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langsmith import traceable
from pydantic import BaseModel
from typing_extensions import TypedDict, Annotated
import operator

from backend.tools import ArxivInsightsTool, TavilyExamplesTool, ResponseComposerTool


class AgentState(TypedDict):
    """
    Agent state model for the ToolNode-based workflow.
    
    This class defines the state that flows through the LangGraph,
    using messages for ToolNode compatibility and tracking workflow progress.
    """
    messages: Annotated[List[Any], operator.add]
    complaint: str
    insights: Dict[str, Any]
    examples: Dict[str, Any]
    response: str
    citations: List[str]
    latency_ms: int
    start_time: float
    iteration_count: int
    decision: str  # "continue", "arxiv_tools", "tavily_tools", "compose", "end"
    arxiv_complete: bool
    tavily_complete: bool
    helpfulness_score: float


class ReplySightAgent:
    """
    LangGraph agent workflow for generating research-backed customer service responses.
    
    This class orchestrates an intelligent agent-based workflow with separate tool nodes:
    1. Agent analyzes complaint and decides which tools to call
    2. Individual ToolNodes for ArXiv, Tavily, and Response Composer
    3. Decision logic with helpfulness checking and specific tool routing
    4. Response composition with citations when ready
    """

    def __init__(self, tavily_api_key: Optional[str] = None):
        """
        Initialize the ReplySight agent workflow with separate tool nodes.
        
        Args:
            tavily_api_key: API key for Tavily search service
        """
        # Initialize individual tools
        self.arxiv_tool = ArxivInsightsTool()
        self.tavily_tool = TavilyExamplesTool(api_key=tavily_api_key or "placeholder")
        self.composer_tool = ResponseComposerTool()
        
        # Create separate ToolNodes for each tool
        self.arxiv_node = ToolNode([self.arxiv_tool])
        self.tavily_node = ToolNode([self.tavily_tool])
        self.composer_node = ToolNode([self.composer_tool])
        
        # Create tool list for LLM binding (research tools only)
        self.research_tools = [self.arxiv_tool, self.tavily_tool]

        # Initialize LLM for agent decisions
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY") or "placeholder"
        ).bind_tools(self.research_tools)
        
        # Initialize helpfulness checker LLM
        self.helpfulness_checker = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY") or "placeholder"
        )

        # Build the graph
        self.graph = self._build_graph()
        self.compiled_graph = self.graph.compile(
            checkpointer=MemorySaver(),
            interrupt_before=[]
        )

    @traceable(name="agent_call_model")
    def call_model(self, state: AgentState) -> AgentState:
        """
        Agent function that analyzes the complaint and decides which tools to call.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated state with agent's decision and tool calls
        """
        messages = state["messages"]
        
        # If this is the first call, create the initial system message
        if len(messages) == 0 or not any(isinstance(msg, SystemMessage) for msg in messages):
            arxiv_status = "✅ Complete" if state.get("arxiv_complete") else "⏳ Pending"
            tavily_status = "✅ Complete" if state.get("tavily_complete") else "⏳ Pending"
            
            system_message = SystemMessage(content=f"""You are an expert customer service research assistant. Your job is to analyze customer complaints and provide helpful, empathetic responses.

COMPLAINT: {state['complaint']}

RESEARCH STATUS:
- ArXiv Research: {arxiv_status}
- Tavily Examples: {tavily_status}

Available tools:
- arxiv_insights: Fetch academic research on customer service, empathy, service recovery
- tavily_examples: Search for customer service best practices and real examples

Your workflow:
1. Analyze the complaint to understand the customer's issue and emotional state
2. If you need more research, call the appropriate tools
3. If you have sufficient information, provide a comprehensive, empathetic response
4. Focus on being helpful, specific, and actionable

Provide either tool calls for research OR a direct helpful response to the customer complaint.""")
            
            messages = [system_message] + messages
        
        # Get LLM response with potential tool calls
        response = self.llm.invoke(messages)
        
        # Add the response to messages
        updated_messages = messages + [response]
        
        return {
            **state,
            "messages": updated_messages
        }

    @traceable(name="helpfulness_check")
    async def check_helpfulness(self, state: AgentState) -> float:
        """
        Use a separate LLM to evaluate the helpfulness of the current response.
        
        Args:
            state: Current agent state
            
        Returns:
            Helpfulness score from 0.0 to 1.0
        """
        messages = state["messages"]
        
        # Get the last AI message (the response to evaluate)
        last_ai_message = None
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and not hasattr(msg, 'tool_calls'):
                last_ai_message = msg
                break
        
        if not last_ai_message:
            return 0.0  # No response to evaluate
        
        evaluation_prompt = f"""You are an expert evaluator of customer service responses. Please rate the following response to a customer complaint on a scale of 0.0 to 1.0.

ORIGINAL COMPLAINT: {state['complaint']}

RESPONSE TO EVALUATE: {last_ai_message.content}

Rate this response based on:
1. Empathy and understanding (25%)
2. Addressing the specific issue (25%) 
3. Providing actionable solutions (25%)
4. Professional and helpful tone (25%)

Respond with ONLY a number between 0.0 and 1.0. Examples:
- 0.9 = Excellent, comprehensive, empathetic response
- 0.7 = Good response with minor improvements needed
- 0.5 = Average response, missing key elements
- 0.3 = Poor response, lacks empathy or solutions
- 0.1 = Very poor response, unhelpful

Score:"""

        try:
            result = await self.helpfulness_checker.ainvoke([HumanMessage(content=evaluation_prompt)])
            score_text = result.content.strip()
            # Extract number from response
            import re
            score_match = re.search(r'(\d+\.?\d*)', score_text)
            if score_match:
                score = float(score_match.group(1))
                return min(max(score, 0.0), 1.0)  # Clamp between 0.0 and 1.0
            return 0.5  # Default middle score if parsing fails
        except:
            return 0.5  # Default middle score on error

    @traceable(name="decision_logic_3_choices_with_separate_tools")
    async def tool_call_or_helpful(self, state: AgentState) -> Literal["arxiv_tools", "tavily_tools", "action"]:
        """
        Makes 3 important decisions like a smart study buddy with separate tool routing:
        
        1. "Do I need to use tools?" - Route to specific tool nodes (arxiv_tools/tavily_tools)
        2. "Have I talked too much?" - If >10 messages, "end" (enough chatting!)
        3. "Is my answer good enough?" - Ask another AI to grade the response
        
        Args:
            state: Current agent state
            
        Returns:
            Next action: "continue", "arxiv_tools", "tavily_tools", "compose", or "end"
        """
        messages = state["messages"]
        last_message = messages[-1] if messages else None
        
        # Decision 1: "Do I need to use tools?" - Route to specific tool nodes
        if last_message and hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            for tool_call in last_message.tool_calls:
                if tool_call['name'] == 'arxiv_insights':
                    return "arxiv_tools"
                elif tool_call['name'] == 'tavily_examples':
                    return "tavily_tools"
        
        # If no tool calls, check if we should compose a response
        return "action"

    @traceable(name="should_continue_decision_gate")
    async def should_continue(self, state: AgentState) -> Literal["continue", "end"]:
        """
        DECISION GATE: Should we continue the workflow or end it?
        
        This is a proper decision diamond that evaluates:
        1. "Have I talked too much?" - If >10 messages, END (enough chatting!)
        2. "Is my answer good enough?" - Ask GPT-4o-mini to grade the response
        
        Args:
            state: Current agent state
            
        Returns:
            "continue" or "end"
        """
        messages = state["messages"]
        
        # Decision 1: "Have I talked too much?" (more than 10 messages)
        if len(messages) > 10:
            return "end"
        
        # Check if we have an AI response to evaluate
        last_ai_message = None
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and not hasattr(msg, 'tool_calls'):
                last_ai_message = msg
                break
        
        if not last_ai_message:
            return "continue"  # No response to evaluate yet
        
        # Decision 2: "Is my answer good enough?" - Use GPT-4o-mini to evaluate
        helpfulness_score = await self.check_helpfulness(state)
        
        # Update state with helpfulness score
        state["helpfulness_score"] = helpfulness_score
        
        # If answer is good enough (>= 0.7), we're done!
        if helpfulness_score >= 0.7:
            return "end"
        else:
            return "continue"

    @traceable(name="action_router")
    def route_action(self, state: AgentState) -> Literal["compose", "agent"]:
        """
        Route to compose response or continue with agent based on research status.
        
        Args:
            state: Current agent state
            
        Returns:
            "compose" or "agent"
        """
        # Check if we have sufficient research for composition
        arxiv_complete = state.get("arxiv_complete", False)
        tavily_complete = state.get("tavily_complete", False)
        iteration_count = state.get("iteration_count", 0)
        
        # If both research types complete or max iterations reached, compose
        if (arxiv_complete and tavily_complete) or iteration_count >= 4:
            return "compose"
        else:
            return "agent"

    @traceable(name="extract_arxiv_results")
    def extract_arxiv_results(self, state: AgentState) -> AgentState:
        """
        Extract and process results from ArXiv tool calls.
        
        Args:
            state: Current agent state with ArXiv tool messages
            
        Returns:
            Updated state with extracted ArXiv insights
        """
        messages = state["messages"]
        insights = state.get("insights", {})
        
        # Process ArXiv tool messages
        for message in reversed(messages):
            if isinstance(message, ToolMessage) and message.name == "arxiv_insights":
                try:
                    tool_result = eval(message.content) if isinstance(message.content, str) else message.content
                    insights.update(tool_result)
                    insights["arxiv_processed"] = True
                except:
                    insights["arxiv_raw_response"] = message.content
                    insights["arxiv_processed"] = True
                break
        
        return {
            **state,
            "insights": insights,
            "arxiv_complete": True,
            "iteration_count": state.get("iteration_count", 0) + 1
        }

    @traceable(name="extract_tavily_results")
    def extract_tavily_results(self, state: AgentState) -> AgentState:
        """
        Extract and process results from Tavily tool calls.
        
        Args:
            state: Current agent state with Tavily tool messages
            
        Returns:
            Updated state with extracted Tavily examples
        """
        messages = state["messages"]
        examples = state.get("examples", {})
        
        # Process Tavily tool messages
        for message in reversed(messages):
            if isinstance(message, ToolMessage) and message.name == "tavily_examples":
                try:
                    tool_result = eval(message.content) if isinstance(message.content, str) else message.content
                    examples.update(tool_result)
                    examples["tavily_processed"] = True
                except:
                    examples["tavily_raw_response"] = message.content
                    examples["tavily_processed"] = True
                break
        
        return {
            **state,
            "examples": examples,
            "tavily_complete": True,
            "iteration_count": state.get("iteration_count", 0) + 1
        }

    @traceable(name="compose_final_response")
    async def compose_response(self, state: AgentState) -> AgentState:
        """
        Compose final empathetic response using gathered research.
        
        Args:
            state: Current agent state with research data
            
        Returns:
            Final state with composed response and citations
        """
        result = await self.composer_tool._arun(
            state["complaint"],
            state.get("insights", {}),
            state.get("examples", {})
        )

        return {
            **state,
            "response": result['response'],
            "citations": result['citations'],
            "decision": "end"
        }

    def _build_graph(self) -> StateGraph:
        """
        Build the agent-based LangGraph workflow with proper decision gate structure.
        
        Returns:
            Configured StateGraph ready for compilation
        """
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("agent", self.call_model)
        workflow.add_node("should_continue", self.should_continue)  # Decision diamond
        workflow.add_node("action", self.route_action)  # Action router
        workflow.add_node("arxiv_tools", self.arxiv_node)
        workflow.add_node("tavily_tools", self.tavily_node)
        workflow.add_node("extract_arxiv", self.extract_arxiv_results)
        workflow.add_node("extract_tavily", self.extract_tavily_results)
        workflow.add_node("compose", self.compose_response)
        
        # Set entry point
        workflow.add_edge(START, "agent")
        
        # Agent decides on tool calls or routes to action
        workflow.add_conditional_edges(
            "agent",
            self.tool_call_or_helpful,
            {
                "arxiv_tools": "arxiv_tools",
                "tavily_tools": "tavily_tools", 
                "action": "action"
            }
        )
        
        # Action router determines next step
        workflow.add_conditional_edges(
            "action",
            self.route_action,
            {
                "compose": "compose",
                "agent": "should_continue"
            }
        )
        
        # DECISION GATE: Should we continue or end?
        workflow.add_conditional_edges(
            "should_continue",
            self.should_continue,
            {
                "continue": "agent",
                "end": END
            }
        )
        
        # Tool-specific flows
        workflow.add_edge("arxiv_tools", "extract_arxiv")
        workflow.add_edge("tavily_tools", "extract_tavily")
        
        # After extracting results, go back to agent for decision
        workflow.add_edge("extract_arxiv", "agent")
        workflow.add_edge("extract_tavily", "agent")
        
        # Compose leads to decision gate
        workflow.add_edge("compose", "should_continue")

        return workflow

    @traceable(name="generate_response")
    async def generate_response(self, complaint: str) -> Dict[str, Any]:
        """
        Generate a complete response to a customer complaint using agent workflow.
        
        This method orchestrates the full agent-based workflow with separate tool nodes and helpfulness checking.
        
        Args:
            complaint: Customer complaint text
            
        Returns:
            Dictionary with response, citations, and quality metrics
        """
        start_time = time.time()

        # Initialize agent state
        initial_state: AgentState = {
            "messages": [],
            "complaint": complaint,
            "insights": {},
            "examples": {},
            "response": "",
            "citations": [],
            "latency_ms": 0,
            "start_time": start_time,
            "iteration_count": 0,
            "decision": "start",
            "arxiv_complete": False,
            "tavily_complete": False,
            "helpfulness_score": 0.0
        }

        # Run the agent workflow
        config = {"configurable": {
            "thread_id": f"complaint_{int(start_time)}"}}

        final_state = await self.compiled_graph.ainvoke(
            initial_state,
            config=config
        )

        # Extract final response - try composed response first, then messages
        final_response = final_state.get("response", "")
        if not final_response:
            # Fallback to last AI message
            for msg in reversed(final_state["messages"]):
                if isinstance(msg, AIMessage) and not hasattr(msg, 'tool_calls'):
                    final_response = msg.content
                    break

        # Calculate latency
        end_time = time.time()
        latency_ms = int((end_time - start_time) * 1000)

        return {
            "reply": final_response,
            "citations": final_state.get("citations", []),
            "latency_ms": latency_ms,
            "iterations": final_state.get("iteration_count", 0),
            "helpfulness_score": final_state.get("helpfulness_score", 0.0),
            "research_quality": "comprehensive" if (final_state.get("arxiv_complete") and final_state.get("tavily_complete")) else "partial",
            "message_count": len(final_state.get("messages", [])),
            "decision_reason": self._get_decision_reason(final_state)
        }

    def _get_decision_reason(self, final_state: AgentState) -> str:
        """
        Determine why the workflow ended based on final state.
        
        Args:
            final_state: Final agent state
            
        Returns:
            Human-readable reason for ending
        """
        message_count = len(final_state.get("messages", []))
        helpfulness_score = final_state.get("helpfulness_score", 0.0)
        
        if message_count > 10:
            return "Reached maximum conversation length (10+ messages)"
        elif helpfulness_score >= 0.7:
            return f"Response quality sufficient (score: {helpfulness_score:.2f})"
        else:
            return "Workflow completed"

    def get_graph_visualization(self) -> str:
        """
        Get the Mermaid diagram representation of the agent workflow graph.
        
        Returns:
            Mermaid diagram as string
        """
        try:
            return self.compiled_graph.get_graph().draw_mermaid()
        except Exception as e:
            return f"Error generating graph visualization: {str(e)}"

    def save_graph_diagram(self, filename: str = "replysight_separate_tools_helpfulness.png") -> str:
        """
        Save the agent workflow diagram as a PNG file.
        
        Args:
            filename: Output filename for the diagram
            
        Returns:
            Path to saved file or error message
        """
        try:
            graph_png = self.compiled_graph.get_graph().draw_mermaid_png()
            with open(filename, "wb") as f:
                f.write(graph_png)
            return f"Separate tools with helpfulness checking workflow diagram saved to {filename}"
        except Exception as e:
            return f"Error saving separate tools helpfulness workflow diagram: {str(e)}"

    def print_graph_structure(self) -> None:
        """
        Print detailed information about the agent graph structure.
        """
        graph = self.compiled_graph.get_graph()
        
        print("🧠🔧 ReplySight Smart Study Buddy with Separate Tool Nodes")
        print("=" * 65)
        
        print(f"📊 Nodes ({len(graph.nodes)}):")
        for node in graph.nodes:
            if hasattr(node, 'id'):
                print(f"  • {node.id}")
            else:
                print(f"  • {node}")
        
        print(f"\n🔗 Edges ({len(graph.edges)}):")
        for edge in graph.edges:
            if hasattr(edge, 'source') and hasattr(edge, 'target'):
                print(f"  • {edge.source} → {edge.target}")
            else:
                print(f"  • {edge}")
        
        print(f"\n📋 Mermaid Diagram:")
        print(self.get_graph_visualization())

    def get_graph_metadata(self) -> Dict[str, Any]:
        """
        Get comprehensive metadata about the agent graph structure.
        
        Returns:
            Dictionary with agent graph metadata
        """
        graph = self.compiled_graph.get_graph()
        
        return {
            "workflow_name": "ReplySight Smart Study Buddy with Decision Gate",
            "workflow_type": "agent_based_with_decision_gate_and_helpfulness_checking",
            "node_count": len(graph.nodes),
            "edge_count": len(graph.edges),
            "has_cycles": True,  # Agent can loop back based on decisions
            "nodes": [str(node) for node in graph.nodes],
            "edges": [f"{edge.source} → {edge.target}" if hasattr(edge, 'source') else str(edge) for edge in graph.edges],
            "mermaid_diagram": self.get_graph_visualization(),
            "execution_flow": [
                "START → agent (analyze complaint)",
                "agent → arxiv_tools (if ArXiv research needed)",
                "agent → tavily_tools (if Tavily examples needed)",
                "agent → action (route to next step)",
                "action → compose (if research complete)",
                "action → should_continue (if more work needed)",
                "should_continue → continue (back to agent)",
                "should_continue → end (if >10 messages or helpful ≥0.7)",
                "arxiv_tools → extract_arxiv → agent",
                "tavily_tools → extract_tavily → agent",
                "compose → should_continue (decision gate)"
            ],
            "decision_logic": [
                {
                    "decision": 1,
                    "question": "Do I need to use tools?",
                    "action": "Route to specific tool node (arxiv_tools/tavily_tools)",
                    "trigger": "Agent message contains specific tool calls"
                },
                {
                    "decision": 2, 
                    "question": "Have I talked too much?",
                    "action": "Route to 'end' to stop chatting",
                    "trigger": "More than 10 messages in conversation"
                },
                {
                    "decision": 3,
                    "question": "Is my answer good enough?",
                    "action": "Route to 'end' if helpful (≥0.7), 'compose' if research complete but not helpful",
                    "trigger": "GPT-4o-mini evaluates response helpfulness"
                }
            ],
            "tool_nodes": [
                {
                    "name": "arxiv_tools",
                    "purpose": "Academic research on customer service topics",
                    "tool": "ArxivInsightsTool",
                    "extractor": "extract_arxiv"
                },
                {
                    "name": "tavily_tools", 
                    "purpose": "Best practice examples and real-world cases",
                    "tool": "TavilyExamplesTool",
                    "extractor": "extract_tavily"
                },
                {
                    "name": "compose",
                    "purpose": "Response synthesis with citations",
                    "tool": "ResponseComposerTool",
                    "trigger": "When research complete or helpfulness insufficient"
                }
            ],
            "features": [
                "3-tier intelligent decision making",
                "Automatic helpfulness evaluation with GPT-4o-mini",
                "Conversation length protection (10 message limit)",
                "Separate tool nodes for granular control",
                "Specific tool routing based on agent decisions",
                "Independent research tracking (ArXiv + Tavily)",
                "Quality-driven workflow termination",
                "Response composition with research synthesis",
                "LangSmith tracing for full observability"
            ]
        }


# Factory function for easy instantiation (updated for agent)
def create_replysight_graph(tavily_api_key: Optional[str] = None) -> ReplySightAgent:
    """
    Factory function to create a configured ReplySight agent workflow.
    
    Args:
        tavily_api_key: API key for Tavily search service
        
    Returns:
        Configured ReplySightAgent instance
    """
    return ReplySightAgent(tavily_api_key=tavily_api_key)
