#!/usr/bin/env python3
"""
Demo script for GameAgentV68 - AI Agent with Observability & Evaluation

This script demonstrates the observability and evaluation features of agent_v68.py
as described in the 68-ai-agents-production documentation.

Key Features Demonstrated:
- Local tracing for VS Code debugging
- Performance metrics collection
- Cost tracking and monitoring
- Error handling and fallbacks
- Offline evaluation capabilities
- JSON export for analysis

Usage:
    python demo_agent_v68.py
"""

import json
from agent_v68 import GameAgentV68

def demo_basic_functionality():
    """Demonstrate basic agent functionality with observability"""
    print("🎯 Demo: Basic Agent Functionality with Observability")
    print("=" * 60)
    
    # Initialize agent
    agent = GameAgentV68()
    
    # Test RPS moves with tracing
    print("\n1. Testing RPS Move Selection (with fallback):")
    move_names = {0: "Rock", 1: "Paper", 2: "Scissors"}
    for i in range(3):
        move = agent.choose_rps_move()
        print(f"   Move {i+1}: {move_names[move]} ({move})")
    
    return agent

def demo_evaluation_features(agent):
    """Demonstrate evaluation capabilities"""
    print("\n🎯 Demo: Evaluation Features")
    print("=" * 60)
    
    # Create a test dataset for offline evaluation
    test_dataset = [
        {"question": "What is 2 + 2?", "expected_answer": "4"},
        {"question": "What is the capital of Australia?", "expected_answer": "canberra"},
        {"question": "What is 5 * 3?", "expected_answer": "15"},
        {"question": "What color is grass?", "expected_answer": "green"}
    ]
    
    print("2. Running Offline Evaluation:")
    print(f"   Test Dataset Size: {len(test_dataset)} questions")
    
    # Note: Without Azure endpoint, this will test fallback behavior
    eval_results = agent.run_offline_evaluation(test_dataset)
    
    print(f"   Results:")
    print(f"   - Accuracy: {eval_results['accuracy']:.2%}")
    print(f"   - Average Latency: {eval_results['average_latency_ms']:.2f}ms")
    print(f"   - Total Cost: ${eval_results['total_cost']:.4f}")
    
    return eval_results

def demo_observability_data(agent):
    """Demonstrate observability data export"""
    print("\n🎯 Demo: Observability Data Export")
    print("=" * 60)
    
    # Get performance metrics
    metrics = agent.get_performance_metrics()
    print("3. Performance Metrics:")
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"   - {key}: {value:.4f}")
        else:
            print(f"   - {key}: {value}")
    
    # Export traces for analysis
    print("\n4. Exporting Trace Data:")
    export_file = agent.export_traces_for_vscode()
    if export_file:
        print(f"   ✅ Traces exported to: {export_file}")
        print("   🔍 Open this file in VS Code to inspect detailed traces")
        
        # Show sample trace structure
        try:
            with open(export_file, 'r') as f:
                trace_data = json.load(f)
            print(f"   📊 Total traces captured: {len(trace_data['traces'])}")
            print(f"   📅 Export timestamp: {trace_data['export_timestamp']}")
        except Exception as e:
            print(f"   ❌ Error reading trace file: {e}")
    
    return export_file

def demo_vs_code_debugging():
    """Show how to use the observability features in VS Code"""
    print("\n🎯 Demo: VS Code Debugging Integration")
    print("=" * 60)
    
    print("5. VS Code Debugging Features:")
    print("   ✅ Structured logging to agent_v68_traces.log")
    print("   ✅ Individual trace files for each operation")
    print("   ✅ Comprehensive JSON export with all traces")
    print("   ✅ Performance metrics tracking")
    print("   ✅ Error tracking and fallback behavior")
    
    print("\n   🛠️  How to use in VS Code:")
    print("   1. Set breakpoints in agent_v68.py methods")
    print("   2. Run your agent code in debug mode")
    print("   3. Inspect span.attributes and trace data")
    print("   4. Monitor metrics in real-time")
    print("   5. Analyze JSON exports for pattern recognition")

def demo_production_readiness():
    """Demonstrate production-ready features"""
    print("\n🎯 Demo: Production-Ready Features")
    print("=" * 60)
    
    print("6. Production Observability Features:")
    print("   ✅ OpenTelemetry-compatible span structure")
    print("   ✅ Cost tracking per request")
    print("   ✅ Latency monitoring")
    print("   ✅ Error rate tracking")
    print("   ✅ Success rate metrics")
    print("   ✅ Fallback mechanism for reliability")
    print("   ✅ Structured logging for monitoring systems")
    print("   ✅ JSON export for analytics platforms")
    
    print("\n   🚀 Ready for integration with:")
    print("   - Azure Monitor / Application Insights")
    print("   - Langfuse for LLM observability")
    print("   - Prometheus/Grafana for metrics")
    print("   - ELK Stack for log analysis")
    print("   - Custom monitoring dashboards")

def main():
    """Main demo function"""
    print("🤖 GameAgentV68 - AI Agent with Observability & Evaluation")
    print("Based on 68-ai-agents-production documentation")
    print("Following agent_v1.py structure with enhanced features")
    print("=" * 70)
    
    try:
        # Run demonstrations
        agent = demo_basic_functionality()
        eval_results = demo_evaluation_features(agent)
        export_file = demo_observability_data(agent)
        demo_vs_code_debugging()
        demo_production_readiness()
        
        print("\n" + "=" * 70)
        print("🎉 Demo completed successfully!")
        print("\n📋 Summary of Generated Files:")
        print("   - agent_v68_traces.log (detailed logs)")
        print("   - agent_v68_all_traces.json (trace export)")
        print("   - trace_*.json (individual trace files)")
        
        print("\n🔧 Next Steps:")
        print("   1. Configure Azure AI endpoint for full functionality")
        print("   2. Integrate with your preferred observability platform")
        print("   3. Customize evaluation datasets for your use case")
        print("   4. Set up monitoring alerts based on metrics")
        print("   5. Use trace data for agent optimization")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)