"""
PSR Game Agent V54 - Tool Use Design Pattern Implementation
Based on lesson 54-tool-use documentation and following agent_v1.py structure.

This version demonstrates the Tool Use Design Pattern with:
- Function/tool calling capabilities for PSR tournament
- Enhanced question answering using structured tools
- Strategic move selection with analysis tools
- Comprehensive tool schemas and execution framework
"""

import random
import re
import os
import json
import requests
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class PSRTournamentTools:
    """Tool collection for PSR tournament functionality as described in lesson 54"""
    
    def answer_tournament_question(self, question: str, difficulty: str = "medium") -> str:
        """Answer a PSR tournament question using knowledge base"""
        print(f"answer_tournament_question called with question: {question}, difficulty: {difficulty}")
        
        question_lower = question.lower()
        
        # Geography questions
        if "capital" in question_lower:
            if "japan" in question_lower:
                return json.dumps({"question": question, "answer": "Tokyo", "confidence": "high"})
            elif "france" in question_lower:
                return json.dumps({"question": question, "answer": "Paris", "confidence": "high"})
            elif "australia" in question_lower:
                return json.dumps({"question": question, "answer": "Canberra", "confidence": "high"})
            elif "germany" in question_lower:
                return json.dumps({"question": question, "answer": "Berlin", "confidence": "high"})
            elif "italy" in question_lower:
                return json.dumps({"question": question, "answer": "Rome", "confidence": "high"})
            elif "spain" in question_lower:
                return json.dumps({"question": question, "answer": "Madrid", "confidence": "high"})
            elif "canada" in question_lower:
                return json.dumps({"question": question, "answer": "Ottawa", "confidence": "high"})
        
        # Science questions  
        elif "largest ocean" in question_lower:
            return json.dumps({"question": question, "answer": "Pacific Ocean", "confidence": "high"})
        elif "fastest land animal" in question_lower:
            return json.dumps({"question": question, "answer": "Cheetah", "confidence": "high"})
        elif "tallest mountain" in question_lower:
            return json.dumps({"question": question, "answer": "Mount Everest", "confidence": "high"})
        elif "chemical formula for water" in question_lower:
            return json.dumps({"question": question, "answer": "H2O", "confidence": "high"})
        
        # Math questions
        elif any(op in question for op in ["+", "plus", "add"]):
            # Simple math parsing
            numbers = re.findall(r'\d+', question)
            if len(numbers) >= 2:
                result = sum(int(n) for n in numbers[:2])
                return json.dumps({"question": question, "answer": str(result), "confidence": "high"})
        
        elif any(op in question for op in ["-", "minus", "subtract"]):
            numbers = re.findall(r'\d+', question)
            if len(numbers) >= 2:
                result = int(numbers[0]) - int(numbers[1])
                return json.dumps({"question": question, "answer": str(result), "confidence": "high"})
        
        # Default response
        return json.dumps({"question": question, "answer": "I need to research this question", "confidence": "low"})

    def select_optimal_move(self, round_number: int, strategy: str, opponent_history: List[str] = None) -> str:
        """Select optimal Rock, Paper, or Scissors move based on strategy"""
        print(f"select_optimal_move called with round: {round_number}, strategy: {strategy}")
        
        moves = ["Rock", "Paper", "Scissors"]
        
        if strategy == "random":
            selected_move = random.choice(moves)
        elif strategy == "aggressive":
            # Aggressive strategy favors Rock (appears strong)
            selected_move = "Rock"
        elif strategy == "defensive":
            # Defensive strategy uses Paper (beats the common Rock)
            selected_move = "Paper"
        elif strategy == "counter":
            # Counter strategy based on opponent history
            if opponent_history and len(opponent_history) > 0:
                last_opponent_move = opponent_history[-1]
                if last_opponent_move == "Rock":
                    selected_move = "Paper"
                elif last_opponent_move == "Paper":
                    selected_move = "Scissors"
                elif last_opponent_move == "Scissors":
                    selected_move = "Rock"
                else:
                    selected_move = "Rock"  # Default
            else:
                selected_move = "Rock"  # Default when no history
        else:
            selected_move = "Rock"  # Safe default
            
        return json.dumps({
            "round_number": round_number,
            "selected_move": selected_move,
            "strategy_used": strategy,
            "reasoning": f"Selected {selected_move} using {strategy} strategy for round {round_number}"
        })


