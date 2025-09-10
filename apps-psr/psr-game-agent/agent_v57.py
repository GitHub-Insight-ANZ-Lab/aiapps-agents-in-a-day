import random
import re
import os
import json
import requests
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class TaskType(str, Enum):
    """Enumeration of different task types in PSR tournament"""
    QUESTION_ANSWERING = "question_answering"
    RPS_MOVE_SELECTION = "rps_move_selection"
    TOURNAMENT_STRATEGY = "tournament_strategy"
    GAME_ANALYSIS = "game_analysis"


class SubTask(BaseModel):
    """Model for individual subtasks in tournament planning"""
    task_type: TaskType
    task_details: str
    priority: int = 1  # 1=high, 2=medium, 3=low
    estimated_effort: str = "low"  # low, medium, high


class TournamentPlan(BaseModel):
    """Model for structured tournament planning output"""
    main_goal: str
    current_round: int = 1
    subtasks: List[SubTask]
    strategy_notes: str = ""
    confidence_level: float = 0.8


class QuestionStrategy(BaseModel):
    """Model for question answering strategy"""
    question_type: str  # math, knowledge, reasoning
    approach: str
    confidence: float
    fallback_strategy: str = "use_general_knowledge"


class RPSStrategy(BaseModel):
    """Model for Rock-Paper-Scissors strategy"""
    move_choice: int  # 0=Rock, 1=Paper, 2=Scissors
    reasoning: str
    confidence: float
    counter_strategy: str = "random"


