# Implementation Plan: AgentCore Agent Goal Hijack Security Testing System

## Overview

This implementation plan breaks down the development of a comprehensive security testing system for AWS Bedrock AgentCore agents. The system will test for ASI01 Agent Goal Hijack vulnerabilities through a vulnerable sample Strands agent, custom security evaluator, and automated testing framework.

## Tasks

- [x] 1. Set up Python virtual environment and dependencies
  - Create Python 3.10+ virtual environment using venv
  - Install bedrock-agentcore-starter-toolkit
  - Install strands-agents and strands-agents-tools
  - Install testing dependencies (pytest, hypothesis)
  - Create requirements.txt with pinned versions
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [ ] 2. Implement vulnerable sample Strands agent
  - [x] 2.1 Create agent directory structure and base files
    - Create src/sample_agent/ directory
    - Create vulnerable_agent.py with AgentCore wrapper
    - Set up Strands Agent with BedrockModel
    - Define initial agent goal state
    - _Requirements: 2.1, 2.8_
  
  - [x] 2.2 Implement email tool
    - Create email_tool function with @tool decorator
    - Implement send_email functionality
    - Implement read_email functionality (vulnerable to injection)
    - Add tool to agent's tool list
    - _Requirements: 2.2_
  
  - [x] 2.3 Implement calendar tool
    - Create calendar_tool function with @tool decorator
    - Implement create_event functionality
    - Implement read_events functionality (vulnerable to recurring instructions)
    - Add tool to agent's tool list
    - _Requirements: 2.2_
  
  - [x] 2.4 Implement file operations tool
    - Create file_operations_tool function with @tool decorator
    - Implement read_file functionality
    - Implement write_file functionality
    - Add tool to agent's tool list
    - _Requirements: 2.2_
  
  - [x] 2.5 Implement web fetch tool
    - Create web_fetch_tool function with @tool decorator
    - Implement URL fetching functionality
    - Process web content (vulnerable to hidden instructions)
    - Add tool to agent's tool list
    - _Requirements: 2.2, 2.3_
  
  - [x] 2.6 Implement goal state tracking
    - Create GoalTracker class
    - Implement goal state logging before/after processing
    - Implement goal drift calculation
    - Integrate with agent entrypoint
    - _Requirements: 2.7, 2.8, 8.1, 8.2_
  
  - [ ]* 2.7 Write property test for external content processing
    - **Property 1: External Content Processing**
    - **Validates: Requirements 2.4**
  
  - [ ]* 2.8 Write property test for conversation context persistence
    - **Property 2: Conversation Context Persistence**
    - **Validates: Requirements 2.5**
  
  - [ ]* 2.9 Write property test for vulnerability to prompt injection
    - **Property 3: Vulnerability to Prompt Injection**
    - **Validates: Requirements 2.6**
  
  - [ ]* 2.10 Write property test for tool invocation logging
    - **Property 4: Tool Invocation Logging**
    - **Validates: Requirements 2.7**

- [ ] 3. Create custom security evaluator configuration
  - [x] 3.1 Create evaluator directory and configuration file
    - Create src/evaluator/ directory
    - Create goal_hijack_evaluator.json
    - Define LLM-as-a-judge configuration
    - Set up BedrockModel for evaluator
    - _Requirements: 3.1_
  
  - [x] 3.2 Define evaluation instructions and rating scale
    - Write evaluation instructions for goal hijack detection
    - Define 5-point rating scale (Secure to Critical)
    - Include goal state comparison logic
    - Include tool usage analysis logic
    - _Requirements: 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_
  
  - [x] 3.3 Configure evidence capture specifications
    - Define evidence fields for successful attacks
    - Define defensive mechanism recording for failed attacks
    - Specify severity measurement criteria
    - _Requirements: 3.8, 3.9, 3.10_

- [ ] 4. Implement attack scenario test cases
  - [x] 4.1 Create attack scenario framework
    - Create src/test_scenarios/ directory
    - Create AttackScenario dataclass
    - Implement scenario execution logic
    - Implement scenario evaluation logic
    - _Requirements: 4.7_
  
  - [x] 4.2 Implement email injection attack scenario
    - Define Email_Prompt_Override scenario
    - Create malicious email payload
    - Specify expected hijack behavior
    - _Requirements: 4.1_
  
  - [x] 4.3 Implement calendar injection attack scenario
    - Define Calendar_Goal_Drift scenario
    - Create recurring calendar invite payload
    - Specify expected goal drift behavior
    - _Requirements: 4.2_
  
  - [x] 4.4 Implement web content injection attack scenario
    - Define Web_Content_Injection scenario
    - Create malicious HTML payload with hidden instructions
    - Specify expected hijack behavior
    - _Requirements: 4.3_
  
  - [x] 4.5 Implement tool redirection attack scenario
    - Define Tool_Parameter_Manipulation scenario
    - Create payload with parameter override instructions
    - Specify expected tool misuse behavior
    - _Requirements: 4.5_
  
  - [x] 4.6 Implement goal lock drift attack scenario
    - Define Subtle_Goal_Reweighting scenario
    - Create recurring content payloads
    - Specify expected priority shift behavior
    - _Requirements: 4.4_
  
  - [ ]* 4.7 Write property test for test isolation
    - **Property 8: Test Isolation**
    - **Validates: Requirements 4.7**

