# LinkedIn Skill

Get LinkedIn profile information and research people and companies.

## Name
linkedin

## Description
Research LinkedIn profiles, get person details, company information, and insights about people's work history and connections. Use this skill when the user wants to look up someone on LinkedIn, research a company, or get professional background information.

## Actions

### person
Get detailed LinkedIn profile for a person

**Usage:**
```
linkedin person PROFILE_URL
```

**Example:**
```
linkedin person https://www.linkedin.com/in/johndoe/
```

### company
Get LinkedIn company profile information

**Usage:**
```
linkedin company COMPANY_URL
```

**Example:**
```
linkedin company https://www.linkedin.com/company/your-company/
```

## When to Use This Skill

This skill should be invoked when the user wants to:
- Look up someone's LinkedIn profile
- Research a person's professional background
- Get company information from LinkedIn
- Check someone's work history or education
- Research a potential candidate or partner
- Get details about a company's employees or structure

Natural language triggers:
- "look up NAME on LinkedIn"
- "get NAME's LinkedIn profile"
- "research COMPANY on LinkedIn"
- "what's PERSON's background"
- "check out COMPANY LinkedIn"
- "find information about PERSON/COMPANY"

## Setup Required

Before using this skill, you need to configure LinkedIn authentication:

1. Get your LinkedIn cookie from an incognito browser session
2. Run the setup script with your cookie value

## Examples

Get person profile - look up a LinkedIn user
Get company profile - research a company on LinkedIn
Natural language - automatically fetch profile from URL
