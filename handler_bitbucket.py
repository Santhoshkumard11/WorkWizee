import logging
from utils_bitbucket import create_pr_to_branches, get_open_pr, comment_on_pr


def handle_create_pr_to_branches(
    source_branch: str,
    target_branch: str,
    title: str,
    description: str,
    repo_slug: str = "work-wizee",
    project_key: str = "JEN",
):
    """
    Handler to create pull requests from the source branch to dev, stg, and prod branches.

    Args:
        source_branch (str): The source branch name.
        title (str): The title of the pull request.
        description (str): The description of the pull request.
        project_key (str): The project key.
        repo_slug (str): The repository slug.

    Returns:
        dict: A dictionary with branch names as keys and PR links as values.
    """
    try:
        logging.info(f"Creating PR from {source_branch} to {target_branch}")

        pr_links, message = create_pr_to_branches(
            source_branch,
            target_branch,
            title,
            description,
            repo_slug,
            project_key,
        )
        if pr_links is None:
            logging.error(f"Error creating PR: {message}")
            raise Exception(f"Error while creating PR {message}")

        return pr_links
    except Exception as e:
        logging.error(f"Error creating PR: {e}")
        return None, f"Error while creating PR {e}"


def handle_get_open_pr(
    source_branch: str,
    repo_slug: str = "work-wizee",
    project_key: str = "JEN",
):
    """
    Handler to retrieve the current open pull request for a given repository and source branch.

    Args:
        repo_slug (str): The repository slug.
        project_key (str): The project key.
        source_branch (str): The source branch name.

    Returns:
        dict: The details of the open pull request, if any.
    """
    try:
        return get_open_pr(repo_slug, project_key, source_branch)
    except Exception as e:
        return {"error": str(e)}


def handle_comment_on_pr(
    pr_id: int,
    comment: str,
    repo_slug: str = "work-wizee",
    project_key: str = "JEN",
):
    """
    Handler to add a comment to a pull request.

    Args:
        repo_slug (str): The repository slug.
        project_key (str): The project key.
        pr_id (int): The ID of the pull request.
        comment (str): The comment to add.

    Returns:
        dict: A success message or error details.
    """
    try:
        comment_on_pr(repo_slug, project_key, pr_id, comment)
        return {"success": "Comment added successfully."}
    except Exception as e:
        return {"error": str(e)}
