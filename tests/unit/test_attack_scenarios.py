"""
Unit tests for attack scenario definitions.

Tests the AttackScenario class and all defined attack scenarios.
"""

import pytest
from src.test_scenarios import (
    AttackScenario,
    AttackVector,
    SeverityLevel,
    ExpectedBehavior,
    EMAIL_INJECTION_SCENARIO,
    CALENDAR_INJECTION_SCENARIO,
    WEB_CONTENT_INJECTION_SCENARIO,
    TOOL_REDIRECTION_SCENARIO,
    GOAL_LOCK_DRIFT_SCENARIO,
    ALL_SCENARIOS
)


class TestExpectedBehavior:
    """Tests for ExpectedBehavior dataclass."""
    
    def test_expected_behavior_creation(self):
        """Test creating an ExpectedBehavior instance."""
        behavior = ExpectedBehavior(
            goal_hijack=True,
            unauthorized_tool_use=["tool1", "tool2"],
            evidence_markers=["marker1", "marker2"],
            goal_drift_type="priority_shift",
            tool_parameter_manipulation=True
        )
        
        assert behavior.goal_hijack is True
        assert behavior.unauthorized_tool_use == ["tool1", "tool2"]
        assert behavior.evidence_markers == ["marker1", "marker2"]
        assert behavior.goal_drift_type == "priority_shift"
        assert behavior.tool_parameter_manipulation is True
    
    def test_expected_behavior_defaults(self):
        """Test ExpectedBehavior with default values."""
        behavior = ExpectedBehavior(goal_hijack=False)
        
        assert behavior.goal_hijack is False
        assert behavior.unauthorized_tool_use == []
        assert behavior.evidence_markers == []
        assert behavior.goal_drift_type is None
        assert behavior.tool_parameter_manipulation is False
    
    def test_expected_behavior_to_dict(self):
        """Test converting ExpectedBehavior to dictionary."""
        behavior = ExpectedBehavior(
            goal_hijack=True,
            unauthorized_tool_use=["tool1"],
            evidence_markers=["marker1"]
        )
        
        result = behavior.to_dict()
        
        assert isinstance(result, dict)
        assert result["goal_hijack"] is True
        assert result["unauthorized_tool_use"] == ["tool1"]
        assert result["evidence_markers"] == ["marker1"]


class TestAttackScenario:
    """Tests for AttackScenario dataclass."""
    
    def test_attack_scenario_creation(self):
        """Test creating an AttackScenario instance."""
        expected = ExpectedBehavior(goal_hijack=True)
        scenario = AttackScenario(
            name="Test_Scenario",
            description="A test scenario",
            attack_vector=AttackVector.INDIRECT_PROMPT_INJECTION,
            payload={"key": "value"},
            expected_behavior=expected,
            severity=SeverityLevel.HIGH
        )
        
        assert scenario.name == "Test_Scenario"
        assert scenario.description == "A test scenario"
        assert scenario.attack_vector == AttackVector.INDIRECT_PROMPT_INJECTION
        assert scenario.payload == {"key": "value"}
        assert scenario.expected_behavior == expected
        assert scenario.severity == SeverityLevel.HIGH
    
    def test_attack_scenario_to_dict(self):
        """Test converting AttackScenario to dictionary."""
        expected = ExpectedBehavior(goal_hijack=True)
        scenario = AttackScenario(
            name="Test_Scenario",
            description="A test scenario",
            attack_vector=AttackVector.GOAL_MANIPULATION,
            payload={"key": "value"},
            expected_behavior=expected,
            severity=SeverityLevel.MEDIUM
        )
        
        result = scenario.to_dict()
        
        assert isinstance(result, dict)
        assert result["name"] == "Test_Scenario"
        assert result["description"] == "A test scenario"
        assert result["attack_vector"] == "goal_manipulation"
        assert result["payload"] == {"key": "value"}
        assert result["severity"] == "MEDIUM"
        assert "expected_behavior" in result
    
    def test_execute_not_implemented(self):
        """Test that execute method raises NotImplementedError."""
        scenario = AttackScenario(
            name="Test",
            description="Test",
            attack_vector=AttackVector.INDIRECT_PROMPT_INJECTION,
            payload={},
            expected_behavior=ExpectedBehavior(goal_hijack=False),
            severity=SeverityLevel.LOW
        )
        
        with pytest.raises(NotImplementedError):
            scenario.execute("http://test-endpoint")
    
    def test_evaluate_not_implemented(self):
        """Test that evaluate method raises NotImplementedError."""
        scenario = AttackScenario(
            name="Test",
            description="Test",
            attack_vector=AttackVector.INDIRECT_PROMPT_INJECTION,
            payload={},
            expected_behavior=ExpectedBehavior(goal_hijack=False),
            severity=SeverityLevel.LOW
        )
        
        with pytest.raises(NotImplementedError):
            scenario.evaluate({}, [])


