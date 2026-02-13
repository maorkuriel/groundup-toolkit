---
name: deal-logger
description: Daily automated tool that checks WhatsApp/channel conversations, identifies deal-related discussions, and auto-logs notes to your CRM or tracking system.
metadata: { "openclaw": { "emoji": "💼", "requires": {} } }
---

# Deal Logger

## Overview

Automatically scans your daily conversations, identifies deal-related contacts, and logs notes for pipeline tracking.

## How It Works

1. **Scans conversations** from the last 24 hours across all channels
2. **Identifies deal contacts** by checking against your pipeline/CRM data  
3. **Summarizes** the conversation using AI
4. **Logs** the note to your tracking system

## Inputs

```json
{
  "action": "scan_and_log",
  "timeframe": "24h",
  "dealSource": "file|api|env",
  "dealDataPath": "~/deals.json",
  "logTarget": "file|crm|notion",
  "logPath": "~/deal-logs/"
}
```

## Configuration

The skill needs access to:
- Your deal pipeline data (list of contacts/companies in deals)
- A place to log the notes (file, CRM API, Notion, etc.)

## Usage

### Manual run
```bash
openclaw agent --message "/deal-logger scan_and_log" --local
```

### Automated (cron)
```bash
openclaw cron add --schedule "0 9 * * *" --command "deal-logger scan_and_log"
```

## Deal Data Format

Expected format in `~/deals.json`:
```json
{
  "deals": [
    {
      "contact": "+1234567890",
      "name": "John Doe",
      "company": "Acme Corp",
      "dealStage": "negotiation",
      "value": "$50k"
    }
  ]
}
```

## Output Format

Logs are written as:
```json
{
  "date": "2026-02-03",
  "contact": "+1234567890",
  "name": "John Doe",  
  "company": "Acme Corp",
  "conversationSummary": "Discussed pricing and delivery timeline. John confirmed budget approval.",
  "nextSteps": "Send proposal by Friday",
  "sentiment": "positive"
}
```
