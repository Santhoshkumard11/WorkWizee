import azure.functions as func
import logging
import urllib.parse

from handler_bitbucket import handle_create_pr_to_branches
from handler_jira import (
    handle_create_jira_ticket,
    handle_get_latest_comments,
    handle_jira_add_comment,
)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="health")
def health(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("OK", status_code=200)


@app.route(route="bitbucket_create_pr", methods=["POST"])
def bitbucket_create_pr(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Bitbucket create PR HTTP trigger function processed a request.")
    response_message = "Bitbucket PR created successfully - "
    try:
        req_body = req.get_body().decode("utf-8")
        logging.info(f"body - {req_body}")

        try:
            print(f"Trying to print the params - {req.params.items()}")
        except Exception as e:
            logging.info(f"Error while trying to print the params - {e}")
            pass

        if req_body == "":
            logging.info(
                "Params are not coming in the body, trying to get from query params"
            )
            params = req.params
            source_branch = params.get("source_branch", [""])
            target_branch = params.get("target_branch", [""]).upper()
            title = params.get("title", [""])
            description = params.get("description", [""])
        else:
            params = urllib.parse.parse_qs(req_body)
            source_branch = params.get("source_branch", [""])[0]
            target_branch = params.get("target_branch", [""])[0].upper()
            title = params.get("title", [""])[0]
            description = params.get("description", [""])[0]

        logging.info(
            f"Source Branch - {source_branch} - Title - {title} - Description - {description} - Target Branch - {target_branch}"
        )

        pr_link = handle_create_pr_to_branches(
            source_branch,
            target_branch,
            title,
            description,
        )

        response_message = response_message + f"PR link - {pr_link}."

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        response_message = f"Error while trying to create Bitbucket PR - {e}"

    return func.HttpResponse(
        response_message,
        status_code=200,
    )


@app.route(route="bitbucket_get_open_pr", methods=["POST"])
def bitbucket_get_open_pr(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Bitbucket get open PR HTTP trigger function processed a request.")
    response_message = "Bitbucket open PR - "
    try:
        req_body = req.get_body().decode("utf-8")
        logging.info(f"body - {req_body}")

        params = urllib.parse.parse_qs(req_body)

        source_branch = params.get("source_branch", [""])[0]

        logging.info(f"Source Branch - {source_branch}")

        response_message = handle_get_latest_comments(source_branch)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        response_message = f"Error while trying to get open Bitbucket PR - {e}"

    return func.HttpResponse(
        response_message,
        status_code=200,
    )


@app.route(route="bitbucket_comment_on_pr", methods=["POST"])
def bitbucket_comment_on_pr(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Bitbucket comment on PR HTTP trigger function processed a request.")
    response_message = "Bitbucket PR comment added successfully - "
    try:
        req_body = req.get_body().decode("utf-8")
        logging.info(f"body - {req_body}")

        params = urllib.parse.parse_qs(req_body)

        pr_id = params.get("pr_id", [""])[0]
        comment = params.get("comment", [""])[0]

        logging.info(f"PR ID - {pr_id} - Comment - {comment}")

        response_message = handle_jira_add_comment(pr_id, comment)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        response_message = f"Error while trying to add comment to Bitbucket PR - {e}"

    return func.HttpResponse(
        response_message,
        status_code=200,
    )


@app.route(route="jira_add_comment", methods=["POST"])
def jira_add_comment(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Jira add comment HTTP trigger function processed a request.")
    response_message = "Jira comment added successfully - "
    try:
        req_body = req.get_body().decode("utf-8")
        logging.info(f"body - {req_body}")

        params = urllib.parse.parse_qs(req_body)

        ticket_key = params.get("ticket_key", [""])[0]
        comment = params.get("comment", [""])[0]

        logging.info(f"Ticket Key - {ticket_key} - Comment - {comment}")

        response_message = handle_jira_add_comment(ticket_key, comment)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        response_message = f"Error while trying to add comment to Jira ticket - {e}"

    return func.HttpResponse(
        response_message,
        status_code=200,
    )


@app.route(route="jira_get_latest_comments", methods=["POST"])
def jira_get_latest_comments(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Jira get latest comments HTTP trigger function processed a request.")
    response_message = "Jira latest comments - "
    try:
        req_body = req.get_body().decode("utf-8")
        logging.info(f"body - {req_body}")

        if req_body == "":
            logging.info(
                "Params are not coming in the body, trying to get from query params"
            )
            params = req.params
            ticket_key = params.get("ticket_key", [""])
        else:
            params = urllib.parse.parse_qs(req_body)
            ticket_key = params.get("ticket_key", [""])[0]

        response_message = handle_get_latest_comments(ticket_key)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        response_message = (
            f"Error while trying to get latest comments from Jira ticket - {e}"
        )

    return func.HttpResponse(
        response_message,
        status_code=200,
    )


@app.route(route="jira_create_ticket", methods=["POST"])
def jira_create_ticket(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Jira create ticket HTTP trigger function processed a request.")
    response_message = "Jira ticket created successfully - "
    try:
        req_body = req.get_body().decode("utf-8")
        logging.info(f"body - {req_body}")

        if req_body == "":
            logging.info(
                "Params are not coming in the body, trying to get from query params"
            )
            params = req.params
            summary = params.get("summary", [""])
            description = params.get("description", [""])
            assignee = params.get("assignee", [""])
            story_points = params.get("story_points", [""])
            issue_type = params.get("issue_type", ["Task"])
            priority = params.get("priority", [""])
        else:
            params = urllib.parse.parse_qs(req_body)
            summary = params.get("summary", [""])[0]
            description = params.get("description", [""])[0]
            assignee = params.get("assignee", [""])[0]
            # default story points is 3
            story_points = params.get("story_points", ["3"])[0]
            issue_type = params.get(
                "issue_type",
                ["Task"],
            )[0]
            priority = params.get("priority", [""])[0]

        jira_ticket = handle_create_jira_ticket(
            summary, description, assignee, story_points, issue_type, priority
        )

        response_message = (
            response_message
            + f"ticket Key - {jira_ticket} and ticket URL is https://sandyinspires.atlassian.net/browse/{jira_ticket}."
        )

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        response_message = f"Error while trying to create Jira ticket - {e}"

    return func.HttpResponse(
        response_message,
        status_code=200,
    )