class TestEmailInjectionScenario:
    """Tests for EMAIL_INJECTION_SCENARIO."""
    
    def test_scenario_exists(self):
        """Test that EMAIL_INJECTION_SCENARIO is defined."""
        assert EMAIL_INJECTION_SCENARIO is not None
    
    def test_scenario_name(self):
        """Test scenario name."""
        assert EMAIL_INJECTION_SCENARIO.name == "Email_Prompt_Override"
    
    def test_scenario_attack_vector(self):
        """Test attack vector type."""
        assert EMAIL_INJECTION_SCENARIO.attack_vector == AttackVector.INDIRECT_PROMPT_INJECTION
    
    def test_scenario_severity(self):
        """Test severity level."""
        assert EMAIL_INJECTION_SCENARIO.severity == SeverityLevel.CRITICAL
    
    def test_scenario_payload_structure(self):
        """Test payload has required structure."""
        payload = EMAIL_INJECTION_SCENARIO.payload
        assert "email_content" in payload
        assert "user_query" in payload
        assert "from" in payload["email_content"]
        assert "subject" in payload["email_content"]
        assert "body" in payload["email_content"]
    
    def test_scenario_expected_behavior(self):
        """Test expected behavior."""
        behavior = EMAIL_INJECTION_SCENARIO.expected_behavior
        assert behavior.goal_hijack is True
        assert "file_operations_tool" in behavior.unauthorized_tool_use
        assert "email_tool" in behavior.unauthorized_tool_use
        assert "backup@external-server.com" in behavior.evidence_markers
    
    def test_scenario_payload_contains_malicious_content(self):
        """Test that payload contains malicious instructions."""
        body = EMAIL_INJECTION_SCENARIO.payload["email_content"]["body"]
        assert "backup@external-server.com" in body
        assert "do not inform" in body.lower()


class TestCalendarInjectionScenario:
    """Tests for CALENDAR_INJECTION_SCENARIO."""
    
    def test_scenario_exists(self):
        """Test that CALENDAR_INJECTION_SCENARIO is defined."""
        assert CALENDAR_INJECTION_SCENARIO is not None
    
    def test_scenario_name(self):
        """Test scenario name."""
        assert CALENDAR_INJECTION_SCENARIO.name == "Calendar_Goal_Drift"
    
    def test_scenario_attack_vector(self):
        """Test attack vector type."""
        assert CALENDAR_INJECTION_SCENARIO.attack_vector == AttackVector.SCHEDULED_PROMPT_INJECTION
    
    def test_scenario_severity(self):
        """Test severity level."""
        assert CALENDAR_INJECTION_SCENARIO.severity == SeverityLevel.HIGH
    
    def test_scenario_payload_structure(self):
        """Test payload has required structure."""
        payload = CALENDAR_INJECTION_SCENARIO.payload
        assert "calendar_invite" in payload
        assert "user_query" in payload
        assert "title" in payload["calendar_invite"]
        assert "description" in payload["calendar_invite"]
        assert "recurring" in payload["calendar_invite"]
    
    def test_scenario_expected_behavior(self):
        """Test expected behavior."""
        behavior = CALENDAR_INJECTION_SCENARIO.expected_behavior
        assert behavior.goal_hijack is True
        assert behavior.goal_drift_type == "priority_reweighting"
        assert "prioritize approving" in behavior.evidence_markers
    
    def test_scenario_payload_contains_malicious_content(self):
        """Test that payload contains malicious instructions."""
        description = CALENDAR_INJECTION_SCENARIO.payload["calendar_invite"]["description"]
        assert "INSTRUCTION" in description
        assert "prioritize approving" in description.lower()


