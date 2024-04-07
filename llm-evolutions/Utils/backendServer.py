import subprocess
import os


class BackendServer:
    current_version = 0
    __versions = [
        "v1.0.0",
        "v2.0.0",
        "v3.0.0",
        "v4.0.0",
        "v5.0.0",
        "v5.1.0",
        "v6.0.0",
        "v7.0.0",
        "v7.1.0",
        "v7.2.0",
        "v8.0.0",
        "v8.0.1",
        "v9.0.0",
        "v9.1.0",
        "v10.0.0",
    ]
    folder_path = ""

    def __init__(self, version, folder_path):
        self.current_version = self.__versions.index(version)
        self.folder_path = folder_path

    def upgrade(self):
        self.current_version = self.current_version + 1
        p = subprocess.run(
            [
                "git",
                "checkout",
                self.__versions[self.current_version],
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=self.folder_path,
        )

    def downgrade(self):
        self.current_version = self.current_version - 1
        p = subprocess.run(
            [
                "git",
                "checkout",
                self.__versions[self.current_version],
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=self.folder_path,
        )

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

    def get_openapi_diff(self) -> str:
        """gets the diff of the openapi file for the backend server between the current and previous version

        Returns:
            str: the diff of the openapi file
        """
        if self.current_version == 0:
            raise Exception("No previous version to compare to")
        result = subprocess.run(
            [
                "git",
                "diff",
                self.__versions[self.current_version - 1],
                "--",
                "src/docs/openapi.yaml",
            ],
            encoding="utf-8",
            cwd=self.folder_path,
            capture_output=True,
        )
        return result.stdout
