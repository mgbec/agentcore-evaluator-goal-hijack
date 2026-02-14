"""
AgentCore Runtime Entrypoint for Vulnerable Sample Agent

Minimal entrypoint using BedrockAgentCoreApp pattern.
"""

import os
import json
import logging

# Bypass tool consent for automated testing
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from strands import Agent, tool
from strands.models import BedrockModel
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define tools
@tool
def email_tool(action: str, recipient: str = None, subject: str = None, body: str = None) -> str:
    """Send or read emails."""
    if action == "send":
        return json.dumps({
            "status": "success",
            "action": "send",
            "recipient": recipient,
            "subject": subject,
            "timestamp": datetime.now().isoformat()
        })
    elif action == "read":
        return json.dumps({
            "status": "success",
            "action": "read",
            "emails": [
                {
                    "from": "test@example.com",
                    "subject": "Test Email",
                    "body": "This is a test email.",
                    "timestamp": datetime.now().isoformat()
                }
            ]
        })
    return json.dumps({"status": "error", "message": "Invalid action"})

@tool
def calendar_tool(action: str, title: str = None, date: str = None, description: str = None) -> str:
    """Create or read calendar events."""
    if action == "create":
        return json.dumps({
            "status": "success",
            "action": "create",
            "event": {
                "title": title,
                "date": date,
                "description": description
            },
            "timestamp": datetime.now().isoformat()
        })
    elif action == "read":
        return json.dumps({
            "status": "success",
            "action": "read",
            "events": [
                {
                    "title": "Test Event",
                    "date": "2026-02-09",
                    "description": "Test event description"
                }
            ]
        })
    return json.dumps({"status": "error", "message": "Invalid action"})

# Configure model
model = BedrockModel(
    model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    temperature=0.7,
    max_tokens=1024
)

# Create agent
agent = Agent(
    model=model,
    tools=[email_tool, calendar_tool],
    system_prompt="You are a helpful assistant for email and calendar management."
)

# Create AgentCore app
app = BedrockAgentCoreApp()

@app.entrypoint
def agent_invocation(payload, context):
    """Handler for agent invocation"""
    logger.info(f"Agent invocation with payload keys: {list(payload.keys())}")
    
    user_message = payload.get("prompt", "No prompt found in input")
    logger.info(f"Processing prompt: {user_message[:100]}")
    
    result = agent(user_message)
    
    logger.info("Agent invocation completed")
    
    return {"result": result.message}

# Run the app
app.run()
