import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta, timezone
import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to parse and categorize pull requests
def parse_pull_requests(pull_requests, one_week_ago):
    open_prs = []
    closed_prs = []

    for pr in pull_requests:
        updated_at = datetime.strptime(pr["updated_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        if updated_at < one_week_ago:
            continue  # Ignore pull requests not updated within the last week

        pr_info = {
            "number": pr["number"],
            "title": pr["title"],
            "user": pr["user"]["login"],
            "updated_at": updated_at,
            "state": pr["state"],
            "html_url": pr["html_url"]
        }

        if pr["state"] == "open":
            open_prs.append(pr_info)
        else:
            closed_prs.append(pr_info)

    return open_prs, closed_prs

# Function to fetch pull requests
def fetch_pull_requests(url, headers, params, one_week_ago):
    open_prs = []
    closed_prs = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        pull_requests = response.json()

        if not pull_requests:
            break

        new_open_prs, new_closed_prs = parse_pull_requests(pull_requests, one_week_ago)
        open_prs.extend(new_open_prs)
        closed_prs.extend(new_closed_prs)

        # Check if the last pull request in the current batch was updated within the last week
        last_pr_updated_at = datetime.strptime(pull_requests[-1]["updated_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        if last_pr_updated_at < one_week_ago:
            break

        # Move to the next page
        params["page"] += 1

    return open_prs, closed_prs

# Function to create the report
def create_report(repo_name, open_prs, closed_prs):
    report = f"Weekly Pull Request Report for {repo_name}\n\n"
    
    if not open_prs and not closed_prs:
        return f"No pull requests have been updated within the last week for {repo_name}."

    if open_prs:
        report += "Open Pull Requests:\n"
        for pr in open_prs:
            report += f"  PR #{pr['number']} - {pr['title']}\n"
            report += f"    Updated at: {pr['updated_at']}\n"
            report += f"    Author: {pr['user']}\n"
            report += f"    Link: {pr['html_url']}\n\n"
    
    if closed_prs:
        report += "Closed Pull Requests:\n"
        for pr in closed_prs:
            report += f"  PR #{pr['number']} - {pr['title']}\n"
            report += f"    Updated at: {pr['updated_at']}\n"
            report += f"    Author: {pr['user']}\n"
            report += f"    Link: {pr['html_url']}\n\n"
    
    return report

# Function to send the email
def send_email(to_address, from_address, subject, body):
    load_dotenv()
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Example for Gmail, adjust as necessary for your SMTP server
            server.starttls()
            server.login(from_address, os.getenv('EMAIL_PASSWORD'))  # Use environment variable for password
            server.send_message(msg)
            print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Generate a pull request report for a GitHub repository.")
    parser.add_argument("repo_url", help="GitHub repository URL (e.g., https://github.com/owner/repo)")
    parser.add_argument("from_address", help="Email address sending the report")
    parser.add_argument("to_address", help="Email address to send the report to")
    parser.add_argument("subject", help="Subject of the email", default="Weekly Pull Request Report")
    args = parser.parse_args()

    repo_name = args.repo_url.split('github.com/')[-1]

    # GitHub API endpoint
    api_url = f"https://api.github.com/repos/{repo_name}/pulls"

    # Headers for the API request
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # Parameters for the initial request
    params = {
        "sort": "updated",
        "per_page": 1,
        "direction": "desc",
        "state": "all",  # To include open and closed pull requests
        "page": 1
    }

    # Time delta to check if a pull request is within the last week
    one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)

    try:
        # Fetch and categorize pull requests
        open_prs, closed_prs = fetch_pull_requests(api_url, headers, params, one_week_ago)

        # Create the report
        report = create_report(repo_name, open_prs, closed_prs)

        # Print the report to the console
        print(report)

        # Send the email only if there are updated pull requests
        if open_prs or closed_prs:
            send_email(args.to_address, args.from_address, args.subject, report)
    except requests.RequestException as e:
        print(f"No pull requests found in the repository: {repo_name}. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
