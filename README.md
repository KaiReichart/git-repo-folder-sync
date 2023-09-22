# Git Repo Sync CLI

The Git Repo Sync CLI is a command-line tool that allows you to load Git repositories specified in a YAML file and synchronize their contents to a local target folder. Additionally, it generates a lockfile containing repository information, including URLs, target folders, and commit hashes.

## Installation

Before using the Git Repo Sync CLI, ensure you have Python 3.x installed on your system. You can then install the required Python packages using pip:

```bash

pip install -r requirements.txt

```

## Usage

To use the Git Repo Sync CLI, follow these steps:

1. Create a YAML file (git_folder_dep.yaml) specifying the Git repositories and their details. Here is an example:

```yaml

dependencies:
  - url: https://github.com/yourusername/repo1.git
    subdirectory: src
    ref: main
    target: local/repo1
  - url: https://github.com/yourusername/repo2.git
    subdirectory: docs
    ref: develop
    target: local/repo2
```

2. Run the Git Repo Sync CLI:

```bash

python git_repo_sync.py

```

The tool will clone each Git repository, synchronize the specified subdirectory to the local target folder, and generate a lockfile (git_folder_dep.lock) in the following format:

```yaml

dependencies:
  - url: https://github.com/yourusername/repo1.git
    target: local/repo1
    hash: <commit_hash1>
  - url: https://github.com/yourusername/repo2.git
    target: local/repo2
    hash: <commit_hash2>

```

The --delete option is used with rsync, ensuring that files no longer present in the source directory are deleted in the target directory during synchronization.


## Configuration

You can customize the behavior of the Git Repo Sync CLI by editing the git_folder_dep.yaml file. Each repository entry includes the following details:


- url: The URL of the Git repository.
- subdirectory: The subdirectory within the repository to synchronize.
- ref: The Git branch, tag, or commit reference to checkout.
- target: The local target folder where the repository will be synchronized.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome!

## Support

If you have any questions or need assistance, please create an issue.

## Acknowledgments

The Git Repo Sync CLI is based on Git and rsync and built using ChatGPT.
