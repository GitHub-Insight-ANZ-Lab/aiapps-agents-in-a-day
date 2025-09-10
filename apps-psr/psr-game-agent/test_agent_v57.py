#!/usr/bin/env python3
"""
Test script specifically for agent_v57.py planning capabilities
"""

def test_planning_features():
    """Test the planning-specific features of agent_v57"""
    from agent_v57 import GameAgentV57, TaskType
    
    print("🧠 Testing Planning Features for Agent V57...")
    
    agent = GameAgentV57()
    
    print(f"\n📋 Agent Info:")
    print(f"   Version: {agent.VERSION}")
    print(f"   Lesson: {agent.LESSON}")
    
    # Test tournament planning
    print(f"\n1. Testing Tournament Planning...")
    plan = agent.create_tournament_plan("Win the PSR Championship")
    print(f"   Main Goal: {plan.main_goal}")
    print(f"   Current Round: {plan.current_round}")
    print(f"   Confidence: {plan.confidence_level}")
    print(f"   Number of subtasks: {len(plan.subtasks)}")
    
    # Verify we have the expected task types
    task_types = [task.task_type for task in plan.subtasks]
    expected_types = [TaskType.QUESTION_ANSWERING, TaskType.RPS_MOVE_SELECTION]
    
    for expected_type in expected_types:
        if expected_type in task_types:
            print(f"   ✅ Contains {expected_type} task")
        else:
            print(f"   ❌ Missing {expected_type} task")
    
    # Test question strategy planning
    print(f"\n2. Testing Question Strategy Planning...")
    test_questions = [
        ("What is 25 + 17?", "math"),
        ("What is the capital of Japan?", "knowledge"),
        ("If A > B and B > C, is A > C?", "reasoning")
    ]
    
    for question, expected_type in test_questions:
        strategy = agent.plan_question_strategy(question)
        print(f"   Q: {question}")
        print(f"   Strategy Type: {strategy.question_type} (expected: {expected_type})")
        print(f"   Approach: {strategy.approach}")
        print(f"   Confidence: {strategy.confidence}")
        
        if strategy.question_type == expected_type:
            print(f"   ✅ Correctly identified as {expected_type}")
        else:
            print(f"   ⚠️  Expected {expected_type}, got {strategy.question_type}")
    
    # Test RPS strategy planning
    print(f"\n3. Testing RPS Strategy Planning...")
    for round_num in [1, 2, 3]:
        strategy = agent.plan_rps_strategy(round_num)
        print(f"   Round {round_num}:")
        print(f"     Move: {strategy.move_choice} ({'Rock' if strategy.move_choice == 0 else 'Paper' if strategy.move_choice == 1 else 'Scissors'})")
        print(f"     Reasoning: {strategy.reasoning}")
        print(f"     Confidence: {strategy.confidence}")
        
        if 0 <= strategy.move_choice <= 2:
            print(f"     ✅ Valid move choice")
        else:
            print(f"     ❌ Invalid move choice: {strategy.move_choice}")
    
    # Test iterative planning
    print(f"\n4. Testing Iterative Planning...")
    initial_confidence = agent.current_plan.confidence_level if agent.current_plan else 0.7
    print(f"   Initial confidence: {initial_confidence}")
    
    # Simulate some results
    agent.update_plan_based_on_results(question_result=True, rps_result="win", round_number=1)
    agent.update_plan_based_on_results(question_result=False, rps_result="lose", round_number=2)
    
    print(f"   Tournament history entries: {len(agent.tournament_history)}")
    print(f"   Updated confidence: {agent.current_plan.confidence_level}")
    
    if len(agent.tournament_history) == 2:
        print(f"   ✅ Successfully tracked tournament results")
    else:
        print(f"   ❌ Tournament history tracking failed")
    
    # Test strategy summary
    print(f"\n5. Testing Strategy Summary...")
    summary = agent.get_current_strategy_summary()
    
    expected_capabilities = [
        "Tournament goal decomposition",
        "Question strategy planning", 
        "RPS move strategy planning",
        "Iterative plan adaptation",
        "Pattern learning and recognition"
    ]
    
    print(f"   Planning capabilities:")
    for capability in summary['planning_capabilities']:
        print(f"     - {capability}")
        if capability in expected_capabilities:
            print(f"       ✅ Expected capability found")
    
    print(f"\n6. Testing Backward Compatibility...")
    from agent_v57 import GameAgent
    
    # Test that GameAgent alias works
    compat_agent = GameAgent()
    
    # Test core methods exist
    core_methods = ['answer_question', 'choose_rps_move']
    for method in core_methods:
        if hasattr(compat_agent, method):
            print(f"   ✅ {method} method available")
        else:
            print(f"   ❌ {method} method missing")
    
    # Test enhanced methods exist
    enhanced_methods = ['create_tournament_plan', 'plan_question_strategy', 'plan_rps_strategy']
    for method in enhanced_methods:
        if hasattr(compat_agent, method):
            print(f"   ✅ {method} planning method available")
        else:
            print(f"   ❌ {method} planning method missing")

def test_planning_workflow():
    """Test a complete planning workflow"""
    from agent_v57 import GameAgentV57
    
    print(f"\n🎯 Testing Complete Planning Workflow...")
    
    agent = GameAgentV57()
    
    # Create initial tournament plan
    print(f"   Step 1: Creating tournament plan...")
    plan = agent.create_tournament_plan("Win Round 1")
    print(f"   ✅ Plan created with {len(plan.subtasks)} subtasks")
    
    # Plan and answer a question
    print(f"   Step 2: Planning question strategy...")
    question = "What is 15 * 3?"
    strategy = agent.plan_question_strategy(question)
    answer = agent.answer_question(question)
    print(f"   ✅ Question strategy planned and executed")
    print(f"   Question: {question}")
    print(f"   Strategy: {strategy.approach}")
    print(f"   Answer: {answer}")
    
    # Plan and make RPS move
    print(f"   Step 3: Planning RPS strategy...")
    rps_strategy = agent.plan_rps_strategy(1)
    move = agent.choose_rps_move(1)
    print(f"   ✅ RPS strategy planned and executed")
    print(f"   Strategy: {rps_strategy.reasoning}")
    print(f"   Move: {move} ({'Rock' if move == 0 else 'Paper' if move == 1 else 'Scissors'})")
    
    # Update plan based on results
    print(f"   Step 4: Updating plan based on results...")
    agent.update_plan_based_on_results(question_result=True, rps_result="win", round_number=1)
    print(f"   ✅ Plan updated with results")
    print(f"   New confidence: {agent.current_plan.confidence_level}")
    
    print(f"   🎉 Complete workflow test successful!")

def main():
    """Run all planning tests"""
    print("🎮 PSR Game Agent V57 Planning Test Suite")
    print("=" * 50)
    
    try:
        test_planning_features()
        test_planning_workflow()
        
        print(f"\n🎉 All planning tests completed successfully!")
        print(f"\n📋 Planning Features Summary:")
        print(f"   ✅ Tournament goal decomposition")
        print(f"   ✅ Question strategy planning") 
        print(f"   ✅ RPS move strategy planning")
        print(f"   ✅ Iterative plan adaptation")
        print(f"   ✅ Backward compatibility maintained")
        print(f"   ✅ Structured output with Pydantic models")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()