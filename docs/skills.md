# Skills Reference

Each skill is an OpenClaw automation module. Skills are invoked by the AI agent, by cron, or manually.

---

## Meeting Reminders

**Path**: `skills/meeting-reminders/`

Sends WhatsApp reminders 10-15 minutes before calendar meetings. Includes HubSpot context (company, deal stage, last note) and optionally enriches attendees with LinkedIn, Crunchbase, and GitHub data.

**Features**:
- Per-member timezone support
- 10 WhatsApp retries with 5-second intervals
- Email fallback when WhatsApp is down
- SQLite deduplication (won't send the same reminder twice)
- On-demand "next meeting" query

**Usage**:
```bash
# Run reminder check (normally via cron)
./skills/meeting-reminders/meeting-reminders reminders

# Query next meeting for a user
./skills/meeting-reminders/reminders.py query user@yourcompany.com
```

---

## Meeting Bot

**Path**: `skills/meeting-bot/`

Two components:
1. **meeting-auto-join** - Checks calendar every 3 min, auto-joins meetings via headless browser
2. **meeting-bot** - Processes recordings, extracts action items with Claude, emails summaries

**Requirements**: Camoufox browser running on port 9377, Google cookies configured.

---

## Deal Automation

**Path**: `skills/deal-automation/`

Monitors Gmail for emails from team members containing company/deal information. Automatically creates HubSpot companies and deals, assigns to the sender.

**Related script**: `scripts/email-to-deal-automation.py`

---

## Deck Analyzer

**Path**: `skills/deck-analyzer/`

AI-powered pitch deck data extraction. Supports DocSend, Google Drive, Dropbox, and direct PDF links. Extracts: company name, product overview, problem/solution, team, go-to-market, traction, and fundraising details.

---

## VC Automation

**Path**: `skills/vc-automation/`

Two tools:
- **meeting-notes-to-crm** - Processes meeting notes, extracts key points, updates HubSpot deals
- **research-founder** - Comprehensive founder background research using web search, LinkedIn, and Crunchbase

---

## Ping Teammate

**Path**: `skills/ping-teammate/`

Calls a team member's phone via Twilio when triggered by a WhatsApp message. Security: only configured team members can use it, can't self-ping.

---

## Google Workspace

**Path**: `skills/google-workspace/`

Wrapper scripts for the gog CLI:
- Calendar operations (list, create, delete events)
- Gmail operations (send, read, search)
- Google Drive/Docs access

---

## LinkedIn

**Path**: `skills/linkedin/`

LinkedIn profile research via MCP bridge. Requires LinkedIn authentication cookie.

---

## Deal Logger

**Path**: `skills/deal-logger/`

Scans WhatsApp conversations for deal-related discussions, summarizes with AI, and logs to tracking system.
