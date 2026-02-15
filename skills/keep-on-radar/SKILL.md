---
name: keep-on-radar
description: Monthly review of Keep on Radar deals with company research updates. Sends digest to deal owners and handles actions (pass, keep, add note) via email reply or WhatsApp.
version: 1.0.0
author: GroundUp VC
actions:
  - review
  - check-replies
  - status
  - pass
---

# Keep on Radar

Monthly review of all HubSpot deals in the "Keep on Radar" stage. Researches what's new with each company using web search and AI analysis, sends a digest email and WhatsApp summary to each deal owner, and handles their replies to take action.

## When to Use This Skill

**WhatsApp triggers (from team members):**
- "pass on [company name]" or "pass [company name]" or "drop [company]"
- "what's on my radar?" or "radar status" or "show my radar deals"
- "keep watching [company name]" or "keep [company name]"
- "add note to [company name]: ..." or "note on [company]: ..."

**Automated (via cron):**
- Monthly review runs on the 15th of each month
- Email reply polling runs every 2 hours

## Actions

### review

Run the monthly review. For each deal in Keep on Radar:
1. Fetch associated company from HubSpot
2. Research what's new (Brave Search + Claude analysis)
3. Send digest email grouped by deal owner
4. Send WhatsApp summary to each owner

```bash
keep-on-radar review
```

### check-replies

Poll Gmail for replies to the monthly digest emails. Parses actions using AI and executes them (move to pass, add note, keep watching).

```bash
keep-on-radar check-replies
```

### status

List all deals currently in Keep on Radar, grouped by owner.

```bash
keep-on-radar status
```

### pass

Move a specific deal to the Pass (Closed Lost) stage with an optional reason.

```bash
keep-on-radar pass <deal_id> "<reason>"
```

**WhatsApp integration:**
When a team member says "pass on [company]" via WhatsApp:
1. Look up the deal by company name in the Keep on Radar stage
2. Confirm with the user: "Move [company] to Pass? (yes/no)"
3. On confirmation, run: `keep-on-radar pass <deal_id> "<reason>"`
4. Confirm completion via WhatsApp

## HubSpot Details

- Pipeline: VC Deal Flow (`default`)
- Keep on Radar stage: `1138024523`
- Pass stage: `closedlost`

## Cron Schedule

```cron
# Monthly review on 15th at 10am UTC
0 10 15 * * source ~/.env && ~/.openclaw/skills/keep-on-radar/keep-on-radar review >> /var/log/keep-on-radar.log 2>&1

# Check email replies every 2 hours
0 */2 * * * source ~/.env && ~/.openclaw/skills/keep-on-radar/keep-on-radar check-replies >> /var/log/keep-on-radar.log 2>&1
```

## Configuration

Uses shared `config.yaml` and `.env` — no additional configuration needed.

Required environment variables:
- `MATON_API_KEY` — HubSpot API access via Maton gateway
- `ANTHROPIC_API_KEY` — Claude AI for research synthesis and reply parsing
- `BRAVE_SEARCH_API_KEY` — Web search for company/founder updates
- `GOG_KEYRING_PASSWORD` — Gmail access for sending digests and polling replies
