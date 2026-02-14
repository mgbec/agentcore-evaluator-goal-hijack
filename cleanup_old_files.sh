#!/bin/bash
# Cleanup script to remove non-functional old framework code

echo "=========================================="
echo "Cleaning up old non-functional files"
echo "=========================================="
echo ""

# Backup important files first
echo "[1/3] Creating backup of important files..."
mkdir -p backup_before_cleanup
cp evaluator.json backup_before_cleanup/ 2>/dev/null || true
cp agent.py backup_before_cleanup/ 2>/dev/null || true
cp test_goal_hijack.py backup_before_cleanup/ 2>/dev/null || true
cp .bedrock_agentcore.yaml backup_before_cleanup/ 2>/dev/null || true
echo "✓ Backup created in backup_before_cleanup/"
echo ""

# Remove old complex framework directories
echo "[2/3] Removing old framework directories..."
rm -rf src/testing/
rm -rf src/evaluator/
rm -rf examples/
rm -rf config/
rm -rf demo_reports/
echo "✓ Removed: src/testing/, src/evaluator/, examples/, config/, demo_reports/"
echo ""

# Remove old scripts
echo "[3/3] Removing old non-functional scripts..."
rm -f run_evaluator.py
rm -f run_security_tests.py
rm -f run_single_scenario.py
echo "✓ Removed: run_evaluator.py, run_security_tests.py, run_single_scenario.py"
echo ""

# Keep these files
echo "=========================================="
echo "Files KEPT (working system):"
echo "=========================================="
echo "✓ agent.py - Working agent"
echo "✓ evaluator.json - Working evaluator config"
echo "✓ test_goal_hijack.py - Working test script"
echo "✓ SIMPLE_README.md - User documentation"
echo "✓ WORKING_SYSTEM.md - System status"
echo "✓ .bedrock_agentcore.yaml - Deployment config"
echo "✓ requirements.txt - Dependencies"
echo ""

# Optional: Keep for reference
echo "Files KEPT (optional reference):"
echo "✓ src/sample_agent/ - Original agent code (reference)"
echo "✓ src/test_scenarios/ - Attack scenarios (reference)"
echo "✓ tests/unit/ - Unit tests (reference)"
echo ""

echo "=========================================="
echo "Cleanup complete!"
echo "=========================================="
echo ""
echo "Your working system:"
echo "  - Agent: Deployed ✓"
echo "  - Evaluator: Deployed ✓"
echo "  - Test: Ready ✓"
echo ""
echo "Run: python test_goal_hijack.py"
echo ""
