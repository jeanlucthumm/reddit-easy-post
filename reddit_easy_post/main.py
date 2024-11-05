import argparse
import os
import sys

import praw
import yaml
from praw.exceptions import APIException, PRAWException


def load_config(file_path):
    """
    Load and parse the YAML configuration file.
    """
    try:
        with open(file_path, "r") as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)


def validate_config(config):
    """
    Validate the required fields in the configuration.
    """
    required_fields = ["type", "title", "subreddit"]
    for field in required_fields:
        if field not in config:
            print(f"Error: Missing required field '{field}' in configuration.")
            sys.exit(1)
    if config["type"] != "text":
        print(
            f"Error: Unsupported post type '{config['type']}'. Only 'text' is supported."
        )
        sys.exit(1)


def get_reddit_instance():
    """
    Create and return a Reddit instance using PRAW.
    """
    try:
        reddit = praw.Reddit(
            username=os.environ["REDDIT_USER"],
            password=os.environ["REDDIT_PASS"],
            client_id=os.environ["REDDIT_CLIENTID"],
            client_secret=os.environ["REDDIT_CLIENTSEC"],
            user_agent="reddit-easy-post by /u/{}".format(os.environ["REDDIT_USER"]),
        )
        return reddit
    except KeyError as e:
        print(f"Error: Missing environment variable {e}")
        sys.exit(1)
    except PRAWException as e:
        print(f"Error initializing Reddit instance: {e}")
        sys.exit(1)


def submit_post(reddit, config):
    """
    Submit the post to Reddit based on the configuration.
    """
    try:
        subreddit = reddit.subreddit(config["subreddit"])
        submission = subreddit.submit(
            title=config["title"], selftext=config.get("body", "")
        )
        print(f"Post submitted: {submission.url}")

        if "flair" in config and config["flair"]:
            try:
                submission.flair.choose(config["flair"])
                print(f"Flair '{config['flair']}' applied.")
            except APIException as e:
                print(f"Error applying flair: {e}")

    except Exception as e:
        print(f"Error submitting post: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Submit a Reddit post based on a YAML configuration file."
    )
    parser.add_argument(
        "--file", required=True, help="Path to the YAML configuration file."
    )
    args = parser.parse_args()

    config = load_config(args.file)
    validate_config(config)
    reddit = get_reddit_instance()
    submit_post(reddit, config)


if __name__ == "__main__":
    main()
