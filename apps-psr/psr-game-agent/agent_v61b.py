import random
import re
import os
import json
import requests
import time
import uuid
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Load environment variables from .env file
load_dotenv()


@dataclass
class AgentCard:
    """A2A Agent Card for agent discovery and capabilities"""
    name: str
    description: str
    skills: List[Dict[str, str]]  # [{"name": "skill_name", "description": "what it does"}]
    endpoint_url: str
    version: str
    capabilities: List[str]  # ["streaming", "push_notifications", etc.]


@dataclass
class A2AArtifact:
    """A2A Artifact containing agent work results"""
    id: str
    agent_name: str
    task_description: str
    result: Dict[str, Any]
    text_context: str
    timestamp: float


@dataclass
class A2ARequest:
    """A2A Request for agent-to-agent communication"""
    id: str
    sender_agent: str
    target_agent: str
    task: str
    context: Dict[str, Any]
    priority: int = 1


class A2AAgent(ABC):
    """Abstract base class for A2A-compatible agents"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.agent_card = self.create_agent_card()
    
    @abstractmethod
    def create_agent_card(self) -> AgentCard:
        """Create agent card describing capabilities"""
        pass
    
    @abstractmethod
    def execute_task(self, request: A2ARequest) -> A2AArtifact:
        """Execute a task and return an artifact"""
        pass


class PSRQuestionSpecialistA2A(A2AAgent):
    """A2A-compatible Question Specialist Agent"""
    
    def create_agent_card(self) -> AgentCard:
        return AgentCard(
            name="PSR Question Specialist",
            description="Specialized agent for answering PSR tournament questions with high accuracy",
            skills=[
                {"name": "answer_geography", "description": "Answer geography questions (capitals, landmarks, etc.)"},
                {"name": "answer_science", "description": "Answer science questions (chemistry, physics, biology)"},
                {"name": "answer_math", "description": "Solve mathematical problems and calculations"},
                {"name": "answer_history", "description": "Answer historical questions and dates"}
            ],
            endpoint_url="a2a://psr-question-specialist/v1",
            version="1.0.0",
            capabilities=["real_time_processing", "confidence_scoring"]
        )
    
    def execute_task(self, request: A2ARequest) -> A2AArtifact:
        task = request.task.lower()
        context = request.context
        
        if "answer" in task and "question" in context:
            question = context["question"]
            answer_result = self._answer_question(question)
            
            return A2AArtifact(
                id=str(uuid.uuid4()),
                agent_name=self.agent_name,
                task_description=f"Answered question: {question}",
                result=answer_result,
                text_context=f"Question: {question}\nAnswer: {answer_result['answer']} (confidence: {answer_result['confidence']})",
                timestamp=time.time()
            )
        
        return A2AArtifact(
            id=str(uuid.uuid4()),
            agent_name=self.agent_name,
            task_description="Task not recognized",
            result={"error": "Unknown task"},
            text_context="Unable to process the requested task",
            timestamp=time.time()
        )
    
    def _answer_question(self, question: str) -> Dict[str, Any]:
        """Answer a question using knowledge base"""
        question_lower = question.lower()
        
        # Geography
        if "capital" in question_lower and "france" in question_lower:
            return {"answer": "Paris", "confidence": 0.98, "domain": "geography"}
        elif "capital" in question_lower and "japan" in question_lower:
            return {"answer": "Tokyo", "confidence": 0.98, "domain": "geography"}
        elif "capital" in question_lower and "australia" in question_lower:
            return {"answer": "Canberra", "confidence": 0.95, "domain": "geography"}
        
        # Science
        elif "chemical symbol" in question_lower and "gold" in question_lower:
            return {"answer": "Au", "confidence": 0.99, "domain": "chemistry"}
        elif "largest ocean" in question_lower:
            return {"answer": "Pacific Ocean", "confidence": 0.95, "domain": "geography"}
        elif "speed of light" in question_lower:
            return {"answer": "299,792,458 m/s", "confidence": 0.99, "domain": "physics"}
        
        # Math
        elif "+" in question or "plus" in question_lower:
            try:
                numbers = re.findall(r'\d+', question)
                if len(numbers) >= 2:
                    result = sum(int(n) for n in numbers)
                    return {"answer": str(result), "confidence": 0.99, "domain": "mathematics"}
            except:
                pass
        elif "-" in question and "minus" in question_lower:
            try:
                numbers = re.findall(r'\d+', question)
                if len(numbers) >= 2:
                    result = int(numbers[0]) - int(numbers[1])
                    return {"answer": str(result), "confidence": 0.99, "domain": "mathematics"}
            except:
                pass
        
        return {"answer": "Unknown", "confidence": 0.1, "domain": "unknown"}


class PSRStrategyAnalystA2A(A2AAgent):
    """A2A-compatible Strategy Analyst Agent"""
    
    def create_agent_card(self) -> AgentCard:
        return AgentCard(
            name="PSR Strategy Analyst",
            description="Advanced strategy analysis for Rock, Paper, Scissors gameplay",
            skills=[
                {"name": "analyze_opponent", "description": "Analyze opponent patterns and tendencies"},
                {"name": "recommend_move", "description": "Recommend optimal RPS moves based on game state"},
                {"name": "evaluate_risk", "description": "Evaluate risk/reward of different strategies"}
            ],
            endpoint_url="a2a://psr-strategy-analyst/v1",
            version="1.0.0",
            capabilities=["pattern_recognition", "predictive_modeling"]
        )
    
    def execute_task(self, request: A2ARequest) -> A2AArtifact:
        task = request.task.lower()
        context = request.context
        
        if "strategy" in task or "move" in task:
            round_number = context.get("round_number", 1)
            current_score = context.get("current_score", 0)
            
            strategy_result = self._analyze_strategy(round_number, current_score)
            
            return A2AArtifact(
                id=str(uuid.uuid4()),
                agent_name=self.agent_name,
                task_description=f"Strategy analysis for round {round_number}",
                result=strategy_result,
                text_context=f"Round {round_number}: Recommend {strategy_result['move']} (confidence: {strategy_result['confidence']})",
                timestamp=time.time()
            )
        
        return A2AArtifact(
            id=str(uuid.uuid4()),
            agent_name=self.agent_name,
            task_description="Task not recognized",
            result={"error": "Unknown task"},
            text_context="Unable to process the requested task",
            timestamp=time.time()
        )
    
    def _analyze_strategy(self, round_number: int, current_score: int) -> Dict[str, Any]:
        """Analyze optimal strategy"""
        moves = ["Rock", "Paper", "Scissors"]
        
        if round_number == 1:
            move = "Paper"  # Counter common Rock choice
            reasoning = "First round: counter common Rock choice"
            confidence = 0.7
        elif round_number <= 3:
            move = "Scissors"  # Counter common Paper choice in early rounds
            reasoning = "Early rounds: counter common Paper choice"
            confidence = 0.6
        else:
            move = "Rock"  # Show strength in later rounds
            reasoning = "Late rounds: show strength with Rock"
            confidence = 0.6
        
        # Score-based adjustments
        if current_score < 0:
            move = "Paper"
            reasoning = "Behind in score: conservative Paper strategy"
            confidence = 0.8
        elif current_score > 2:
            move = "Rock"
            reasoning = "Ahead in score: aggressive Rock strategy"
            confidence = 0.8
        
        return {
            "move": move,
            "confidence": confidence,
            "reasoning": reasoning,
            "move_number": {"Rock": 0, "Paper": 1, "Scissors": 2}[move],
            "round_analysis": f"Round {round_number} strategic assessment"
        }


class A2ACoordinator:
    """A2A Coordinator for managing agent interactions"""
    
    def __init__(self):
        self.registered_agents: Dict[str, A2AAgent] = {}
        self.artifacts: List[A2AArtifact] = []
    
    def register_agent(self, agent: A2AAgent):
        """Register an A2A agent"""
        self.registered_agents[agent.agent_name] = agent
        print(f"[A2A] Registered agent: {agent.agent_name}")
    
    def list_agents(self) -> List[AgentCard]:
        """List all registered agent cards"""
        return [agent.agent_card for agent in self.registered_agents.values()]
    
    def send_request(self, request: A2ARequest) -> Optional[A2AArtifact]:
        """Send request to target agent and get artifact"""
        if request.target_agent not in self.registered_agents:
            print(f"[A2A] Agent {request.target_agent} not found")
            return None
        
        target_agent = self.registered_agents[request.target_agent]
        artifact = target_agent.execute_task(request)
        self.artifacts.append(artifact)
        
        print(f"[A2A] Task completed by {request.target_agent}: {artifact.task_description}")
        return artifact
    
    def get_communication_stats(self) -> Dict[str, Any]:
        """Get A2A communication statistics"""
        return {
            "registered_agents": len(self.registered_agents),
            "artifacts_created": len(self.artifacts),
            "agent_names": list(self.registered_agents.keys())
        }


class GameAgentV61B:
    """Game Agent V61B - Enhanced with A2A (Agent-to-Agent) protocol capability
    
    This version demonstrates A2A concepts from lesson 61:
    - Agent-to-agent communication and collaboration
    - Distributed agent coordination
    - Agent card-based capability discovery
    - Artifact-based work product exchange
    """
    
    def __init__(self, azure_ai_endpoint: Optional[str] = None, azure_ai_key: Optional[str] = None):
        """
        Initialize the A2A-enhanced game agent
        
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
        
        # Initialize A2A coordinator and agents
        self.a2a_coordinator = A2ACoordinator()
        self.setup_a2a_agents()
    
    def setup_a2a_agents(self):
        """Setup A2A agents for specialized tasks"""
        # Create and register specialized agents
        question_agent = PSRQuestionSpecialistA2A("PSR Question Specialist")
        strategy_agent = PSRStrategyAnalystA2A("PSR Strategy Analyst")
        
        self.a2a_coordinator.register_agent(question_agent)
        self.a2a_coordinator.register_agent(strategy_agent)
        
        agents = self.a2a_coordinator.list_agents()
        print(f"[A2A] Initialized A2A coordinator with {len(agents)} agents")
        for agent in agents:
            print(f"[A2A]   - {agent.name}: {len(agent.skills)} skills")
    
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
        Generate an answer to the question using A2A coordination first, then fallback to Azure AI
        
        Args:
            question: The question to answer
            
        Returns:
            Answer to the question
        """
        print(f"[A2A] Coordinating question answering: {question}")
        
        # Create A2A request for question specialist
        request = A2ARequest(
            id=str(uuid.uuid4()),
            sender_agent="PSR Tournament Coordinator",
            target_agent="PSR Question Specialist",
            task="answer question",
            context={"question": question},
            priority=1
        )
        
        # Send request to A2A agent
        artifact = self.a2a_coordinator.send_request(request)
        
        if artifact and "error" not in artifact.result:
            answer = artifact.result.get("answer", "")
            confidence = artifact.result.get("confidence", 0)
            domain = artifact.result.get("domain", "")
            
            if confidence > 0.5:
                print(f"[A2A] Answer found: {answer} (confidence: {confidence:.2f}, domain: {domain})")
                return answer
        
        print(f"[A2A] No confident answer from specialist, falling back to Azure AI")
        
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
        Choose Rock (0), Paper (1), or Scissors (2) using A2A strategy coordination first, then fallback
        
        Returns:
            Move selection as integer (0=Rock, 1=Paper, 2=Scissors)
        """
        print(f"[A2A] Coordinating strategy analysis for move selection")
        
        # Create A2A request for strategy analyst
        request = A2ARequest(
            id=str(uuid.uuid4()),
            sender_agent="PSR Tournament Coordinator",
            target_agent="PSR Strategy Analyst",
            task="analyze strategy and recommend move",
            context={
                "round_number": 1,  # Default round, could be enhanced to track actual round
                "current_score": 0   # Default score, could be enhanced to track actual score
            },
            priority=1
        )
        
        # Send request to A2A agent
        artifact = self.a2a_coordinator.send_request(request)
        
        if artifact and "error" not in artifact.result:
            move_number = artifact.result.get("move_number", 0)
            move_name = artifact.result.get("move", "Rock")
            confidence = artifact.result.get("confidence", 0)
            reasoning = artifact.result.get("reasoning", "")
            
            if confidence > 0.5:
                print(f"[A2A] Strategy: {move_name} (confidence: {confidence:.2f}) - {reasoning}")
                return move_number
        
        print(f"[A2A] No confident strategy from analyst, falling back to Azure AI")
        
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

    def get_a2a_capabilities(self) -> Dict[str, Any]:
        """Get information about A2A coordinator capabilities"""
        agent_cards = self.a2a_coordinator.list_agents()
        stats = self.a2a_coordinator.get_communication_stats()
        
        return {
            "agents": [
                {
                    "name": card.name,
                    "description": card.description,
                    "skills": card.skills,
                    "version": card.version,
                    "capabilities": card.capabilities
                }
                for card in agent_cards
            ],
            "communication_stats": stats,
            "coordinator_info": "PSR Tournament A2A Coordinator v1.0"
        }


