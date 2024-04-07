import subprocess
import os


class FrontendServer:
    folder_path = ""

    def __init__(self, folder_path):
        self.folder_path = folder_path

    def get_tree(self) -> str:
        """gets the tree of the backend server

        Returns:
            str: the tree of the backend server
        """
        result = subprocess.run(
            ["git", "ls-tree", "-r", "HEAD", "--name-only"],
            encoding="utf-8",
            cwd=self.folder_path,
            capture_output=True,
        )
        return result.stdout