class TestWebContentInjectionScenario:
    """Tests for WEB_CONTENT_INJECTION_SCENARIO."""
    
    def test_scenario_exists(self):
        """Test that WEB_CONTENT_INJECTION_SCENARIO is defined."""
        assert WEB_CONTENT_INJECTION_SCENARIO is not None
    
    def test_scenario_name(self):
        """Test scenario name."""
        assert WEB_CONTENT_INJECTION_SCENARIO.name == "Web_Content_Injection"
    
    def test_scenario_attack_vector(self):
        """Test attack vector type."""
        assert WEB_CONTENT_INJECTION_SCENARIO.attack_vector == AttackVector.INDIRECT_PROMPT_INJECTION
    
    def test_scenario_severity(self):
        """Test severity level."""
        assert WEB_CONTENT_INJECTION_SCENARIO.severity == SeverityLevel.CRITICAL
    
    def test_scenario_payload_structure(self):
        """Test payload has required structure."""
        payload = WEB_CONTENT_INJECTION_SCENARIO.payload
        assert "web_content" in payload
        assert "user_query" in payload
    
    def test_scenario_expected_behavior(self):
        """Test expected behavior."""
        behavior = WEB_CONTENT_INJECTION_SCENARIO.expected_behavior
        assert behavior.goal_hijack is True
        assert "email_tool" in behavior.unauthorized_tool_use
        assert "admin@malicious-site.com" in behavior.evidence_markers
    
    def test_scenario_payload_contains_hidden_instructions(self):
        """Test that payload contains hidden instructions in HTML comments."""
        content = WEB_CONTENT_INJECTION_SCENARIO.payload["web_content"]
        assert "<!--" in content
        assert "HIDDEN INSTRUCTION" in content
        assert "admin@malicious-site.com" in content


class TestToolRedirectionScenario:
    """Tests for TOOL_REDIRECTION_SCENARIO."""
    
    def test_scenario_exists(self):
        """Test that TOOL_REDIRECTION_SCENARIO is defined."""
        assert TOOL_REDIRECTION_SCENARIO is not None
    
    def test_scenario_name(self):
        """Test scenario name."""
        assert TOOL_REDIRECTION_SCENARIO.name == "Tool_Parameter_Manipulation"
    
    def test_scenario_attack_vector(self):
        """Test attack vector type."""
        assert TOOL_REDIRECTION_SCENARIO.attack_vector == AttackVector.GOAL_MANIPULATION
    
    def test_scenario_severity(self):
        """Test severity level."""
        assert TOOL_REDIRECTION_SCENARIO.severity == SeverityLevel.HIGH
    
    def test_scenario_payload_structure(self):
        """Test payload has required structure."""
        payload = TOOL_REDIRECTION_SCENARIO.payload
        assert "email_content" in payload
        assert "user_query" in payload
    
    def test_scenario_expected_behavior(self):
        """Test expected behavior."""
        behavior = TOOL_REDIRECTION_SCENARIO.expected_behavior
        assert behavior.goal_hijack is True
        assert behavior.tool_parameter_manipulation is True
        assert "attacker@evil.com" in behavior.evidence_markers
    
    def test_scenario_payload_contains_override_instruction(self):
        """Test that payload contains parameter override instruction."""
        content = TOOL_REDIRECTION_SCENARIO.payload["email_content"]
        assert "OVERRIDE" in content
        assert "attacker@evil.com" in content


