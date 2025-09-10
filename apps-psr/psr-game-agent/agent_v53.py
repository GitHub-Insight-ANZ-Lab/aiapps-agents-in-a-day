"""
PSR Game Agent V53 - Agentic Frameworks Implementation
This version demonstrates the concepts from lesson 53 (Agentic Frameworks)
- Implements simple agents for Semantic Kernel, Azure AI Agent Service, and AutoGen
- Multiple framework options for different enterprise scenarios
- Follows the same interface as agent_v1.py for consistency
"""

import random
import re
import os
import json
import asyncio
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Try to import framework dependencies
try:
    from semantic_kernel import Kernel
    from semantic_kernel.functions import kernel_function
    from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
    SEMANTIC_KERNEL_AVAILABLE = True
except ImportError:
    SEMANTIC_KERNEL_AVAILABLE = False

try:
    from azure.identity.aio import DefaultAzureCredential
    from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings
    AZURE_AI_SERVICE_AVAILABLE = True
except ImportError:
    AZURE_AI_SERVICE_AVAILABLE = False

try:
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.messages import TextMessage
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    AUTOGEN_AVAILABLE = True
except ImportError:
    AUTOGEN_AVAILABLE = False


class SemanticKernelGameAgent:
    """Game agent implementation using Semantic Kernel framework"""
    
    def __init__(self, azure_openai_endpoint: Optional[str] = None, azure_openai_key: Optional[str] = None):
        """Initialize Semantic Kernel game agent"""
        self.endpoint = azure_openai_endpoint or os.getenv('AZURE_OPENAI_ENDPOINT')
        self.api_key = azure_openai_key or os.getenv('AZURE_OPENAI_KEY')
        self.kernel = None
        
        if SEMANTIC_KERNEL_AVAILABLE and self.endpoint and self.api_key:
            try:
                self.kernel = Kernel()
                # Add Azure OpenAI chat completion service
                self.kernel.add_service(
                    AzureChatCompletion(
                        deployment_name="gpt-4o-mini",
                        api_key=self.api_key,
                        endpoint=self.endpoint,
                    )
                )
            except Exception as e:
                print(f"Failed to initialize Semantic Kernel: {e}")
                self.kernel = None
    
    async def answer_question(self, question: str) -> str:
        """Answer question using Semantic Kernel"""
        if not self.kernel:
            return f"Semantic Kernel not available. Direct answer: {self._fallback_answer(question)}"
        
        try:
            # Create a prompt function for question answering
            from semantic_kernel.functions import KernelFunctionFromPrompt
            
            answer_function = KernelFunctionFromPrompt(
                function_name="AnswerQuestion",
                prompt="""
                You are a knowledgeable assistant in a Paper-Scissors-Rock tournament. 
                Answer the question accurately and concisely.
                Question: {{$question}}
                
                Provide a brief, factual answer. For math problems, give only the number.
                """,
            )
            
            response = await answer_function.invoke(kernel=self.kernel, question=question)
            return str(response).strip()[:50]
            
        except Exception as e:
            print(f"Semantic Kernel error: {e}")
            return self._fallback_answer(question)
    
    async def choose_rps_move(self) -> int:
        """Choose RPS move using Semantic Kernel"""
        if not self.kernel:
            return random.randint(0, 2)
        
        try:
            from semantic_kernel.functions import KernelFunctionFromPrompt
            
            strategy_function = KernelFunctionFromPrompt(
                function_name="ChooseRPSMove",
                prompt="""
                You are a strategic Rock-Paper-Scissors player in a tournament.
                Choose the best move: Rock, Paper, or Scissors.
                Respond with only one word: Rock, Paper, or Scissors.
                """,
            )
            
            response = await strategy_function.invoke(kernel=self.kernel)
            choice = str(response).lower().strip()
            
            if 'rock' in choice:
                return 0
            elif 'paper' in choice:
                return 1
            elif 'scissors' in choice or 'scissor' in choice:
                return 2
            else:
                return random.randint(0, 2)
                
        except Exception as e:
            print(f"Semantic Kernel strategy error: {e}")
            return random.randint(0, 2)
    
    def _fallback_answer(self, question: str) -> str:
        """Simple fallback for basic questions"""
        question_lower = question.lower()
        
        # Basic math operations
        if '+' in question:
            numbers = re.findall(r'\d+', question)
            if len(numbers) >= 2:
                return str(int(numbers[0]) + int(numbers[1]))
        elif '-' in question:
            numbers = re.findall(r'\d+', question)
            if len(numbers) >= 2:
                return str(int(numbers[0]) - int(numbers[1]))
        elif '*' in question or 'times' in question_lower:
            numbers = re.findall(r'\d+', question)
            if len(numbers) >= 2:
                return str(int(numbers[0]) * int(numbers[1]))
        
        # Basic knowledge
        if 'capital' in question_lower and 'france' in question_lower:
            return "Paris"
        elif 'sky' in question_lower and 'color' in question_lower:
            return "Blue"
        
        return "I don't know"


