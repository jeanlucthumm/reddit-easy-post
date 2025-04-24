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


def list_flairs(reddit, subreddit_name):
    """
    List available flairs for the specified subreddit.
    """
    try:
        subreddit = reddit.subreddit(subreddit_name)
        flairs = list(subreddit.flair.link_templates.user_selectable())
        if not flairs:
            print(f"No available flairs found for r/{subreddit_name}.")
            return
        print(f"Available flairs for r/{subreddit_name}:")
        for flair in flairs:
            flair_text = flair.get("flair_text", "N/A")
            flair_id = flair.get("flair_template_id", "N/A")
            text_editable = flair.get("text_editable", False)
            print(f" - {flair_text} (ID: {flair_id}, Editable: {text_editable})")
    except Exception as e:
        print(f"Error fetching flairs for r/{subreddit_name}: {e}")
        sys.exit(1)


def generate_example_yaml():
    """
    Generate and print an example YAML configuration file.
    """
    example_config = """# Example Reddit post configuration

# Required fields
type: text                          # Post type (currently only 'text' is supported)
title: Your post title here         # Title of your Reddit post
subreddit: nameofsubreddit          # Subreddit to post to (without the r/)

# Optional fields
body: |
  This is the main content of your post.
  
  You can include multiple paragraphs.
  
  * Markdown formatting is supported
  * Like bullet points
  * And more

# Optional flair (use --flairs SUBREDDIT to see available flairs)
# flair: Discussion
"""
    print(example_config)


def submit_post(reddit, config):
    """
    Submit the post to Reddit based on the configuration.
    """
    try:
        subreddit = reddit.subreddit(config["subreddit"])

        # Handling flair
        flair_id = None
        flair_text = config.get("flair")
        if flair_text:
            flairs = list(subreddit.flair.link_templates.user_selectable())
            desired_flair = next(
                (flair for flair in flairs if flair.get("flair_text") == flair_text),
                None,
            )
            if desired_flair:
                flair_id = desired_flair.get("flair_template_id")
                if not flair_id:
                    print(f"Error: Flair ID not found for flair '{flair_text}'.")
                    sys.exit(1)
            else:
                print(
                    f"Error: Flair '{flair_text}' not found in r/{config['subreddit']}."
                )
                sys.exit(1)

        # Submit the post with or without flair
        if flair_id:
            submission = subreddit.submit(
                title=config["title"],
                selftext=config.get("body", ""),
                flair_id=flair_id,
            )
            print(f"Post submitted: {submission.url}")
            print(f"Flair '{flair_text}' applied.")
        else:
            submission = subreddit.submit(
                title=config["title"], selftext=config.get("body", "")
            )
            print(f"Post submitted: {submission.url}")

    except APIException as e:
        print(f"API Error submitting post: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error submitting post: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Submit a Reddit post or list available flairs for a subreddit."
    )

    # Create mutually exclusive group for command options
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="Path to the YAML configuration file.")
    group.add_argument(
        "--flairs", metavar="SUBREDDIT", help="List available flairs for a subreddit."
    )
    group.add_argument(
        "--example",
        action="store_true",
        help="Generate an example YAML configuration file.",
    )

    args = parser.parse_args()

    if args.example:
        # Generate example YAML configuration
        generate_example_yaml()
        return

    reddit = get_reddit_instance()

    if args.flairs:
        # List flairs for the specified subreddit
        list_flairs(reddit, args.flairs)
    elif args.file:
        # Proceed with submitting the post
        config = load_config(args.file)
        validate_config(config)
        submit_post(reddit, config)
