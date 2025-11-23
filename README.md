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
type: text # text or video
title: Sample Title
subreddit: test # Omit the r/ prefix
body: |
    Multi line strings in YAML start with the '|' prefix.
    Alternatively, you can use '>' instead of '|' if you don't want to preserve line breaks.
    Or you can leave this empty for no body
flair: Sample Flair # Optional. Use --flairs to get names
```

## Video posts and custom thumbnails

Video posts are configured similarly to text posts:

```yml
type: video
title: Sample Video
subreddit: test
video_path: /path/to/video.mp4
# thumbnail_path: /path/to/thumbnail.jpg  # Optional
```

If `thumbnail_path` is omitted, the tool will auto-generate a thumbnail from the first frame of the video using FFmpeg.

If you know the exact timestamp you want to use for the thumbnail, you can generate it yourself with FFmpeg and reference it in `thumbnail_path`:

```sh
ffmpeg -ss 00:00:05 -i /path/to/video.mp4 -frames:v 1 /path/to/thumbnail.jpg
```

- `-ss 00:00:05` is the timestamp (here, 5 seconds in).
- `-frames:v 1` extracts a single frame as an image.

Then point your YAML configuration at the generated image:

```yml
type: video
title: Sample Video
subreddit: test
video_path: /path/to/video.mp4
thumbnail_path: /path/to/thumbnail.jpg
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