class AzureAIServiceGameAgent:
    """Game agent implementation using Azure AI Agent Service"""
    
    def __init__(self, project_connection_string: Optional[str] = None):
        """Initialize Azure AI Agent Service game agent"""
        self.connection_string = project_connection_string or os.getenv('AZURE_AI_PROJECT_CONNECTION_STRING')
        self.agent_client = None
        self.agent_id = None
        
        # Note: This would require actual Azure AI Agent Service setup
        # For demonstration purposes, we'll use a simulated approach
        
    async def answer_question(self, question: str) -> str:
        """Answer question using Azure AI Agent Service"""
        if not AZURE_AI_SERVICE_AVAILABLE or not self.connection_string:
            return f"Azure AI Service not available. Direct answer: {self._fallback_answer(question)}"
        
        try:
            # In a real implementation, this would create an agent and get response
            # For now, simulate the service call
            return await self._simulate_azure_ai_service(
                f"Answer this question accurately and briefly: {question}"
            )
            
        except Exception as e:
            print(f"Azure AI Service error: {e}")
            return self._fallback_answer(question)
    
    async def choose_rps_move(self) -> int:
        """Choose RPS move using Azure AI Agent Service"""
        if not AZURE_AI_SERVICE_AVAILABLE or not self.connection_string:
            return random.randint(0, 2)
        
        try:
            response = await self._simulate_azure_ai_service(
                "Choose Rock, Paper, or Scissors for a strategic game. Respond with one word only."
            )
            
            choice = response.lower().strip()
            if 'rock' in choice:
                return 0
            elif 'paper' in choice:
                return 1
            elif 'scissors' in choice or 'scissor' in choice:
                return 2
            else:
                return random.randint(0, 2)
                
        except Exception as e:
            print(f"Azure AI Service strategy error: {e}")
            return random.randint(0, 2)
    
    async def _simulate_azure_ai_service(self, prompt: str) -> str:
        """Simulate Azure AI Agent Service response"""
        # This simulates what would be a real Azure AI Agent Service call
        # In production, this would use the actual Azure AI Agent Service SDK
        
        if "question" in prompt.lower():
            if "+" in prompt:
                numbers = re.findall(r'\d+', prompt)
                if len(numbers) >= 2:
                    return str(int(numbers[0]) + int(numbers[1]))
            elif "capital" in prompt.lower() and "france" in prompt.lower():
                return "Paris"
            elif "sky" in prompt.lower():
                return "Blue"
            return "Unknown"
        elif "rock" in prompt.lower() or "paper" in prompt.lower() or "scissors" in prompt.lower():
            return random.choice(["Rock", "Paper", "Scissors"])
        
        return "I cannot answer that"
    
    def _fallback_answer(self, question: str) -> str:
        """Simple fallback for basic questions"""
        return SemanticKernelGameAgent._fallback_answer(self, question)


