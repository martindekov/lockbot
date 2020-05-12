import os
from datetime import datetime
from github import Github


def get_issues():
    desired_repo = os.getenv("github_repository")
    desired_days = int(os.getenv("inactive_days"))
    auth = None
    with open("/var/openfaas/secrets/auth-token") as file:
        auth = Github(file.read().strip())

    issues_for_lock = []
    for repo in auth.get_user().get_repos():
        if repo.name == desired_repo:
            for issue in repo.get_issues():
                if not issue.pull_request and not issue.locked:
                    last_comment = issue.get_comments()[
                        issue.comments-1].updated_at
                    difference = datetime.now() - datetime(last_comment.year,
                                                           last_comment.month,
                                                           last_comment.day)
                    if difference.days > desired_days:
                        issues_for_lock.append(issue)

    return issues_for_lock


def lock(issues):
    response = "no unlocked inactive issues"
    if len(issues) > 0:
        response = "issues locked:"
        for issue in issues:
            issue.lock("off-topic")
            response = response + f"\n{issue.title}"
    return response


def handle(req):
    issues = get_issues()
    response = lock(issues)
    return response
