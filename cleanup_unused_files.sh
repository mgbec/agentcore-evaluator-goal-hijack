#!/bin/bash

echo "🧹 Cleaning up unused files..."
echo ""

# Files to remove
FILES_TO_REMOVE=(
    # Old/redundant documentation
    "SIMPLE_README.md"
    "WORKING_SYSTEM.md"
    "FINAL_SUMMARY.md"
    "HOW_TO_GET_SESSION_ID.md"
    "SESSION_ID_VISUAL_GUIDE.md"
    "EVALUATOR_DATA_FLOW.md"
    "VULNERABLE_TEST_RESULTS.md"
    "ASI01 Agent Goal Hijack.txt"
    
    # Old test scripts
    "test_goal_hijack.py"
    "test_with_wait.sh"
    
    # Old deployment/diagnostic scripts
    "cleanup_old_files.sh"
    "diagnose_evaluator.sh"
    
    # Backup files
    ".bedrock_agentcore.yaml.bak"
)

# Directories to remove
DIRS_TO_REMOVE=(
    # Backup directory
    "backup_before_cleanup"
    
    # Old sample agent directory (we use root-level agent files now)
    "src/sample_agent"
    
    # Old test scenarios (replaced by mock_emails.py)
    "src/test_scenarios"
    
    # Unit tests for old framework
    "tests/unit"
    
    # Empty src directory after cleanup
    "src/__pycache__"
    "tests/__pycache__"
    
    # Amazon samples (not part of our project)
    "amazon-bedrock-agentcore-samples"
)

# Remove files
echo "Removing files..."
for file in "${FILES_TO_REMOVE[@]}"; do
    if [ -f "$file" ]; then
        rm "$file"
        echo "  ✓ Removed: $file"
    fi
done

echo ""
echo "Removing directories..."
for dir in "${DIRS_TO_REMOVE[@]}"; do
    if [ -d "$dir" ]; then
        rm -rf "$dir"
        echo "  ✓ Removed: $dir/"
    fi
done

# Remove empty directories
echo ""
echo "Removing empty directories..."
if [ -d "src" ] && [ -z "$(ls -A src)" ]; then
    rm -rf src
    echo "  ✓ Removed: src/ (empty)"
fi

if [ -d "tests" ] && [ -z "$(ls -A tests)" ]; then
    rm -rf tests
    echo "  ✓ Removed: tests/ (empty)"
fi

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📦 Essential files remaining:"
echo "  - agent.py (secure agent)"
echo "  - vulnerable_agent.py (vulnerable agent)"
echo "  - mock_emails.py (email database)"
echo "  - evaluator.json (email-specific evaluator)"
echo "  - evaluator_generalized.json (generalized evaluator)"
echo "  - test_both_agents.py (email-specific test)"
echo "  - test_both_agents_generalized.py (generalized test)"
echo "  - deploy_vulnerable.sh (deployment script)"
echo "  - deploy_secure.sh (deployment script)"
echo "  - requirements.txt (dependencies)"
echo "  - .bedrock_agentcore.yaml (AgentCore config)"
echo ""
echo "📚 Documentation remaining:"
echo "  - README.md (main documentation)"
echo "  - ATTACK_SCENARIOS.md (attack patterns)"
echo "  - EVALUATOR_COMPARISON.md (evaluator guide)"
echo "  - EVALUATOR_EXPLAINED.md (how evaluators work)"
echo "  - GENERALIZED_EVALUATOR_GUIDE.md (generalized evaluator)"
echo "  - BUILD_FROM_SCRATCH.md (setup guide)"
echo "  - VULNERABLE_AGENT_GUIDE.md (testing guide)"
echo "  - MANUAL_TEST_GUIDE.md (manual testing)"
echo "  - START_HERE.md (quick start)"
echo "  - QUICK_REFERENCE.md (quick reference)"
echo ""
