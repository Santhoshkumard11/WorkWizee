import logging
from atlassian.bitbucket import Cloud
import os

# Initialize Bitbucket client
bitbucket_username = os.environ.get("BITBUCKET_USERNAME")
bitbucket_password = os.environ.get("BITBUCKET_APP_PASSWORD")
bitbucket_client = Cloud(
    username=bitbucket_username, password=bitbucket_password, cloud=True
)

repo_slug: str = "work-wizee"
project_key: str = "JEN"


def create_pr_to_branches(
    source_branch: str,
    target_branch: str,
    title: str,
    description: str,
    repo_slug: str,
    project_key: str,
):
    """
    Creates pull requests from the source branch to dev, stg, and prod branches.

    Args:
        repo_slug (str): The repository slug.
        project_key (str): The project key.
        source_branch (str): The source branch name.
        title (str): The title of the pull request.
        description (str): The description of the pull request.

    Returns:
        dict: A dictionary with branch names as keys and PR links as values.
    """
    target_branches = ["DEV", "STG", "MAIN", "PROD"]
    pr_links = ""

    workplace = bitbucket_client.workspaces.get(bitbucket_username)

    repository = workplace.repositories.get(repo_slug)

    if target_branch in target_branches:
        pr = repository.pullrequests.create(
            title=title,
            description=description,
            source_branch=source_branch,
            destination_branch=target_branch,
        )
        pr_links = pr.url
        logging.info(f"Pull request created: {pr_links}")
    else:
        # Handle invalid target branch
        return None, "Invalid target branch. Please use one of the following: dev, stg, main."

    return pr_links, "Pull requests created successfully."


def get_open_pr(repo_slug: str, project_key: str, source_branch: str):
    """
    Retrieves the current open pull request for a given repository and source branch.

    Args:
        repo_slug (str): The repository slug.
        project_key (str): The project key.
        source_branch (str): The source branch name.

    Returns:
        dict: The details of the open pull request, if any.
    """
    prs = bitbucket_client.repositories.get_pull_requests(
        project_key=project_key, repository_slug=repo_slug, state="OPEN"
    )
    for pr in prs:
        if pr.get("fromRef", {}).get("displayId") == source_branch:
            return pr
    return None


def comment_on_pr(repo_slug: str, project_key: str, pr_id: int, comment: str):
    """
    Adds a comment to a pull request.

    Args:
        repo_slug (str): The repository slug.
        project_key (str): The project key.
        pr_id (int): The ID of the pull request.
        comment (str): The comment to add.
    """
    bitbucket_client.repositories.add_pull_request_comment(
        project_key=project_key,
        repository_slug=repo_slug,
        pull_request_id=pr_id,
        text=comment,
    )
