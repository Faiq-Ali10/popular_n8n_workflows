def prompt(values) -> str:
    return f"""
You are given a list of forum topics in the format (id, title).

A valid entry is an **n8n automation workflow name** (e.g. "WhatsApp → Slack automation", "Google Sheets → Email alerts").
It does NOT need to mention "n8n".

Do NOT include:
- Tutorials or guides
- Troubleshooting or errors
- Questions or discussions
- Announcements or generic posts

⚠️ Important:
- Output ONLY the IDs of valid workflows.
- Format: comma-separated numbers (e.g., 1,3,5).
- Do NOT explain, do NOT write code, do NOT add text.

Input: {values}
"""
