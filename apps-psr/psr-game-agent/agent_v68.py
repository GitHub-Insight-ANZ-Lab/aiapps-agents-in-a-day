import random
import re
import os
import json
import requests
import time
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import traceback

# Load environment variables from .env file (if available)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not available, using environment variables directly")

# Configure logging for observability
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent_v68_traces.log'),
        logging.StreamHandler()
    ]
)

@dataclass
class Span:
    """Simple span implementation for tracing"""
    name: str
    start_time: float
    end_time: Optional[float] = None
    attributes: Optional[Dict[str, Any]] = None
    status: str = "success"
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}
    
    def end(self, status: str = "success", error: Optional[str] = None):
        self.end_time = time.time()
        self.status = status
        self.error = error
    
    def duration(self) -> float:
        if self.end_time:
            return self.end_time - self.start_time
        return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class Trace:
    """Simple trace implementation for observability"""
    trace_id: str
    spans: List[Span]
    start_time: float
    end_time: Optional[float] = None
    total_cost: float = 0.0
    
    def __post_init__(self):
        if not hasattr(self, 'spans') or self.spans is None:
            self.spans = []
    
    def add_span(self, span: Span):
        self.spans.append(span)
    
    def end(self):
        self.end_time = time.time()
    
    def duration(self) -> float:
        if self.end_time:
            return self.end_time - self.start_time
        return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'trace_id': self.trace_id,
            'spans': [span.to_dict() for span in self.spans],
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration(),
            'total_cost': self.total_cost
        }

@dataclass
class EvaluationMetrics:
    """Evaluation metrics for agent performance"""
    accuracy: float = 0.0
    latency_ms: float = 0.0
    cost_per_request: float = 0.0
    success_rate: float = 0.0
    error_count: int = 0
    total_requests: int = 0
    
    def update(self, success: bool, latency: float, cost: float = 0.0):
        self.total_requests += 1
        if not success:
            self.error_count += 1
        
        self.success_rate = (self.total_requests - self.error_count) / self.total_requests
        self.latency_ms = ((self.latency_ms * (self.total_requests - 1)) + latency * 1000) / self.total_requests
        self.cost_per_request = ((self.cost_per_request * (self.total_requests - 1)) + cost) / self.total_requests

