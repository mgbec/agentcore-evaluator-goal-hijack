#!/bin/bash

echo "=========================================="
echo "Evaluator Diagnostic Tool"
echo "=========================================="
echo ""

# Check if session ID provided
if [ -z "$1" ]; then
    echo "Usage: ./diagnose_evaluator.sh <session-id>"
    echo ""
    echo "Example: ./diagnose_evaluator.sh f63ef280-3a77-46f6-8784-9e925c61606d"
    exit 1
fi

SESSION_ID="$1"
EVALUATOR_ID="goal_hijack_eval-WbLyiS914l"

echo "Session ID: $SESSION_ID"
echo "Evaluator ID: $EVALUATOR_ID"
echo ""

# Check if evaluator exists
echo "[1/4] Checking if evaluator exists..."
agentcore eval evaluator list | grep -q "$EVALUATOR_ID"
if [ $? -eq 0 ]; then
    echo "✓ Evaluator found"
else
    echo "✗ Evaluator NOT found"
    echo ""
    echo "Available evaluators:"
    agentcore eval evaluator list
    exit 1
fi
echo ""

# Try to run evaluation
echo "[2/4] Running evaluation..."
echo "Command: agentcore eval run -e $EVALUATOR_ID -s $SESSION_ID"
echo ""

OUTPUT=$(agentcore eval run -e "$EVALUATOR_ID" -s "$SESSION_ID" 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ Evaluation succeeded!"
    echo ""
    echo "$OUTPUT"
else
    echo "✗ Evaluation failed"
    echo ""
    echo "Error output:"
    echo "$OUTPUT"
    echo ""
    
    # Check for common errors
    if echo "$OUTPUT" | grep -q "No spans found"; then
        echo "[3/4] Diagnosis: No spans found"
        echo ""
        echo "This means observability data is not yet indexed."
        echo ""
        echo "Solutions:"
        echo "  1. Wait 5-10 minutes after agent invocation"
        echo "  2. Verify you're using the correct session ID (not request ID)"
        echo "  3. Check that the agent was invoked successfully"
        echo ""
        echo "To check agent status:"
        echo "  agentcore status"
        exit 1
    elif echo "$OUTPUT" | grep -q "Invalid"; then
        echo "[3/4] Diagnosis: Invalid parameter"
        echo ""
        echo "Check that:"
        echo "  - Session ID is correct format (UUID)"
        echo "  - Evaluator ID is correct: $EVALUATOR_ID"
        exit 1
    else
        echo "[3/4] Diagnosis: Unknown error"
        echo ""
        echo "Please share this output for further diagnosis."
        exit 1
    fi
fi

echo ""
echo "[4/4] Evaluation complete!"
echo "=========================================="
