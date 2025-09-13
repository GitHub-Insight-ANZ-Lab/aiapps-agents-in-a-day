const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const SERVER_URL = process.env.SERVER_URL || 'http://localhost:5289';

// Middleware
app.use(express.json());
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));

// Game state - now supports multiple sessions
let gameState = {
    playerId: null,
    playerName: '',
    isRegistered: false,
    currentRound: 0,
    tournamentStatus: 'Pending',
    roundStatus: null,
    currentQuestion: '',
    gameActive: false,
    results: []
};

// Multiple session support
let sessions = new Map(); // sessionId -> gameState

// Move enum matching server
const Move = {
    Rock: 0,
    Paper: 1,
    Scissors: 2
};

// Move names for display
const MoveNames = ['Rock', 'Paper', 'Scissors'];

// API client functions
class GameClient {
    static async registerPlayer(name) {
        try {
            const response = await axios.post(`${SERVER_URL}/api/player/register`, {
                Name: name
            });
            return response.data;
        } catch (error) {
            console.error('Registration error:', error.response?.data || error.message);
            throw error;
        }
    }

    static async getStatus(playerId) {
        try {
            const response = await axios.get(`${SERVER_URL}/api/player/${playerId}/status`);
            return response.data;
        } catch (error) {
            console.error('Status error:', error.response?.data || error.message);
            throw error;
        }
    }

    static async submitAnswer(playerId, roundNumber, answer, move) {
        try {
            const response = await axios.post(`${SERVER_URL}/api/player/submit-answer`, {
                PlayerId: playerId,
                RoundNumber: roundNumber,
                Answer: answer,
                Move: move
            });
            return response.data;
        } catch (error) {
            console.error('Submit error:', error.response?.data || error.message);
            throw error;
        }
    }

    static async getResults(playerId) {
        try {
            const response = await axios.get(`${SERVER_URL}/api/player/${playerId}/results`);
            return response.data;
        } catch (error) {
            console.error('Results error:', error.response?.data || error.message);
            throw error;
        }
    }
}

// Question answering logic (simple pattern matching)
function attemptAnswerQuestion(question) {
    const q = question.toLowerCase();
    
    // Simple answer patterns
    const patterns = {
        '2+2': '4',
        '2 + 2': '4',
        'capital of australia': 'canberra',
        'largest planet': 'jupiter',
        'world war ii end': '1945',
        'chemical symbol for gold': 'au',
        'continents': '7',
        'how many continents': '7',
        'smallest prime': '2',
        'currency of japan': 'yen',
        '10 squared': '100',
        'longest river': 'nile',
        'freezing point': '0',
        'programming language': 'c#',
        'http stand': 'hypertext transfer protocol',
        'speed of light': '299792458',
        'largest ocean': 'pacific',
        'hexagon': '6',
        'square root of 64': '8',
        'capital of france': 'paris',
        'plants absorb': 'carbon dioxide',
        '15% of 200': '30'
    };

    for (const [key, value] of Object.entries(patterns)) {
        if (q.includes(key)) {
            return value;
        }
    }

    // Default fallback answers for common question types
    if (q.includes('what is') && q.includes('+')) return '4';
    if (q.includes('capital')) return 'unknown';
    if (q.includes('year')) return '2000';
    if (q.includes('how many')) return '1';
    
    return 'unknown';
}

// Random move selection
function getRandomMove() {
    const moves = [Move.Rock, Move.Paper, Move.Scissors];
    return moves[Math.floor(Math.random() * moves.length)];
}

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/register', async (req, res) => {
    try {
        const { playerName, sessionId } = req.body;
        
        if (!playerName) {
            return res.status(400).json({ error: 'Player name is required' });
        }

        if (!sessionId) {
            return res.status(400).json({ error: 'Session ID is required' });
        }

        const result = await GameClient.registerPlayer(playerName);
        
        // Ensure sessionId is always treated as a string
        const sessionIdStr = String(sessionId);
        
        // Create session state
        const sessionState = {
            playerId: result.playerId,
            playerName: playerName,
            isRegistered: true,
            currentRound: 0,
            tournamentStatus: 'Pending',
            currentRoundStatus: null,
            currentQuestion: '',
            gameActive: false,
            canSubmit: false,
            results: []
        };
        
        sessions.set(sessionIdStr, sessionState);
        
        console.log(`Player ${playerName} registered with ID: ${result.playerId} (Session: ${sessionIdStr})`);
        
        res.json({ 
            success: true, 
            playerId: result.playerId, 
            message: result.message 
        });

        // Start monitoring game state for this session
        startGameMonitoring(sessionIdStr);
        
    } catch (error) {
        res.status(500).json({ 
            error: 'Registration failed', 
            details: error.response?.data?.message || error.message 
        });
    }
});