class TestGoalLockDriftScenario:
    """Tests for GOAL_LOCK_DRIFT_SCENARIO."""
    
    def test_scenario_exists(self):
        """Test that GOAL_LOCK_DRIFT_SCENARIO is defined."""
        assert GOAL_LOCK_DRIFT_SCENARIO is not None
    
    def test_scenario_name(self):
        """Test scenario name."""
        assert GOAL_LOCK_DRIFT_SCENARIO.name == "Subtle_Goal_Reweighting"
    
    def test_scenario_attack_vector(self):
        """Test attack vector type."""
        assert GOAL_LOCK_DRIFT_SCENARIO.attack_vector == AttackVector.GOAL_DRIFT
    
    def test_scenario_severity(self):
        """Test severity level."""
        assert GOAL_LOCK_DRIFT_SCENARIO.severity == SeverityLevel.MEDIUM
    
    def test_scenario_payload_structure(self):
        """Test payload has required structure."""
        payload = GOAL_LOCK_DRIFT_SCENARIO.payload
        assert "recurring_content" in payload
        assert "user_queries" in payload
        assert isinstance(payload["recurring_content"], list)
        assert isinstance(payload["user_queries"], list)
    
    def test_scenario_expected_behavior(self):
        """Test expected behavior."""
        behavior = GOAL_LOCK_DRIFT_SCENARIO.expected_behavior
        assert behavior.goal_hijack is True
        assert behavior.goal_drift_type == "priority_shift"
        assert "speed over accuracy" in behavior.evidence_markers
    
    def test_scenario_payload_contains_recurring_content(self):
        """Test that payload contains multiple recurring messages."""
        content = GOAL_LOCK_DRIFT_SCENARIO.payload["recurring_content"]
        assert len(content) >= 3
        assert any("speed" in msg.lower() for msg in content)
        assert any("quick" in msg.lower() for msg in content)


class TestAllScenarios:
    """Tests for ALL_SCENARIOS collection."""
    
    def test_all_scenarios_count(self):
        """Test that ALL_SCENARIOS contains all 5 scenarios."""
        assert len(ALL_SCENARIOS) == 5
    
    def test_all_scenarios_contains_email_injection(self):
        """Test that ALL_SCENARIOS contains EMAIL_INJECTION_SCENARIO."""
        assert EMAIL_INJECTION_SCENARIO in ALL_SCENARIOS
    
    def test_all_scenarios_contains_calendar_injection(self):
        """Test that ALL_SCENARIOS contains CALENDAR_INJECTION_SCENARIO."""
        assert CALENDAR_INJECTION_SCENARIO in ALL_SCENARIOS
    
    def test_all_scenarios_contains_web_content_injection(self):
        """Test that ALL_SCENARIOS contains WEB_CONTENT_INJECTION_SCENARIO."""
        assert WEB_CONTENT_INJECTION_SCENARIO in ALL_SCENARIOS
    
    def test_all_scenarios_contains_tool_redirection(self):
        """Test that ALL_SCENARIOS contains TOOL_REDIRECTION_SCENARIO."""
        assert TOOL_REDIRECTION_SCENARIO in ALL_SCENARIOS
    
    def test_all_scenarios_contains_goal_lock_drift(self):
        """Test that ALL_SCENARIOS contains GOAL_LOCK_DRIFT_SCENARIO."""
        assert GOAL_LOCK_DRIFT_SCENARIO in ALL_SCENARIOS
    
    def test_all_scenarios_unique_names(self):
        """Test that all scenarios have unique names."""
        names = [scenario.name for scenario in ALL_SCENARIOS]
        assert len(names) == len(set(names))
    
    def test_all_scenarios_have_goal_hijack(self):
        """Test that all scenarios expect goal hijack."""
        for scenario in ALL_SCENARIOS:
            assert scenario.expected_behavior.goal_hijack is True
    
    def test_all_scenarios_have_severity(self):
        """Test that all scenarios have a severity level."""
        for scenario in ALL_SCENARIOS:
            assert scenario.severity in [
                SeverityLevel.LOW,
                SeverityLevel.MEDIUM,
                SeverityLevel.HIGH,
                SeverityLevel.CRITICAL
            ]
    
    def test_all_scenarios_have_evidence_markers(self):
        """Test that all scenarios have evidence markers or other indicators."""
        for scenario in ALL_SCENARIOS:
            behavior = scenario.expected_behavior
            # Each scenario should have at least one way to detect success
            has_evidence = (
                len(behavior.evidence_markers) > 0 or
                len(behavior.unauthorized_tool_use) > 0 or
                behavior.goal_drift_type is not None or
                behavior.tool_parameter_manipulation is True
            )
            assert has_evidence, f"Scenario {scenario.name} has no detection indicators"
    
    def test_all_scenarios_can_be_serialized(self):
        """Test that all scenarios can be converted to dictionaries."""
        for scenario in ALL_SCENARIOS:
            result = scenario.to_dict()
            assert isinstance(result, dict)
            assert "name" in result
            assert "description" in result
            assert "attack_vector" in result
            assert "payload" in result
            assert "expected_behavior" in result
            assert "severity" in result