class GameAgentV54:
    """Azure AI Agent service-based agent class implementing Tool Use Design Pattern from lesson 54"""
    
    def __init__(self, azure_ai_endpoint: Optional[str] = None, azure_ai_key: Optional[str] = None):
        """
        Initialize the Azure AI Agent service-based game agent with tool use capabilities
        
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
        
        # Initialize PSR tournament tools
        self.tools = PSRTournamentTools()
        
        # Tool schemas as described in lesson 54
        self.tool_schemas = [
            {
                "type": "function",
                "function": {
                    "name": "answer_tournament_question",
                    "description": "Answer a PSR tournament question using knowledge base",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "The tournament question to answer, e.g. 'What is the capital of France?'",
                            },
                            "difficulty": {
                                "type": "string", 
                                "description": "Question difficulty level: easy, medium, hard",
                                "enum": ["easy", "medium", "hard"]
                            }
                        },
                        "required": ["question"],
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "select_optimal_move",
                    "description": "Select the optimal Rock, Paper, or Scissors move based on strategy analysis",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "opponent_history": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Previous moves by opponents if available",
                            },
                            "round_number": {
                                "type": "integer",
                                "description": "Current round number in tournament"
                            },
                            "strategy": {
                                "type": "string",
                                "description": "Strategy to use: random, aggressive, defensive, counter",
                                "enum": ["random", "aggressive", "defensive", "counter"]
                            }
                        },
                        "required": ["round_number", "strategy"],
                    },
                }
            }
        ]
    
    def _call_azure_ai_agent_with_tools(self, prompt: str, system_message: str = None) -> str:
        """
        Call Azure AI Agent service with tool use capabilities
        
        Args:
            prompt: The user prompt/question
            system_message: Optional system message for context
            
        Returns:
            Response from Azure AI agent after tool execution
        """
        try:
            # Construct the payload for Azure AI Agent service with tools
            messages = [
                {
                    "role": "system",
                    "content": system_message or "You are a helpful assistant specialized in PSR tournament questions and strategy. Use the available tools to provide accurate answers and strategic moves."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            payload = {
                "messages": messages,
                "tools": self.tool_schemas,
                "tool_choice": "auto",
                "max_tokens": 500,
                "temperature": 0.1,
                "top_p": 0.9
            }
            
            # First API call: Ask the model to use the function
            response = requests.post(
                f"{self.azure_ai_endpoint}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"Azure AI API error: {response.status_code} - {response.text}")
                return None
            
            result = response.json()
            response_message = result.get('choices', [{}])[0].get('message', {})
            messages.append(response_message)
            
            # Handle tool calls if any
            if response_message.get('tool_calls'):
                for tool_call in response_message['tool_calls']:
                    function_args = json.loads(tool_call['function']['arguments'])
                    
                    if tool_call['function']['name'] == "answer_tournament_question":
                        question_response = self.tools.answer_tournament_question(
                            question=function_args.get("question"),
                            difficulty=function_args.get("difficulty", "medium")
                        )
                        
                        messages.append({
                            "tool_call_id": tool_call['id'],
                            "role": "tool",
                            "name": "answer_tournament_question",
                            "content": question_response,
                        })
                        
                    elif tool_call['function']['name'] == "select_optimal_move":
                        move_response = self.tools.select_optimal_move(
                            round_number=function_args.get("round_number"),
                            strategy=function_args.get("strategy"),
                            opponent_history=function_args.get("opponent_history", [])
                        )
                        
                        messages.append({
                            "tool_call_id": tool_call['id'],
                            "role": "tool", 
                            "name": "select_optimal_move",
                            "content": move_response,
                        })
                
                # Second API call: Get the final response from the model
                final_payload = {
                    "messages": messages,
                    "max_tokens": 200,
                    "temperature": 0.1
                }
                
                final_response = requests.post(
                    f"{self.azure_ai_endpoint}/chat/completions",
                    headers=self.headers,
                    json=final_payload,
                    timeout=30
                )
                
                if final_response.status_code == 200:
                    final_result = final_response.json()
                    return final_result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
            
            else:
                # No tool calls, return direct response
                return response_message.get('content', '').strip()
                
        except Exception as e:
            print(f"Error calling Azure AI Agent service with tools: {str(e)}")
            return None
    
    def answer_question(self, question: str) -> str:
        """
        Generate an answer to the question using Azure AI Agent service with tool use
        
        Args:
            question: The question to answer
            
        Returns:
            Answer to the question
        """
        # Use tool-enhanced Azure AI service
        system_message = """You are a knowledgeable assistant participating in a Paper-Scissors-Rock tournament. 
        Use the answer_tournament_question tool to provide accurate answers to questions.
        For any tournament question, always use the tool to get the best answer.
        Return only the answer value, not the full JSON response."""
        
        prompt = f"I need to answer this question for the PSR tournament: '{question}'"
        
        azure_answer = self._call_azure_ai_agent_with_tools(prompt, system_message)
        
        if azure_answer:
            # Clean up the response to extract just the answer
            cleaned_answer = azure_answer.strip()
            
            # Try to extract JSON if present and get the answer
            try:
                if cleaned_answer.startswith('{') and cleaned_answer.endswith('}'):
                    json_response = json.loads(cleaned_answer)
                    if 'answer' in json_response:
                        return json_response['answer']
            except:
                pass
            
            # Remove common prefixes and keep it concise
            if cleaned_answer.lower().startswith(('the answer is', 'answer:', 'result:')):
                cleaned_answer = cleaned_answer.split(':', 1)[-1].strip()
            
            # For mathematical expressions, try to extract just the number
            if any(op in question for op in ['+', '-', '*', '/', '=']):
                number_match = re.search(r'\b\d+(?:\.\d+)?\b', cleaned_answer)
                if number_match:
                    return number_match.group()
            
            return cleaned_answer[:50]  # Limit response length
        
        # Fallback to direct tool use if API fails
        try:
            tool_response = self.tools.answer_tournament_question(question, "medium")
            result = json.loads(tool_response)
            return result.get("answer", "Unable to answer")
        except:
            return "Unable to answer"
    
    def choose_rps_move(self) -> int:
        """
        Choose Rock (0), Paper (1), or Scissors (2) using Azure AI Agent service with tools
        
        Returns:
            Move selection as integer (0=Rock, 1=Paper, 2=Scissors)
        """
        # Use tool-enhanced move selection
        system_message = """You are a strategic Rock-Paper-Scissors player in a tournament.
        Use the select_optimal_move tool to choose the best move.
        Consider the current round and use an appropriate strategy.
        Return only the move name (Rock, Paper, or Scissors)."""
        
        prompt = "I need to select my move for this round. Use a defensive strategy for round 1."
        
        azure_choice = self._call_azure_ai_agent_with_tools(prompt, system_message)
        
        if azure_choice:
            choice_lower = azure_choice.lower().strip()
            
            # Try to extract JSON if present and get the move
            try:
                if choice_lower.startswith('{') and choice_lower.endswith('}'):
                    json_response = json.loads(azure_choice)
                    if 'selected_move' in json_response:
                        move = json_response['selected_move'].lower()
                        if 'rock' in move:
                            return 0
                        elif 'paper' in move:
                            return 1
                        elif 'scissors' in move or 'scissor' in move:
                            return 2
            except:
                pass
            
            # Direct text parsing
            if 'rock' in choice_lower:
                return 0
            elif 'paper' in choice_lower:
                return 1
            elif 'scissors' in choice_lower or 'scissor' in choice_lower:
                return 2
        
        # Fallback to direct tool use if API fails
        try:
            tool_response = self.tools.select_optimal_move(1, "defensive", [])
            result = json.loads(tool_response)
            move = result.get("selected_move", "Rock").lower()
            if 'rock' in move:
                return 0
            elif 'paper' in move:
                return 1
            elif 'scissors' in move:
                return 2
        except:
            pass
        
        # Final fallback
        return random.randint(0, 2)


# Backward compatibility - maintain same interface as original GameAgent
class GameAgent(GameAgentV54):
    """Alias for backward compatibility with existing code"""
    pass


# Example usage and testing
if __name__ == "__main__":
    # Initialize agent
    agent = GameAgentV54()
    
    # Test question answering with tool use
    test_questions = [
        "What is 15 + 27?",
        "What is the capital of France?",
        "What color is the sky?",
        "What is 100 - 35?",
        "What is the capital of Japan?",
        "What is the largest ocean?"
    ]
    
    print("Testing Azure AI Agent V54 - Tool Use Design Pattern:")
    print("=" * 60)
    
    for question in test_questions:
        answer = agent.answer_question(question)
        print(f"Q: {question}")
        print(f"A: {answer}")
        print()
    
    # Test RPS move selection with tools
    print("RPS Move Selection Test with Tools:")
    print("-" * 40)
    for i in range(5):
        move = agent.choose_rps_move()
        move_names = {0: "Rock", 1: "Paper", 2: "Scissors"}
        print(f"Round {i+1}: {move_names[move]} ({move})")
    
    print("\nAgent V54 - Tool Use Design Pattern testing complete!")