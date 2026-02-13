# Deal Automation

Automated email monitoring that creates HubSpot companies and deals from team member emails.

## Name
deal-automation

## Description
Monitors Gmail for emails from team members with company info or deck attachments. Automatically creates companies and deals in HubSpot, assigns them to the sender, and sets the stage to "Meeting 1".

## How It Works

1. **Checks Gmail every 2 hours** for emails from team members
2. **Identifies emails** with attachments (decks, presentations, company info)
3. **Extracts company name** from email subject
4. **Creates HubSpot company** with extracted information
5. **Creates HubSpot deal** assigned to the email sender
6. **Sets deal stage** to "Meeting 1" (appointmentscheduled)
7. **Associates deal** with the company

## Team Members Monitored

Team members are loaded from `config.yaml`. See `config.example.yaml` for the format.

## Requirements

- Maton API key for HubSpot access
- gog CLI authenticated for Gmail
- Python 3 with requests library

## Setup

1. Get your Maton API key from https://maton.ai/settings
2. Set environment variable: `export MATON_API_KEY="your_key"`
3. Add to cron: `0 */2 * * * $TOOLKIT_DIR/scripts/email-to-deal-automation.py >> /var/log/deal-automation.log 2>&1`

## Manual Run

Test the automation:
```bash
export MATON_API_KEY="your_key"
$TOOLKIT_DIR/scripts/email-to-deal-automation.py
```

## Logs

Check logs at `/var/log/deal-automation.log`
