---
name: ping-teammate
description: Call a team member's phone when someone pings them on WhatsApp. Only team members can use this.
version: 1.0.0
actions:
  - call
---

# Ping Teammate

Calls a team member's phone via Twilio when another team member asks the assistant to ping them.

## Usage

When a team member sends a WhatsApp message like "ping Alice" or "call Bob" or "get Alice on the phone", invoke this skill.

**Arguments:**
1. Target name (first name of the team member to call) -- must match a name in config.yaml
2. Sender's phone number (the WhatsApp number of the person requesting the ping)

**Example:** `ping-teammate Alice +15551234567`

## Valid team members

Team members are loaded from `config.yaml`. See `config.example.yaml` for format.

## Security

- Only team members defined in config.yaml can use this skill (validated by sender phone number)
- A team member cannot ping themselves
- The called person hears a Twilio voice message telling them who is trying to reach them

## Natural language triggers

- "ping NAME"
- "call NAME"
- "get NAME on the phone"
- "ring NAME"
- "phone NAME"
- "dial NAME"
- "reach NAME"
- "buzz NAME"
