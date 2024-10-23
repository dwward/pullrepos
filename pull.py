#!/usr/bin/env python3

import os
import subprocess
import yaml

# Function to clone or pull a repository
def clone_or_pull_repo(repo_url, repo_dir):
    if os.path.isdir(repo_dir):
        # Repository already exists, pull the latest changes
        print(f"Pulling updates for {os.path.basename(repo_dir)} in {os.path.dirname(repo_dir)}...")
        subprocess.run(["git", "-C", repo_dir, "pull"], check=True)
    else:
        # Repository does not exist, clone it
        print(f"Cloning {repo_url} into {os.path.dirname(repo_dir)}...")
        subprocess.run(["git", "clone", repo_url, repo_dir], check=True)

# Iterate over all directories (each group)
def process_groups(base_dir):
    for group in os.listdir(base_dir):
        group_dir = os.path.join(base_dir, group)
        if os.path.isdir(group_dir):
            yaml_file = os.path.join(group_dir, 'repos.yaml')
            if os.path.isfile(yaml_file):
                print(f"Processing group: {group}")

                # Load the YAML file and get the list of repositories
                with open(yaml_file, 'r') as file:
                    repos = yaml.safe_load(file)

                # Process each repository in the group
                for repo in repos.get('repositories', []):
                    repo_url = repo.get('url')
                    repo_name = os.path.basename(repo_url).replace('.git', '')
                    repo_dir = os.path.join(group_dir, repo_name)
                    
                    # Clone or pull the repository
                    clone_or_pull_repo(repo_url, repo_dir)
            else:
                print(f"No repos.yaml found in {group}. Skipping.")
        else:
            print(f"{group} is not a directory. Skipping.")

# Main function
if __name__ == "__main__":
    base_directory = os.path.abspath(".")  # Current directory as base
    process_groups(base_directory)
