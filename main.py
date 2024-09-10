import tkinter
import customtkinter
import requests
import re

# GitHub Personal Access Token (replace with your actual token)
GITHUB_TOKEN = "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"

# Function to trigger a GitHub Action for the given repository
def trigger_github_action():
    try:
        base_url = url_var.get()

        # Extract the owner and repository name from the URL using regex
        match = re.match(r"https://github\.com/([^/]+)/([^/]+)", base_url)
        if not match:
            output_label.configure(text="Invalid GitHub repository URL.")
            return
        
        owner, repo = match.groups()

        # GitHub API URL to trigger workflow dispatch
        workflow_file = "github-actions-demo.yml"  # Specify the workflow file or use the workflow ID
        api_url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_file}/dispatches"

        # Payload to trigger the action (target the branch to run the action on)
        payload = {
            "ref": "main",  # Branch name to trigger the action
        }

        # Headers to authorize the request
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
        }

        # Send POST request to trigger GitHub action
        response = requests.post(api_url, json=payload, headers=headers)
        
        if response.status_code == 204:
            output_label.configure(text="GitHub Action triggered successfully!")
        else:
            output_label.configure(text=f"Failed to trigger action: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        output_label.configure(text=f"Error triggering GitHub action: {e}")

# System Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

# App Frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("GitHub Action Trigger")

# UI elements
title = customtkinter.CTkLabel(app, text="Insert a GitHub repository link")
title.pack(padx=10, pady=10)

# Link input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack(padx=10, pady=10)

# Output label to display results
output_label = customtkinter.CTkLabel(app, text="")
output_label.pack(padx=10, pady=10)

# Trigger GitHub Action button
scanning = customtkinter.CTkButton(app, text="Trigger GitHub Action", command=trigger_github_action)
scanning.pack(padx=10, pady=10)

# Start the app's main loop
app.mainloop()