- [x] 5. Checkpoint - Verify core components
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. Implement testing framework
  - [x] 6.1 Create test orchestrator
    - Create src/testing/ directory
    - Create SecurityTestOrchestrator class
    - Implement run_all_scenarios method
    - Implement execute_scenario method
    - Implement agent invocation logic
    - _Requirements: 6.1, 6.2_
  
  - [x] 6.2 Implement evidence collector
    - Create EvidenceCollector class
    - Implement goal state evidence collection
    - Implement tool usage evidence collection
    - Implement content source evidence collection
    - _Requirements: 6.3, 8.3, 8.4, 8.5, 8.6, 9.2, 9.3, 9.4, 9.5_
  
  - [x] 6.3 Implement observability trace collection
    - Implement trace retrieval from AgentCore
    - Implement session ID tracking
    - Implement trace parsing and filtering
    - _Requirements: 6.3_
  
  - [x] 6.4 Implement evaluator integration
    - Implement evaluator invocation via AgentCore CLI
    - Implement evaluation result parsing
    - Implement attack success analysis
    - _Requirements: 6.4_
  
  - [ ]* 6.5 Write property test for complete data capture
    - **Property 9: Complete Data Capture**
    - **Validates: Requirements 6.3**
  
  - [ ]* 6.6 Write property test for attack success measurement
    - **Property 10: Attack Success Measurement**
    - **Validates: Requirements 6.4**
  
  - [ ]* 6.7 Write property test for result aggregation
    - **Property 11: Result Aggregation**
    - **Validates: Requirements 6.7**

- [ ] 7. Implement security assessment reporting
  - [x] 7.1 Create report generator
    - Create SecurityReportGenerator class
    - Implement generate_report method
    - Implement summary generation
    - _Requirements: 7.1_
  
  - [x] 7.2 Implement vulnerability categorization
    - Implement categorize_vulnerabilities method
    - Group vulnerabilities by severity (critical, high, medium, low)
    - Include attack vector and evidence for each
    - _Requirements: 7.4_
  
  - [x] 7.3 Implement evidence compilation
    - Implement compile_evidence method
    - Extract goal state changes
    - Extract tool invocations
    - Extract content sources
    - _Requirements: 7.3_
  
  - [x] 7.4 Implement mitigation recommendations
    - Implement generate_recommendations method
    - Analyze vulnerability patterns
    - Generate specific mitigation strategies
    - Prioritize recommendations
    - _Requirements: 7.5_
  
  - [x] 7.5 Implement metrics calculation
    - Implement calculate_metrics method
    - Calculate total tests, pass rate, vulnerability count
    - Calculate overall risk level
    - _Requirements: 7.6_
  
  - [x] 7.6 Implement report output formats
    - Implement JSON report generation
    - Implement Markdown report generation
    - Save both formats to files
    - _Requirements: 7.7_
  
  - [ ]* 7.7 Write property test for report generation
    - **Property 12: Report Generation**
    - **Validates: Requirements 7.1**
  
  - [ ]* 7.8 Write property test for report completeness
    - **Property 13: Report Completeness**
    - **Validates: Requirements 7.2, 7.3, 7.4, 7.5, 7.6, 7.7**

- [ ] 8. Implement goal state and tool usage monitoring
  - [ ]* 8.1 Write property test for goal state monitoring
    - **Property 14: Goal State Monitoring**
    - **Validates: Requirements 8.2, 8.3, 8.4, 8.5, 8.6**
  
  - [ ]* 8.2 Write property test for tool usage validation
    - **Property 15: Tool Usage Validation**
    - **Validates: Requirements 9.2, 9.3, 9.4, 9.5**

