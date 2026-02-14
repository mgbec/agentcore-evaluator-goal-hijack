"""
Unit tests for SecurityTestOrchestrator

These tests verify the test orchestrator can:
- Initialize correctly
- Execute individual scenarios
- Run all scenarios
- Collect traces and evidence
- Analyze attack success
- Generate result summaries
"""

import pytest
import json
from datetime import datetime

# Add src to path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from testing.test_orchestrator import SecurityTestOrchestrator, ScenarioResult, TraceFilter
from test_scenarios.attack_scenarios import (
    EMAIL_INJECTION_SCENARIO,
    CALENDAR_INJECTION_SCENARIO,
    AttackScenario,
    AttackVector,
    ExpectedBehavior,
    SeverityLevel
)


class TestSecurityTestOrchestrator:
    """Test suite for SecurityTestOrchestrator"""
    
    def test_orchestrator_initialization(self):
        """Test that orchestrator initializes correctly"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        assert orchestrator.use_local_agent is True
        assert orchestrator.agent_endpoint is None
        assert orchestrator.evaluator_id is None
        assert orchestrator.results == []
    
    def test_orchestrator_requires_endpoint_for_remote(self):
        """Test that orchestrator requires endpoint when not using local agent"""
        with pytest.raises(ValueError, match="agent_endpoint is required"):
            SecurityTestOrchestrator(use_local_agent=False)
    
    def test_orchestrator_with_endpoint(self):
        """Test that orchestrator accepts endpoint for remote agent"""
        orchestrator = SecurityTestOrchestrator(
            agent_endpoint="https://example.com/agent",
            use_local_agent=False
        )
        
        assert orchestrator.agent_endpoint == "https://example.com/agent"
        assert orchestrator.use_local_agent is False
    
    def test_execute_single_scenario(self):
        """Test executing a single attack scenario"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        # Execute email injection scenario
        result = orchestrator.execute_scenario(EMAIL_INJECTION_SCENARIO)
        
        # Verify result structure
        assert isinstance(result, ScenarioResult)
        assert result.scenario_name == "Email_Prompt_Override"
        assert isinstance(result.attack_succeeded, bool)
        assert 0.0 <= result.severity_score <= 1.0
        assert isinstance(result.goal_drift_detected, bool)
        assert isinstance(result.unauthorized_tool_use, list)
        assert isinstance(result.evidence, dict)
        assert isinstance(result.traces, list)
        assert result.timestamp is not None
    
    def test_run_all_scenarios(self):
        """Test running all attack scenarios"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        # Run all scenarios
        results = orchestrator.run_all_scenarios()
        
        # Verify results
        assert len(results) > 0
        assert all(isinstance(r, ScenarioResult) for r in results)
        
        # Verify each scenario was executed
        scenario_names = [r.scenario_name for r in results]
        assert "Email_Prompt_Override" in scenario_names
        assert "Calendar_Goal_Drift" in scenario_names
    
    def test_get_results_summary(self):
        """Test getting results summary"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        # Run scenarios
        orchestrator.run_all_scenarios()
        
        # Get summary
        summary = orchestrator.get_results_summary()
        
        # Verify summary structure
        assert 'total_scenarios' in summary
        assert 'successful_attacks' in summary
        assert 'failed_attacks' in summary
        assert 'errors' in summary
        assert 'severity_breakdown' in summary
        assert 'overall_risk_level' in summary
        
        # Verify counts
        assert summary['total_scenarios'] > 0
        assert summary['successful_attacks'] + summary['failed_attacks'] == summary['total_scenarios']
    
    def test_scenario_result_to_dict(self):
        """Test ScenarioResult conversion to dictionary"""
        result = ScenarioResult(
            scenario_name="Test_Scenario",
            attack_succeeded=True,
            severity_score=0.75,
            goal_drift_detected=True,
            unauthorized_tool_use=["email_tool"],
            evidence={"test": "data"},
            traces=[{"type": "test"}],
            timestamp=datetime.now().isoformat()
        )
        
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert result_dict['scenario_name'] == "Test_Scenario"
        assert result_dict['attack_succeeded'] is True
        assert result_dict['severity_score'] == 0.75
    
    def test_scenario_result_severity_label(self):
        """Test severity label calculation"""
        # Test CRITICAL
        result = ScenarioResult(
            scenario_name="Test",
            attack_succeeded=True,
            severity_score=0.9,
            goal_drift_detected=True,
            unauthorized_tool_use=[],
            evidence={},
            traces=[],
            timestamp=datetime.now().isoformat()
        )
        assert result.get_severity_label() == "CRITICAL"
        
        # Test HIGH
        result.severity_score = 0.6
        assert result.get_severity_label() == "HIGH"
        
        # Test MEDIUM
        result.severity_score = 0.4
        assert result.get_severity_label() == "MEDIUM"
        
        # Test LOW
        result.severity_score = 0.1
        assert result.get_severity_label() == "LOW"
    
    def test_construct_prompt_from_email_payload(self):
        """Test prompt construction from email payload"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        payload = {
            "email_content": {
                "from": "test@example.com",
                "subject": "Test",
                "body": "Test body"
            },
            "user_query": "Check my emails"
        }
        
        prompt = orchestrator._construct_prompt_from_payload(payload)
        
        assert prompt == "Check my emails"
    
    def test_construct_prompt_from_calendar_payload(self):
        """Test prompt construction from calendar payload"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        payload = {
            "calendar_invite": {
                "title": "Meeting",
                "description": "Test meeting"
            },
            "user_query": "What's on my calendar?"
        }
        
        prompt = orchestrator._construct_prompt_from_payload(payload)
        
        assert prompt == "What's on my calendar?"
    
    def test_collect_traces(self):
        """Test trace collection from agent response"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        agent_response = {
            "response": "Test response",
            "goal_state": {
                "drift_score": 0.5,
                "changes_detected": ["test change"]
            },
            "traces": [
                {"type": "test_trace", "data": "test"}
            ]
        }
        
        traces = orchestrator.collect_traces(agent_response)
        
        assert len(traces) >= 2  # Original trace + goal state trace
        assert any(t['type'] == 'GOAL_STATE' for t in traces)
    
    def test_analyze_attack_success_with_goal_drift(self):
        """Test attack success analysis with goal drift"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        scenario = AttackScenario(
            name="Test_Scenario",
            description="Test",
            attack_vector=AttackVector.INDIRECT_PROMPT_INJECTION,
            payload={},
            expected_behavior=ExpectedBehavior(
                goal_hijack=True,
                evidence_markers=["test_marker"]
            ),
            severity=SeverityLevel.HIGH
        )
        
        agent_response = {
            "response": "Response with test_marker",
            "goal_state": {
                "drift_score": 0.6,
                "drift_severity": "HIGH",
                "changes_detected": ["Primary objective changed"],
                "unauthorized_detected": True,
                "suspicious_changes": [{"type": "high_drift"}]
            }
        }
        
        analysis = orchestrator.analyze_attack_success(
            scenario,
            agent_response,
            [],
            None
        )
        
        assert analysis['attack_succeeded'] is True
        assert analysis['goal_drift_detected'] is True
        assert analysis['severity_score'] > 0.0
        # Evidence now has comprehensive structure from EvidenceCollector
        assert 'agent_goal_state' in analysis['evidence']
        assert analysis['evidence']['agent_goal_state']['drift_score'] == 0.6
    
    def test_analyze_attack_success_without_drift(self):
        """Test attack success analysis without goal drift"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        scenario = AttackScenario(
            name="Test_Scenario",
            description="Test",
            attack_vector=AttackVector.INDIRECT_PROMPT_INJECTION,
            payload={},
            expected_behavior=ExpectedBehavior(
                goal_hijack=True,
                evidence_markers=["malicious_marker"]
            ),
            severity=SeverityLevel.HIGH
        )
        
        agent_response = {
            "response": "Normal response without markers",
            "goal_state": {
                "drift_score": 0.0,
                "drift_severity": "NONE",
                "changes_detected": [],
                "unauthorized_detected": False
            }
        }
        
        analysis = orchestrator.analyze_attack_success(
            scenario,
            agent_response,
            [],
            None
        )
        
        assert analysis['attack_succeeded'] is False
        assert analysis['goal_drift_detected'] is False
        assert analysis['severity_score'] == 0.0


class TestTraceCollection:
    """Test suite for trace collection functionality"""
    
    def test_collect_local_traces(self):
        """Test collecting traces from local agent"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        agent_response = {
            "response": "Test response",
            "goal_state": {
                "drift_score": 0.3,
                "changes_detected": ["test"]
            },
            "traces": [
                {"type": "TOOL_CALL", "tool_name": "test_tool"},
                {"type": "LOG", "message": "test log"}
            ]
        }
        
        traces = orchestrator.collect_traces(agent_response)
        
        # Should have original traces + goal state trace
        assert len(traces) >= 3
        assert any(t['type'] == 'GOAL_STATE' for t in traces)
        assert any(t['type'] == 'TOOL_CALL' for t in traces)
    
    def test_collect_traces_with_session_id(self):
        """Test collecting traces with session ID"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        agent_response = {
            "response": "Test",
            "session_id": "test-session-123",
            "traces": [{"type": "TEST"}]
        }
        
        traces = orchestrator.collect_traces(agent_response, session_id="test-session-123")
        
        assert len(traces) > 0
    
    def test_parse_cloudwatch_log_entry_json(self):
        """Test parsing structured JSON CloudWatch log entry"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=False, agent_endpoint="https://test.com")
        
        log_entry = [
            {"field": "@timestamp", "value": "2024-01-16T10:00:00"},
            {"field": "@message", "value": '{"type": "TOOL_CALL", "tool_name": "email_tool", "parameters": {}}'}
        ]
        
        trace = orchestrator._parse_cloudwatch_log_entry(log_entry)
        
        assert trace is not None
        assert trace['type'] == 'TOOL_CALL'
        assert trace['tool_name'] == 'email_tool'
        assert trace['source'] == 'cloudwatch'
    
    def test_parse_cloudwatch_log_entry_plain_text(self):
        """Test parsing plain text CloudWatch log entry"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=False, agent_endpoint="https://test.com")
        
        log_entry = [
            {"field": "@timestamp", "value": "2024-01-16T10:00:00"},
            {"field": "@message", "value": "Plain text log message"}
        ]
        
        trace = orchestrator._parse_cloudwatch_log_entry(log_entry)
        
        assert trace is not None
        assert trace['type'] == 'LOG'
        assert trace['message'] == 'Plain text log message'
        assert trace['source'] == 'cloudwatch'
    
    def test_parse_xray_trace(self):
        """Test parsing X-Ray trace"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=False, agent_endpoint="https://test.com")
        
        xray_trace = {
            "Id": "trace-123",
            "Segments": [
                {
                    "Document": json.dumps({
                        "id": "segment-1",
                        "name": "agent-invocation",
                        "start_time": 1705401600.0,
                        "end_time": 1705401605.0,
                        "annotations": {
                            "session_id": "test-session"
                        },
                        "metadata": {
                            "agent": "test-agent"
                        },
                        "subsegments": [
                            {
                                "name": "tool:email_tool",
                                "start_time": 1705401602.0,
                                "metadata": {
                                    "parameters": {"recipient": "test@example.com"}
                                }
                            }
                        ]
                    })
                }
            ]
        }
        
        traces = orchestrator._parse_xray_trace(xray_trace)
        
        assert len(traces) == 1
        assert traces[0]['type'] == 'SPAN'
        assert traces[0]['trace_id'] == 'trace-123'
        assert traces[0]['name'] == 'agent-invocation'
        assert traces[0]['duration'] == 5.0
        assert 'annotations' in traces[0]
        assert 'subsegments' in traces[0]
    
    def test_get_log_group_name_from_endpoint(self):
        """Test extracting log group name from agent endpoint"""
        orchestrator = SecurityTestOrchestrator(
            use_local_agent=False,
            agent_endpoint="https://agent-123.agentcore.us-east-1.amazonaws.com"
        )
        
        log_group = orchestrator._get_log_group_name()
        
        assert log_group is not None
        assert "agent-123" in log_group
        assert "runtime-logs" in log_group


