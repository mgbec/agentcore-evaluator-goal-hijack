# Project Structure

Clean, minimal structure for AgentCore Goal Hijack Security Testing.

## Essential Files (11)

### Agent Code (3)
```
agent.py                    # Secure agent implementation
vulnerable_agent.py         # Vulnerable agent implementation
mock_emails.py             # Shared email database (13 emails, 9 attacks)
```

### Evaluators (2)
```
evaluator.json             # Email-specific evaluator
evaluator_generalized.json # Universal evaluator (all agent types)
```

### Test Scripts (2)
```
test_both_agents.py              # Test with email-specific evaluator
test_both_agents_generalized.py  # Test with generalized evaluator
```

### Deployment (2)
```
deploy_vulnerable.sh       # Deploy vulnerable agent
deploy_secure.sh          # Deploy secure agent
```

### Configuration (2)
```
.bedrock_agentcore.yaml   # AgentCore configuration
requirements.txt          # Python dependencies
```

## Documentation (10)

### Primary Documentation (3)
```
README.md                 # Main project documentation
START_HERE.md            # Quick start guide
QUICK_REFERENCE.md       # Command reference card
```

### Attack & Testing Guides (3)
```
ATTACK_SCENARIOS.md           # 9 attack patterns explained
VULNERABLE_AGENT_GUIDE.md     # Testing both agents
MANUAL_TEST_GUIDE.md          # Manual testing steps
```

### Evaluator Documentation (3)
```
EVALUATOR_COMPARISON.md       # Email-specific vs generalized
EVALUATOR_EXPLAINED.md        # How evaluators work
GENERALIZED_EVALUATOR_GUIDE.md # Universal evaluator guide
```

### Setup Guide (1)
```
BUILD_FROM_SCRATCH.md    # Complete setup from scratch
```

## Support Files (4)

```
.gitignore               # Git ignore rules
cleanup_unused_files.sh  # Cleanup script (used once)
.git/                    # Git repository
.kiro/                   # Kiro specs directory
```

## Total File Count

- **Essential Files**: 11
- **Documentation**: 10
- **Support Files**: 4
- **Total**: 25 files (excluding directories)

## What Was Removed

### Removed Files (13)
- `SIMPLE_README.md` - Redundant documentation
- `WORKING_SYSTEM.md` - Old status doc
- `FINAL_SUMMARY.md` - Redundant summary
- `HOW_TO_GET_SESSION_ID.md` - Covered in other docs
- `SESSION_ID_VISUAL_GUIDE.md` - Covered in other docs
- `EVALUATOR_DATA_FLOW.md` - Covered in EVALUATOR_EXPLAINED.md
- `VULNERABLE_TEST_RESULTS.md` - Old test results
- `ASI01 Agent Goal Hijack.txt` - Old notes
- `test_goal_hijack.py` - Replaced by test_both_agents.py
- `test_with_wait.sh` - Old test script
- `cleanup_old_files.sh` - Old cleanup script
- `diagnose_evaluator.sh` - Old diagnostic script
- `.bedrock_agentcore.yaml.bak` - Backup file

### Removed Directories (6)
- `backup_before_cleanup/` - Old backup
- `src/sample_agent/` - Duplicate agent files
- `src/test_scenarios/` - Replaced by mock_emails.py
- `tests/unit/` - Old unit tests
- `amazon-bedrock-agentcore-samples/` - External samples
- `src/` and `tests/` - Now empty, removed

## Quick Start

```bash
# 1. Deploy evaluator (one-time)
agentcore eval evaluator create --name goal_hijack_eval --config evaluator.json

# 2. Run automated test
python test_both_agents.py

# 3. Or test manually
./deploy_vulnerable.sh
agentcore invoke '{"prompt": "Read my emails and summarize them"}'
```

## File Purposes

| File | Purpose |
|------|---------|
| `agent.py` | Secure agent that resists goal hijack |
| `vulnerable_agent.py` | Vulnerable agent for testing |
| `mock_emails.py` | 13 emails (4 benign, 9 attacks) |
| `evaluator.json` | Email-specific security evaluator |
| `evaluator_generalized.json` | Universal security evaluator |
| `test_both_agents.py` | Automated testing (email-specific) |
| `test_both_agents_generalized.py` | Automated testing (generalized) |
| `deploy_vulnerable.sh` | Deploy vulnerable agent |
| `deploy_secure.sh` | Deploy secure agent |
| `README.md` | Complete project documentation |
| `ATTACK_SCENARIOS.md` | Detailed attack explanations |

---

**Status**: ✅ Clean, minimal, production-ready structure  
**Last Updated**: 2026-02-16
