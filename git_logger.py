import os
import datetime
import requests


def get_changed_files(log_directory):
    changed_files = []
    today = datetime.date.today()
    for file_name in os.listdir(log_directory):
        file_path = os.path.join(log_directory, file_name)
        modified_time = datetime.datetime.fromtimestamp(
            os.path.getmtime(file_path)
        ).date()
        if modified_time == today:
            changed_files.append(file_path)
    print(f"Changed files: {changed_files}")
    return changed_files


def commit_to_github(
    repo_owner,
    repo_name,
    branch_name,
    github_token,
    commit_message,
    files,
    log_directory,
):
    if not files:
        print("No files have changed. Skipping commit.")
        return

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs/heads/{branch_name}"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Get the latest commit SHA for the branch
    response = requests.get(url, headers=headers)
    response_json = response.json()

    # Check if 'object' key exists in the response
    if "object" not in response_json:
        print("Error: 'object' key not found in response.")
        return

    latest_commit_sha = response_json["object"]["sha"]

    # Create a new tree with the updated files
    tree_data = {
        "base_tree": latest_commit_sha,
        "tree": [
            {
                "path": file_path.split("/")[-1],  # Only take the filename
                "mode": "100644",
                "content": open(file_path, "r").read(),
            }
            for file_path in files
        ],
    }
    response = requests.post(
        f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/trees",
        json=tree_data,
        headers=headers,
    )
    tree_sha = response.json()["sha"]
    commit_data = {
        "message": commit_message,
        "parents": [latest_commit_sha],
        "tree": tree_sha,
    }
    response = requests.post(
        f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/commits",
        json=commit_data,
        headers=headers,
    )
    commit_sha = response.json()["sha"]

    # Update the branch reference to the new commit
    ref_data = {"sha": commit_sha}
    response = requests.patch(url, json=ref_data, headers=headers)


if __name__ == "__main__":
    log_directory = "./"
    repo_owner = "namansehwal"
    repo_name = "Phishing-detection-based-Associative-Classification-data-mining"
    branch_name = "logs"
    github_token = "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"
    commit_message = "Added daily log entry"
    files = get_changed_files(log_directory)

    commit_to_github(
        repo_owner,
        repo_name,
        branch_name,
        github_token,
        commit_message,
        files,
        log_directory,
    )