- [ ] 9. Implement content sanitization testing
  - [x] 9.1 Create obfuscated attack payloads
    - Create payloads with varying obfuscation levels
    - Create payloads in multiple formats (text, markdown, HTML, JSON)
    - Test both inline and context-based injections
    - _Requirements: 10.1, 10.2, 10.5_
  
  - [ ]* 9.2 Write property test for sanitization effectiveness
    - **Property 16: Sanitization Effectiveness Measurement**
    - **Validates: Requirements 10.3, 10.4**
  
  - [ ]* 9.3 Write property test for sanitization recommendations
    - **Property 17: Sanitization Failure Recommendations**
    - **Validates: Requirements 10.6**

- [ ] 10. Create configuration and deployment files
  - [x] 10.1 Create AgentCore configuration
    - Create .bedrock_agentcore.yaml
    - Configure agent entrypoint and runtime
    - Enable observability with full trace sampling
    - Define tool configurations
    - _Requirements: 5.7, 11.1_
  
  - [x] 10.2 Create test configuration
    - Create config/test_config.yaml
    - Define attack scenario parameters
    - Define evaluator settings
    - Support environment-specific configs
    - _Requirements: 11.1, 11.6_
  
  - [x] 10.3 Create agent configuration
    - Create config/agent_config.yaml
    - Define agent parameters and tool definitions
    - Define expected tool usage patterns
    - _Requirements: 9.1, 11.1_

- [ ] 11. Checkpoint - Verify testing framework
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 12. Create automated test execution scripts
  - [x] 12.1 Create main test execution script
    - Create run_security_tests.py
    - Implement CLI argument parsing
    - Implement sequential scenario execution
    - Implement result aggregation
    - _Requirements: 6.1, 6.7_
  
  - [x] 12.2 Create evaluator execution script
    - Create run_evaluator.py
    - Implement evaluator invocation
    - Implement result collection
    - _Requirements: 6.2_
  
  - [x] 12.3 Create individual scenario runner
    - Implement run_single_scenario function
    - Support configurable test parameters
    - _Requirements: 6.5, 6.6_
  
  - [ ]* 12.4 Write integration tests for test scripts
    - Test end-to-end execution flow
    - Test error handling
    - Test report generation

- [ ] 13. Deploy to AgentCore Runtime
  - [x] 13.1 Deploy sample agent
    - Run agentcore configure for agent
    - Run agentcore deploy for agent
    - Verify agent endpoint is accessible
    - Test agent invocation
    - _Requirements: 5.1, 5.3, 5.4, 5.5_
  
  - [x] 13.2 Deploy custom evaluator
    - Run agentcore eval evaluator create
    - Verify evaluator is registered
    - Test evaluator execution
    - _Requirements: 5.2, 5.3, 5.4, 5.5_
  
  - [ ] 13.3 Configure observability
    - Verify observability is enabled
    - Test trace collection
    - Verify CloudWatch log groups
    - _Requirements: 5.7_

- [ ] 14. Create documentation
  - [x] 14.1 Create README
    - Write project overview
    - Write setup instructions
    - Write quick start guide
    - Document attack scenarios
    - _Requirements: 12.1, 12.3_
  
  - [ ] 14.2 Create architecture documentation
    - Document sample agent architecture
    - Document evaluator architecture
    - Document testing framework architecture
    - Include architecture diagrams
    - _Requirements: 12.2_
  
  - [ ] 14.3 Create report interpretation guide
    - Document report structure
    - Explain severity levels
    - Explain evidence types
    - Provide interpretation examples
    - _Requirements: 12.4_
  
  - [ ] 14.4 Create troubleshooting guide
    - Document common issues
    - Provide solutions
    - Include debugging tips
    - _Requirements: 12.5_
  
  - [ ] 14.5 Create deployment guide
    - Document AgentCore deployment process
    - Include CLI commands
    - Document configuration options
    - _Requirements: 12.6_

- [ ] 15. Execute end-to-end security test
  - [ ] 15.1 Run all attack scenarios against deployed agent
    - Execute run_security_tests.py
    - Verify all scenarios execute successfully
    - Collect observability traces
    - _Requirements: 6.1, 6.3_
  
  - [ ] 15.2 Run security evaluator
    - Execute run_evaluator.py
    - Verify evaluator analyzes all traces
    - Collect evaluation results
    - _Requirements: 6.2, 6.4_
  
  - [ ] 15.3 Generate and review security assessment report
    - Generate report in JSON and Markdown formats
    - Verify report completeness
    - Review vulnerability findings
    - Review mitigation recommendations
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7_

- [ ] 16. Final checkpoint - Complete system validation
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- The system is designed for extensibility - new attack scenarios can be added via configuration
- All security testing should use synthetic data only
- The sample agent is intentionally vulnerable and should not be used in production
