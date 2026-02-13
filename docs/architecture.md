# Architecture

## Overview

The GroundUp Toolkit runs on a single Linux server and orchestrates communication between WhatsApp, Google Workspace, HubSpot, and AI services through OpenClaw.

## System Components

### OpenClaw Gateway
The core process that maintains the WhatsApp Web connection and routes messages. Runs as a background process (`nohup openclaw gateway &`).

### Skills
OpenClaw skills are self-contained automation modules in `skills/`. Each skill has:
- `SKILL.md` - Description and usage for the AI agent
- Executable scripts (Python or Bash)
- Optional `package.json` for Node.js dependencies

### Scripts
Operational scripts in `scripts/` handle monitoring, health checks, and scheduled tasks. These run via cron.

### Config Layer
`lib/config.py` (Python) and `lib/config.js` (Node.js) provide a unified interface to `config.yaml` and `.env`. All skills and scripts use these instead of hardcoding values.

## Data Flow

### Meeting Reminders
```
Cron (every 5 min)
  → reminders.py checks each team member's Google Calendar (via gog CLI)
  → Finds meetings starting in 10-15 minutes
  → Enriches with HubSpot context (company, deal stage, notes)
  → Optionally enriches attendees (LinkedIn, Crunchbase, GitHub)
  → Sends WhatsApp message via OpenClaw
  → Falls back to email if WhatsApp fails (10 retries first)
  → Tracks sent notifications in SQLite to avoid duplicates
```

### Deal Automation
```
Cron (every 2 hours)
  → email-to-deal-automation.py checks Gmail for team member emails
  → Identifies company names and attachments
  → Checks HubSpot for existing companies/deals
  → Creates new company + deal if not found
  → Assigns deal to the email sender
  → Sends WhatsApp confirmation
  → Labels email as processed
```

### Meeting Bot
```
Cron (every 3 min): meeting-auto-join checks upcoming meetings
  → If meeting starts within 5 min and the assistant is invited
  → Launches camofox-join.js (headless browser via Camoufox)
  → Joins Google Meet, enables recording
  → Monitors attendance, pings missing team members via Twilio
  → When meeting ends, processes Gemini notes
  → Emails action items to relevant team members

Cron (every 2 hours): meeting-bot processes recordings
  → Finds new recordings in Google Drive
  → Downloads transcripts
  → Extracts action items with Claude AI
  → Emails summaries
```

### Health Monitoring
```
health-check.sh (every 15 min):
  → Checks gateway process, RPC health, WhatsApp status
  → Checks agent heartbeats, disk/memory, Camoufox browser
  → Auto-restarts failed services
  → Emails alerts on critical failures

whatsapp-watchdog.sh (every 5 min):
  → Sends actual test message via WhatsApp
  → On failure: restarts gateway, retries
  → If still failing: calls admin via Twilio + emails alert
  → 1-hour cooldown between alerts
```

## External Services

| Service | Protocol | Used By |
|---------|----------|---------|
| WhatsApp | OpenClaw gateway | Meeting reminders, deal confirmations, team pings |
| Google Calendar | gog CLI (OAuth) | Meeting reminders, auto-join, scheduling |
| Gmail | gog CLI (OAuth) | Email fallback, deal monitoring, meeting summaries |
| Google Meet | Headless browser | Meeting bot auto-join |
| Google Drive | gog CLI (OAuth) | Meeting recordings, transcripts |
| HubSpot | Maton API gateway | Deal creation, company lookup, CRM notes |
| Claude AI | Anthropic API | Meeting analysis, deck extraction, note processing |
| Twilio | REST API | Phone call alerts, teammate pings |
| Brave Search | REST API | Founder research, web enrichment |
| LinkedIn | MCP bridge | Profile research |

## Database

- **SQLite** (`/tmp/meeting-reminders.db`) - Tracks which meetings have been notified
- **SQLite** (`attendee_cache.db`) - 7-day cache for attendee enrichment data
- **JSON** (`processed-meetings.json`) - Tracks processed meeting recordings
