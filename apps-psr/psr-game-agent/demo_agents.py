#!/usr/bin/env python3
"""
Demonstration script comparing agent_v1.py, agent_v61a.py (MCP), and agent_v61b.py (A2A)
This script shows the key differences and capabilities of each agent approach.
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demonstrate_agent_capabilities():
    """Demonstrate the capabilities of each agent version"""
    
    print("🎯 PSR Tournament Agent Capabilities Comparison")
    print("=" * 80)
    
    # Test with agent_v1.py (baseline)
    print("\n1️⃣  AGENT V1 (Baseline Azure AI)")
    print("-" * 40)
    try:
        from agent_v1 import GameAgentV1
        agent_v1 = GameAgentV1()
        
        print("✅ Agent V1 initialized successfully")
        print("📋 Capabilities:")
        print("   - Direct Azure AI integration")
        print("   - Basic question answering")
        print("   - Simple RPS move selection")
        print("   - Fallback to random selection")
        
        # Test question answering
        answer = agent_v1.answer_question("What is 10 + 5?")
        print(f"   🧠 Sample answer: {answer}")
        
    except Exception as e:
        print(f"❌ Agent V1 error: {e}")
    
    # Test with agent_v61a.py (MCP)
    print("\n2️⃣  AGENT V61A (MCP Enhanced)")
    print("-" * 40)
    try:
        from agent_v61a import GameAgentV61A
        agent_v61a = GameAgentV61A()
        
        print("✅ Agent V61A initialized successfully")
        
        capabilities = agent_v61a.get_mcp_capabilities()
        print("📋 MCP Capabilities:")
        print(f"   - MCP Server: {capabilities['server_info']}")
        print(f"   - Tools available: {len(capabilities['tools'])}")
        for tool in capabilities['tools']:
            print(f"     • {tool['name']}: {tool['description']}")
        print(f"   - Resources available: {len(capabilities['resources'])}")
        for resource in capabilities['resources']:
            print(f"     • {resource['name']}: {resource['description']}")
        
        # Test MCP question answering
        answer = agent_v61a.answer_question("What is the capital of France?")
        print(f"   🧠 MCP Sample answer: {answer}")
        
    except Exception as e:
        print(f"❌ Agent V61A error: {e}")
    
    # Test with agent_v61b.py (A2A)
    print("\n3️⃣  AGENT V61B (A2A Enhanced)")
    print("-" * 40)
    try:
        from agent_v61b import GameAgentV61B
        agent_v61b = GameAgentV61B()
        
        print("✅ Agent V61B initialized successfully")
        
        capabilities = agent_v61b.get_a2a_capabilities()
        print("📋 A2A Capabilities:")
        print(f"   - A2A Coordinator: {capabilities['coordinator_info']}")
        print(f"   - Registered agents: {len(capabilities['agents'])}")
        for agent_info in capabilities['agents']:
            print(f"     • {agent_info['name']} (v{agent_info['version']})")
            print(f"       Skills: {[skill['name'] for skill in agent_info['skills']]}")
            print(f"       Capabilities: {agent_info['capabilities']}")
        
        # Test A2A question answering
        answer = agent_v61b.answer_question("What is the chemical symbol for gold?")
        print(f"   🧠 A2A Sample answer: {answer}")
        
        stats = capabilities['communication_stats']
        print(f"   📊 Communication stats: {stats}")
        
    except Exception as e:
        print(f"❌ Agent V61B error: {e}")
    
    print("\n🏆 COMPARISON SUMMARY")
    print("-" * 40)
    print("Agent V1:   Basic Azure AI integration with simple fallbacks")
    print("Agent V61A: MCP protocol with tool discovery and resource access")
    print("Agent V61B: A2A protocol with multi-agent coordination")
    print("\nAll agents maintain the same interface for backward compatibility!")
    print("=" * 80)

def demonstrate_protocol_differences():
    """Show the key differences between MCP and A2A protocols"""
    
    print("\n🔬 PROTOCOL ANALYSIS")
    print("=" * 50)
    
    print("\n📡 MCP (Model Context Protocol):")
    print("   • Client-server architecture")
    print("   • Dynamic tool discovery")
    print("   • Standardized resource access")
    print("   • Universal adaptor approach")
    print("   • Single LLM connection point")
    
    print("\n🤝 A2A (Agent-to-Agent Protocol):")
    print("   • Distributed agent collaboration")
    print("   • Agent card-based discovery")
    print("   • Artifact-based communication")
    print("   • Multi-agent coordination")
    print("   • Each agent can use different LLMs")
    
    print("\n⚖️  WHEN TO USE WHICH:")
    print("   MCP: When you need standardized tool access across different LLMs")
    print("   A2A: When you need specialized agents to collaborate on complex tasks")

if __name__ == "__main__":
    demonstrate_agent_capabilities()
    demonstrate_protocol_differences()