app.post('/reconnect', async (req, res) => {
    try {
        const { playerId, sessionId } = req.body;
        
        if (!playerId) {
            return res.status(400).json({ error: 'Player ID is required' });
        }

        if (!sessionId) {
            return res.status(400).json({ error: 'Session ID is required' });
        }

        // Ensure sessionId is always treated as a string
        const sessionIdStr = String(sessionId);

        // Try to get player status to verify the player exists
        const status = await GameClient.getStatus(playerId);
        
        // Get player name from results or use a default
        let playerName = `Player ${playerId}`;
        try {
            const results = await GameClient.getResults(playerId);
            if (results && results.length > 0) {
                // We can't get player name from results, so keep the default
                playerName = `Player ${playerId}`;
            }
        } catch (error) {
            // If results fail, player might not exist or have no results yet
        }
        
        // Create session state for reconnection
        const sessionState = {
            playerId: playerId,
            playerName: playerName,
            isRegistered: true,
            currentRound: status.currentRound || 0,
            tournamentStatus: status.tournamentStatus || 'Pending',
            currentRoundStatus: status.currentRoundStatus,
            currentQuestion: status.currentQuestion || '',
            gameActive: status.tournamentStatus === 1,
            canSubmit: status.canSubmit || false,
            results: []
        };
        
        // Ensure session is saved before starting monitoring and returning success
        sessions.set(sessionIdStr, sessionState);
        
        // Start monitoring game state for this session BEFORE returning success
        // This ensures the monitoring is active when the client starts status polling
        startGameMonitoring(sessionIdStr);
        
        console.log(`Player ${playerName} reconnected with ID: ${playerId} (Session: ${sessionIdStr})`);
        
        // Return success only after session is fully established
        res.json({ 
            success: true, 
            playerId: playerId,
            playerName: playerName,
            message: 'Reconnected successfully!' 
        });
        
    } catch (error) {
        res.status(500).json({ 
            error: 'Reconnection failed', 
            details: error.response?.data?.message || error.message 
        });
    }
});

app.get('/status', (req, res) => {
    const sessionId = req.query.sessionId || req.headers['session-id'];
    // Ensure sessionId is always treated as a string for consistent lookup
    const sessionIdStr = String(sessionId);
    console.log(`Status check for sessionId: ${sessionIdStr}, sessions.has: ${sessions.has(sessionIdStr)}`);
    if (sessionIdStr && sessions.has(sessionIdStr)) {
        const sessionState = sessions.get(sessionIdStr);
        console.log(`Found session state for ${sessionIdStr}:`, sessionState ? 'exists' : 'null');
        res.json(sessionState);
    } else {
        console.log(`No session found for ${sessionIdStr}, available sessions:`, Array.from(sessions.keys()));
        // Return default state if no session found
        res.json({
            isRegistered: false,
            playerId: null,
            playerName: '',
            tournamentStatus: 0,
            currentRound: 0,
            currentRoundStatus: null,
            currentQuestion: '',
            gameActive: false,
            canSubmit: false
        });
    }
});

app.get('/results', async (req, res) => {
    try {
        const sessionId = req.query.sessionId || req.headers['session-id'];
        const sessionIdStr = String(sessionId);
        const sessionState = sessions.get(sessionIdStr);
        
        if (!sessionState || !sessionState.playerId) {
            return res.status(400).json({ error: 'Player not registered' });
        }

        const results = await GameClient.getResults(sessionState.playerId);
        res.json(results);
    } catch (error) {
        res.status(500).json({ 
            error: 'Failed to get results', 
            details: error.message 
        });
    }
});

