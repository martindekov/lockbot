import os
import requests
from datetime import datetime


def get_difference_in_days(string_date):
    # GitHub date format: 2019-01-13T21:17:09Z
    created_date = string_date.split('T')[0].split('-')
    for i in range(0, len(created_date)):
        created_date[i] = int(created_date[i])
    created_date = datetime(created_date[0], created_date[1], created_date[2])
    return datetime.now() - created_date


def lock_issue(issue_number, auth_header, username, repo):
    r = requests.put(
        url=f"https://api.github.com/repos/{username}/{repo}/issues/{issue_number}/lock", headers=auth_header)
    if r.status_code == 204:
        return f"Issue: {issue_number} locked"


def get_authorization_header():
    with open("/var/openfaas/secrets/auth-token") as file:
        return {'Authorization': f"token {file.read().strip()}"}


def handle(req):
    username = os.getenv("github_username")
    repo = os.getenv("github_repository")
    r = requests.get(f"https://api.github.com/repos/{username}/{repo}/issues")
    issues = r.json()

    issue_numbers = []
    for issue in issues:
        if not issue.get('pull_request'):
            diff = get_difference_in_days(issue.get('created_at'))
            if diff.days > 100 and not issue.get("locked"):
                issue_numbers.append(int(issue.get('number')))

    locked_issues = ""
    if len(issue_numbers) > 0:
        auth_header = get_authorization_header()
        for issue_number in issue_numbers:
            locked_issues = locked_issues + \
                f"{lock_issue(issue_number, auth_header, username, repo)}\n"

    if locked_issues != "":
        return locked_issues

    return "No issues locked"