import argparse
import tomllib
from Utils.backendServer import BackendServer
from Utils.frontendServer import FrontendServer
import ollama
import logging


def main():
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # config
    with open("config.toml", "rb") as f:
        data = tomllib.load(f)

    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--from_version", type=str, help="Specify the from version", required=True
    )
    args = parser.parse_args()

    # Openapi Diff
    backend = BackendServer(args.from_version, data.get("backend-path"))
    backend.upgrade()
    diff = backend.get_openapi_diff()
    backend.downgrade()

    # frontend tree
    frontend = FrontendServer(data.get("frontend-path"))
    tree = frontend.get_tree()

    # Model Call
    logger.info("pulling model " + str(data.get("ollama-model")) + "...")

    modelfile = f"""
FROM {str(data.get("ollama-model"))}
SYSTEM You are a frontend Sofware Engineer expert in updating react application, you only answer with the asked format. you don't explain your answers. You don't format your answers.
"""
    ollama.create(model="gemma-frontend-engineer", modelfile=modelfile)

    # asking for the most probable files to change given a diff and the list of files
    content = f"""
    Your frontend react application has the following tree:
    
    {tree}
    
    The backend REST api specification changed, here is the diff of the openAPI file from the last version to the current one:
    
     {diff} 
     
     Give me a list ranking the files that are the most probable to need to change in your React App from highest to lowest, in the following format:
     [fileName1, fileName2, fileName3, ...]
     
     """
    
    logger.info(
        "asking for the most probable files to change given a diff and the list of files..."
    )
    print(
        ollama.chat(
            model="gemma-frontend-engineer",
            messages=[{"role": "user", "content": content}],
        )
    )


if __name__ == "__main__":
    main()
