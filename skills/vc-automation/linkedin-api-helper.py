#!/usr/bin/env python3
"""
LinkedIn API Helper for Founder Research
Uses Maton's LinkedIn API gateway with OAuth
"""

import sys
import os
import json
import urllib.request
import urllib.parse

MATON_API_KEY = os.getenv("MATON_API_KEY")
LINKEDIN_CONNECTION_ID = os.getenv("LINKEDIN_CONNECTION_ID", "your-connection-id")


def linkedin_api_request(endpoint, headers=None):
    """Make request to LinkedIn API via Maton gateway"""
    if not MATON_API_KEY:
        return {"error": "MATON_API_KEY not set"}

    url = f"https://gateway.maton.ai/linkedin{endpoint}"

    default_headers = {
        "Authorization": f"Bearer {MATON_API_KEY}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Maton-Connection": LINKEDIN_CONNECTION_ID
    }

    if headers:
        default_headers.update(headers)

    try:
        req = urllib.request.Request(url, headers=default_headers)
        response = urllib.request.urlopen(req, timeout=15)
        return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else str(e)
        return {"error": f"HTTP {e.code}", "details": error_body}
    except Exception as e:
        return {"error": str(e)}


def search_person_by_name(name):
    """
    Search for LinkedIn profile by name using userinfo endpoint
    Note: This requires the person to be in your network or public profile
    """
    # Get current user info first to test connection
    userinfo = linkedin_api_request("/v2/userinfo")

    if "error" in userinfo:
        return userinfo

    # For now, return userinfo as we need search API access
    # which requires different API endpoints
    return {
        "method": "direct_api",
        "note": "LinkedIn API search requires Company/Organization pages or ads API",
        "test_profile": userinfo,
        "recommendation": "Use web search for finding profiles"
    }


def get_profile(profile_url=None):
    """
    Get LinkedIn profile information
    If no URL provided, returns current authenticated user's profile
    """
    if profile_url:
        return {
            "error": "Direct URL lookup requires LinkedIn premium API access",
            "recommendation": "Use /v2/me endpoint for authenticated user only"
        }

    # Get authenticated user profile
    profile = linkedin_api_request("/v2/me?projection=(id,firstName,lastName,profilePicture,headline)")

    if "error" in profile:
        return profile

    # Also get userinfo for more details
    userinfo = linkedin_api_request("/v2/userinfo")

    # Combine results
    combined = {
        "profile": profile,
        "userinfo": userinfo if "error" not in userinfo else None,
        "api_method": "authenticated_user_only"
    }

    return combined


def format_profile_for_research(profile_data):
    """Format LinkedIn profile data for founder research"""
    if "error" in profile_data:
        return f"LinkedIn API Error: {profile_data['error']}"

    lines = ["LinkedIn Profile (via API):"]
    lines.append("-" * 40)

    if "userinfo" in profile_data and profile_data["userinfo"]:
        ui = profile_data["userinfo"]
        lines.append(f"Name: {ui.get('name', 'N/A')}")
        lines.append(f"Email: {ui.get('email', 'N/A')}")
        lines.append(f"Locale: {ui.get('locale', 'N/A')}")

    if "profile" in profile_data:
        prof = profile_data["profile"]
        if "headline" in prof:
            lines.append(f"Headline: {prof['headline']}")
        lines.append(f"LinkedIn ID: {prof.get('id', 'N/A')}")

    lines.append("-" * 40)
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: linkedin-api-helper <command> [args]")
        print("Commands:")
        print("  profile              Get authenticated user profile")
        print("  search <name>        Search for person (limited)")
        print("  test                 Test API connection")
        sys.exit(1)

    command = sys.argv[1]

    if command == "test":
        print("Testing LinkedIn API connection...")
        result = linkedin_api_request("/v2/userinfo")
        print(json.dumps(result, indent=2))

    elif command == "profile":
        print("Fetching profile...")
        result = get_profile()
        print(json.dumps(result, indent=2))

    elif command == "search":
        if len(sys.argv) < 3:
            print("Error: search requires a name")
            sys.exit(1)
        name = " ".join(sys.argv[2:])
        print(f"Searching for: {name}")
        result = search_person_by_name(name)
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
