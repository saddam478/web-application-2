import json
import os

def lambda_handler(event, context):
    path = event.get("rawPath", "/")

    # Map paths to HTML files
    html_files = {
        "/": "index.html",
        "/logged_in": "logged_in.html",
        "/logged_out": "logged_out.html"
    }

    file_name = html_files.get(path, "index.html")

    # Read the HTML file
    try:
        with open(f"/var/task/app/{file_name}", "r") as file:
            html_content = file.read()
    except FileNotFoundError:
        return {"statusCode": 404, "body": "Page not found", "headers": {"Content-Type": "text/html"}}

    return {
        "statusCode": 200,
        "body": html_content,
        "headers": {"Content-Type": "text/html"}
    }
