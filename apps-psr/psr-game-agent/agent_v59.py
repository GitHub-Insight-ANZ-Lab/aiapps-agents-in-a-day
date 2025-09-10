import random
import re
import os
import json
import requests
from typing import Optional, Dict, List, Tuple
from datetime import datetime
import time

# Try to import dotenv, fallback to manual env loading if not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Manual environment loading fallback
    pass


class GameAgentV59:
    """
    Metacognitive Azure AI Agent for PSR Tournament
    
    This agent implements metacognition by:
    - Tracking game history (wins, losses, moves, opponent moves)
    - Analyzing patterns in losses and opponent behavior
    - Adapting strategy based on historical performance
    - Self-reflecting on decision-making process
    """
    
    def __init__(self, player_name: str = "MetaCognitive_Agent", azure_ai_endpoint: Optional[str] = None, 
                 azure_ai_key: Optional[str] = None):
        """
        Initialize the metacognitive game agent
        
        Args:
            player_name: Name of the player for history tracking
            azure_ai_endpoint: Azure AI Foundry endpoint URL
            azure_ai_key: Azure AI service API key
        """
        self.azure_ai_endpoint = azure_ai_endpoint or os.getenv('AZURE_AI_ENDPOINT')
        self.azure_ai_key = azure_ai_key or os.getenv('AZURE_AI_KEY')
        self.player_name = player_name
        
        # Initialize headers for Azure AI API calls
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.azure_ai_key}' if self.azure_ai_key else None
        }
        
        # Metacognitive components
        self.game_history: List[Dict] = []
        self.strategy_adjustments: List[Dict] = []
        self.opponent_patterns: Dict = {}
        self.current_strategy = "balanced"  # balanced, aggressive, defensive, adaptive
        self.confidence_level = 0.5  # 0.0 to 1.0
        
        # Performance tracking
        self.win_rate = 0.0
        self.loss_patterns = []
        self.strategy_effectiveness = {
            "balanced": {"wins": 0, "losses": 0},
            "aggressive": {"wins": 0, "losses": 0}, 
            "defensive": {"wins": 0, "losses": 0},
            "adaptive": {"wins": 0, "losses": 0}
        }
        
        # Load existing history
        self._load_history()
    
    def _load_history(self):
        """Load game history from persistent storage"""
        history_file = f"game_history_{self.player_name}.json"
        try:
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    data = json.load(f)
                    self.game_history = data.get('game_history', [])
                    self.strategy_adjustments = data.get('strategy_adjustments', [])
                    self.opponent_patterns = data.get('opponent_patterns', {})
                    self.current_strategy = data.get('current_strategy', 'balanced')
                    self.confidence_level = data.get('confidence_level', 0.5)
                    self.strategy_effectiveness = data.get('strategy_effectiveness', self.strategy_effectiveness)
                    
                    # Recalculate performance metrics
                    self._update_performance_metrics()
        except Exception as e:
            print(f"Error loading history: {e}")
    
    def _save_history(self):
        """Save game history to persistent storage"""
        history_file = f"game_history_{self.player_name}.json"
        try:
            data = {
                'game_history': self.game_history,
                'strategy_adjustments': self.strategy_adjustments,
                'opponent_patterns': self.opponent_patterns,
                'current_strategy': self.current_strategy,
                'confidence_level': self.confidence_level,
                'strategy_effectiveness': self.strategy_effectiveness,
                'last_updated': datetime.now().isoformat()
            }
            with open(history_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
    
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
        Generate an answer to the question using Azure AI Agent service or local fallback
        
        Args:
            question: The question to answer
            
        Returns:
            Answer to the question
        """
        # Metacognitive enhancement: Consider past question patterns
        similar_questions = self._find_similar_questions(question)
        
        # Build context from similar past questions
        context = ""
        if similar_questions:
            context = f"Based on similar questions I've answered before: {similar_questions[-1].get('answer', '')}"
        
        # Try Azure AI Agent service first
        system_message = f"""You are a knowledgeable assistant participating in a Paper-Scissors-Rock tournament. 
        You need to answer questions accurately and concisely. 
        For math problems, provide only the numerical answer. 
        For knowledge questions, provide brief, factual answers.
        Keep responses short and direct.
        
        {context}"""
        
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
                    cleaned_answer = number_match.group()
            
            # Store question and answer for future metacognitive learning
            self._record_question_answer(question, cleaned_answer[:50])
            
            return cleaned_answer[:50]  # Limit response length
        
        # Fallback to local processing
        return self._fallback_answer(question)
    
    def _find_similar_questions(self, question: str) -> List[Dict]:
        """Find similar questions from history"""
        similar = []
        question_lower = question.lower()
        for entry in self.game_history:
            if 'question' in entry:
                past_question = entry['question'].lower()
                # Simple similarity check - could be enhanced with NLP
                if any(word in past_question for word in question_lower.split() if len(word) > 3):
                    similar.append(entry)
        return similar[-3:]  # Return last 3 similar questions
    
    def _record_question_answer(self, question: str, answer: str):
        """Record question and answer for learning"""
        entry = {
            'type': 'question_answer',
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'answer': answer
        }
        self.game_history.append(entry)
        self._save_history()
    
    def _fallback_answer(self, question: str) -> str:
        """Fallback answer generation when Azure AI is not available"""
        # Simple pattern matching for common question types
        if any(op in question for op in ['+', 'plus', 'add']):
            # Try to extract numbers and add them
            numbers = re.findall(r'\d+', question)
            if len(numbers) >= 2:
                return str(sum(int(n) for n in numbers[:2]))
        
        if any(op in question for op in ['-', 'minus', 'subtract']):
            numbers = re.findall(r'\d+', question)
            if len(numbers) >= 2:
                return str(int(numbers[0]) - int(numbers[1]))
        
        if any(op in question for op in ['*', 'times', 'multiply']):
            numbers = re.findall(r'\d+', question)
            if len(numbers) >= 2:
                return str(int(numbers[0]) * int(numbers[1]))
        
        # Default responses for common questions
        fallback_answers = {
            'capital of france': 'Paris',
            'capital of australia': 'Canberra',
            'color': 'blue',  # For any color question containing "sky"
            'colour': 'blue',  # British spelling
            'how many continents': '7'
        }
        
        question_lower = question.lower()
        
        # Special handling for color/sky questions
        if ('color' in question_lower or 'colour' in question_lower) and 'sky' in question_lower:
            return 'blue'
        
        for key, answer in fallback_answers.items():
            if key in question_lower:
                return answer
        
        return "I need more information to answer that question."
    
    def choose_rps_move(self) -> int:
        """
        Choose Rock (0), Paper (1), or Scissors (2) using metacognitive strategy
        
        Returns:
            Move selection as integer (0=Rock, 1=Paper, 2=Scissors)
        """
        # Metacognitive decision process
        move = self._metacognitive_move_selection()
        
        # Record the move decision with reasoning
        self._record_move_decision(move)
        
        return move
    
    def _metacognitive_move_selection(self) -> int:
        """
        Use metacognitive reasoning to select the best move
        """
        # Step 1: Analyze recent performance
        recent_performance = self._analyze_recent_performance()
        
        # Step 2: Detect opponent patterns
        opponent_prediction = self._predict_opponent_move()
        
        # Step 3: Evaluate current strategy effectiveness
        strategy_evaluation = self._evaluate_current_strategy()
        
        # Step 4: Self-reflection on decision process
        reflection = self._reflect_on_decision_process()
        
        # Step 5: Make adaptive decision
        if self.confidence_level < 0.3:
            # Low confidence - be more defensive
            return self._defensive_move(opponent_prediction)
        elif recent_performance['win_rate'] > 0.7:
            # High win rate - continue current strategy
            return self._strategy_based_move()
        elif len(self.game_history) > 5 and recent_performance['loss_streak'] >= 3:
            # Losing streak - change strategy and adapt
            self._adapt_strategy_after_losses()
            return self._adaptive_move(opponent_prediction)
        else:
            # Balanced approach
            return self._balanced_move(opponent_prediction)
    
    def _analyze_recent_performance(self) -> Dict:
        """Analyze recent game performance"""
        recent_games = [g for g in self.game_history if g.get('type') == 'game_result'][-10:]
        
        if not recent_games:
            return {'win_rate': 0.5, 'loss_streak': 0, 'total_games': 0}
        
        wins = sum(1 for g in recent_games if g.get('result') == 'win')
        losses = sum(1 for g in recent_games if g.get('result') == 'loss')
        
        # Calculate loss streak
        loss_streak = 0
        for game in reversed(recent_games):
            if game.get('result') == 'loss':
                loss_streak += 1
            else:
                break
        
        return {
            'win_rate': wins / len(recent_games) if recent_games else 0.5,
            'loss_streak': loss_streak,
            'total_games': len(recent_games)
        }
    
    def _predict_opponent_move(self) -> int:
        """Predict opponent's next move based on patterns"""
        recent_opponent_moves = []
        
        for game in self.game_history[-10:]:  # Look at last 10 games
            if game.get('type') == 'game_result' and 'opponent_move' in game:
                recent_opponent_moves.append(game['opponent_move'])
        
        if len(recent_opponent_moves) < 2:
            return random.randint(0, 2)  # Random if insufficient data
        
        # Simple pattern detection
        if len(recent_opponent_moves) >= 3:
            # Check for repeated patterns
            last_three = recent_opponent_moves[-3:]
            if last_three[0] == last_three[1] == last_three[2]:
                return last_three[0]  # Predict same move
            
            # Check for alternating pattern
            if len(recent_opponent_moves) >= 4:
                if recent_opponent_moves[-1] == recent_opponent_moves[-3]:
                    return recent_opponent_moves[-2]  # Predict alternating
        
        # Most frequent move
        from collections import Counter
        move_counts = Counter(recent_opponent_moves)
        predicted_move = move_counts.most_common(1)[0][0]
        
        return predicted_move
    
    def _evaluate_current_strategy(self) -> Dict:
        """Evaluate effectiveness of current strategy"""
        strategy_stats = self.strategy_effectiveness.get(self.current_strategy, {"wins": 0, "losses": 0})
        total_games = strategy_stats["wins"] + strategy_stats["losses"]
        
        if total_games == 0:
            return {'effectiveness': 0.5, 'games_played': 0}
        
        effectiveness = strategy_stats["wins"] / total_games
        return {'effectiveness': effectiveness, 'games_played': total_games}
    
    def _reflect_on_decision_process(self) -> str:
        """Self-reflection on the decision-making process"""
        reflection = f"Strategy: {self.current_strategy}, Confidence: {self.confidence_level:.2f}"
        
        # Add reasoning about recent performance
        recent_perf = self._analyze_recent_performance()
        if recent_perf['loss_streak'] >= 2:
            reflection += f" - Concerned about {recent_perf['loss_streak']} game loss streak"
            
        if recent_perf['win_rate'] > 0.7:
            reflection += " - Confident due to high recent win rate"
        elif recent_perf['win_rate'] < 0.3:
            reflection += " - Need to adapt strategy due to poor performance"
        
        # Record reflection for learning
        self.strategy_adjustments.append({
            'timestamp': datetime.now().isoformat(),
            'reflection': reflection,
            'strategy': self.current_strategy,
            'confidence': self.confidence_level
        })
        
        return reflection
    
    def _defensive_move(self, predicted_opponent_move: int) -> int:
        """Make a defensive move to counter predicted opponent move"""
        # Counter the predicted move: Rock beats Scissors, Paper beats Rock, Scissors beats Paper
        counter_moves = {0: 1, 1: 2, 2: 0}  # Rock->Paper, Paper->Scissors, Scissors->Rock
        return counter_moves.get(predicted_opponent_move, random.randint(0, 2))
    
    def _strategy_based_move(self) -> int:
        """Make a move based on current strategy"""
        if self.current_strategy == "aggressive":
            # Favor Rock (aggressive)
            return 0 if random.random() < 0.5 else random.randint(0, 2)
        elif self.current_strategy == "defensive":
            # Favor Paper (defensive)
            return 1 if random.random() < 0.5 else random.randint(0, 2)
        else:
            # Balanced approach
            return random.randint(0, 2)
    
    def _adaptive_move(self, predicted_opponent_move: int) -> int:
        """Make an adaptive move considering all factors"""
        # Use Azure AI for strategic decision if available
        if self.azure_ai_endpoint and self.azure_ai_key:
            try:
                context = f"Recent performance: {self._analyze_recent_performance()}, Predicted opponent move: {predicted_opponent_move}"
                prompt = f"""In a Rock-Paper-Scissors game, choose the best strategic move.
                Context: {context}
                Consider the opponent's predicted move and choose to counter it.
                Respond with only one word: Rock, Paper, or Scissors."""
                
                system_message = f"You are a strategic Rock-Paper-Scissors player using metacognitive reasoning. Current strategy: {self.current_strategy}"
                
                azure_choice = self._call_azure_ai_agent(prompt, system_message)
                
                if azure_choice:
                    choice_lower = azure_choice.lower().strip()
                    if 'rock' in choice_lower:
                        return 0
                    elif 'paper' in choice_lower:
                        return 1
                    elif 'scissors' in choice_lower or 'scissor' in choice_lower:
                        return 2
            except Exception as e:
                print(f"Error in adaptive move selection: {e}")
        
        # Fallback to counter-move
        return self._defensive_move(predicted_opponent_move)
    
    def _balanced_move(self, predicted_opponent_move: int) -> int:
        """Make a balanced move with some randomness"""
        # 60% chance to counter predicted move, 40% random
        if random.random() < 0.6:
            return self._defensive_move(predicted_opponent_move)
        else:
            return random.randint(0, 2)
    
    def _adapt_strategy_after_losses(self):
        """Adapt strategy after experiencing losses"""
        strategies = ["balanced", "aggressive", "defensive", "adaptive"]
        
        # Remove current strategy and try a different one
        available_strategies = [s for s in strategies if s != self.current_strategy]
        
        # Choose strategy with best historical performance
        best_strategy = self.current_strategy
        best_effectiveness = 0.0
        
        for strategy in available_strategies:
            stats = self.strategy_effectiveness.get(strategy, {"wins": 0, "losses": 0})
            total = stats["wins"] + stats["losses"]
            if total > 0:
                effectiveness = stats["wins"] / total
                if effectiveness > best_effectiveness:
                    best_effectiveness = effectiveness
                    best_strategy = strategy
        
        if best_strategy != self.current_strategy:
            old_strategy = self.current_strategy
            self.current_strategy = best_strategy
            self.confidence_level = max(0.3, self.confidence_level * 0.8)  # Reduce confidence
            
            print(f"Strategy adapted from {old_strategy} to {best_strategy} due to losses")
        
        self._save_history()
    
    def _record_move_decision(self, move: int):
        """Record the move decision and reasoning"""
        entry = {
            'type': 'move_decision',
            'timestamp': datetime.now().isoformat(),
            'move': move,
            'strategy': self.current_strategy,
            'confidence': self.confidence_level
        }
        self.game_history.append(entry)
    
    def record_game_result(self, my_move: int, opponent_move: int, result: str):
        """
        Record the result of a game for learning
        
        Args:
            my_move: The move this agent made (0=Rock, 1=Paper, 2=Scissors)
            opponent_move: The opponent's move
            result: 'win', 'loss', or 'draw'
        """
        game_entry = {
            'type': 'game_result',
            'timestamp': datetime.now().isoformat(),
            'my_move': my_move,
            'opponent_move': opponent_move,
            'result': result,
            'strategy_used': self.current_strategy
        }
        
        self.game_history.append(game_entry)
        
        # Update strategy effectiveness
        if result in ['win', 'loss']:
            if self.current_strategy not in self.strategy_effectiveness:
                self.strategy_effectiveness[self.current_strategy] = {"wins": 0, "losses": 0}
            
            if result == 'win':
                self.strategy_effectiveness[self.current_strategy]["wins"] += 1
                self.confidence_level = min(1.0, self.confidence_level + 0.1)
            else:
                self.strategy_effectiveness[self.current_strategy]["losses"] += 1
                self.confidence_level = max(0.1, self.confidence_level - 0.05)
        
        # Update performance metrics
        self._update_performance_metrics()
        
        # Metacognitive analysis after loss
        if result == 'loss':
            self._analyze_loss(my_move, opponent_move)
        
        self._save_history()
    
    def _analyze_loss(self, my_move: int, opponent_move: int):
        """Analyze a loss to learn from it"""
        loss_pattern = {
            'timestamp': datetime.now().isoformat(),
            'my_move': my_move,
            'opponent_move': opponent_move,
            'strategy': self.current_strategy,
            'analysis': self._generate_loss_analysis(my_move, opponent_move)
        }
        
        self.loss_patterns.append(loss_pattern)
        
        # Keep only recent loss patterns
        self.loss_patterns = self.loss_patterns[-20:]
    
    def _generate_loss_analysis(self, my_move: int, opponent_move: int) -> str:
        """Generate analysis of why the loss occurred"""
        moves = {0: 'Rock', 1: 'Paper', 2: 'Scissors'}
        analysis = f"Lost with {moves[my_move]} against opponent's {moves[opponent_move]}. "
        
        # Pattern analysis
        recent_losses = [p for p in self.loss_patterns[-5:]]
        if len(recent_losses) >= 2:
            if all(p['opponent_move'] == opponent_move for p in recent_losses):
                analysis += f"Opponent has used {moves[opponent_move]} repeatedly."
            
            if all(p['my_move'] == my_move for p in recent_losses):
                analysis += f"I've been using {moves[my_move]} too frequently."
        
        return analysis
    
    def _update_performance_metrics(self):
        """Update overall performance metrics"""
        game_results = [g for g in self.game_history if g.get('type') == 'game_result']
        
        if game_results:
            wins = sum(1 for g in game_results if g.get('result') == 'win')
            total_games = len(game_results)
            self.win_rate = wins / total_games
    
    def get_performance_summary(self) -> Dict:
        """Get a summary of the agent's performance and learning"""
        return {
            'total_games': len([g for g in self.game_history if g.get('type') == 'game_result']),
            'win_rate': self.win_rate,
            'current_strategy': self.current_strategy,
            'confidence_level': self.confidence_level,
            'strategy_effectiveness': self.strategy_effectiveness,
            'recent_performance': self._analyze_recent_performance(),
            'loss_patterns_identified': len(self.loss_patterns)
        }
    
    def reset_learning(self):
        """Reset the learning history (for testing or new tournaments)"""
        self.game_history = []
        self.strategy_adjustments = []
        self.loss_patterns = []
        self.current_strategy = "balanced"
        self.confidence_level = 0.5
        self.win_rate = 0.0
        self.strategy_effectiveness = {
            "balanced": {"wins": 0, "losses": 0},
            "aggressive": {"wins": 0, "losses": 0},
            "defensive": {"wins": 0, "losses": 0},
            "adaptive": {"wins": 0, "losses": 0}
        }
        self._save_history()
    
    def get_move_name(self, move: int) -> str:
        """
        Convert move integer to move name for compatibility with tests
        
        Args:
            move: Integer move (0=Rock, 1=Paper, 2=Scissors)
            
        Returns:
            String name of the move
        """
        moves = {0: 'Rock', 1: 'Paper', 2: 'Scissors'}
        return moves.get(move, 'Unknown')


# Backward compatibility - maintain same interface as original GameAgent
class GameAgent(GameAgentV59):
    """Alias for backward compatibility with existing code"""
    pass


# Example usage and testing
if __name__ == "__main__":
    # Initialize metacognitive agent
    agent = GameAgentV59(player_name="TestAgent")
    
    print("🧠 Testing Metacognitive Game Agent V59:")
    print("=" * 50)
    
    # Test question answering
    test_questions = [
        "What is 15 + 27?",
        "What is the capital of France?", 
        "What color is the sky?",
        "What is 100 - 35?"
    ]
    
    print("\n📚 Question Answering Test:")
    for question in test_questions:
        answer = agent.answer_question(question)
        print(f"Q: {question}")
        print(f"A: {answer}")
        print()
    
    # Test RPS move selection with metacognitive learning
    print("\n🎮 RPS Move Selection with Learning:")
    moves = ['Rock', 'Paper', 'Scissors']
    
    # Simulate a series of games
    for round_num in range(10):
        my_move = agent.choose_rps_move()
        opponent_move = random.randint(0, 2)  # Random opponent
        
        # Determine result
        if my_move == opponent_move:
            result = 'draw'
        elif (my_move == 0 and opponent_move == 2) or \
             (my_move == 1 and opponent_move == 0) or \
             (my_move == 2 and opponent_move == 1):
            result = 'win'
        else:
            result = 'loss'
        
        # Record the game result for learning
        agent.record_game_result(my_move, opponent_move, result)
        
        print(f"Round {round_num + 1}: My {moves[my_move]} vs Opponent {moves[opponent_move]} -> {result.upper()}")
        
        # Show strategy adaptation
        if round_num % 3 == 2:  # Every 3 rounds
            summary = agent.get_performance_summary()
            print(f"   Strategy: {summary['current_strategy']}, Confidence: {summary['confidence_level']:.2f}, Win Rate: {summary['win_rate']:.2f}")
    
    # Final performance summary
    print("\n📊 Final Performance Summary:")
    summary = agent.get_performance_summary()
    for key, value in summary.items():
        print(f"   {key}: {value}")
    
    print(f"\n🎯 Metacognitive features demonstrated:")
    print(f"   ✅ Game history tracking: {summary['total_games']} games recorded")
    print(f"   ✅ Strategy adaptation: Currently using '{summary['current_strategy']}' strategy")
    print(f"   ✅ Confidence adjustment: {summary['confidence_level']:.2f}")
    print(f"   ✅ Loss pattern analysis: {summary['loss_patterns_identified']} patterns identified")
    print(f"   ✅ Performance reflection: Win rate {summary['win_rate']:.2%}")