import pytest
from unittest.mock import patch, MagicMock
from utils_jira import (
    create_jira_ticket,
    update_jira_ticket,
    comment_on_jira_ticket,
    get_latest_comment_from_jira,
    get_user_details,
)

@patch("utils_jira.jira_client")
def test_create_jira_ticket(mock_jira_client):
    mock_jira_client.create_issue.return_value = MagicMock(key="JIRA-123")
    ticket_key, message = create_jira_ticket(
        "TEST", "Test Summary", "Test Description", "user123", "5", "Task", "High"
    )
    assert ticket_key == "JIRA-123"
    assert message == "Ticket created successfully"

@patch("utils_jira.jira_client")
def test_update_jira_ticket(mock_jira_client):
    mock_issue = MagicMock()
    mock_jira_client.issue.return_value = mock_issue
    update_jira_ticket("JIRA-123", story_points=8, assignee="user123", sprint_id=42, priority="Medium")
    mock_issue.update.assert_called_once_with(
        fields={
            "customfield_10016": 8,
            "customfield_10007": 42,
            "assignee": {"name": "user123"},
            "priority": {"name": "Medium"},
        }
    )

@patch("utils_jira.jira_client")
def test_comment_on_jira_ticket(mock_jira_client):
    comment_on_jira_ticket("JIRA-123", "This is a test comment.")
    mock_jira_client.add_comment.assert_called_once_with("JIRA-123", "This is a test comment.")

@patch("utils_jira.jira_client")
def test_get_latest_comment_from_jira(mock_jira_client):
    mock_comment = MagicMock(body="This is the latest comment.")
    mock_jira_client.comments.return_value = [mock_comment]
    latest_comment = get_latest_comment_from_jira("JIRA-123")
    assert latest_comment == "This is the latest comment."

@patch("utils_jira.jira_client")
def test_get_user_details(mock_jira_client):
    mock_user = MagicMock(accountId="user123", displayName="Test User")
    mock_jira_client.search_users.return_value = [mock_user]
    user_id = get_user_details("Test User")
    assert user_id == "user123"