class GameAgentV57:
    """Planning-enhanced game agent for PSR Tournament with strategic decomposition"""
    
    VERSION = "57"
    LESSON = "Planning Design - Task Decomposition and Strategic Planning"
    
    def __init__(self, azure_ai_endpoint: Optional[str] = None, azure_ai_key: Optional[str] = None):
        """
        Initialize the planning-enhanced game agent
        
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
        
        # Planning state tracking
        self.current_plan: Optional[TournamentPlan] = None
        self.tournament_history: List[Dict[str, Any]] = []
        self.learned_patterns: Dict[str, Any] = {
            "question_patterns": {},
            "rps_patterns": {},
            "opponent_behavior": {}
        }
    
    def _call_azure_ai_agent(self, prompt: str, system_message: str = None, use_json_format: bool = False) -> str:
        """
        Call Azure AI Agent service with the given prompt
        
        Args:
            prompt: The user prompt/question
            system_message: Optional system message for context
            use_json_format: Whether to request JSON format response
            
        Returns:
            Response from Azure AI agent
        """
        try:
            # Construct the payload for Azure AI Agent service
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": system_message or "You are a helpful assistant specialized in strategic planning and problem-solving."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 300,
                "temperature": 0.3,  # Slightly higher for creative planning
                "top_p": 0.9
            }
            
            # Add JSON format request if needed
            if use_json_format:
                payload["response_format"] = {"type": "json_object"}
            
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
    
    def create_tournament_plan(self, goal: str = "Win PSR Tournament", current_round: int = 1) -> TournamentPlan:
        """
        Create a structured tournament plan using task decomposition
        
        Args:
            goal: Main tournament goal
            current_round: Current tournament round
            
        Returns:
            Structured tournament plan
        """
        system_message = """You are a strategic tournament planner for Paper-Scissors-Rock games.
        Create a detailed plan breaking down the tournament goal into actionable subtasks.
        Focus on question answering strategy, RPS move selection, and overall tournament progression.
        Provide your response in JSON format with the structure:
        {
            "main_goal": "tournament goal",
            "current_round": 1,
            "subtasks": [
                {
                    "task_type": "question_answering",
                    "task_details": "specific approach for answering questions",
                    "priority": 1,
                    "estimated_effort": "medium"
                }
            ],
            "strategy_notes": "overall strategic considerations",
            "confidence_level": 0.8
        }"""
        
        prompt = f"""Create a tournament plan for: {goal}
        Current round: {current_round}
        
        Consider these aspects:
        1. Question answering optimization
        2. RPS move selection strategy  
        3. Learning from opponent patterns
        4. Adapting to tournament progression
        
        Break down into specific, actionable subtasks with priorities."""
        
        response = self._call_azure_ai_agent(prompt, system_message, use_json_format=True)
        
        if response:
            try:
                plan_data = json.loads(response)
                # Convert to TournamentPlan model for validation
                plan = TournamentPlan(**plan_data)
                self.current_plan = plan
                return plan
            except (json.JSONDecodeError, Exception) as e:
                print(f"Error parsing tournament plan: {e}")
        
        # Fallback plan if AI call fails
        fallback_plan = TournamentPlan(
            main_goal=goal,
            current_round=current_round,
            subtasks=[
                SubTask(
                    task_type=TaskType.QUESTION_ANSWERING,
                    task_details="Use systematic approach to analyze and answer questions accurately",
                    priority=1,
                    estimated_effort="medium"
                ),
                SubTask(
                    task_type=TaskType.RPS_MOVE_SELECTION,
                    task_details="Apply strategic thinking to RPS moves based on game theory",
                    priority=1,
                    estimated_effort="low"
                )
            ],
            strategy_notes="Focus on accuracy and strategic consistency",
            confidence_level=0.7
        )
        self.current_plan = fallback_plan
        return fallback_plan
    
    def plan_question_strategy(self, question: str) -> QuestionStrategy:
        """
        Plan strategy for answering a specific question
        
        Args:
            question: The question to analyze and plan for
            
        Returns:
            Question answering strategy
        """
        system_message = """You are a strategic question analysis expert.
        Analyze the given question and create a strategy for answering it effectively.
        Determine the question type and the best approach to take.
        Provide response in JSON format:
        {
            "question_type": "math/knowledge/reasoning",
            "approach": "specific method to use",
            "confidence": 0.9,
            "fallback_strategy": "alternative if main approach fails"
        }"""
        
        prompt = f"""Analyze this question and create an answering strategy: "{question}"
        
        Consider:
        1. What type of question is this? (mathematical, factual knowledge, reasoning)
        2. What's the best approach to answer it accurately?
        3. How confident should we be in our approach?
        4. What's a good fallback if the main approach doesn't work?"""
        
        response = self._call_azure_ai_agent(prompt, system_message, use_json_format=True)
        
        if response:
            try:
                strategy_data = json.loads(response)
                return QuestionStrategy(**strategy_data)
            except (json.JSONDecodeError, Exception) as e:
                print(f"Error parsing question strategy: {e}")
        
        # Fallback strategy
        question_lower = question.lower()
        if any(op in question_lower for op in ['+', '-', '*', '/', '=', 'calculate', 'compute']):
            question_type = "math"
            approach = "Parse mathematical expression and compute result"
        elif any(word in question_lower for word in ['what', 'where', 'when', 'who', 'capital', 'country']):
            question_type = "knowledge"
            approach = "Use factual knowledge base to provide accurate answer"
        else:
            question_type = "reasoning"
            approach = "Apply logical reasoning to derive answer"
        
        return QuestionStrategy(
            question_type=question_type,
            approach=approach,
            confidence=0.7,
            fallback_strategy="use_general_knowledge"
        )
    
    def plan_rps_strategy(self, round_number: int = 1, opponent_history: List[int] = None) -> RPSStrategy:
        """
        Plan Rock-Paper-Scissors move strategy
        
        Args:
            round_number: Current round number
            opponent_history: Previous opponent moves if available
            
        Returns:
            RPS strategy with move choice and reasoning
        """
        system_message = """You are a strategic Rock-Paper-Scissors expert.
        Analyze the game state and recommend the optimal move with reasoning.
        Provide response in JSON format:
        {
            "move_choice": 0,
            "reasoning": "explanation for move choice",
            "confidence": 0.8,
            "counter_strategy": "approach if opponent adapts"
        }
        Move choices: 0=Rock, 1=Paper, 2=Scissors"""
        
        history_text = f"Opponent history: {opponent_history}" if opponent_history else "No opponent history available"
        
        prompt = f"""Plan the optimal RPS move for round {round_number}.
        {history_text}
        
        Consider:
        1. Game theory principles (Nash equilibrium suggests random play)
        2. If there's opponent history, look for patterns
        3. Early rounds might favor certain moves psychologically
        4. Provide reasoning for your choice
        
        Choose move (0=Rock, 1=Paper, 2=Scissors) and explain strategy."""
        
        response = self._call_azure_ai_agent(prompt, system_message, use_json_format=True)
        
        if response:
            try:
                strategy_data = json.loads(response)
                # Validate move choice is in valid range
                move_choice = strategy_data.get("move_choice", 0)
                if move_choice not in [0, 1, 2]:
                    move_choice = random.randint(0, 2)
                    strategy_data["move_choice"] = move_choice
                return RPSStrategy(**strategy_data)
            except (json.JSONDecodeError, Exception) as e:
                print(f"Error parsing RPS strategy: {e}")
        
        # Fallback strategy
        move_choice = random.randint(0, 2)
        move_names = ["Rock", "Paper", "Scissors"]
        
        return RPSStrategy(
            move_choice=move_choice,
            reasoning=f"Strategic choice of {move_names[move_choice]} based on game theory and randomization",
            confidence=0.6,
            counter_strategy="adapt_to_patterns"
        )
    
    def answer_question(self, question: str) -> str:
        """
        Answer question using planned strategy approach
        
        Args:
            question: The question to answer
            
        Returns:
            Answer to the question
        """
        # First, plan the strategy for this question
        strategy = self.plan_question_strategy(question)
        
        # Use the planned approach to answer
        system_message = f"""You are a knowledgeable assistant participating in a Paper-Scissors-Rock tournament.
        Question type identified: {strategy.question_type}
        Planned approach: {strategy.approach}
        
        Answer the question accurately and concisely using the planned approach.
        For math problems, provide only the numerical answer.
        For knowledge questions, provide brief, factual answers.
        Keep responses short and direct."""
        
        azure_answer = self._call_azure_ai_agent(question, system_message)
        
        if azure_answer:
            # Clean up the response
            cleaned_answer = azure_answer.strip()
            if cleaned_answer.lower().startswith(('the answer is', 'answer:', 'result:')):
                cleaned_answer = cleaned_answer.split(':', 1)[-1].strip()
            
            # For mathematical expressions, extract the number
            if strategy.question_type == "math":
                number_match = re.search(r'\b\d+(?:\.\d+)?\b', cleaned_answer)
                if number_match:
                    return number_match.group()
            
            # Store learning for future improvement
            self.learned_patterns["question_patterns"][strategy.question_type] = {
                "last_approach": strategy.approach,
                "confidence": strategy.confidence
            }
            
            return cleaned_answer[:50]  # Limit response length
        
        # Fallback if Azure AI fails
        return strategy.fallback_strategy
    
    def choose_rps_move(self, round_number: int = 1, opponent_history: List[int] = None) -> int:
        """
        Choose RPS move using planned strategy
        
        Args:
            round_number: Current round number
            opponent_history: Previous opponent moves if available
            
        Returns:
            Move selection as integer (0=Rock, 1=Paper, 2=Scissors)
        """
        # Plan the strategy for this move
        strategy = self.plan_rps_strategy(round_number, opponent_history)
        
        # Store learning for future improvement
        self.learned_patterns["rps_patterns"][f"round_{round_number}"] = {
            "chosen_move": strategy.move_choice,
            "reasoning": strategy.reasoning,
            "confidence": strategy.confidence
        }
        
        return strategy.move_choice
    
    def update_plan_based_on_results(self, question_result: bool = None, rps_result: str = None, round_number: int = 1):
        """
        Update planning based on tournament results (iterative planning)
        
        Args:
            question_result: Whether question was answered correctly
            rps_result: Result of RPS round ("win", "lose", "tie")
            round_number: Current round number
        """
        if not self.current_plan:
            self.create_tournament_plan(current_round=round_number)
        
        # Record results for learning
        result_data = {
            "round": round_number,
            "question_result": question_result,
            "rps_result": rps_result,
            "timestamp": f"round_{round_number}"
        }
        self.tournament_history.append(result_data)
        
        # Adapt strategy based on results
        if question_result is False:
            # Adjust question answering strategy
            for subtask in self.current_plan.subtasks:
                if subtask.task_type == TaskType.QUESTION_ANSWERING:
                    subtask.task_details = "Revise approach - previous strategy needs improvement"
                    subtask.priority = 1  # Increase priority
        
        if rps_result == "lose":
            # Adjust RPS strategy
            for subtask in self.current_plan.subtasks:
                if subtask.task_type == TaskType.RPS_MOVE_SELECTION:
                    subtask.task_details = "Analyze opponent patterns more carefully for better predictions"
                    subtask.priority = 1
        
        # Update confidence based on overall performance
        success_rate = len([r for r in self.tournament_history if r.get("question_result") == True or r.get("rps_result") == "win"]) / max(len(self.tournament_history), 1)
        self.current_plan.confidence_level = success_rate
    
    def get_current_strategy_summary(self) -> Dict[str, Any]:
        """
        Get a summary of current planning state and strategies
        
        Returns:
            Dictionary with current strategy information
        """
        return {
            "version": f"GameAgent V{self.VERSION}",
            "lesson": self.LESSON,
            "current_plan": self.current_plan.model_dump() if self.current_plan else None,
            "tournament_history_count": len(self.tournament_history),
            "learned_patterns": self.learned_patterns,
            "planning_capabilities": [
                "Tournament goal decomposition",
                "Question strategy planning",
                "RPS move strategy planning", 
                "Iterative plan adaptation",
                "Pattern learning and recognition"
            ]
        }


# Backward compatibility - maintain same interface as original GameAgent
class GameAgent(GameAgentV57):
    """Alias for backward compatibility with existing code"""
    pass


# Example usage and testing
if __name__ == "__main__":
    # Initialize planning agent
    agent = GameAgentV57()
    
    print(f"Testing Game Agent V{agent.VERSION} - {agent.LESSON}")
    print("=" * 60)
    
    # Test tournament planning
    print("\n=== Tournament Planning Test ===")
    tournament_plan = agent.create_tournament_plan("Win PSR Tournament Round 1")
    print(f"Main Goal: {tournament_plan.main_goal}")
    print(f"Confidence: {tournament_plan.confidence_level}")
    print("Subtasks:")
    for i, subtask in enumerate(tournament_plan.subtasks, 1):
        print(f"  {i}. [{subtask.task_type}] {subtask.task_details} (Priority: {subtask.priority})")
    print(f"Strategy Notes: {tournament_plan.strategy_notes}")
    
    # Test question strategy planning
    print("\n=== Question Strategy Planning Test ===")
    test_questions = [
        "What is 15 + 27?",
        "What is the capital of France?", 
        "If all cats are animals and some animals are pets, are some cats pets?"
    ]
    
    for question in test_questions:
        strategy = agent.plan_question_strategy(question)
        answer = agent.answer_question(question)
        print(f"Q: {question}")
        print(f"Strategy: {strategy.approach} (Type: {strategy.question_type}, Confidence: {strategy.confidence})")
        print(f"A: {answer}")
        print()
    
    # Test RPS strategy planning
    print("\n=== RPS Strategy Planning Test ===")
    for round_num in range(1, 4):
        strategy = agent.plan_rps_strategy(round_num)
        move = agent.choose_rps_move(round_num)
        move_names = ["Rock", "Paper", "Scissors"]
        print(f"Round {round_num}:")
        print(f"  Planned Move: {move_names[move]} ({move})")
        print(f"  Reasoning: {strategy.reasoning}")
        print(f"  Confidence: {strategy.confidence}")
    
    # Test iterative planning
    print("\n=== Iterative Planning Test ===")
    agent.update_plan_based_on_results(question_result=True, rps_result="win", round_number=1)
    agent.update_plan_based_on_results(question_result=False, rps_result="lose", round_number=2)
    
    # Get strategy summary
    print("\n=== Strategy Summary ===")
    summary = agent.get_current_strategy_summary()
    print(f"Version: {summary['version']}")
    print(f"Lesson: {summary['lesson']}")
    print(f"Tournament History: {summary['tournament_history_count']} rounds")
    print("Planning Capabilities:")
    for capability in summary['planning_capabilities']:
        print(f"  - {capability}")
    
    print("\n=== Planning Test Complete ===")