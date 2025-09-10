# PSR Game Agent

A Python web application that acts as an autonomous player for the Paper-Scissors-Rock Tournament Game Server.

## Features

### Web Interface
- **Player Registration**: Simple form to enter player name (only user interaction required)
- **Live Status Display**: Real-time monitoring of tournament and round status
- **Activity Log**: Detailed log of all agent actions and decisions
- **Results Display**: Complete round-by-round results and scoring
- **Auto-refresh**: Page updates every 3 seconds to show live progress

### Autonomous Agent
- **Player Registration**: Automatically registers with the game server
- **Status Monitoring**: Continuously polls server for tournament status changes
- **Question Answering**: Intelligent question answering with fallback logic
- **RPS Selection**: Random Rock/Paper/Scissors move selection
- **Result Tracking**: Displays final scores and round details

## Prerequisites

- Python 3.8 or higher
- PSR Game Server running on localhost:5289
- pip (Python package manager)
- Azure AI Foundry endpoint and API key (optional, for enhanced question answering)

## Configuration

### Environment Variables

The agent supports Azure AI integration for intelligent question answering. Create a `.env` file with the following variables:

```bash
# Azure AI Foundry Configuration (optional)
AZURE_AI_ENDPOINT=https://your-azure-ai-endpoint.cognitiveservices.azure.com
AZURE_AI_KEY=your-azure-ai-api-key-here
```

**Note**: If Azure AI credentials are not provided, the agent will fall back to local pattern-based question answering.

## Installation

1. Navigate to the agent directory:
   ```bash
   cd apps-psr/psr-game-agent
   ```

2. Set up environment variables:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env file and add your Azure AI credentials
   # AZURE_AI_ENDPOINT=https://your-azure-ai-endpoint.cognitiveservices.azure.com
   # AZURE_AI_KEY=your-azure-ai-api-key-here
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Agent

1. Make sure the PSR Game Server is running:
   ```bash
   cd ../psr-game-server
   dotnet run
   ```

2. In a new terminal, start the agent:
   ```bash
   cd apps-psr/psr-game-agent
   python app.py
   ```

3. Open your browser and navigate to:
   - **Agent Interface**: http://localhost:5001

## How to Use

1. **Enter Player Name**: Open the web interface and enter your player name
2. **Watch the Agent**: The agent will automatically:
   - Register with the server
   - Monitor tournament status
   - Answer questions when rounds start
   - Submit Rock/Paper/Scissors moves
   - Display all actions in real-time
3. **View Results**: See final scores and round details when tournament completes

## Agent Versions

This repository contains multiple agent implementations demonstrating different AI concepts:

### agent_v1.py
- **Basic Azure AI Agent**: Foundation agent with Azure AI integration and fallback logic
- **Features**: Question answering, RPS move selection, error handling
- **Use Case**: Standard autonomous gameplay

### agent_v67.py - **Trustworthy AI Agent with Human-in-the-Loop** 🛡️
- **Human Oversight**: Implements human-in-the-loop decision making based on lesson 67
- **Safety Features**: Built-in safety checks and validation
- **Interactive Mode**: Human can approve, modify, or reject AI decisions in real-time
- **Transparency**: Complete logging and tracking of all decisions
- **Use Case**: Trustworthy AI applications requiring human oversight

#### Key Features of agent_v67.py:
- ✅ **Human Approval Workflow**: Every AI decision can be reviewed by a human
- ✅ **Safety Validation**: Automatic detection of suspicious or malicious content
- ✅ **Termination Control**: Human can stop the process at any time
- ✅ **Decision Tracking**: Complete audit trail of approved/rejected decisions
- ✅ **Override Capability**: Human can provide their own answers/moves
- ✅ **Backward Compatibility**: Same interface as agent_v1.py

#### Using the Trustworthy Agent:
```bash
# Run interactive demo
python demo_agent_v67.py

# Run comprehensive tests
python test_agent_v67.py

# Use in your code
from agent_v67 import GameAgentV67
agent = GameAgentV67(interactive_mode=True)  # Enable human oversight
```

### Other Agent Versions
- **agent_v2_tool_use.py**: Tool use and function calling
- **agent_v3_agentic_rag.py**: Agentic RAG implementation  
- **agent_v4_multi_agent.py**: Multi-agent collaboration
- **agent_v5_agentic_protocols.py**: Advanced agentic protocols

## Agent Behavior

### Question Answering Logic
The agent uses simple pattern matching for common question types:
- **Math**: Basic addition and subtraction
- **Geography**: Capital cities (Australia, France, Japan)
- **Colors**: Common color associations (sky=blue, grass=green, sun=yellow)
- **Fallback**: Random selection from common answers

### RPS Strategy
- Completely random selection between Rock (0), Paper (1), and Scissors (2)
- No strategic logic - pure chance

### Monitoring
- Polls server status every 2 seconds
- Automatically detects tournament state changes
- Submits answers immediately when rounds become available
- Continues until tournament completion or 5 rounds finished

## API Integration

The agent communicates with these server endpoints:
- `POST /api/player/register` - Register player
- `GET /api/player/{id}/status` - Get current status and questions
- `POST /api/player/submit-answer` - Submit answers and RPS moves
- `GET /api/player/{id}/results` - Get final results

## Testing

To test the complete flow:

1. Start the PSR Game Server
2. Start the PSR Game Agent
3. Register a player through the agent web interface
4. Use the server's web interface (localhost:5289) to:
   - Start the tournament
   - Start each round with questions
   - End rounds to see results
5. Watch the agent automatically respond to each round

## Architecture

- **app.py**: Flask web application with routes and UI
- **agent.py**: Core autonomous game logic and monitoring
- **api_client.py**: HTTP client for server communication
- **templates/index.html**: Responsive web interface
- **requirements.txt**: Python dependencies

## Troubleshooting

**Agent not connecting to server:**
- Verify PSR Game Server is running on localhost:5289
- Check server logs for any errors

**Agent not responding to rounds:**
- Ensure tournament has been started by referee
- Check that rounds are being started with questions
- Verify agent status log for error messages

**Web interface not updating:**
- The page auto-refreshes every 3 seconds
- Check browser console for JavaScript errors
- Verify Flask app is running on localhost:5001