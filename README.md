# reddit-easy-post

> [!IMPORTANT]
> Currently WIP, will remove this when ready to use. Feel free to file issues though!

Define your Reddit post via YAML, run this script to post it to Reddit.

## Input file format (YAML)

TODO

## Scheduling

Use any of the following tools to run the script on demand:

* `cron`
* `at`
* `systemd` timers

# Environment variables

| Variable         | Desc                     | Required |
|------------------|--------------------------|----------|
| REDDIT_USER      | Username                 | Yes      |
| REDDIT_PASS      | Password                 | Yes      |
| REDDIT_CLIENTID  | Reddit API Client ID     | Yes      |
| REDDIT_CLIENTSEC | Reddit API Client Secret | Yes      |
