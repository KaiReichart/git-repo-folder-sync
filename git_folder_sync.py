import os
import yaml
import subprocess
import tempfile
from git import Repo

def load_repositories_from_yaml(file_path):
    try:
        with open(file_path, 'r') as yaml_file:
            data = yaml.safe_load(yaml_file)
            return data.get('dependencies', [])
    except Exception as e:
        print(f"Error loading YAML file: {str(e)}")
        return []

def get_commit_hash(repo):
    try:
        return repo.head.commit.hexsha
    except Exception as e:
        print(f"Error getting commit hash: {str(e)}")
        return None

def sync_git_repo(repo_url, subdirectory, ref, target, repository_data):
    try:
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Repo.clone_from(repo_url, temp_dir)
            repo.git.checkout(ref)

            source_path = os.path.join(temp_dir, subdirectory)
            if os.path.exists(source_path):
                # Create parent directories of the target if they don't exist
                os.makedirs(target, exist_ok=True)

                # Use rsync to sync the files to the target directory and delete extraneous files
                rsync_command = ["rsync", "-av", "--delete", source_path + "/", target]
                subprocess.run(rsync_command, check=True)
                print(f"Synchronized {source_path} to {target}")

                # Get the commit hash
                commit_hash = get_commit_hash(repo)
                if commit_hash:
                    # Append the repository data to the repository_data list
                    repository_data.append({"url": repo_url, "target": target, "hash": commit_hash})
            else:
                print(f"Subdirectory {source_path} does not exist in the repository.")
    except Exception as e:
        print(f"Error syncing repository: {str(e)}")

def write_lockfile(lockfile_path, repository_data):
    try:
        lockfile_content = {"dependencies": repository_data}
        with open(lockfile_path, 'w') as lockfile:
            yaml.dump(lockfile_content, lockfile, default_flow_style=False)
    except Exception as e:
        print(f"Error writing lockfile: {str(e)}")

def main():
    yaml_file = 'git_folder_dep.yaml'
    lockfile_path = 'git_folder_dep.lock'
    repositories = load_repositories_from_yaml(yaml_file)
    repository_data = []

    for repo_data in repositories:
        repo_url = repo_data.get('url')
        subdirectory = repo_data.get('subdirectory')
        ref = repo_data.get('ref')
        target = repo_data.get('target')

        if repo_url and subdirectory and ref and target:
            sync_git_repo(repo_url, subdirectory, ref, target, repository_data)
        else:
            print("Incomplete repository information. Skipping.")

    # Write the lockfile with all repository data
    write_lockfile(lockfile_path, repository_data)

if __name__ == '__main__':
    main()
