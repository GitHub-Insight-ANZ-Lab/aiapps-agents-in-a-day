# GameAgentV68 - AI Agent with Observability & Evaluation

GameAgentV68 is an enhanced version of the PSR (Paper-Scissors-Rock) tournament game agent based on the `agent_v1.py` structure, with added observability and evaluation capabilities as described in the **68-ai-agents-production** documentation.

## Features

### 🔍 Observability
- **Local Tracing**: OpenTelemetry-compatible spans and traces for VS Code debugging
- **Performance Metrics**: Latency, cost, accuracy, success rate tracking
- **Error Monitoring**: Comprehensive error tracking and fallback mechanisms  
- **Structured Logging**: Detailed logs for monitoring and debugging
- **Cost Tracking**: Per-request cost estimation for Azure AI calls

### 📊 Evaluation
- **Offline Evaluation**: Automated testing with custom datasets
- **Accuracy Measurement**: Answer correctness assessment
- **Performance Benchmarking**: Latency and cost analysis
- **Detailed Reporting**: Individual and aggregate evaluation results

### 🛠️ VS Code Integration
- **Breakpoint Debugging**: Full debugging support for agent operations
- **Trace Files**: Individual JSON files for each operation
- **Comprehensive Export**: All traces exported to single JSON file
- **Real-time Monitoring**: Live metrics during development

## Quick Start

### Basic Usage

```python
from agent_v68 import GameAgentV68

# Initialize agent with observability
agent = GameAgentV68()

# Answer questions with full tracing
answer = agent.answer_question("What is 2 + 2?")

# Make strategic RPS moves with observability  
move = agent.choose_rps_move()  # Returns 0=Rock, 1=Paper, 2=Scissors

# Get performance metrics
metrics = agent.get_performance_metrics()
print(f"Success rate: {metrics['success_rate']:.2%}")
```

### Offline Evaluation

```python
# Define test dataset
test_questions = [
    {"question": "What is 2 + 2?", "expected_answer": "4"},
    {"question": "What is the capital of France?", "expected_answer": "paris"}
]

# Run evaluation with detailed metrics
results = agent.run_offline_evaluation(test_questions)
print(f"Accuracy: {results['accuracy']:.2%}")
```

### Export Traces for Analysis

```python
# Export all traces to JSON for VS Code debugging
export_file = agent.export_traces_for_vscode()
print(f"Traces exported to: {export_file}")
```

## Configuration

### Azure AI Setup

Set environment variables for Azure AI integration:

```bash
export AZURE_AI_ENDPOINT="https://your-endpoint.openai.azure.com"
export AZURE_AI_KEY="your-api-key"
```

Or create a `.env` file:
```
AZURE_AI_ENDPOINT=https://your-endpoint.openai.azure.com
AZURE_AI_KEY=your-api-key
```

### Fallback Behavior

The agent gracefully handles missing Azure AI configuration:
- **Question Answering**: Returns error message when Azure AI unavailable
- **RPS Moves**: Falls back to random selection
- **All Operations**: Fully traced and logged regardless of Azure AI status

## Generated Files

### Trace Files
- `trace_*.json` - Individual operation traces
- `agent_v68_all_traces.json` - Complete trace export
- `agent_v68_traces.log` - Structured logging output

### File Structure
```
├── agent_v68.py              # Main agent implementation
├── demo_agent_v68.py         # Demonstration script
├── agent_v68_traces.log      # Generated logs (when running)
├── agent_v68_all_traces.json # Exported traces (when running)
└── trace_*.json              # Individual traces (when running)
```

## VS Code Debugging

### Setup Debugging
1. Open `agent_v68.py` in VS Code
2. Set breakpoints in methods like `answer_question()` or `choose_rps_move()`
3. Run your agent code in debug mode
4. Inspect `span.attributes` and trace data in the debugger

### Trace Analysis
1. Run the agent to generate trace files
2. Open `agent_v68_all_traces.json` in VS Code
3. Use JSON formatting for easy inspection
4. Analyze spans, latency, and error patterns

## Production Integration

### Observability Platforms
The agent is ready for integration with:
- **Azure Monitor / Application Insights**
- **Langfuse** for LLM observability
- **Prometheus/Grafana** for metrics
- **ELK Stack** for log analysis
- **Custom monitoring dashboards**

### Key Metrics Tracked
- `accuracy` - Answer correctness rate
- `average_latency_ms` - Response time performance
- `cost_per_request` - Azure AI usage costs
- `success_rate` - Request success percentage
- `error_count` - Total failed requests
- `total_requests` - Total operations processed

## Demo Script

Run the comprehensive demo:
```bash
python demo_agent_v68.py
```

This demonstrates:
- Basic functionality with observability
- Evaluation features
- Observability data export
- VS Code debugging integration
- Production-ready features

## Compatibility

- **Python 3.7+**
- **VS Code** with Python extension
- **Optional**: python-dotenv for .env file support
- **Backend Compatible**: Follows `agent_v1.py` interface for drop-in replacement

## Architecture

### Classes
- `GameAgentV68` - Main agent class with observability
- `LocalTracer` - Tracing implementation for local debugging
- `Span` - Individual operation tracking
- `Trace` - Complete operation context
- `EvaluationMetrics` - Performance metrics collection

### Key Methods
- `answer_question(question)` - Answer questions with tracing
- `choose_rps_move()` - Strategic move selection with observability
- `run_offline_evaluation(dataset)` - Automated evaluation
- `get_performance_metrics()` - Current metrics snapshot
- `export_traces_for_vscode()` - Export for analysis

## Contributing

This agent follows the patterns established in `agent_v1.py` while adding comprehensive observability as outlined in the **68-ai-agents-production** documentation. Enhancements should maintain backward compatibility and focus on production observability needs.

---

**Based on**: 68-ai-agents-production documentation  
**Follows**: agent_v1.py structure and interface  
**Adds**: Observability, evaluation, and production monitoring capabilities