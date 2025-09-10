import random
import re
import os
import json
import requests
import time
from typing import Optional

# Simple dotenv replacement for environments where python-dotenv isn't available
def load_dotenv_simple():
    """Simple .env file loader"""
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# Load environment variables from .env file
load_dotenv_simple()


class GameAgentV67:
    """
    Trustworthy AI Agent with Human-in-the-Loop capabilities for PSR Tournament
    
    This agent implements human oversight and feedback mechanisms as described in 
    the Building Trustworthy AI Agents documentation (lesson 67).
    
    Features:
    - Human approval for AI-generated answers
    - Human override capabilities for move selection  
    - Safety checks and validation
    - Termination conditions based on user feedback
    """
    
    def __init__(self, azure_ai_endpoint: Optional[str] = None, azure_ai_key: Optional[str] = None, 
                 interactive_mode: bool = True):
        """
        Initialize the Trustworthy AI Agent with Human-in-the-Loop capabilities
        
        Args:
            azure_ai_endpoint: Azure AI Foundry endpoint URL
            azure_ai_key: Azure AI service API key
            interactive_mode: Whether to enable human-in-the-loop interactions
        """
        self.azure_ai_endpoint = azure_ai_endpoint or os.getenv('AZURE_AI_ENDPOINT')
        self.azure_ai_key = azure_ai_key or os.getenv('AZURE_AI_KEY')
        self.interactive_mode = interactive_mode

        # Initialize headers for Azure AI API calls
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.azure_ai_key}' if self.azure_ai_key else None
        }
        
        # Conversation history for human oversight
        self.conversation_history = []
        self.approved_decisions = []
        self.rejected_decisions = []
    
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
    
    def _get_human_approval(self, ai_decision: str, decision_type: str, context: str) -> tuple[bool, str]:
        """
        Get human approval for an AI decision
        
        Args:
            ai_decision: The AI's proposed decision/answer
            decision_type: Type of decision (e.g., "answer", "move")
            context: Additional context for the decision
            
        Returns:
            Tuple of (approved, final_decision)
        """
        if not self.interactive_mode:
            return True, ai_decision
            
        print(f"\n🤖 AI {decision_type.upper()} PROPOSAL:")
        print(f"Context: {context}")
        print(f"AI suggests: {ai_decision}")
        print("\n🧑 HUMAN OVERSIGHT:")
        print("1. APPROVE - Accept AI decision")
        print("2. MODIFY - Provide your own answer")
        print("3. REJECT - Try different AI approach")
        print("4. TERMINATE - Stop the process")
        
        while True:
            try:
                choice = input("\nYour decision (1-4): ").strip()
                
                if choice == "1" or choice.upper() == "APPROVE":
                    self.approved_decisions.append({
                        'type': decision_type,
                        'ai_decision': ai_decision,
                        'context': context,
                        'final_decision': ai_decision
                    })
                    print("✅ AI decision APPROVED")
                    return True, ai_decision
                    
                elif choice == "2" or choice.upper() == "MODIFY":
                    user_input = input("Enter your preferred answer/move: ").strip()
                    if user_input:
                        self.approved_decisions.append({
                            'type': decision_type,
                            'ai_decision': ai_decision,
                            'context': context,
                            'final_decision': user_input,
                            'human_override': True
                        })
                        print(f"✅ Using HUMAN decision: {user_input}")
                        return True, user_input
                    else:
                        print("❌ Invalid input. Please try again.")
                        
                elif choice == "3" or choice.upper() == "REJECT":
                    self.rejected_decisions.append({
                        'type': decision_type,
                        'ai_decision': ai_decision,
                        'context': context,
                        'reason': 'human_rejection'
                    })
                    print("❌ AI decision REJECTED. Trying fallback approach...")
                    return False, None
                    
                elif choice == "4" or choice.upper() == "TERMINATE":
                    print("🛑 Process TERMINATED by human oversight")
                    raise KeyboardInterrupt("Human terminated the process")
                    
                else:
                    print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                    
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"❌ Error getting input: {e}. Please try again.")
    
    def _apply_safety_checks(self, content: str, content_type: str) -> bool:
        """
        Apply safety checks to content before presenting to human
        
        Args:
            content: Content to check
            content_type: Type of content (answer/move)
            
        Returns:
            True if content passes safety checks
        """
        # Basic safety checks
        if not content or len(content.strip()) == 0:
            print(f"⚠️ Safety Check: Empty {content_type} detected")
            return False
            
        # Check for suspicious patterns
        suspicious_patterns = [
            r'ignore.*previous.*instructions',
            r'system.*prompt',
            r'forget.*instructions',
            r'override.*safety'
        ]
        
        content_lower = content.lower()
        for pattern in suspicious_patterns:
            if re.search(pattern, content_lower):
                print(f"⚠️ Safety Check: Suspicious pattern detected in {content_type}")
                return False
                
        return True
    
    def answer_question(self, question: str) -> str:
        """
        Generate an answer to the question with human-in-the-loop oversight
        
        Args:
            question: The question to answer
            
        Returns:
            Answer to the question (AI or human-approved)
        """
        print(f"\n📝 QUESTION: {question}")
        
        # System message for trustworthy responses
        system_message = """You are a knowledgeable and trustworthy assistant participating in a Paper-Scissors-Rock tournament. 
        You must answer questions accurately and concisely while being transparent about your reasoning.
        For math problems, show your work briefly then provide the numerical answer. 
        For knowledge questions, provide brief, factual answers with confidence indicators.
        If you're uncertain, indicate your level of confidence.
        Keep responses short and direct while being helpful."""
        
        # Try Azure AI Agent service first
        azure_answer = self._call_azure_ai_agent(question, system_message)
        
        if azure_answer:
            # Apply safety checks
            if not self._apply_safety_checks(azure_answer, "answer"):
                azure_answer = None
            else:
                # Clean up the response
                cleaned_answer = azure_answer.strip()
                if cleaned_answer.lower().startswith(('the answer is', 'answer:', 'result:')):
                    cleaned_answer = cleaned_answer.split(':', 1)[-1].strip()
                
                # For mathematical expressions, try to extract just the number
                if any(op in question for op in ['+', '-', '*', '/', '=']):
                    number_match = re.search(r'\b\d+(?:\.\d+)?\b', cleaned_answer)
                    if number_match:
                        cleaned_answer = number_match.group()
                
                azure_answer = cleaned_answer[:100]  # Limit response length
        
        # Get human approval for AI answer
        if azure_answer:
            try:
                approved, final_answer = self._get_human_approval(
                    azure_answer, 
                    "answer", 
                    f"Question: {question}"
                )
                
                if approved and final_answer:
                    return final_answer
                    
            except KeyboardInterrupt:
                print("\n🛑 Question answering terminated by user")
                return "Process terminated by human oversight"
        
        # Fallback to simple logic if AI fails or is rejected
        print("🔄 Using fallback answer generation...")
        fallback_answer = self._generate_fallback_answer(question)
        
        if self.interactive_mode:
            try:
                approved, final_answer = self._get_human_approval(
                    fallback_answer,
                    "fallback answer",
                    f"Question: {question} (AI unavailable)"
                )
                return final_answer if approved else "Unable to provide answer"
            except KeyboardInterrupt:
                return "Process terminated by human oversight"
        
        return fallback_answer
    
    def _generate_fallback_answer(self, question: str) -> str:
        """Generate a simple fallback answer when AI is unavailable"""
        question_lower = question.lower()
        
        # Simple math detection and solving
        if any(op in question for op in ['+', '-', '*', '/']):
            import re
            # Extract numbers and operators
            numbers = re.findall(r'\d+(?:\.\d+)?', question)
            if len(numbers) >= 2:
                try:
                    if '+' in question:
                        result = float(numbers[0]) + float(numbers[1])
                    elif '-' in question:
                        result = float(numbers[0]) - float(numbers[1])
                    elif '*' in question:
                        result = float(numbers[0]) * float(numbers[1])
                    elif '/' in question:
                        result = float(numbers[0]) / float(numbers[1])
                    else:
                        return "Unable to solve"
                    
                    return str(int(result) if result.is_integer() else result)
                except:
                    return "Unable to calculate"
        
        # Common knowledge fallbacks
        fallback_responses = {
            'capital of france': 'Paris',
            'capital of australia': 'Canberra',
            'color of the sky': 'Blue',
            'what color is the sky': 'Blue',
            'sky': 'Blue',
            'continents': '7',
            'how many continents': '7'
        }
        
        for key, value in fallback_responses.items():
            if key in question_lower:
                return value
                
        return "I need more information to answer this question"
    
    def choose_rps_move(self) -> int:
        """
        Choose Rock (0), Paper (1), or Scissors (2) with human-in-the-loop oversight
        
        Returns:
            Move selection as integer (0=Rock, 1=Paper, 2=Scissors)
        """
        print(f"\n🎮 CHOOSING RPS MOVE")
        
        # Use Azure AI to make a strategic move choice
        prompt = """In a Rock-Paper-Scissors game, choose the best strategic move. 
        Consider game theory, common human patterns, and winning strategies.
        Respond with only one word: Rock, Paper, or Scissors.
        Explain your reasoning briefly."""
        
        system_message = """You are a strategic Rock-Paper-Scissors player with human oversight. 
        Choose wisely and be transparent about your reasoning.
        Consider: Rock beats Scissors, Paper beats Rock, Scissors beats Paper."""
        
        azure_choice = self._call_azure_ai_agent(prompt, system_message)
        
        ai_move = None
        ai_move_name = "Unknown"
        
        if azure_choice and self._apply_safety_checks(azure_choice, "move"):
            choice_lower = azure_choice.lower().strip()
            if 'rock' in choice_lower:
                ai_move = 0
                ai_move_name = "Rock"
            elif 'paper' in choice_lower:
                ai_move = 1
                ai_move_name = "Paper"
            elif 'scissors' in choice_lower or 'scissor' in choice_lower:
                ai_move = 2
                ai_move_name = "Scissors"
        
        # Get human approval for AI move
        if ai_move is not None:
            try:
                move_description = f"{ai_move_name} ({ai_move})"
                approved, final_decision = self._get_human_approval(
                    move_description,
                    "move",
                    f"AI reasoning: {azure_choice[:100]}..."
                )
                
                if approved:
                    # Parse human decision if modified
                    if final_decision != move_description:
                        # Human provided different move
                        decision_lower = final_decision.lower()
                        if 'rock' in decision_lower or '0' in decision_lower:
                            return 0
                        elif 'paper' in decision_lower or '1' in decision_lower:
                            return 1
                        elif 'scissors' in decision_lower or '2' in decision_lower:
                            return 2
                    
                    return ai_move
                    
            except KeyboardInterrupt:
                print("\n🛑 Move selection terminated by user")
                return random.randint(0, 2)
        
        # Fallback to strategic random choice
        print("🔄 Using fallback move selection...")
        fallback_move = random.randint(0, 2)
        move_names = ["Rock", "Paper", "Scissors"]
        
        if self.interactive_mode:
            try:
                approved, final_decision = self._get_human_approval(
                    f"{move_names[fallback_move]} ({fallback_move})",
                    "fallback move",
                    "AI unavailable - random strategic choice"
                )
                
                if approved:
                    # Parse final decision
                    decision_lower = final_decision.lower()
                    if 'rock' in decision_lower or '0' in decision_lower:
                        return 0
                    elif 'paper' in decision_lower or '1' in decision_lower:
                        return 1
                    elif 'scissors' in decision_lower or '2' in decision_lower:
                        return 2
                    
                return fallback_move
            except KeyboardInterrupt:
                return random.randint(0, 2)
        
        return fallback_move
    
    def get_move_name(self, move: int) -> str:
        """Convert move integer to name"""
        move_names = ["Rock", "Paper", "Scissors"]
        return move_names[move] if 0 <= move <= 2 else "Unknown"
    
    def get_oversight_summary(self) -> dict:
        """Get summary of human oversight decisions"""
        return {
            'total_approved': len(self.approved_decisions),
            'total_rejected': len(self.rejected_decisions),
            'human_overrides': len([d for d in self.approved_decisions if d.get('human_override')]),
            'approved_decisions': self.approved_decisions,
            'rejected_decisions': self.rejected_decisions
        }
    
    def save_oversight_log(self, filename: str = "oversight_log.json"):
        """Save oversight decisions to a log file"""
        log_data = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'summary': self.get_oversight_summary(),
            'conversation_history': self.conversation_history
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(log_data, f, indent=2)
            print(f"📄 Oversight log saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving oversight log: {e}")


