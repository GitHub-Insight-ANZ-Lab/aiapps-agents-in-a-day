import random
import re
import os
import json
import requests
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
from dataclasses import dataclass

# Load environment variables from .env file
load_dotenv()


@dataclass
class MCPTool:
    """MCP Tool definition"""
    name: str
    description: str
    input_schema: Dict[str, Any]
    

@dataclass
class MCPResource:
    """MCP Resource definition"""
    uri: str
    name: str
    description: str
    mime_type: str


class MCPServer:
    """Simplified MCP Server for PSR Tournament Knowledge"""
    
    def __init__(self):
        self.tools = {}
        self.resources = {}
        self.setup_capabilities()
    
    def setup_capabilities(self):
        """Setup MCP server capabilities for PSR tournament"""
        
        # Register tools
        self.tools["answer_question"] = MCPTool(
            name="answer_question",
            description="Answer tournament questions using knowledge base",
            input_schema={
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "The question to answer"}
                },
                "required": ["question"]
            }
        )
        
        self.tools["analyze_strategy"] = MCPTool(
            name="analyze_strategy",
            description="Analyze optimal Rock, Paper, Scissors strategy",
            input_schema={
                "type": "object",
                "properties": {
                    "round_number": {"type": "integer"},
                    "current_score": {"type": "integer"}
                },
                "required": ["round_number"]
            }
        )
        
        # Register resources
        self.resources["knowledge_base"] = MCPResource(
            uri="psr://knowledge/general",
            name="General Knowledge Base",
            description="Comprehensive knowledge base for tournament questions",
            mime_type="application/json"
        )
    
    def list_tools(self) -> List[MCPTool]:
        """MCP: List available tools"""
        return list(self.tools.values())
    
    def list_resources(self) -> List[MCPResource]:
        """MCP: List available resources"""
        return list(self.resources.values())
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """MCP: Execute a tool with given arguments"""
        if tool_name not in self.tools:
            return {"error": f"Tool {tool_name} not found"}
        
        if tool_name == "answer_question":
            return self._answer_question(arguments)
        elif tool_name == "analyze_strategy":
            return self._analyze_strategy(arguments)
        else:
            return {"error": f"Tool {tool_name} not implemented"}
    
    def _answer_question(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of answer_question tool"""
        question = args.get("question", "")
        question_lower = question.lower()
        
        # Geography
        if "capital" in question_lower and "france" in question_lower:
            return {"answer": "Paris", "confidence": 0.98, "source": "geography_database"}
        elif "capital" in question_lower and "japan" in question_lower:
            return {"answer": "Tokyo", "confidence": 0.98, "source": "geography_database"}
        elif "capital" in question_lower and "australia" in question_lower:
            return {"answer": "Canberra", "confidence": 0.95, "source": "geography_database"}
        
        # Science
        elif "chemical symbol" in question_lower and "gold" in question_lower:
            return {"answer": "Au", "confidence": 0.99, "source": "chemistry_database"}
        elif "largest ocean" in question_lower:
            return {"answer": "Pacific Ocean", "confidence": 0.95, "source": "geography_database"}
        elif "speed of light" in question_lower:
            return {"answer": "299,792,458 m/s", "confidence": 0.99, "source": "physics_database"}
        
        # Math
        elif "+" in question or "plus" in question_lower:
            try:
                numbers = re.findall(r'\d+', question)
                if len(numbers) >= 2:
                    result = sum(int(n) for n in numbers)
                    return {"answer": str(result), "confidence": 0.99, "source": "calculation"}
            except:
                pass
        elif "-" in question and "minus" in question_lower:
            try:
                numbers = re.findall(r'\d+', question)
                if len(numbers) >= 2:
                    result = int(numbers[0]) - int(numbers[1])
                    return {"answer": str(result), "confidence": 0.99, "source": "calculation"}
            except:
                pass
        
        return {"answer": "Unknown", "confidence": 0.1, "source": "fallback"}
    
    def _analyze_strategy(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of analyze_strategy tool"""
        round_number = args.get("round_number", 1)
        current_score = args.get("current_score", 0)
        
        # Round-based strategy
        if round_number == 1:
            recommended_move = "Paper"
            reasoning = "Round 1: Most beginners choose Rock, counter with Paper"
            confidence = 0.7
        elif round_number <= 3:
            recommended_move = "Scissors"
            reasoning = "Early rounds: People often choose Paper, counter with Scissors"
            confidence = 0.6
        else:
            recommended_move = "Rock"
            reasoning = "Late rounds: Show strength with Rock"
            confidence = 0.6
        
        # Score adjustment
        if current_score < 0:
            recommended_move = "Paper"
            reasoning = "Behind in score: Conservative Paper strategy"
            confidence = 0.8
        elif current_score > 2:
            recommended_move = "Rock"
            reasoning = "Ahead in score: Aggressive Rock strategy"
            confidence = 0.8
        
        return {
            "recommended_move": recommended_move,
            "confidence": confidence,
            "reasoning": reasoning,
            "move_number": {"Rock": 0, "Paper": 1, "Scissors": 2}[recommended_move]
        }


class GameAgentV61A:
    """Game Agent V61A - Enhanced with MCP (Model Context Protocol) capability
    
    This version demonstrates MCP concepts from lesson 61:
    - Dynamic tool discovery from MCP server
    - Standardized tool calling interface
    - Resource access through MCP protocol
    - Interoperability across different systems
    """
    
    def __init__(self, azure_ai_endpoint: Optional[str] = None, azure_ai_key: Optional[str] = None):
        """
        Initialize the MCP-enhanced game agent
        
        Args:
            azure_ai_endpoint: Azure AI Foundry endpoint URL
            azure_ai_key: Azure AI service API key
        """
        self.azure_ai_endpoint = azure_ai_endpoint or os.getenv('AZURE_AI_ENDPOINT')
        self.azure_ai_key = azure_ai_key or os.getenv('AZURE_AI_KEY')

        # Initialize headers for Azure AI API calls
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.azure_ai_key}' if self.azure_ai_key else None
        }
        
        # Initialize MCP server
        self.mcp_server = MCPServer()
        print(f"[MCP] Initialized MCP server with {len(self.mcp_server.list_tools())} tools")
    
    def _call_azure_ai_agent(self, prompt: str, system_message: str = None) -> str:
        """
        Call Azure AI Agent service with the given prompt
        
        Args:
            prompt: The user prompt/question
            system_message: Optional system message for context
            
        Returns:
            Response from Azure AI agent
        """
        try:
            # Construct the payload for Azure AI Agent service
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": system_message or "You are a helpful assistant specialized in answering questions accurately and concisely."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 150,
                "temperature": 0.1,  # Low temperature for consistent answers
                "top_p": 0.9
            }
            
            # Make API call to Azure AI Agent service
            response = requests.post(
                f"{self.azure_ai_endpoint}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
            else:
                print(f"Azure AI API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error calling Azure AI Agent service: {str(e)}")
            return None
    
    def answer_question(self, question: str) -> str:
        """
        Generate an answer to the question using MCP protocol first, then fallback to Azure AI
        
        Args:
            question: The question to answer
            
        Returns:
            Answer to the question
        """
        print(f"[MCP] Processing question: {question}")
        
        # Try MCP server first
        mcp_result = self.mcp_server.call_tool("answer_question", {"question": question})
        
        if "error" not in mcp_result and mcp_result.get("confidence", 0) > 0.5:
            answer = mcp_result["answer"]
            confidence = mcp_result["confidence"]
            source = mcp_result["source"]
            print(f"[MCP] Answer found: {answer} (confidence: {confidence:.2f}, source: {source})")
            return answer
        
        print(f"[MCP] No confident answer found, falling back to Azure AI")
        
        # Fallback to Azure AI Agent service
        system_message = """You are a knowledgeable assistant participating in a Paper-Scissors-Rock tournament. 
        You need to answer questions accurately and concisely. 
        For math problems, provide only the numerical answer. 
        For knowledge questions, provide brief, factual answers.
        Keep responses short and direct."""
        
        azure_answer = self._call_azure_ai_agent(question, system_message)
        
        if azure_answer:
            # Clean up the response to extract just the answer
            cleaned_answer = azure_answer.strip()
            if cleaned_answer.lower().startswith(('the answer is', 'answer:', 'result:')):
                cleaned_answer = cleaned_answer.split(':', 1)[-1].strip()
            
            # For mathematical expressions, try to extract just the number
            if any(op in question for op in ['+', '-', '*', '/', '=']):
                number_match = re.search(r'\b\d+(?:\.\d+)?\b', cleaned_answer)
                if number_match:
                    return number_match.group()
            
            print(f"[Azure AI] Answer: {cleaned_answer[:50]}")
            return cleaned_answer[:50]  # Limit response length
        
        # Ultimate fallback
        print("[Fallback] Using default response")
        return "I don't know"
    
    def choose_rps_move(self) -> int:
        """
        Choose Rock (0), Paper (1), or Scissors (2) using MCP strategy analysis first, then fallback
        
        Returns:
            Move selection as integer (0=Rock, 1=Paper, 2=Scissors)
        """
        print(f"[MCP] Analyzing strategy for move selection")
        
        # Try MCP server strategy analysis first
        mcp_result = self.mcp_server.call_tool("analyze_strategy", {
            "round_number": 1,  # Default round, could be enhanced to track actual round
            "current_score": 0   # Default score, could be enhanced to track actual score
        })
        
        if "error" not in mcp_result and mcp_result.get("confidence", 0) > 0.5:
            move_number = mcp_result["move_number"]
            move_name = mcp_result["recommended_move"]
            confidence = mcp_result["confidence"]
            reasoning = mcp_result["reasoning"]
            print(f"[MCP] Strategy: {move_name} (confidence: {confidence:.2f}) - {reasoning}")
            return move_number
        
        print(f"[MCP] No confident strategy found, falling back to Azure AI")
        
        # Fallback to Azure AI for strategic choice
        prompt = """In a Rock-Paper-Scissors game, choose the best move. 
        Respond with only one word: Rock, Paper, or Scissors.
        Consider that this is part of a tournament and you want to win."""
        
        system_message = "You are a strategic Rock-Paper-Scissors player. Choose wisely."
        
        azure_choice = self._call_azure_ai_agent(prompt, system_message)
        
        if azure_choice:
            choice_lower = azure_choice.lower().strip()
            if 'rock' in choice_lower:
                print(f"[Azure AI] Chose: Rock")
                return 0
            elif 'paper' in choice_lower:
                print(f"[Azure AI] Chose: Paper")
                return 1
            elif 'scissors' in choice_lower or 'scissor' in choice_lower:
                print(f"[Azure AI] Chose: Scissors")
                return 2
        
        # Ultimate fallback - random choice
        fallback_move = random.randint(0, 2)
        move_names = {0: "Rock", 1: "Paper", 2: "Scissors"}
        print(f"[Fallback] Random choice: {move_names[fallback_move]}")
        return fallback_move

    def get_mcp_capabilities(self) -> Dict[str, Any]:
        """Get information about MCP server capabilities"""
        tools = self.mcp_server.list_tools()
        resources = self.mcp_server.list_resources()
        
        return {
            "tools": [{"name": tool.name, "description": tool.description} for tool in tools],
            "resources": [{"name": resource.name, "description": resource.description} for resource in resources],
            "server_info": "PSR Tournament MCP Server v1.0"
        }


# Backward compatibility - maintain same interface as original GameAgent
class GameAgent(GameAgentV61A):
    """Alias for backward compatibility with existing code"""
    pass


# Example usage and testing
if __name__ == "__main__":
    # Initialize MCP-enhanced agent
    agent = GameAgentV61A()
    
    # Display MCP capabilities
    print("MCP-Enhanced Game Agent V61A")
    print("=" * 50)
    
    capabilities = agent.get_mcp_capabilities()
    print(f"MCP Server: {capabilities['server_info']}")
    print(f"Available Tools: {len(capabilities['tools'])}")
    for tool in capabilities['tools']:
        print(f"  - {tool['name']}: {tool['description']}")
    print(f"Available Resources: {len(capabilities['resources'])}")
    for resource in capabilities['resources']:
        print(f"  - {resource['name']}: {resource['description']}")
    
    print("\nTesting MCP-enhanced question answering:")
    print("=" * 50)
    
    # Test question answering with MCP
    test_questions = [
        "What is the capital of France?",
        "What is the chemical symbol for gold?",
        "What is 15 + 27?",
        "What is the largest ocean?",
        "What color is the sky?"  # This should fallback to Azure AI
    ]
    
    for question in test_questions:
        answer = agent.answer_question(question)
        print(f"Q: {question}")
        print(f"A: {answer}")
        print()
    
    # Test MCP-enhanced RPS move selection
    print("Testing MCP-enhanced RPS move selection:")
    print("=" * 50)
    for i in range(3):
        move = agent.choose_rps_move()
        move_names = {0: "Rock", 1: "Paper", 2: "Scissors"}
        print(f"Move {i+1}: {move_names[move]} ({move})")
        print()