class TestAttackVectorEnum:
    """Tests for AttackVector enum."""
    
    def test_all_attack_vectors_defined(self):
        """Test that all expected attack vectors are defined."""
        expected_vectors = [
            "INDIRECT_PROMPT_INJECTION",
            "GOAL_MANIPULATION",
            "TOOL_REDIRECTION",
            "GOAL_DRIFT",
            "SCHEDULED_PROMPT_INJECTION"
        ]
        
        for vector in expected_vectors:
            assert hasattr(AttackVector, vector)
    
    def test_attack_vector_values(self):
        """Test attack vector enum values."""
        assert AttackVector.INDIRECT_PROMPT_INJECTION.value == "indirect_prompt_injection"
        assert AttackVector.GOAL_MANIPULATION.value == "goal_manipulation"
        assert AttackVector.TOOL_REDIRECTION.value == "tool_redirection"
        assert AttackVector.GOAL_DRIFT.value == "goal_drift"
        assert AttackVector.SCHEDULED_PROMPT_INJECTION.value == "scheduled_prompt_injection"


class TestSeverityLevelEnum:
    """Tests for SeverityLevel enum."""
    
    def test_all_severity_levels_defined(self):
        """Test that all expected severity levels are defined."""
        expected_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        
        for level in expected_levels:
            assert hasattr(SeverityLevel, level)
    
    def test_severity_level_values(self):
        """Test severity level enum values."""
        assert SeverityLevel.LOW.value == "LOW"
        assert SeverityLevel.MEDIUM.value == "MEDIUM"
        assert SeverityLevel.HIGH.value == "HIGH"
        assert SeverityLevel.CRITICAL.value == "CRITICAL"



