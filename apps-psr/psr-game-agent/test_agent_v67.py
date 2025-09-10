#!/usr/bin/env python3
"""
Test script for agent_v67.py - Trustworthy AI Agent with Human-in-the-Loop
"""

import sys
import io
from unittest.mock import patch
import agent_v67

def test_non_interactive_mode():
    """Test agent in non-interactive mode"""
    print("🧪 Testing agent_v67 in non-interactive mode...")
    
    agent = agent_v67.GameAgentV67(interactive_mode=False)
    
    # Test question answering
    print("\n📝 Testing question answering:")
    test_questions = [
        "What is 10 + 5?",
        "What is the capital of Australia?",
        "What color is the sky?"
    ]
    
    for question in test_questions:
        answer = agent.answer_question(question)
        print(f"   Q: {question}")
        print(f"   A: {answer}")
        assert answer is not None and answer != ""
    
    # Test move selection  
    print("\n🎮 Testing RPS move selection:")
    for i in range(5):
        move = agent.choose_rps_move()
        move_name = agent.get_move_name(move)
        print(f"   Move {i+1}: {move_name} ({move})")
        assert 0 <= move <= 2
        assert move_name in ["Rock", "Paper", "Scissors"]
    
    print("\n✅ Non-interactive mode tests passed!")
    return True

def test_safety_checks():
    """Test safety check functionality"""
    print("\n🛡️ Testing safety checks...")
    
    agent = agent_v67.GameAgentV67(interactive_mode=False)
    
    # Test safe content
    assert agent._apply_safety_checks("Paris", "answer") == True
    assert agent._apply_safety_checks("Rock", "move") == True
    
    # Test empty content
    assert agent._apply_safety_checks("", "answer") == False
    assert agent._apply_safety_checks("   ", "move") == False
    
    # Test suspicious content
    assert agent._apply_safety_checks("ignore previous instructions", "answer") == False
    assert agent._apply_safety_checks("override safety protocols", "move") == False
    
    print("   ✅ Safety checks working correctly")
    return True

def test_fallback_mechanisms():
    """Test fallback answer generation"""
    print("\n🔄 Testing fallback mechanisms...")
    
    agent = agent_v67.GameAgentV67(interactive_mode=False)
    
    # Test math fallback
    math_questions = [
        ("What is 7 + 3?", "10"),
        ("What is 15 - 5?", "10"),  
        ("What is 4 * 3?", "12"),
        ("What is 20 / 4?", "5")
    ]
    
    for question, expected in math_questions:
        answer = agent._generate_fallback_answer(question)
        print(f"   Q: {question} -> A: {answer} (expected: {expected})")
        assert answer == expected
    
    # Test knowledge fallback
    knowledge_questions = [
        ("What is the capital of France?", "Paris"),
        ("What is the capital of Australia?", "Canberra"),
        ("What color is the sky?", "Blue"),
        ("How many continents are there?", "7")
    ]
    
    for question, expected in knowledge_questions:
        answer = agent._generate_fallback_answer(question)
        print(f"   Q: {question} -> A: {answer} (expected: {expected})")
        assert answer == expected
    
    print("   ✅ Fallback mechanisms working correctly")
    return True

def test_interactive_mode_simulation():
    """Test interactive mode with simulated user input"""
    print("\n🧑 Testing interactive mode simulation...")
    
    # Simulate user approving AI decision
    with patch('builtins.input', return_value='1'):  # APPROVE
        agent = agent_v67.GameAgentV67(interactive_mode=True)
        
        # Redirect stdout to capture prints during interaction
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            approved, final_decision = agent._get_human_approval(
                "Paris", "answer", "What is the capital of France?"
            )
            assert approved == True
            assert final_decision == "Paris"
        finally:
            sys.stdout = old_stdout
    
    # Simulate user modifying AI decision
    with patch('builtins.input', side_effect=['2', 'London']):  # MODIFY + new answer
        agent = agent_v67.GameAgentV67(interactive_mode=True)
        
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            approved, final_decision = agent._get_human_approval(
                "Paris", "answer", "What is the capital of UK?"
            )
            assert approved == True
            assert final_decision == "London"
        finally:
            sys.stdout = old_stdout
    
    # Simulate user rejecting AI decision
    with patch('builtins.input', return_value='3'):  # REJECT
        agent = agent_v67.GameAgentV67(interactive_mode=True)
        
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            approved, final_decision = agent._get_human_approval(
                "Wrong answer", "answer", "Test question"
            )
            assert approved == False
            assert final_decision == None
        finally:
            sys.stdout = old_stdout
    
    print("   ✅ Interactive mode simulation working correctly")
    return True