# Backward compatibility - maintain same interface as original GameAgent
class GameAgent(GameAgentV61B):
    """Alias for backward compatibility with existing code"""
    pass


# Example usage and testing
if __name__ == "__main__":
    # Initialize A2A-enhanced agent
    agent = GameAgentV61B()
    
    # Display A2A capabilities
    print("A2A-Enhanced Game Agent V61B")
    print("=" * 50)
    
    capabilities = agent.get_a2a_capabilities()
    print(f"A2A Coordinator: {capabilities['coordinator_info']}")
    print(f"Registered Agents: {len(capabilities['agents'])}")
    
    for agent_info in capabilities['agents']:
        print(f"\nAgent: {agent_info['name']} (v{agent_info['version']})")
        print(f"  Description: {agent_info['description']}")
        print(f"  Skills: {[skill['name'] for skill in agent_info['skills']]}")
        print(f"  Capabilities: {agent_info['capabilities']}")
    
    print(f"\nCommunication Stats: {capabilities['communication_stats']}")
    
    print("\nTesting A2A-enhanced question answering:")
    print("=" * 50)
    
    # Test question answering with A2A coordination
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
    
    # Test A2A-enhanced RPS move selection
    print("Testing A2A-enhanced RPS move selection:")
    print("=" * 50)
    for i in range(3):
        move = agent.choose_rps_move()
        move_names = {0: "Rock", 1: "Paper", 2: "Scissors"}
        print(f"Move {i+1}: {move_names[move]} ({move})")
        print()
    
    # Display final A2A communication stats
    final_capabilities = agent.get_a2a_capabilities()
    print("Final A2A Communication Statistics:")
    print("=" * 50)
    print(json.dumps(final_capabilities['communication_stats'], indent=2))