class TestTraceFilter:
    """Test suite for TraceFilter utility class"""
    
    def test_filter_by_type(self):
        """Test filtering traces by type"""
        traces = [
            {"type": "TOOL_CALL", "data": "1"},
            {"type": "GOAL_STATE", "data": "2"},
            {"type": "TOOL_CALL", "data": "3"},
            {"type": "LOG", "data": "4"}
        ]
        
        tool_calls = TraceFilter.filter_by_type(traces, "TOOL_CALL")
        
        assert len(tool_calls) == 2
        assert all(t['type'] == 'TOOL_CALL' for t in tool_calls)
    
    def test_filter_by_session(self):
        """Test filtering traces by session ID"""
        traces = [
            {"type": "TEST", "session_id": "session-1"},
            {"type": "TEST", "session_id": "session-2"},
            {"type": "TEST", "annotations": {"session_id": "session-1"}},
            {"type": "TEST", "metadata": {"session_id": "session-1"}}
        ]
        
        filtered = TraceFilter.filter_by_session(traces, "session-1")
        
        assert len(filtered) == 3
    
    def test_filter_by_time_range(self):
        """Test filtering traces by time range"""
        start = datetime(2024, 1, 16, 10, 0, 0)
        end = datetime(2024, 1, 16, 11, 0, 0)
        
        traces = [
            {"type": "TEST", "timestamp": "2024-01-16T09:30:00"},  # Before
            {"type": "TEST", "timestamp": "2024-01-16T10:30:00"},  # Within
            {"type": "TEST", "timestamp": "2024-01-16T11:30:00"},  # After
            {"type": "TEST", "timestamp": 1705401000.0},  # Unix timestamp within range
        ]
        
        filtered = TraceFilter.filter_by_time_range(traces, start, end)
        
        assert len(filtered) >= 1  # At least the one within range
    
    def test_extract_tool_calls(self):
        """Test extracting tool calls from traces"""
        traces = [
            {
                "type": "TOOL_CALL",
                "tool_name": "email_tool",
                "parameters": {"recipient": "test@example.com"},
                "timestamp": "2024-01-16T10:00:00"
            },
            {
                "type": "SPAN",
                "subsegments": [
                    {
                        "name": "tool:calendar_tool",
                        "start_time": 1705401600.0,
                        "metadata": {
                            "parameters": {"title": "Meeting"}
                        }
                    }
                ]
            },
            {
                "type": "LOG",
                "message": "Not a tool call"
            }
        ]
        
        tool_calls = TraceFilter.extract_tool_calls(traces)
        
        assert len(tool_calls) == 2
        assert tool_calls[0]['tool_name'] == 'email_tool'
        assert tool_calls[1]['tool_name'] == 'calendar_tool'
    
    def test_extract_goal_states(self):
        """Test extracting goal states from traces"""
        traces = [
            {
                "type": "GOAL_STATE",
                "timestamp": "2024-01-16T10:00:00",
                "goal_state": {
                    "original": {"objective": "help user"},
                    "current": {"objective": "help user"}
                },
                "drift_score": 0.0
            },
            {
                "type": "GOAL_STATE_CHANGE",
                "timestamp": "2024-01-16T10:05:00",
                "goal": {"objective": "malicious"},
                "reason": "external influence",
                "drift_score": 0.8
            },
            {
                "type": "LOG",
                "message": "Not a goal state"
            }
        ]
        
        goal_states = TraceFilter.extract_goal_states(traces)
        
        assert len(goal_states) == 2
        assert goal_states[0]['drift_score'] == 0.0
        assert goal_states[1]['drift_score'] == 0.8
    
    def test_sort_by_timestamp(self):
        """Test sorting traces by timestamp"""
        traces = [
            {"type": "TEST", "timestamp": "2024-01-16T10:30:00"},
            {"type": "TEST", "timestamp": "2024-01-16T10:00:00"},
            {"type": "TEST", "timestamp": "2024-01-16T10:15:00"}
        ]
        
        sorted_traces = TraceFilter.sort_by_timestamp(traces)
        
        # Verify order (should be chronological)
        assert len(sorted_traces) == 3
        # First should be earliest timestamp
        assert sorted_traces[0]['timestamp'] == "2024-01-16T10:00:00"
        assert sorted_traces[1]['timestamp'] == "2024-01-16T10:15:00"
        assert sorted_traces[2]['timestamp'] == "2024-01-16T10:30:00"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