class LocalTracer:
    """Simple local tracer for VS Code debugging and observability"""
    
    def __init__(self):
        self.traces: Dict[str, Trace] = {}
        self.logger = logging.getLogger(f"{__name__}.LocalTracer")
        self.current_trace_id: Optional[str] = None
    
    def start_trace(self, name: str) -> str:
        trace_id = f"{name}_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
        trace = Trace(
            trace_id=trace_id,
            spans=[],
            start_time=time.time()
        )
        self.traces[trace_id] = trace
        self.current_trace_id = trace_id
        self.logger.info(f"Started trace: {trace_id}")
        return trace_id
    
    def start_span(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> Span:
        span = Span(
            name=name,
            start_time=time.time(),
            attributes=attributes or {}
        )
        
        if self.current_trace_id and self.current_trace_id in self.traces:
            self.traces[self.current_trace_id].add_span(span)
        
        self.logger.info(f"Started span: {name}")
        return span
    
    def end_trace(self, trace_id: str):
        if trace_id in self.traces:
            self.traces[trace_id].end()
            self.logger.info(f"Ended trace: {trace_id}, duration: {self.traces[trace_id].duration():.3f}s")
            
            # Log trace summary
            trace = self.traces[trace_id]
            self.logger.info(f"Trace Summary - ID: {trace_id}, Spans: {len(trace.spans)}, Cost: ${trace.total_cost:.4f}")
            
            # Log to file for VS Code debugging
            self._write_trace_to_file(trace)
    
    def _write_trace_to_file(self, trace: Trace):
        """Write trace data to JSON file for VS Code debugging"""
        try:
            trace_file = f"trace_{trace.trace_id}.json"
            with open(trace_file, 'w') as f:
                json.dump(trace.to_dict(), f, indent=2)
            self.logger.info(f"Trace data written to {trace_file}")
        except Exception as e:
            self.logger.error(f"Failed to write trace file: {e}")
    
    def get_trace(self, trace_id: str) -> Optional[Trace]:
        return self.traces.get(trace_id)
    
    def get_all_traces(self) -> Dict[str, Trace]:
        return self.traces.copy()

class GameAgentV68:
    """
    Azure AI Agent service-based agent class with observability and evaluation capabilities
    Following agent_v1.py structure but adding tracing and evaluation features
    """
    
    def __init__(self, azure_ai_endpoint: Optional[str] = None, azure_ai_key: Optional[str] = None):
        """
        Initialize the Azure AI Agent service-based game agent with observability
        
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
        
        # Initialize observability components
        self.tracer = LocalTracer()
        self.metrics = EvaluationMetrics()
        self.logger = logging.getLogger(f"{__name__}.GameAgentV68")
        
        # Cost tracking (approximate Azure OpenAI pricing)
        self.cost_per_1k_tokens = 0.002  # Approximate cost for GPT-4
        
        self.logger.info("GameAgentV68 initialized with observability enabled")
    
    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation for cost calculation"""
        return len(text.split()) * 1.3  # Approximate token count
    
    def _calculate_cost(self, prompt: str, response: str) -> float:
        """Calculate approximate cost for API call"""
        total_tokens = self._estimate_tokens(prompt) + self._estimate_tokens(response or "")
        return (total_tokens / 1000) * self.cost_per_1k_tokens
    
    def _call_azure_ai_agent(self, prompt: str, system_message: str = None, span: Optional[Span] = None) -> str:
        """
        Call Azure AI Agent service with the given prompt and observability
        
        Args:
            prompt: The user prompt/question
            system_message: Optional system message for context
            span: Optional span for tracing
            
        Returns:
            Response from Azure AI agent
        """
        start_time = time.time()
        
        if span:
            span.attributes.update({
                'azure_ai_endpoint': self.azure_ai_endpoint[:50] + "..." if self.azure_ai_endpoint and len(self.azure_ai_endpoint) > 50 else self.azure_ai_endpoint,
                'prompt_length': len(prompt),
                'system_message_length': len(system_message) if system_message else 0
            })
        
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
            
            self.logger.debug(f"Making Azure AI API call with prompt length: {len(prompt)}")
            
            # Make API call to Azure AI Agent service
            response = requests.post(
                f"{self.azure_ai_endpoint}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            latency = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
                
                # Calculate cost and update metrics
                cost = self._calculate_cost(prompt, content)
                self.metrics.update(success=True, latency=latency, cost=cost)
                
                if span:
                    span.attributes.update({
                        'response_length': len(content),
                        'latency_ms': latency * 1000,
                        'cost': cost,
                        'status_code': response.status_code
                    })
                    span.end(status="success")
                
                self.logger.debug(f"Azure AI API success: {latency:.3f}s, cost: ${cost:.4f}")
                return content
            else:
                error_msg = f"Azure AI API error: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                self.metrics.update(success=False, latency=latency)
                
                if span:
                    span.attributes.update({
                        'status_code': response.status_code,
                        'error_message': response.text[:100]
                    })
                    span.end(status="error", error=error_msg)
                
                return None
                
        except Exception as e:
            latency = time.time() - start_time
            error_msg = f"Error calling Azure AI Agent service: {str(e)}"
            self.logger.error(error_msg)
            self.metrics.update(success=False, latency=latency)
            
            if span:
                span.attributes.update({
                    'error': str(e),
                    'error_type': type(e).__name__
                })
                span.end(status="error", error=error_msg)
            
            return None
    
    def answer_question(self, question: str) -> str:
        """
        Generate an answer to the question using Azure AI Agent service with full observability
        
        Args:
            question: The question to answer
            
        Returns:
            Answer to the question
        """
        trace_id = self.tracer.start_trace("answer_question")
        span = self.tracer.start_span("answer_question", {
            'question': question[:100],  # Truncate for logging
            'question_length': len(question)
        })
        
        try:
            # Try Azure AI Agent service first
            system_message = """You are a knowledgeable assistant participating in a Paper-Scissors-Rock tournament. 
            You need to answer questions accurately and concisely. 
            For math problems, provide only the numerical answer. 
            For knowledge questions, provide brief, factual answers.
            Keep responses short and direct."""
            
            # Create sub-span for Azure AI call
            ai_span = self.tracer.start_span("azure_ai_call", {
                'system_message_length': len(system_message)
            })
            
            azure_answer = self._call_azure_ai_agent(question, system_message, ai_span)
            
            if azure_answer:
                # Create span for answer processing
                process_span = self.tracer.start_span("process_answer", {
                    'raw_answer_length': len(azure_answer)
                })
                
                # Clean up the response to extract just the answer
                cleaned_answer = azure_answer.strip()
                if cleaned_answer.lower().startswith(('the answer is', 'answer:', 'result:')):
                    cleaned_answer = cleaned_answer.split(':', 1)[-1].strip()
                
                # For mathematical expressions, try to extract just the number
                if any(op in question for op in ['+', '-', '*', '/', '=']):
                    number_match = re.search(r'\b\d+(?:\.\d+)?\b', cleaned_answer)
                    if number_match:
                        cleaned_answer = number_match.group()
                
                final_answer = cleaned_answer[:50]  # Limit response length
                
                process_span.attributes.update({
                    'final_answer': final_answer,
                    'answer_length': len(final_answer)
                })
                process_span.end(status="success")
                
                span.attributes.update({
                    'final_answer': final_answer,
                    'processing_successful': True
                })
                span.end(status="success")
                
                self.logger.info(f"Question answered successfully: '{question[:50]}...' -> '{final_answer}'")
                
                self.tracer.end_trace(trace_id)
                return final_answer
            else:
                span.end(status="error", error="Azure AI call failed")
                self.tracer.end_trace(trace_id)
                return "Error processing question"
                
        except Exception as e:
            error_msg = f"Error in answer_question: {str(e)}"
            self.logger.error(error_msg)
            span.end(status="error", error=error_msg)
            self.tracer.end_trace(trace_id)
            return "Error processing question"
    
    def choose_rps_move(self) -> int:
        """
        Choose Rock (0), Paper (1), or Scissors (2) using Azure AI Agent service with observability
        
        Returns:
            Move selection as integer (0=Rock, 1=Paper, 2=Scissors)
        """
        trace_id = self.tracer.start_trace("choose_rps_move")
        span = self.tracer.start_span("choose_rps_move")
        
        try:
            # Use Azure AI to make a strategic move choice
            prompt = """In a Rock-Paper-Scissors game, choose the best move. 
            Respond with only one word: Rock, Paper, or Scissors.
            Consider that this is part of a tournament and you want to win."""
            
            system_message = "You are a strategic Rock-Paper-Scissors player. Choose wisely."
            
            # Create sub-span for Azure AI call
            ai_span = self.tracer.start_span("azure_ai_strategy_call", {
                'strategy_prompt_length': len(prompt)
            })
            
            azure_choice = self._call_azure_ai_agent(prompt, system_message, ai_span)
            
            if azure_choice:
                # Create span for move processing
                process_span = self.tracer.start_span("process_move", {
                    'raw_choice': azure_choice
                })
                
                choice_lower = azure_choice.lower().strip()
                move = random.randint(0, 2)  # Fallback
                
                if 'rock' in choice_lower:
                    move = 0
                elif 'paper' in choice_lower:
                    move = 1
                elif 'scissors' in choice_lower or 'scissor' in choice_lower:
                    move = 2
                
                move_names = {0: "Rock", 1: "Paper", 2: "Scissors"}
                
                process_span.attributes.update({
                    'final_move': move,
                    'move_name': move_names[move],
                    'choice_parsing_successful': True
                })
                process_span.end(status="success")
                
                span.attributes.update({
                    'chosen_move': move,
                    'move_name': move_names[move],
                    'ai_choice': azure_choice
                })
                span.end(status="success")
                
                self.logger.info(f"RPS move chosen: {move_names[move]} ({move})")
                
                self.tracer.end_trace(trace_id)
                return move
            else:
                # Fallback to random choice
                fallback_move = random.randint(0, 2)
                move_names = {0: "Rock", 1: "Paper", 2: "Scissors"}
                
                span.attributes.update({
                    'chosen_move': fallback_move,
                    'move_name': move_names[fallback_move],
                    'fallback_used': True
                })
                span.end(status="success")
                
                self.logger.warning(f"Used fallback random move: {move_names[fallback_move]} ({fallback_move})")
                
                self.tracer.end_trace(trace_id)
                return fallback_move
                
        except Exception as e:
            error_msg = f"Error in choose_rps_move: {str(e)}"
            self.logger.error(error_msg)
            fallback_move = random.randint(0, 2)
            span.attributes.update({
                'chosen_move': fallback_move,
                'error_fallback': True
            })
            span.end(status="error", error=error_msg)
            self.tracer.end_trace(trace_id)
            return fallback_move
    
    def run_offline_evaluation(self, test_questions: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Run offline evaluation with a test dataset
        
        Args:
            test_questions: List of test cases with 'question' and 'expected_answer' keys
            
        Returns:
            Evaluation results dictionary
        """
        trace_id = self.tracer.start_trace("offline_evaluation")
        span = self.tracer.start_span("offline_evaluation", {
            'test_count': len(test_questions)
        })
        
        results = {
            'total_questions': len(test_questions),
            'correct_answers': 0,
            'accuracy': 0.0,
            'average_latency_ms': 0.0,
            'total_cost': 0.0,
            'detailed_results': []
        }
        
        start_time = time.time()
        total_latency = 0.0
        total_cost = 0.0
        
        for i, test_case in enumerate(test_questions):
            question = test_case['question']
            expected = test_case['expected_answer'].lower().strip()
            
            question_start = time.time()
            answer = self.answer_question(question)
            question_latency = time.time() - question_start
            
            total_latency += question_latency
            
            # Simple accuracy check (can be enhanced)
            is_correct = expected in answer.lower() if answer else False
            if is_correct:
                results['correct_answers'] += 1
            
            question_result = {
                'question': question,
                'expected_answer': expected,
                'actual_answer': answer,
                'correct': is_correct,
                'latency_ms': question_latency * 1000
            }
            results['detailed_results'].append(question_result)
            
            self.logger.info(f"Evaluation {i+1}/{len(test_questions)}: {'✓' if is_correct else '✗'} - {question[:30]}...")
        
        # Calculate final metrics
        results['accuracy'] = results['correct_answers'] / results['total_questions'] if results['total_questions'] > 0 else 0.0
        results['average_latency_ms'] = (total_latency / results['total_questions']) * 1000 if results['total_questions'] > 0 else 0.0
        results['total_cost'] = self.metrics.cost_per_request * results['total_questions']
        
        span.attributes.update({
            'accuracy': results['accuracy'],
            'correct_answers': results['correct_answers'],
            'average_latency_ms': results['average_latency_ms'],
            'total_cost': results['total_cost']
        })
        span.end(status="success")
        
        self.logger.info(f"Offline evaluation completed: {results['correct_answers']}/{results['total_questions']} correct ({results['accuracy']:.2%})")
        
        self.tracer.end_trace(trace_id)
        return results
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        return {
            'accuracy': self.metrics.accuracy,
            'average_latency_ms': self.metrics.latency_ms,
            'cost_per_request': self.metrics.cost_per_request,
            'success_rate': self.metrics.success_rate,
            'error_count': self.metrics.error_count,
            'total_requests': self.metrics.total_requests
        }
    
    def export_traces_for_vscode(self, output_file: str = "agent_v68_all_traces.json"):
        """Export all traces to a JSON file for VS Code debugging and analysis"""
        try:
            all_traces = self.tracer.get_all_traces()
            export_data = {
                'export_timestamp': datetime.now(timezone.utc).isoformat(),
                'agent_version': 'v68',
                'metrics': self.get_performance_metrics(),
                'traces': {trace_id: trace.to_dict() for trace_id, trace in all_traces.items()}
            }
            
            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            self.logger.info(f"Exported {len(all_traces)} traces to {output_file}")
            return output_file
        except Exception as e:
            self.logger.error(f"Failed to export traces: {e}")
            return None


# Backward compatibility - maintain same interface as original GameAgent
class GameAgent(GameAgentV68):
    """Alias for backward compatibility with existing code"""
    pass


# Example usage and testing with observability
if __name__ == "__main__":
    # Initialize agent with observability
    agent = GameAgentV68()
    
    # Test question answering with observability
    test_questions = [
        "What is 15 + 27?",
        "What is the capital of France?", 
        "What color is the sky?",
        "What is 100 - 35?"
    ]
    
    print("Testing Azure AI Agent V68 with Observability:")
    print("=" * 50)
    
    for question in test_questions:
        answer = agent.answer_question(question)
        print(f"Q: {question}")
        print(f"A: {answer}")
        print()
    
    # Test RPS move selection with observability
    print("RPS Move Selection Test with Tracing:")
    move_names = {0: "Rock", 1: "Paper", 2: "Scissors"}
    for i in range(5):
        move = agent.choose_rps_move()
        print(f"Move {i+1}: {move_names[move]} ({move})")
    
    print("\n" + "=" * 50)
    
    # Run offline evaluation
    evaluation_dataset = [
        {"question": "What is 2 + 2?", "expected_answer": "4"},
        {"question": "What is the capital of France?", "expected_answer": "paris"},
        {"question": "What is 10 - 5?", "expected_answer": "5"},
        {"question": "What color is the sky?", "expected_answer": "blue"}
    ]
    
    print("Running Offline Evaluation:")
    eval_results = agent.run_offline_evaluation(evaluation_dataset)
    print(f"Evaluation Results:")
    print(f"- Accuracy: {eval_results['accuracy']:.2%}")
    print(f"- Average Latency: {eval_results['average_latency_ms']:.2f}ms")
    print(f"- Total Cost: ${eval_results['total_cost']:.4f}")
    print()
    
    # Display performance metrics
    print("Performance Metrics:")
    metrics = agent.get_performance_metrics()
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"- {key}: {value:.4f}")
        else:
            print(f"- {key}: {value}")
    
    # Export traces for VS Code debugging
    print("\nExporting traces for VS Code debugging...")
    export_file = agent.export_traces_for_vscode()
    if export_file:
        print(f"Traces exported to: {export_file}")
        print("You can open this file in VS Code to inspect the detailed tracing data.")
    
    print("\n🔍 Observability Features Enabled:")
    print("- ✅ Request tracing with spans")
    print("- ✅ Performance metrics collection")
    print("- ✅ Cost tracking")
    print("- ✅ Error monitoring") 
    print("- ✅ Offline evaluation capabilities")
    print("- ✅ VS Code debugging support")
    print("- ✅ JSON trace export")
    print("\n📊 Check the generated log files and JSON exports for detailed observability data!")