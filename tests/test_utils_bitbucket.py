import pytest
from unittest.mock import patch, MagicMock
from utils_bitbucket import create_pr_to_branches, get_open_pr, comment_on_pr

@patch("utils_bitbucket.bitbucket_client")
def test_create_pr_to_branches(mock_bitbucket_client):
    mock_repo = MagicMock()
    mock_repo.pullrequests.create.return_value = MagicMock(url="http://example.com/pr")
    mock_workspace = MagicMock()
    mock_workspace.repositories.get.return_value = mock_repo
    mock_bitbucket_client.workspaces.get.return_value = mock_workspace

    pr_links, message = create_pr_to_branches(
        "feature-branch", "DEV", "Test PR", "This is a test PR", "work-wizee", "JEN"
    )
    assert pr_links == "http://example.com/pr"
    assert message == "Pull requests created successfully."

@patch("utils_bitbucket.bitbucket_client")
def test_get_open_pr(mock_bitbucket_client):
    mock_bitbucket_client.repositories.get_pull_requests.return_value = [
        {"fromRef": {"displayId": "feature-branch"}, "id": 123}
    ]
    pr = get_open_pr("work-wizee", "JEN", "feature-branch")
    assert pr["id"] == 123

@patch("utils_bitbucket.bitbucket_client")
def test_comment_on_pr(mock_bitbucket_client):
    comment_on_pr("work-wizee", "JEN", 123, "This is a test comment.")
    mock_bitbucket_client.repositories.add_pull_request_comment.assert_called_once_with(
        project_key="JEN", repository_slug="work-wizee", pull_request_id=123, text="This is a test comment."
    )