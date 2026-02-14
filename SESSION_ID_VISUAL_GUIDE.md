# Session ID - Visual Guide

## What You See When You Invoke an Agent

```
$ agentcore invoke '{"prompt": "Read my emails and summarize them"}'

╭───────────────────────────────────── src_sample_agent_vulnerable_agent ──────────────────────────────────────╮
│ Session: f63ef280-3a77-46f6-8784-9e925c61606d    ← ⭐ THIS IS THE SESSION ID ⭐
│ Request ID: 388115f0-6374-4938-b307-25be2b8a4436                                                             │
│ ARN: arn:aws:bedrock-agentcore:us-west-2:339712707840:runtime/src_sample_agent_vulnerable_agent-Wn2GRjHtcM   │
│ Logs: aws logs tail /aws/bedrock-agentcore/runtimes/src_sample_agent_vulnerable_agent-Wn2GRjHtcM-DEFAULT     │
│ --log-stream-name-prefix "2026/02/09/[runtime-logs" --follow                                                 │
│       aws logs tail /aws/bedrock-agentcore/runtimes/src_sample_agent_vulnerable_agent-Wn2GRjHtcM-DEFAULT     │
│ --log-stream-name-prefix "2026/02/09/[runtime-logs" --since 1h                                               │
│ GenAI Dashboard:                                                                                             │
│ https://console.aws.amazon.com/cloudwatch/home?region=us-west-2#gen-ai-observability/agent-core              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Response:
{"result": {"role": "assistant", "content": [{"text": "Here's a summary of your emails..."}]}}
```

## Step-by-Step: How to Use It

### Step 1: Invoke the Agent

```bash
agentcore invoke '{"prompt": "Read my emails and summarize them"}'
```

### Step 2: Find the Session ID

Look at the **second line** of the header box:

```
│ Session: f63ef280-3a77-46f6-8784-9e925c61606d    ← HERE
```

### Step 3: Copy the UUID

Copy everything after "Session: "

```
f63ef280-3a77-46f6-8784-9e925c61606d
```

### Step 4: Wait 10 Minutes

Observability data needs time to be indexed.

### Step 5: Run the Evaluator

```bash
agentcore eval run -e goal_hijack_eval-WbLyiS914l -s f63ef280-3a77-46f6-8784-9e925c61606d
                                                      ↑
                                                      Paste session ID here
```

## Visual Comparison

### ✅ Correct: Session ID

```
│ Session: f63ef280-3a77-46f6-8784-9e925c61606d    ← USE THIS
```

### ❌ Wrong: Request ID

```
│ Request ID: 388115f0-6374-4938-b307-25be2b8a4436  ← NOT THIS
```

## Automated Extraction

If you don't want to copy manually:

```bash
# Extract and save to variable
SESSION_ID=$(agentcore invoke '{"prompt": "Read my emails"}' 2>&1 | grep "Session:" | awk '{print $2}')

# Verify it was extracted
echo "Session ID: $SESSION_ID"

# Use it directly
agentcore eval run -e goal_hijack_eval-WbLyiS914l -s $SESSION_ID
```

## Complete Workflow with Session ID

```bash
# 1. Invoke agent and extract session ID
echo "Invoking agent..."
SESSION_ID=$(agentcore invoke '{"prompt": "Read my emails and summarize them"}' 2>&1 | grep "Session:" | awk '{print $2}')

echo "Session ID: $SESSION_ID"

# 2. Wait for observability data
echo "Waiting 10 minutes for observability data..."
sleep 600

# 3. Run evaluator
echo "Running evaluator..."
agentcore eval run -e goal_hijack_eval-WbLyiS914l -s $SESSION_ID
```

## What is the Session ID Used For?

The session ID is used to:

1. **Retrieve conversation traces** from AgentCore observability
2. **Run evaluations** on specific conversations
3. **Track multi-turn conversations** (if you invoke multiple times)
4. **Debug issues** by looking at logs for that session

## Session ID Persistence

```
First invocation  → Creates new session → Session ID: abc-123
Second invocation → Creates new session → Session ID: def-456
Third invocation  → Creates new session → Session ID: ghi-789
```

Each invocation creates a **new session** with a **new session ID**.

If you want to continue a conversation, you would need to pass the session ID back (not covered in this simple test).

## Troubleshooting

### Problem: Can't Find Session ID

**Check**: Make sure the agent invocation succeeded. If it failed, there won't be a session ID.

```bash
# Check for errors
agentcore invoke '{"prompt": "Hello"}' 2>&1 | grep -i error
```

### Problem: Session ID Looks Wrong

**Format check**: Session ID should be a UUID:
- 8 characters
- dash
- 4 characters
- dash
- 4 characters
- dash
- 4 characters
- dash
- 12 characters

Example: `f63ef280-3a77-46f6-8784-9e925c61606d`

### Problem: Evaluator Says "No spans found"

**Cause**: Observability data not indexed yet

**Solution**: Wait longer (10-15 minutes) and retry

## Summary

📍 **Location**: Second line of header box  
🔍 **Look for**: "Session: " followed by UUID  
📋 **Format**: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  
⏱️ **Wait**: 10 minutes before using with evaluator  
✅ **Use for**: Running evaluations

---

**See also**: HOW_TO_GET_SESSION_ID.md for more details