class AutoGenGameAgent:
    """Game agent implementation using AutoGen framework"""
    
    def __init__(self, model_endpoint: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize AutoGen game agent"""
        self.model_endpoint = model_endpoint or os.getenv('AZURE_OPENAI_ENDPOINT')
        self.api_key = api_key or os.getenv('AZURE_OPENAI_KEY')
        self.assistant_agent = None
        
        if AUTOGEN_AVAILABLE and self.model_endpoint and self.api_key:
            try:
                # Create OpenAI client for AutoGen
                model_client = OpenAIChatCompletionClient(
                    model="gpt-4o-mini",
                    api_key=self.api_key,
                    base_url=f"{self.model_endpoint}/openai/deployments/gpt-4o-mini"
                )
                
                # Create assistant agent
                self.assistant_agent = AssistantAgent(
                    name="PSRTournamentAgent",
                    model_client=model_client
                )
                
            except Exception as e:
                print(f"Failed to initialize AutoGen: {e}")
                self.assistant_agent = None
    
    async def answer_question(self, question: str) -> str:
        """Answer question using AutoGen"""
        if not self.assistant_agent:
            return f"AutoGen not available. Direct answer: {self._fallback_answer(question)}"
        
        try:
            # Create message for the agent
            message = TextMessage(
                content=f"Answer this question accurately and briefly for a PSR tournament: {question}",
                source="user"
            )
            
            # Get response from assistant agent
            response = await self.assistant_agent.on_messages([message], None)
            
            if response and response.chat_message:
                return str(response.chat_message.content).strip()[:50]
            else:
                return self._fallback_answer(question)
                
        except Exception as e:
            print(f"AutoGen error: {e}")
            return self._fallback_answer(question)
    
    async def choose_rps_move(self) -> int:
        """Choose RPS move using AutoGen"""
        if not self.assistant_agent:
            return random.randint(0, 2)
        
        try:
            message = TextMessage(
                content="Choose Rock, Paper, or Scissors for a strategic tournament game. Respond with one word only.",
                source="user"
            )
            
            response = await self.assistant_agent.on_messages([message], None)
            
            if response and response.chat_message:
                choice = str(response.chat_message.content).lower().strip()
                
                if 'rock' in choice:
                    return 0
                elif 'paper' in choice:
                    return 1
                elif 'scissors' in choice or 'scissor' in choice:
                    return 2
            
            return random.randint(0, 2)
                
        except Exception as e:
            print(f"AutoGen strategy error: {e}")
            return random.randint(0, 2)
    
    def _fallback_answer(self, question: str) -> str:
        """Simple fallback for basic questions"""
        return SemanticKernelGameAgent._fallback_answer(self, question)


class GameAgentV53:
    """
    PSR Game Agent V53 - Agentic Frameworks Implementation
    
    This version demonstrates lesson 53 concepts:
    - Support for multiple agentic frameworks (Semantic Kernel, Azure AI Agent Service, AutoGen)
    - Framework switching capability for different enterprise scenarios
    - Consistent interface regardless of underlying framework
    - Fallback mechanisms when frameworks are not available
    """
    
    VERSION = "53.0.0"
    LESSON = "53 - Agentic Frameworks"
    
    def __init__(self, framework: str = "semantic_kernel", **kwargs):
        """
        Initialize game agent with specified framework
        
        Args:
            framework: Framework to use ("semantic_kernel", "azure_ai_service", "autogen")
            **kwargs: Framework-specific configuration parameters
        """
        self.framework = framework.lower()
        self.agent = None
        
        # Initialize the appropriate framework agent
        if self.framework == "semantic_kernel":
            self.agent = SemanticKernelGameAgent(**kwargs)
        elif self.framework == "azure_ai_service":
            self.agent = AzureAIServiceGameAgent(**kwargs)
        elif self.framework == "autogen":
            self.agent = AutoGenGameAgent(**kwargs)
        else:
            raise ValueError(f"Unsupported framework: {framework}")
        
        print(f"Initialized GameAgentV53 with {self.framework} framework")
    
    async def answer_question(self, question: str) -> str:
        """
        Generate an answer to the question using the selected framework
        
        Args:
            question: The question to answer
            
        Returns:
            Answer to the question
        """
        if self.agent:
            return await self.agent.answer_question(question)
        else:
            return "Agent not initialized"
    
    async def choose_rps_move(self) -> int:
        """
        Choose Rock (0), Paper (1), or Scissors (2) using the selected framework
        
        Returns:
            Move selection as integer (0=Rock, 1=Paper, 2=Scissors)
        """
        if self.agent:
            return await self.agent.choose_rps_move()
        else:
            return random.randint(0, 2)
    
    def get_framework_info(self) -> Dict[str, Any]:
        """Get information about the current framework and availability"""
        return {
            "current_framework": self.framework,
            "semantic_kernel_available": SEMANTIC_KERNEL_AVAILABLE,
            "azure_ai_service_available": AZURE_AI_SERVICE_AVAILABLE,
            "autogen_available": AUTOGEN_AVAILABLE,
            "agent_initialized": self.agent is not None
        }


# Backward compatibility - maintain same interface as original GameAgent
class GameAgent(GameAgentV53):
    """Alias for backward compatibility with existing code"""
    pass


# Example usage and testing
if __name__ == "__main__":
    async def test_frameworks():
        """Test all available frameworks"""
        frameworks = ["semantic_kernel", "azure_ai_service", "autogen"]
        
        # Test questions
        test_questions = [
            "What is 15 + 27?",
            "What is the capital of France?",
            "What color is the sky?",
            "What is 100 - 35?"
        ]
        
        print("Testing Agentic Frameworks - Agent V53:")
        print("=" * 50)
        
        for framework in frameworks:
            print(f"\n=== Testing {framework.upper()} Framework ===")
            
            try:
                agent = GameAgentV53(framework=framework)
                
                # Display framework availability
                info = agent.get_framework_info()
                print(f"Framework availability: {info}")
                
                # Test question answering
                print(f"\nQuestion Answering with {framework}:")
                for question in test_questions[:2]:  # Test first 2 questions
                    answer = await agent.answer_question(question)
                    print(f"Q: {question}")
                    print(f"A: {answer}")
                
                # Test RPS move selection
                print(f"\nRPS Move Selection with {framework}:")
                moves = ["Rock", "Paper", "Scissors"]
                for i in range(3):
                    move_idx = await agent.choose_rps_move()
                    move_name = moves[move_idx] if 0 <= move_idx <= 2 else "Invalid"
                    print(f"Move {i+1}: {move_name} ({move_idx})")
                
            except Exception as e:
                print(f"Failed to test {framework}: {e}")
        
        print(f"\n=== Framework Comparison ===")
        print("Semantic Kernel: Enterprise-ready AI orchestration with plugins and memory")
        print("Azure AI Service: Platform service with built-in Azure integrations")
        print("AutoGen: Event-driven, distributed multi-agent applications")
    
    # Run the async test
    asyncio.run(test_frameworks())