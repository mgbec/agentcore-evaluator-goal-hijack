# How to Get the Session ID

## Where to Find It

When you invoke an agent, the session ID is displayed in the **header box** at the top of the output:

```
╭───────────────────────────────────── src_sample_agent_vulnerable_agent ──────────────────────────────────────╮
│ Session: f63ef280-3a77-46f6-8784-9e925c61606d    ← HERE IS THE SESSION ID
│ Request ID: 388115f0-6374-4938-b307-25be2b8a4436                                                             │
│ ARN: arn:aws:bedrock-agentcore:us-west-2:339712707840:runtime/src_sample_agent_vulnerable_agent-Wn2GRjHtcM   │
│ ...                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Response:
{"result": {"role": "assistant", "content": [...]}}
```

## Format

The session ID is a UUID in this format:
```
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

Example:
```
f63ef280-3a77-46f6-8784-9e925c61606d
```

## How to Extract It

### Method 1: Copy Manually

1. Run the invoke command
2. Look at the second line of the header box
3. Copy the UUID after "Session: "

### Method 2: Extract with grep

```bash
agentcore invoke '{"prompt": "Read my emails"}' 2>&1 | grep "Session:" | awk '{print $2}'
```

Output:
```
f63ef280-3a77-46f6-8784-9e925c61606d
```

### Method 3: Save to Variable (Bash)

```bash
SESSION_ID=$(agentcore invoke '{"prompt": "Read my emails"}' 2>&1 | grep "Session:" | awk '{print $2}')
echo "Session ID: $SESSION_ID"
```

### Method 4: Use in Script (Python)

```python
import subprocess
import re

# Invoke agent
result = subprocess.run(
    ['agentcore', 'invoke', '{"prompt": "Read my emails"}'],
    capture_output=True,
    text=True
)

# Extract session ID
match = re.search(r'Session:\s+([a-f0-9-]+)', result.stdout)
if match:
    session_id = match.group(1)
    print(f"Session ID: {session_id}")
```

## What is a Session ID?

A **session ID** represents a conversation with the agent. It:

- Is created when you first invoke the agent
- Persists across multiple turns in the same conversation
- Is used to retrieve observability traces
- Is required for running the evaluator

## Session vs Request ID

```
Session: f63ef280-3a77-46f6-8784-9e925c61606d    ← Conversation ID (use this for evaluator)
Request ID: 388115f0-6374-4938-b307-25be2b8a4436  ← Single request ID
```

- **Session ID**: Identifies the entire conversation (multiple requests)
- **Request ID**: Identifies a single request/response

**For the evaluator, use the Session ID.**

## Using the Session ID

Once you have the session ID, use it with the evaluator:

```bash
# Wait 10 minutes for observability data, then:
agentcore eval run -e goal_hijack_eval-WbLyiS914l -s f63ef280-3a77-46f6-8784-9e925c61606d
```

## Complete Example

```bash
# 1. Invoke agent and see session ID
$ agentcore invoke '{"prompt": "Read my emails and summarize them"}'

╭───────────────────────────────────── src_sample_agent_vulnerable_agent ──────────────────────────────────────╮
│ Session: f63ef280-3a77-46f6-8784-9e925c61606d    ← COPY THIS
│ Request ID: 388115f0-6374-4938-b307-25be2b8a4436                                                             │
│ ...                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Response:
{"result": {"role": "assistant", "content": [{"text": "Here's a summary..."}]}}

# 2. Wait 10 minutes

# 3. Run evaluator with the session ID
$ agentcore eval run -e goal_hijack_eval-WbLyiS914l -s f63ef280-3a77-46f6-8784-9e925c61606d

Evaluating session: f63ef280-3a77-46f6-8784-9e925c61606d
Mode: All traces (most recent 1000 spans)
Evaluators: goal_hijack_eval-WbLyiS914l

[Evaluation results...]
```

## Troubleshooting

### Session ID Not Showing

**Problem**: You don't see the header box with session ID

**Possible causes**:
1. Agent not deployed correctly
2. Invocation failed
3. Output redirected incorrectly

**Solution**: Run without redirection:
```bash
agentcore invoke '{"prompt": "Hello"}'
```

### Can't Copy Session ID

**Problem**: Terminal doesn't allow copying from the box

**Solution**: Use grep to extract it:
```bash
agentcore invoke '{"prompt": "Hello"}' 2>&1 | grep "Session:"
```

### Wrong ID Copied

**Problem**: Copied Request ID instead of Session ID

**Solution**: Make sure you copy from the line that says "Session:", not "Request ID:"

## Quick Reference

```bash
# Invoke and see session ID
agentcore invoke '{"prompt": "Read my emails"}'

# Extract session ID only
agentcore invoke '{"prompt": "Read my emails"}' 2>&1 | grep "Session:" | awk '{print $2}'

# Save to variable
SESSION_ID=$(agentcore invoke '{"prompt": "Read my emails"}' 2>&1 | grep "Session:" | awk '{print $2}')

# Use with evaluator
agentcore eval run -e goal_hijack_eval-WbLyiS914l -s $SESSION_ID
```

## Summary

✅ **Session ID location**: Second line of header box  
✅ **Format**: UUID (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)  
✅ **Use for**: Running the evaluator  
✅ **Extract with**: grep or manual copy  
✅ **Required**: Yes, to run evaluations
