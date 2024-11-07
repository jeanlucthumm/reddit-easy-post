# reddit-easy-post

Define your Reddit post via YAML, run this script to post it to Reddit. Ideal for scheduling using external tool.

## Usage

1. Create a YAML file with the post contents
2. (Optional) List available flairs for target subreddit.
```sh
poetry run main --flairs <subreddit>
```
3. Run the script:
```sh
poetry run main --file <post-file.yaml>
```

## Input file format (YAML)

```yml
type: text # Only text currently supported
title: Sample Title
subreddit: test # Omit the r/ prefix
body: |
    Multi line strings in YAML start with the '|' prefix.
    Alternatively, you can use '>' instead of '|' if you don't want to preserve line breaks.
    Or you can leave this empty for no body
flair: f1905376-40e9-11e7-a0dc-0e2f53ef3712 # Optional. Use --flairs to get IDs
```

## Scheduling

Use any of the following tools to run the script on demand:

* `at`
* `cron`
* `systemd` timers

# Environment variables

| Variable         | Desc                     | Required |
|------------------|--------------------------|----------|
| REDDIT_USER      | Username                 | Yes      |
| REDDIT_PASS      | Password                 | Yes      |
| REDDIT_CLIENTID  | Reddit API Client ID     | Yes      |
| REDDIT_CLIENTSEC | Reddit API Client Secret | Yes      |

See the following for how to get `REDDIT_CLIENTID` and `REDDIT_CLIENTSEC`:

[https://www.reddit.com/r/redditdev/comments/hasnnc/where_do_i_find_the_reddit_client_id_and_secret](https://www.reddit.com/r/redditdev/comments/hasnnc/where_do_i_find_the_reddit_client_id_and_secret)
