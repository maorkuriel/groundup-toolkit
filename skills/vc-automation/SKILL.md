---
name: vc-automation
description: Process meeting notes and research founders with automated CRM updates
metadata: { "openclaw": { "emoji": "📝", "requires": {} } }
---

# VC Automation Tools

## Overview

Automated workflow tools for venture capital operations including meeting notes processing and founder research.

## Skills

### 1. meeting-notes-to-crm

Process meeting notes and automatically update HubSpot CRM.

**Via WhatsApp:**
Just send the assistant: "Process these meeting notes: Met with Acme Corp CEO..."

**Command line:**
```bash
$TOOLKIT_DIR/skills/vc-automation/meeting-notes-to-crm "Meeting notes text..."
```

**What it does:**
1. Extracts company name, key points, action items, sentiment
2. Finds the deal in HubSpot  
3. Creates a note with structured meeting summary
4. Updates deal stage if appropriate
5. Creates calendar reminders for follow-ups

### 2. research-founder  

Research a founder and generate comprehensive due diligence report.

**Via WhatsApp:**
Send the assistant: "Research founder: Brian Chesky, Airbnb"

**Command line:**
```bash
$TOOLKIT_DIR/skills/vc-automation/research-founder "Brian Chesky" "Airbnb"
```

## Configuration

Requires:
- MATON_API_KEY for HubSpot access
- ANTHROPIC_API_KEY for AI processing
- GOG_KEYRING_PASSWORD for Google Workspace access