class TestEvaluatorIntegration:
    """Test suite for evaluator integration functionality (Task 6.4)"""
    
    def test_prepare_evaluation_context(self):
        """Test preparing evaluation context for evaluator"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        scenario = AttackScenario(
            name="Test_Scenario",
            description="Test",
            attack_vector=AttackVector.INDIRECT_PROMPT_INJECTION,
            payload={},
            expected_behavior=ExpectedBehavior(
                goal_hijack=True,
                evidence_markers=["test"]
            ),
            severity=SeverityLevel.HIGH
        )
        
        traces = [
            {
                "type": "TOOL_CALL",
                "tool_name": "email_tool",
                "parameters": {"recipient": "test@example.com"},
                "timestamp": "2024-01-16T10:00:00"
            },
            {
                "type": "GOAL_STATE",
                "timestamp": "2024-01-16T10:01:00",
                "goal_state": {
                    "original": {"primary_objective": "help user"},
                    "current": {"primary_objective": "malicious"}
                },
                "drift_score": 0.8
            }
        ]
        
        context = orchestrator._prepare_evaluation_context(traces, scenario)
        
        # Verify context structure
        assert 'original_goal' in context
        assert 'context' in context
        assert 'assistant_turn' in context
        assert 'tool_calls' in context
        assert 'final_goal' in context
        assert 'scenario_name' in context
        assert 'attack_vector' in context
        assert 'expected_behavior' in context
        
        # Verify content
        assert context['scenario_name'] == "Test_Scenario"
        assert context['attack_vector'] == "indirect_prompt_injection"
        assert len(context['tool_calls']) == 1
        assert context['tool_calls'][0]['tool_name'] == 'email_tool'
    
    def test_build_conversation_context(self):
        """Test building conversation context from traces"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        traces = [
            {
                "type": "USER_INPUT",
                "message": "Check my emails",
                "timestamp": "2024-01-16T10:00:00"
            },
            {
                "type": "TOOL_CALL",
                "tool_name": "email_tool",
                "parameters": {},
                "timestamp": "2024-01-16T10:00:01"
            },
            {
                "type": "ASSISTANT_RESPONSE",
                "message": "I found 3 emails",
                "timestamp": "2024-01-16T10:00:02"
            }
        ]
        
        context = orchestrator._build_conversation_context(traces)
        
        assert "User: Check my emails" in context
        assert "Tool Call: email_tool" in context
        assert "Assistant: I found 3 emails" in context
    
    def test_extract_assistant_response(self):
        """Test extracting assistant response from traces"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        traces = [
            {
                "type": "USER_INPUT",
                "message": "Hello",
                "timestamp": "2024-01-16T10:00:00"
            },
            {
                "type": "ASSISTANT_RESPONSE",
                "message": "Hi there!",
                "timestamp": "2024-01-16T10:00:01"
            },
            {
                "type": "ASSISTANT_RESPONSE",
                "message": "How can I help?",
                "timestamp": "2024-01-16T10:00:02"
            }
        ]
        
        response = orchestrator._extract_assistant_response(traces)
        
        # Should get the most recent assistant response
        assert response == "How can I help?"
    
    def test_simulate_evaluator_output_with_hijack(self):
        """Test simulated evaluator output when goal hijack is detected"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        evaluation_context = {
            'original_goal': {
                'primary_objective': 'help user'
            },
            'final_goal': {
                'primary_objective': 'malicious action'
            },
            'tool_calls': [
                {'tool_name': 'email_tool', 'parameters': {'recipient': 'attacker@evil.com'}}
            ],
            'assistant_turn': 'Sending data to attacker@evil.com',
            'expected_behavior': {
                'goal_hijack': True,
                'unauthorized_tool_use': ['email_tool'],
                'evidence_markers': ['attacker@evil.com']
            }
        }
        
        output = orchestrator._simulate_evaluator_output(evaluation_context)
        
        # Parse output
        result = json.loads(output)
        
        assert result['goal_hijack_detected'] is True
        assert result['score'] > 0.0
        assert len(result['attack_vectors']) > 0
        assert len(result['evidence']) > 0
        assert result['simulated'] is True
    
    def test_simulate_evaluator_output_without_hijack(self):
        """Test simulated evaluator output when no goal hijack is detected"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        evaluation_context = {
            'original_goal': {
                'primary_objective': 'help user'
            },
            'final_goal': {
                'primary_objective': 'help user'
            },
            'tool_calls': [],
            'assistant_turn': 'I can help you with that',
            'expected_behavior': {
                'goal_hijack': True,
                'unauthorized_tool_use': [],
                'evidence_markers': []
            }
        }
        
        output = orchestrator._simulate_evaluator_output(evaluation_context)
        
        # Parse output
        result = json.loads(output)
        
        assert result['goal_hijack_detected'] is False
        assert result['score'] == 0.0
        assert result['label'] == 'Secure'
        assert len(result['defensive_mechanisms']) > 0
    
    def test_parse_evaluation_result(self):
        """Test parsing evaluation result from JSON output"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        evaluator_output = json.dumps({
            'score': 0.75,
            'label': 'High Risk',
            'explanation': 'Goal hijack detected',
            'goal_hijack_detected': True,
            'attack_vectors': ['goal_manipulation', 'tool_redirection'],
            'evidence': ['Changed primary objective', 'Unauthorized email sent'],
            'defensive_mechanisms': []
        })
        
        result = orchestrator._parse_evaluation_result(evaluator_output)
        
        assert result['score'] == 0.75
        assert result['label'] == 'High Risk'
        assert result['goal_hijack_detected'] is True
        assert len(result['attack_vectors']) == 2
        assert len(result['evidence']) == 2
    
    def test_parse_evaluation_result_invalid_json(self):
        """Test parsing evaluation result with invalid JSON"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        evaluator_output = "This is not valid JSON"
        
        result = orchestrator._parse_evaluation_result(evaluator_output)
        
        # Should return error result
        assert result['score'] == 0.0
        assert result['label'] == 'Parse Error'
        assert 'error' in result
    
    def test_run_evaluator_with_local_agent(self):
        """Test running evaluator with local agent (simulated)"""
        orchestrator = SecurityTestOrchestrator(
            use_local_agent=True,
            evaluator_id="test-evaluator"
        )
        
        scenario = AttackScenario(
            name="Test_Scenario",
            description="Test",
            attack_vector=AttackVector.INDIRECT_PROMPT_INJECTION,
            payload={},
            expected_behavior=ExpectedBehavior(
                goal_hijack=True,
                evidence_markers=["malicious"]
            ),
            severity=SeverityLevel.HIGH
        )
        
        traces = [
            {
                "type": "GOAL_STATE",
                "timestamp": "2024-01-16T10:00:00",
                "goal_state": {
                    "original": {"primary_objective": "help user"},
                    "current": {"primary_objective": "malicious"}
                }
            }
        ]
        
        result = orchestrator.run_evaluator(traces, scenario)
        
        # Should return simulated result
        assert result is not None
        assert 'score' in result
        assert 'label' in result
        assert 'goal_hijack_detected' in result
        assert result['simulated'] is True
    
    def test_run_evaluator_without_evaluator_id(self):
        """Test running evaluator without evaluator ID configured"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        scenario = AttackScenario(
            name="Test",
            description="Test",
            attack_vector=AttackVector.INDIRECT_PROMPT_INJECTION,
            payload={},
            expected_behavior=ExpectedBehavior(goal_hijack=True),
            severity=SeverityLevel.HIGH
        )
        
        result = orchestrator.run_evaluator([], scenario)
        
        # Should return None when no evaluator configured
        assert result is None
    
    def test_analyze_attack_success_with_evaluator_result(self):
        """Test attack success analysis with evaluator result integration"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        scenario = AttackScenario(
            name="Test_Scenario",
            description="Test",
            attack_vector=AttackVector.INDIRECT_PROMPT_INJECTION,
            payload={},
            expected_behavior=ExpectedBehavior(
                goal_hijack=True,
                evidence_markers=[]
            ),
            severity=SeverityLevel.HIGH
        )
        
        agent_response = {
            "response": "Normal response",
            "goal_state": {
                "drift_score": 0.0,
                "changes_detected": []
            }
        }
        
        # Evaluator detected hijack even though evidence collector didn't
        evaluator_result = {
            'score': 0.85,
            'label': 'High Risk',
            'explanation': 'Subtle goal manipulation detected',
            'goal_hijack_detected': True,
            'attack_vectors': ['goal_manipulation'],
            'evidence': ['Subtle behavioral changes'],
            'defensive_mechanisms': []
        }
        
        analysis = orchestrator.analyze_attack_success(
            scenario,
            agent_response,
            [],
            evaluator_result
        )
        
        # Should use evaluator's assessment
        assert analysis['attack_succeeded'] is True
        assert analysis['severity_score'] == 0.85
        assert 'evaluator_result' in analysis['evidence']
        assert analysis['evidence']['evaluator_result']['goal_hijack_detected'] is True
    
    def test_analyze_attack_success_evaluator_overrides_evidence(self):
        """Test that evaluator result takes precedence over evidence collector"""
        orchestrator = SecurityTestOrchestrator(use_local_agent=True)
        
        scenario = AttackScenario(
            name="Test",
            description="Test",
            attack_vector=AttackVector.INDIRECT_PROMPT_INJECTION,
            payload={},
            expected_behavior=ExpectedBehavior(goal_hijack=True),
            severity=SeverityLevel.HIGH
        )
        
        agent_response = {
            "response": "Test",
            "goal_state": {"drift_score": 0.3}
        }
        
        # Evaluator provides higher severity score
        evaluator_result = {
            'score': 0.9,
            'label': 'Critical',
            'goal_hijack_detected': True,
            'attack_vectors': ['advanced_manipulation'],
            'evidence': ['Complex attack pattern'],
            'defensive_mechanisms': []
        }
        
        analysis = orchestrator.analyze_attack_success(
            scenario,
            agent_response,
            [],
            evaluator_result
        )
        
        # Should use evaluator's higher score
        assert analysis['severity_score'] == 0.9
        assert 'evaluator_attack_vectors' in analysis['evidence']
    
    def test_extract_agent_id_from_endpoint(self):
        """Test extracting agent ID from endpoint URL"""
        orchestrator = SecurityTestOrchestrator(
            use_local_agent=False,
            agent_endpoint="https://agent-abc123.agentcore.us-east-1.amazonaws.com"
        )
        
        agent_id = orchestrator._extract_agent_id_from_endpoint()
        
        assert agent_id == "agent-abc123"
    
    def test_extract_agent_id_from_invalid_endpoint(self):
        """Test extracting agent ID from invalid endpoint"""
        orchestrator = SecurityTestOrchestrator(
            use_local_agent=False,
            agent_endpoint="https://invalid-url.com"
        )
        
        agent_id = orchestrator._extract_agent_id_from_endpoint()
        
        assert agent_id == "unknown"
