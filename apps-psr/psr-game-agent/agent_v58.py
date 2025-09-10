"""
PSR Game Agent V58 - Multi-Agent Tournament Coordinator
Based on lesson 58 (Multi-Agent Design Patterns) and following agent_v1.py structure

This agent implements multi-agent design patterns for PSR tournament coordination:
- Tournament coordination with specialized sub-agents
- Inter-agent communication protocols
- Collaborative decision making for questions and moves
- Performance monitoring and optimization
"""

import random
import re
import os
import json
import requests
import time
import threading
from typing import Optional, Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum
# Try to load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Gracefully handle missing dotenv dependency
    pass


class AgentSpecialty(Enum):
    """Define specialized agent types for tournament coordination"""
    QUESTION_ANALYST = "question_analyst"
    STRATEGY_COORDINATOR = "strategy_coordinator"
    PERFORMANCE_TRACKER = "performance_tracker"


@dataclass
class AgentDecision:
    """Structure for agent decision results"""
    agent_type: str
    decision: str
    confidence: float
    reasoning: str
    timestamp: float


class TournamentCoordinatorV58:
    """Multi-agent tournament coordinator following agent_v1.py pattern"""
    
    def __init__(self, azure_ai_endpoint: Optional[str] = None, azure_ai_key: Optional[str] = None):
        """
        Initialize the multi-agent tournament coordinator
        
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
        
        # Multi-agent system components
        self.sub_agents = {
            AgentSpecialty.QUESTION_ANALYST: QuestionAnalystAgent(),
            AgentSpecialty.STRATEGY_COORDINATOR: StrategyCoordinatorAgent(),
            AgentSpecialty.PERFORMANCE_TRACKER: PerformanceTrackerAgent()
        }
        
        # Communication and coordination state
        self.decision_history: List[AgentDecision] = []
        self.performance_metrics = {
            "questions_processed": 0,
            "moves_coordinated": 0,
            "agent_consultations": 0,
            "average_confidence": 0.0
        }
        
        # Tournament coordination state
        self.round_history: List[Dict[str, Any]] = []
        self.current_strategy = "balanced"  # balanced, aggressive, defensive
        
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
                        "content": system_message or "You are a specialized tournament coordinator agent focused on optimal decision making."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 150,
                "temperature": 0.2,  # Lower temperature for more consistent strategic decisions
                "top_p": 0.8
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
    
    def coordinate_decision(self, question: str, context: Dict[str, Any] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Coordinate decision making across multiple specialized agents
        
        Args:
            question: The question to process
            context: Additional context for decision making
            
        Returns:
            Tuple of (final_answer, coordination_metadata)
        """
        context = context or {}
        coordination_start = time.time()
        
        # Step 1: Question Analysis Agent consultation
        question_analysis = self.sub_agents[AgentSpecialty.QUESTION_ANALYST].analyze_question(question)
        
        # Step 2: Strategy Coordinator consultation
        strategy_input = {
            "question": question,
            "analysis": question_analysis,
            "round_number": context.get("round_number", 1),
            "current_strategy": self.current_strategy
        }
        strategy_decision = self.sub_agents[AgentSpecialty.STRATEGY_COORDINATOR].recommend_strategy(strategy_input)
        
        # Step 3: Performance Tracker consultation
        performance_input = {
            "question_complexity": question_analysis.get("complexity", "medium"),
            "strategy_confidence": strategy_decision.get("confidence", 0.5),
            "round_history": self.round_history
        }
        performance_guidance = self.sub_agents[AgentSpecialty.PERFORMANCE_TRACKER].assess_performance(performance_input)
        
        # Step 4: Coordinator synthesis using Azure AI if available
        coordination_prompt = f"""
        As a tournament coordinator, synthesize the following agent inputs to provide the best answer:
        
        Question: {question}
        Question Analysis: {question_analysis.get('category', 'general')} - {question_analysis.get('approach', 'direct')}
        Strategy Recommendation: {strategy_decision.get('recommendation', 'standard')}
        Performance Guidance: {performance_guidance.get('recommendation', 'proceed')}
        
        Provide a clear, concise answer focusing on accuracy and strategic value.
        """
        
        system_message = "You are a tournament coordinator agent synthesizing input from specialized sub-agents to make optimal decisions."
        
        # Try Azure AI coordination
        coordinated_answer = self._call_azure_ai_agent(coordination_prompt, system_message)
        
        # Fallback to local coordination if Azure AI unavailable
        if not coordinated_answer:
            coordinated_answer = self._local_coordination_fallback(question, question_analysis, strategy_decision)
        
        # Calculate overall confidence
        confidence_scores = [
            question_analysis.get("confidence", 0.5),
            strategy_decision.get("confidence", 0.5),
            performance_guidance.get("confidence", 0.5)
        ]
        overall_confidence = sum(confidence_scores) / len(confidence_scores)
        
        # Record decision
        decision = AgentDecision(
            agent_type="coordinator_v58",
            decision=coordinated_answer,
            confidence=overall_confidence,
            reasoning=f"Multi-agent coordination: {len(self.sub_agents)} specialists consulted",
            timestamp=time.time()
        )
        self.decision_history.append(decision)
        
        # Update metrics
        self.performance_metrics["questions_processed"] += 1
        self.performance_metrics["agent_consultations"] += len(self.sub_agents)
        self.performance_metrics["average_confidence"] = (
            (self.performance_metrics["average_confidence"] * (self.performance_metrics["questions_processed"] - 1) + overall_confidence) /
            self.performance_metrics["questions_processed"]
        )
        
        coordination_metadata = {
            "coordination_time": time.time() - coordination_start,
            "agents_consulted": list(self.sub_agents.keys()),
            "overall_confidence": overall_confidence,
            "question_analysis": question_analysis,
            "strategy_decision": strategy_decision,
            "performance_guidance": performance_guidance
        }
        
        return coordinated_answer, coordination_metadata
    
    def _local_coordination_fallback(self, question: str, question_analysis: Dict, strategy_decision: Dict) -> str:
        """
        Local fallback coordination when Azure AI is unavailable
        
        Args:
            question: The original question
            question_analysis: Analysis from question analyst agent
            strategy_decision: Decision from strategy coordinator
            
        Returns:
            Coordinated answer
        """
        # Use question analysis to determine answer approach
        if question_analysis.get("category") == "math":
            # Mathematical questions - try to compute
            import re
            numbers = re.findall(r'\d+', question)
            if len(numbers) >= 2:
                if '+' in question or 'plus' in question.lower():
                    result = sum(int(n) for n in numbers)
                    return str(result)
                elif '-' in question or 'minus' in question.lower():
                    result = int(numbers[0]) - int(numbers[1])
                    return str(result)
        
        elif question_analysis.get("category") == "geography":
            # Geography knowledge base
            capitals = {
                "france": "Paris", "japan": "Tokyo", "australia": "Canberra",
                "germany": "Berlin", "italy": "Rome", "spain": "Madrid"
            }
            question_lower = question.lower()
            for country, capital in capitals.items():
                if country in question_lower:
                    return capital
        
        elif question_analysis.get("category") == "science":
            # Science knowledge base
            science_facts = {
                "gold": "Au", "water": "H2O", "oxygen": "O2",
                "largest ocean": "Pacific Ocean", "smallest planet": "Mercury"
            }
            question_lower = question.lower()
            for topic, answer in science_facts.items():
                if topic in question_lower:
                    return answer
        
        # Default coordinated response
        return strategy_decision.get("fallback_answer", "Need to research this question")
    
    def answer_question(self, question: str) -> str:
        """
        Generate an answer to the question using multi-agent coordination
        Following agent_v1.py interface for compatibility
        
        Args:
            question: The question to answer
            
        Returns:
            Answer to the question
        """
        answer, metadata = self.coordinate_decision(question)
        
        # Clean up the response to extract just the answer (similar to agent_v1.py)
        cleaned_answer = answer.strip()
        if cleaned_answer.lower().startswith(('the answer is', 'answer:', 'result:')):
            cleaned_answer = cleaned_answer.split(':', 1)[-1].strip()
        
        # For mathematical expressions, try to extract just the number
        if any(op in question for op in ['+', '-', '*', '/', '=']):
            number_match = re.search(r'\b\d+(?:\.\d+)?\b', cleaned_answer)
            if number_match:
                return number_match.group()
        
        return cleaned_answer[:50]  # Limit response length like agent_v1.py
    
    def coordinate_rps_strategy(self, context: Dict[str, Any] = None) -> Tuple[int, Dict[str, Any]]:
        """
        Coordinate Rock-Paper-Scissors move selection across agents
        
        Args:
            context: Context for move selection (round number, opponent history, etc.)
            
        Returns:
            Tuple of (move_selection, coordination_metadata)
        """
        context = context or {}
        
        # Get strategic input from coordinator agent
        strategy_input = {
            "round_number": context.get("round_number", 1),
            "opponent_history": context.get("opponent_history", []),
            "current_score": context.get("current_score", 0),
            "current_strategy": self.current_strategy
        }
        
        strategy_decision = self.sub_agents[AgentSpecialty.STRATEGY_COORDINATOR].recommend_rps_move(strategy_input)
        
        # Use Azure AI for enhanced strategic thinking if available
        if self.azure_ai_endpoint and self.azure_ai_key:
            prompt = f"""
            In a Rock-Paper-Scissors tournament (Round {context.get('round_number', 1)}), choose the optimal move.
            Strategy recommendation: {strategy_decision.get('recommended_move', 'balanced')}
            Current strategy: {self.current_strategy}
            
            Respond with only: Rock, Paper, or Scissors
            """
            
            system_message = "You are a strategic tournament coordinator making optimal RPS decisions based on multi-agent analysis."
            azure_choice = self._call_azure_ai_agent(prompt, system_message)
            
            if azure_choice:
                choice_lower = azure_choice.lower().strip()
                if 'rock' in choice_lower:
                    final_move = 0
                elif 'paper' in choice_lower:
                    final_move = 1
                elif 'scissors' in choice_lower or 'scissor' in choice_lower:
                    final_move = 2
                else:
                    final_move = strategy_decision.get("move_number", random.randint(0, 2))
            else:
                final_move = strategy_decision.get("move_number", random.randint(0, 2))
        else:
            final_move = strategy_decision.get("move_number", random.randint(0, 2))
        
        # Update metrics
        self.performance_metrics["moves_coordinated"] += 1
        
        # Record round for future strategy adaptation
        round_record = {
            "round_number": context.get("round_number", 1),
            "move_selected": final_move,
            "strategy_used": self.current_strategy,
            "confidence": strategy_decision.get("confidence", 0.5),
            "timestamp": time.time()
        }
        self.round_history.append(round_record)
        
        coordination_metadata = {
            "strategy_recommendation": strategy_decision,
            "agents_consulted": ["strategy_coordinator"],
            "final_confidence": strategy_decision.get("confidence", 0.5)
        }
        
        return final_move, coordination_metadata
    
    def choose_rps_move(self) -> int:
        """
        Choose Rock (0), Paper (1), or Scissors (2) using multi-agent coordination
        Following agent_v1.py interface for compatibility
        
        Returns:
            Move selection as integer (0=Rock, 1=Paper, 2=Scissors)
        """
        move, metadata = self.coordinate_rps_strategy()
        return move
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive performance summary of the multi-agent system
        
        Returns:
            Performance metrics and analysis
        """
        total_decisions = len(self.decision_history)
        
        if total_decisions > 0:
            confidence_scores = [d.confidence for d in self.decision_history]
            avg_confidence = sum(confidence_scores) / len(confidence_scores)
            
            # Analyze decision patterns
            agent_usage = {}
            for decision in self.decision_history:
                agent_usage[decision.agent_type] = agent_usage.get(decision.agent_type, 0) + 1
        else:
            avg_confidence = 0.0
            agent_usage = {}
        
        return {
            "total_decisions": total_decisions,
            "average_confidence": avg_confidence,
            "agent_usage_distribution": agent_usage,
            "performance_metrics": self.performance_metrics,
            "round_history_count": len(self.round_history),
            "current_strategy": self.current_strategy,
            "sub_agents_active": len(self.sub_agents)
        }


class QuestionAnalystAgent:
    """Specialized agent for analyzing and categorizing questions"""
    
    def analyze_question(self, question: str) -> Dict[str, Any]:
        """
        Analyze question type and determine optimal approach
        
        Args:
            question: Question to analyze
            
        Returns:
            Analysis results with category, approach, and confidence
        """
        question_lower = question.lower()
        
        # Mathematical questions
        if any(op in question for op in ['+', 'plus', '-', 'minus', '*', 'times', '/', 'divided']):
            return {
                "category": "math",
                "approach": "calculation",
                "confidence": 0.9,
                "complexity": "low"
            }
        
        # Geography questions
        if any(geo_word in question_lower for geo_word in ['capital', 'country', 'city', 'continent']):
            return {
                "category": "geography",
                "approach": "knowledge_lookup",
                "confidence": 0.8,
                "complexity": "medium"
            }
        
        # Science questions
        if any(sci_word in question_lower for sci_word in ['chemical', 'symbol', 'element', 'ocean', 'planet']):
            return {
                "category": "science", 
                "approach": "knowledge_lookup",
                "confidence": 0.7,
                "complexity": "medium"
            }
        
        # General knowledge
        return {
            "category": "general",
            "approach": "direct",
            "confidence": 0.5,
            "complexity": "high"
        }


class StrategyCoordinatorAgent:
    """Specialized agent for strategic decision making"""
    
    def recommend_strategy(self, strategy_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recommend strategy based on question analysis and context
        
        Args:
            strategy_input: Input data for strategy decision
            
        Returns:
            Strategy recommendation with confidence
        """
        question_analysis = strategy_input.get("analysis", {})
        round_number = strategy_input.get("round_number", 1)
        
        # Strategy based on question complexity
        if question_analysis.get("complexity") == "low":
            recommendation = "confident_direct"
            confidence = 0.8
        elif question_analysis.get("complexity") == "medium":
            recommendation = "balanced_approach" 
            confidence = 0.6
        else:
            recommendation = "cautious_research"
            confidence = 0.4
        
        # Adjust for round number (later rounds might need different strategy)
        if round_number > 3:
            confidence *= 1.1  # More confident in later rounds
            
        return {
            "recommendation": recommendation,
            "confidence": min(confidence, 1.0),
            "reasoning": f"Based on {question_analysis.get('complexity', 'unknown')} complexity question in round {round_number}",
            "fallback_answer": "Analyzing this question carefully"
        }
    
    def recommend_rps_move(self, strategy_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recommend RPS move based on strategic analysis
        
        Args:
            strategy_input: Input data for move selection
            
        Returns:
            Move recommendation with reasoning
        """
        round_number = strategy_input.get("round_number", 1)
        current_strategy = strategy_input.get("current_strategy", "balanced")
        
        # Strategy-based move selection
        if current_strategy == "aggressive":
            # Favor Rock (strong move)
            recommended_move = 0
            confidence = 0.7
        elif current_strategy == "defensive":
            # Favor Paper (covers Rock)
            recommended_move = 1
            confidence = 0.6
        else:  # balanced
            # Random with slight bias based on round
            if round_number % 3 == 1:
                recommended_move = 0  # Rock
            elif round_number % 3 == 2:
                recommended_move = 1  # Paper
            else:
                recommended_move = 2  # Scissors
            confidence = 0.5
        
        move_names = ["Rock", "Paper", "Scissors"]
        
        return {
            "move_number": recommended_move,
            "recommended_move": move_names[recommended_move],
            "confidence": confidence,
            "reasoning": f"Strategic {current_strategy} approach for round {round_number}"
        }


class PerformanceTrackerAgent:
    """Specialized agent for monitoring and optimizing performance"""
    
    def assess_performance(self, performance_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess current performance and provide guidance
        
        Args:
            performance_input: Performance data for analysis
            
        Returns:
            Performance assessment and recommendations
        """
        question_complexity = performance_input.get("question_complexity", "medium")
        strategy_confidence = performance_input.get("strategy_confidence", 0.5)
        round_history = performance_input.get("round_history", [])
        
        # Analyze recent performance
        if len(round_history) > 0:
            recent_rounds = round_history[-3:]  # Last 3 rounds
            avg_confidence = sum(r.get("confidence", 0.5) for r in recent_rounds) / len(recent_rounds)
        else:
            avg_confidence = 0.5
        
        # Performance guidance
        if avg_confidence > 0.7:
            recommendation = "maintain_current_approach"
            confidence = 0.8
        elif avg_confidence < 0.4:
            recommendation = "adjust_strategy_conservative"
            confidence = 0.6
        else:
            recommendation = "proceed_with_monitoring"
            confidence = 0.7
        
        return {
            "recommendation": recommendation,
            "confidence": confidence,
            "performance_trend": "improving" if avg_confidence > 0.6 else "needs_attention",
            "suggested_adjustments": ["monitor_question_patterns", "track_confidence_trends"]
        }


# Backward compatibility - maintain same interface as original GameAgent and agent_v1.py
class GameAgentV58(TournamentCoordinatorV58):
    """Alias for backward compatibility with existing code"""
    pass


class GameAgent(TournamentCoordinatorV58):
    """Alias for backward compatibility with existing code"""
    pass


# Example usage and testing
if __name__ == "__main__":
    # Initialize multi-agent coordinator
    agent = TournamentCoordinatorV58()
    
    # Test question answering with multi-agent coordination
    test_questions = [
        "What is 15 + 27?",
        "What is the capital of France?", 
        "What color is the sky?",
        "What is 100 - 35?",
        "What is the chemical symbol for gold?"
    ]
    
    print("Testing Multi-Agent Tournament Coordinator V58:")
    print("=" * 50)
    
    for question in test_questions:
        print(f"\nQ: {question}")
        
        # Get coordinated answer
        answer, metadata = agent.coordinate_decision(question)
        simple_answer = agent.answer_question(question)  # Compatible interface
        
        print(f"Coordinated Answer: {answer}")
        print(f"Simple Interface: {simple_answer}")
        print(f"Confidence: {metadata['overall_confidence']:.2f}")
        print(f"Agents Consulted: {len(metadata['agents_consulted'])}")
    
    # Test RPS move coordination
    print(f"\n{'='*50}")
    print("RPS Move Coordination Test:")
    for i in range(5):
        move, metadata = agent.coordinate_rps_strategy({"round_number": i+1})
        simple_move = agent.choose_rps_move()  # Compatible interface
        move_names = ["Rock", "Paper", "Scissors"]
        print(f"Round {i+1}: Coordinated={move_names[move]}, Simple={move_names[simple_move]}")
    
    # Display performance summary
    print(f"\n{'='*50}")
    print("Multi-Agent Performance Summary:")
    summary = agent.get_performance_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")