import logging

from utils_jira import (
    comment_on_jira_ticket,
    create_jira_ticket,
    get_latest_comment_from_jira,
    get_user_details,
)


def handle_create_jira_ticket(
    summary: str,
    description: str,
    assignee: str,
    story_points: int = None,
    issue_type: str = "Task",
    priority: str = "Medium",
    project_key: str = "WOWZEE",
):
    """
    Handles the creation of a JIRA ticket.

    Args:
        project_key (str): The key of the JIRA project.
        summary (str): The summary of the ticket.
        description (str): The description of the ticket.
        assignee (str): The username of the assignee.
        story_points (int, optional): The story points to set.
        sprint_id (int, optional): The sprint ID to set.
        priority (str, optional): The priority to set.

    Returns:
        str: The key of the created ticket.
    """
    try:
        logging.info(
            f"Creating JIRA ticket with summary: {summary}, description: {description}, assignee: {assignee}, story points: {story_points}, issue type: {issue_type}, priority: {priority}"
        )

        user_id = get_user_details(assignee)

        ticket_key, message = create_jira_ticket(
            project_key,
            summary,
            description,
            user_id,
            story_points,
            issue_type,
            priority,
        )

        logging.info(f"JIRA ticket created successfully: {ticket_key}")
        if not ticket_key:
            logging.error("Failed to create JIRA ticket.")
            return "Error while creating JIRA ticket - " + message

        return ticket_key
    except Exception as e:
        logging.error(f"Error creating JIRA ticket: {e}")
        return "Error while creating JIRA ticket "


def handle_jira_add_comment(
    ticket_key: str,
    comment: str,
):
    """
    Handles the addition of a comment to a JIRA ticket.

    Args:
        ticket_key (str): The key of the JIRA ticket.
        comment (str): The comment to add.

    Returns:
        str: The response message.
    """
    try:
        logging.info(f"Adding comment to JIRA ticket {ticket_key}: {comment}")
        message = comment_on_jira_ticket(ticket_key, comment)
        return message
    except Exception as e:
        logging.error(f"Error adding comment to JIRA ticket: {e}")
        return "Error while adding comment to JIRA ticket"


def handle_get_latest_comments(ticket_key: str):
    """
    Handles the retrieval of the latest comment from a JIRA ticket.

    Args:
        ticket_key (str): The key of the JIRA ticket.

    Returns:
        str: The latest comment.
    """
    try:
        logging.info(f"Retrieving latest comment from JIRA ticket {ticket_key}")
        message = get_latest_comment_from_jira(ticket_key)
        return message
    except Exception as e:
        logging.error(f"Error retrieving latest comment from JIRA ticket: {e}")
        return "Error while retrieving latest comment from JIRA ticket"