# Backward compatibility - maintain same interface as original GameAgent
class GameAgent(GameAgentV67):
    """Alias for backward compatibility with existing code"""
    pass


# Example usage and testing
if __name__ == "__main__":
    import time
    
    print("🛡️ TRUSTWORTHY AI AGENT WITH HUMAN-IN-THE-LOOP")
    print("=" * 60)
    print("This agent implements human oversight for trustworthy AI decisions.")
    print("You can approve, modify, or reject AI suggestions at any point.")
    print("=" * 60)
    
    # Initialize agent with interactive mode
    agent = GameAgentV67(interactive_mode=True)
    
    # Test question answering with human oversight
    test_questions = [
        "What is 15 + 27?",
        "What is the capital of France?",
        "What color is the sky?"
    ]
    
    print("\n🧠 TESTING QUESTION ANSWERING WITH HUMAN OVERSIGHT:")
    print("-" * 50)
    
    for question in test_questions:
        try:
            answer = agent.answer_question(question)
            print(f"✅ Final Answer: {answer}\n")
        except KeyboardInterrupt:
            print("\n🛑 Testing interrupted by user")
            break
    
    # Test RPS move selection with human oversight
    print("\n🎮 TESTING RPS MOVE SELECTION WITH HUMAN OVERSIGHT:")
    print("-" * 50)
    
    try:
        for i in range(3):
            print(f"\n🎯 Round {i+1}:")
            move = agent.choose_rps_move()
            move_name = agent.get_move_name(move)
            print(f"✅ Final Move: {move_name} ({move})\n")
    except KeyboardInterrupt:
        print("\n🛑 Testing interrupted by user")
    
    # Display oversight summary
    print("\n📊 HUMAN OVERSIGHT SUMMARY:")
    print("-" * 30)
    summary = agent.get_oversight_summary()
    print(f"Total Approved Decisions: {summary['total_approved']}")
    print(f"Total Rejected Decisions: {summary['total_rejected']}")
    print(f"Human Overrides: {summary['human_overrides']}")
    
    # Save log
    agent.save_oversight_log("agent_v67_oversight_log.json")
    
    print("\n✅ Testing completed!")
    print("🔍 This agent demonstrates trustworthy AI with human oversight.")