app.post('/submit-answer', async (req, res) => {
    try {
        const { playerId, roundNumber, answer, move, sessionId } = req.body;
        
        if (!playerId || !roundNumber || !answer || move === null || move === undefined) {
            return res.status(400).json({ error: 'Missing required fields' });
        }

        const result = await GameClient.submitAnswer(playerId, roundNumber, answer, move);
        
        console.log(`Manual submission for player ${playerId}, round ${roundNumber}: ${answer}, ${MoveNames[move]}`);
        
        res.json({ 
            success: true, 
            message: result.message || 'Answer submitted successfully'
        });
        
    } catch (error) {
        res.status(500).json({ 
            error: 'Failed to submit answer', 
            details: error.response?.data?.message || error.message 
        });
    }
});

app.get('/final-results', async (req, res) => {
    try {
        const sessionId = req.query.sessionId || req.headers['session-id'];
        const sessionIdStr = String(sessionId);
        const sessionState = sessions.get(sessionIdStr);
        
        if (!sessionState || !sessionState.playerId) {
            return res.status(400).json({ error: 'Player not registered' });
        }

        // Get tournament status first
        const status = await GameClient.getStatus(sessionState.playerId);
        
        if (status.tournamentStatus !== 2) { // Not completed
            return res.json({ success: false, error: 'Tournament not completed yet' });
        }

        // Get player results
        const results = await GameClient.getResults(sessionState.playerId);
        const totalScore = results.reduce((sum, result) => sum + result.Score, 0);
        
        // For final results, we would need an endpoint from the server to get all players' rankings
        // Since we don't have that, we'll simulate it based on the player's score
        // In a real implementation, this would come from the server
        
        res.json({
            success: true,
            finalResults: true,
            playerRank: 1, // Would come from server
            totalPlayers: 5, // Would come from server  
            playerScore: totalScore
        });
        
    } catch (error) {
        res.status(500).json({ 
            error: 'Failed to get final results', 
            details: error.message 
        });
    }
});

// Game monitoring and manual submission support
let monitoringIntervals = new Map(); // sessionId -> interval
let hasSubmittedForRound = {};

function startGameMonitoring(sessionId) {
    // Ensure sessionId is always treated as a string
    const sessionIdStr = String(sessionId);
    
    // Clear existing interval for this session
    if (monitoringIntervals.has(sessionIdStr)) {
        clearInterval(monitoringIntervals.get(sessionIdStr));
    }

    console.log(`Starting game monitoring for session ${sessionIdStr}...`);
    
    const interval = setInterval(async () => {
        try {
            const sessionState = sessions.get(sessionIdStr);
            if (!sessionState || !sessionState.playerId) return;

            const status = await GameClient.getStatus(sessionState.playerId);
            
            // Update session state
            sessionState.tournamentStatus = status.tournamentStatus;
            sessionState.currentRound = status.currentRound;
            sessionState.currentRoundStatus = status.currentRoundStatus;
            sessionState.currentQuestion = status.currentQuestion;
            sessionState.gameActive = status.tournamentStatus === 1; // InProgress
            sessionState.canSubmit = status.canSubmit; // Add missing canSubmit property

            console.log(`Session ${sessionIdStr}: Tournament=${status.tournamentStatus}, Round=${status.currentRound}, RoundStatus=${status.currentRoundStatus}, CanSubmit=${status.canSubmit}`);

            // Note: We removed the auto-submission logic here
            // The client will now manually submit through the confirmation popup

            // Stop monitoring if tournament is completed
            if (status.tournamentStatus === 2) { // Completed
                console.log(`Tournament completed for session ${sessionIdStr}, stopping monitoring`);
                clearInterval(interval);
                monitoringIntervals.delete(sessionIdStr);
            }

        } catch (error) {
            console.error(`Monitoring error for session ${sessionIdStr}:`, error.message);
        }
    }, 2000); // Check every 2 seconds
    
    monitoringIntervals.set(sessionIdStr, interval);
}

// Start server
app.listen(PORT, () => {
    console.log(`RPS Game Client running on http://localhost:${PORT}`);
    console.log(`Connecting to game server at: ${SERVER_URL}`);
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\nShutting down game client...');
    // Clear all monitoring intervals
    monitoringIntervals.forEach((interval, sessionId) => {
        clearInterval(interval);
        console.log(`Stopped monitoring for session ${sessionId}`);
    });
    monitoringIntervals.clear();
    process.exit(0);
});