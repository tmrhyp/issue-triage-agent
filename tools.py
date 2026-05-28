from github import Github
from langchain.tools import tool
import os

gh = Github(os.getenv("GITHUB_TOKEN"))

@tool
def list_open_issues(repo: str) -> str:
    """List open issues from a GitHub repo. Input: 'owner/repo'"""
    issues = gh.get_repo(repo).get_issues(state="open")
    return "\n".join([f"#{i.number}: {i.title}" for i in issues[:10]])

@tool
def get_issue_body(repo: str, issue_number: int) -> str:
    """Get the full body of a specific issue."""
    issue = gh.get_repo(repo).get_issue(issue_number)
    return f"Title: {issue.title}\nBody: {issue.body}"

@tool
def post_triage_comment(repo: str, issue_number: int, category: str, summary: str) -> str:
    """Post a triage comment on an issue."""
    issue = gh.get_repo(repo).get_issue(issue_number)
    issue.create_comment(f"**[Auto-triage]** Category: `{category}`\n\n{summary}")
    return f"Comment posted on #{issue_number}"