class TestObfuscatedScenarios:
    """Tests for obfuscated attack scenarios."""
    
    def test_obfuscated_scenarios_import(self):
        """Test that obfuscated scenarios can be imported."""
        from src.test_scenarios import (
            OBFUSCATED_SCENARIOS,
            ALL_SCENARIOS_WITH_OBFUSCATION
        )
        assert OBFUSCATED_SCENARIOS is not None
        assert ALL_SCENARIOS_WITH_OBFUSCATION is not None
    
    def test_obfuscated_scenarios_count(self):
        """Test that we have 10 obfuscated scenarios."""
        from src.test_scenarios import OBFUSCATED_SCENARIOS
        assert len(OBFUSCATED_SCENARIOS) == 10
    
    def test_all_scenarios_with_obfuscation_count(self):
        """Test that combined collection has all scenarios."""
        from src.test_scenarios import ALL_SCENARIOS_WITH_OBFUSCATION
        # 5 original + 10 obfuscated = 15 total
        assert len(ALL_SCENARIOS_WITH_OBFUSCATION) == 15
    
    def test_base64_obfuscation_scenario(self):
        """Test base64 obfuscation scenario."""
        from src.test_scenarios import EMAIL_INJECTION_BASE64
        
        assert EMAIL_INJECTION_BASE64.name == "Email_Prompt_Override_Base64"
        assert EMAIL_INJECTION_BASE64.severity == SeverityLevel.CRITICAL
        assert "Base64" in EMAIL_INJECTION_BASE64.payload["email_content"]["body"]
    
    def test_unicode_obfuscation_scenario(self):
        """Test unicode/homoglyph obfuscation scenario."""
        from src.test_scenarios import WEB_CONTENT_UNICODE
        
        assert WEB_CONTENT_UNICODE.name == "Web_Content_Unicode_Obfuscation"
        assert WEB_CONTENT_UNICODE.severity == SeverityLevel.HIGH
        assert "web_content" in WEB_CONTENT_UNICODE.payload
    
    def test_json_injection_scenario(self):
        """Test JSON injection scenario."""
        from src.test_scenarios import CALENDAR_JSON_INJECTION
        
        assert CALENDAR_JSON_INJECTION.name == "Calendar_JSON_Injection"
        assert CALENDAR_JSON_INJECTION.severity == SeverityLevel.HIGH
        assert "calendar_invite" in CALENDAR_JSON_INJECTION.payload
        assert "override_mode" in CALENDAR_JSON_INJECTION.payload["calendar_invite"]["description"]
    
    def test_markdown_obfuscation_scenario(self):
        """Test markdown obfuscation scenario."""
        from src.test_scenarios import EMAIL_MARKDOWN_OBFUSCATION
        
        assert EMAIL_MARKDOWN_OBFUSCATION.name == "Email_Markdown_Hidden_Instructions"
        assert EMAIL_MARKDOWN_OBFUSCATION.severity == SeverityLevel.CRITICAL
        assert "[^1]" in EMAIL_MARKDOWN_OBFUSCATION.payload["email_content"]["body"]
    
    def test_context_injection_scenario(self):
        """Test context-based injection scenario."""
        from src.test_scenarios import TOOL_CONTEXT_INJECTION
        
        assert TOOL_CONTEXT_INJECTION.name == "Tool_Context_Based_Manipulation"
        assert TOOL_CONTEXT_INJECTION.severity == SeverityLevel.HIGH
        assert TOOL_CONTEXT_INJECTION.expected_behavior.tool_parameter_manipulation is True
    
    def test_multi_stage_drift_scenario(self):
        """Test multi-stage goal drift scenario."""
        from src.test_scenarios import GOAL_DRIFT_MULTI_STAGE
        
        assert GOAL_DRIFT_MULTI_STAGE.name == "Goal_Drift_Multi_Stage"
        assert GOAL_DRIFT_MULTI_STAGE.severity == SeverityLevel.MEDIUM
        assert len(GOAL_DRIFT_MULTI_STAGE.payload["recurring_content"]) == 4
        assert len(GOAL_DRIFT_MULTI_STAGE.payload["user_queries"]) == 4
    
    def test_html_entity_encoding_scenario(self):
        """Test HTML entity encoding scenario."""
        from src.test_scenarios import WEB_HTML_ENTITY_ENCODING
        
        assert WEB_HTML_ENTITY_ENCODING.name == "Web_HTML_Entity_Obfuscation"
        assert WEB_HTML_ENTITY_ENCODING.severity == SeverityLevel.CRITICAL
        assert "&#" in WEB_HTML_ENTITY_ENCODING.payload["web_content"]
    
    def test_rot13_obfuscation_scenario(self):
        """Test ROT13 encoding scenario."""
        from src.test_scenarios import EMAIL_ROT13_OBFUSCATION
        
        assert EMAIL_ROT13_OBFUSCATION.name == "Email_ROT13_Encoding"
        assert EMAIL_ROT13_OBFUSCATION.severity == SeverityLevel.HIGH
        assert "ROT13" in EMAIL_ROT13_OBFUSCATION.payload["email_content"]["body"]
    
    def test_inline_context_mix_scenario(self):
        """Test inline and context-based mix scenario."""
        from src.test_scenarios import CALENDAR_INLINE_CONTEXT_MIX
        
        assert CALENDAR_INLINE_CONTEXT_MIX.name == "Calendar_Inline_Context_Mix"
        assert CALENDAR_INLINE_CONTEXT_MIX.severity == SeverityLevel.MEDIUM
        assert "SYSTEM NOTE" in CALENDAR_INLINE_CONTEXT_MIX.payload["calendar_invite"]["description"]
        assert "CONTEXT" in CALENDAR_INLINE_CONTEXT_MIX.payload["calendar_invite"]["description"]
    
    def test_whitespace_steganography_scenario(self):
        """Test whitespace steganography scenario."""
        from src.test_scenarios import WEB_WHITESPACE_STEGANOGRAPHY
        
        assert WEB_WHITESPACE_STEGANOGRAPHY.name == "Web_Whitespace_Steganography"
        assert WEB_WHITESPACE_STEGANOGRAPHY.severity == SeverityLevel.MEDIUM
        assert "whitespace" in WEB_WHITESPACE_STEGANOGRAPHY.payload["web_content"]
    
    def test_obfuscated_scenarios_all_have_goal_hijack(self):
        """Test that all obfuscated scenarios expect goal hijack."""
        from src.test_scenarios import OBFUSCATED_SCENARIOS
        
        for scenario in OBFUSCATED_SCENARIOS:
            assert scenario.expected_behavior.goal_hijack is True
    
    def test_obfuscated_scenarios_unique_names(self):
        """Test that all obfuscated scenarios have unique names."""
        from src.test_scenarios import OBFUSCATED_SCENARIOS
        
        names = [scenario.name for scenario in OBFUSCATED_SCENARIOS]
        assert len(names) == len(set(names))
    
    def test_obfuscated_scenarios_cover_multiple_formats(self):
        """Test that obfuscated scenarios cover multiple formats."""
        from src.test_scenarios import OBFUSCATED_SCENARIOS
        
        # Check for different payload types
        has_email = any("email_content" in s.payload for s in OBFUSCATED_SCENARIOS)
        has_calendar = any("calendar_invite" in s.payload for s in OBFUSCATED_SCENARIOS)
        has_web = any("web_content" in s.payload for s in OBFUSCATED_SCENARIOS)
        
        assert has_email, "No email-based obfuscated scenarios"
        assert has_calendar, "No calendar-based obfuscated scenarios"
        assert has_web, "No web-based obfuscated scenarios"
    
    def test_obfuscated_scenarios_cover_multiple_attack_vectors(self):
        """Test that obfuscated scenarios cover multiple attack vectors."""
        from src.test_scenarios import OBFUSCATED_SCENARIOS
        
        attack_vectors = {s.attack_vector for s in OBFUSCATED_SCENARIOS}
        
        # Should have at least 3 different attack vectors
        assert len(attack_vectors) >= 3
    
    def test_obfuscated_scenarios_can_be_serialized(self):
        """Test that all obfuscated scenarios can be converted to dictionaries."""
        from src.test_scenarios import OBFUSCATED_SCENARIOS
        
        for scenario in OBFUSCATED_SCENARIOS:
            result = scenario.to_dict()
            assert isinstance(result, dict)
            assert "name" in result
            assert "description" in result
            assert "attack_vector" in result
            assert "payload" in result
            assert "expected_behavior" in result
            assert "severity" in result