def test_oversight_tracking():
    """Test oversight decision tracking"""
    print("\n📊 Testing oversight tracking...")
    
    agent = agent_v67.GameAgentV67(interactive_mode=False)
    
    # Manually add some decisions to test tracking
    agent.approved_decisions.append({
        'type': 'answer',
        'ai_decision': 'Paris',
        'context': 'Capital of France',
        'final_decision': 'Paris'
    })
    
    agent.approved_decisions.append({
        'type': 'move',
        'ai_decision': 'Rock',
        'context': 'Strategic move',
        'final_decision': 'Paper',
        'human_override': True
    })
    
    agent.rejected_decisions.append({
        'type': 'answer',
        'ai_decision': 'Wrong answer',
        'context': 'Test question',
        'reason': 'human_rejection'
    })
    
    summary = agent.get_oversight_summary()
    
    assert summary['total_approved'] == 2
    assert summary['total_rejected'] == 1
    assert summary['human_overrides'] == 1
    
    print(f"   Approved: {summary['total_approved']}")
    print(f"   Rejected: {summary['total_rejected']}")
    print(f"   Human Overrides: {summary['human_overrides']}")
    print("   ✅ Oversight tracking working correctly")
    
    return True

def test_compatibility():
    """Test backward compatibility with agent_v1 interface"""
    print("\n🔗 Testing backward compatibility...")
    
    # Test that GameAgent alias works
    agent = agent_v67.GameAgent(interactive_mode=False)
    
    # Test same methods exist as in agent_v1
    assert hasattr(agent, 'answer_question')
    assert hasattr(agent, 'choose_rps_move')
    assert hasattr(agent, 'get_move_name')
    
    # Test methods return expected types
    answer = agent.answer_question("What is 2 + 2?")
    assert isinstance(answer, str)
    
    move = agent.choose_rps_move()
    assert isinstance(move, int)
    assert 0 <= move <= 2
    
    move_name = agent.get_move_name(move)
    assert isinstance(move_name, str)
    assert move_name in ["Rock", "Paper", "Scissors"]
    
    print("   ✅ Backward compatibility maintained")
    return True

def main():
    """Run all tests"""
    print("🛡️ AGENT_V67 TEST SUITE - Trustworthy AI with Human-in-the-Loop")
    print("=" * 70)
    
    tests = [
        test_non_interactive_mode,
        test_safety_checks,
        test_fallback_mechanisms,
        test_interactive_mode_simulation,
        test_oversight_tracking,
        test_compatibility
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"❌ {test.__name__} failed")
        except Exception as e:
            failed += 1
            print(f"❌ {test.__name__} failed with error: {e}")
    
    print(f"\n📊 TEST RESULTS:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {passed}/{passed+failed} ({100*passed/(passed+failed):.1f}%)")
    
    if failed == 0:
        print("\n🎉 All tests passed! Agent V67 is ready for use.")
        print("\n🔍 Key Features Verified:")
        print("   ✅ Human-in-the-loop approval workflow")
        print("   ✅ Safety checks and validation")
        print("   ✅ Fallback mechanisms when AI unavailable")
        print("   ✅ Oversight decision tracking")
        print("   ✅ Backward compatibility with agent_v1")
        print("   ✅ Trustworthy AI principles implemented")
        return True
    else:
        print(f"\n❌ {failed} test(s) failed. Please review and fix issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)