# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

reddit-easy-post is a Python CLI tool that automates Reddit posting via YAML configuration files. It supports text and video posts with flair management and follow-up comments.

## Key Commands

### Development Environment
```bash
# Setup (using devenv)
devenv shell

# Install dependencies
poetry install

# Run the main script
poetry run main --file <post-file.yaml>

# List available flairs for a subreddit
poetry run main --flairs <subreddit>

# Generate example YAML configuration
poetry run main --example
```

### Code Quality Tools
```bash
# Format code
black reddit_easy_post/

# Sort imports
isort reddit_easy_post/

# Type checking
mypy reddit_easy_post/

# Static analysis
pyright reddit_easy_post/
```

## Architecture

### Core Components
- `reddit_easy_post/main.py`: Single-file application containing all functionality
- Configuration via YAML files (see `example/text-post.yaml`)
- Uses PRAW (Python Reddit API Wrapper) for Reddit interactions
- FFmpeg integration for video thumbnail generation

### Key Functions
- `load_config()`: Parses YAML configuration files
- `validate_config()`: Validates required fields and post types
- `get_reddit_instance()`: Creates authenticated Reddit client
- `submit_post()`: Handles text and video post submission
- `list_flairs()`: Retrieves available flairs for subreddits

### Post Types Supported
- **Text posts**: Title, body (optional), flair (optional)
- **Video posts**: Video file, auto-generated or custom thumbnail, flair (optional)

### Environment Variables Required
- `REDDIT_USER`: Reddit username
- `REDDIT_PASS`: Reddit password  
- `REDDIT_CLIENTID`: Reddit API client ID
- `REDDIT_CLIENTSEC`: Reddit API client secret

## Development Notes

### Dependencies
- Python 3.12+
- Poetry for dependency management
- PRAW for Reddit API access
- PyYAML for configuration parsing
- FFmpeg for video processing (available in devenv)

### Configuration Structure
YAML files must contain:
- `type`: "text" or "video"
- `title`: Post title
- `subreddit`: Target subreddit (without r/ prefix)

Optional fields:
- `body`: Post content (text posts)
- `video_path`: Path to video file (video posts)
- `flair`: Flair name (use `--flairs` to discover)
- `follow_up_comment`: Comment posted 30 seconds after submission
- `thumbnail_path`: Custom thumbnail (video posts, auto-generated if omitted)

### Error Handling
The application includes comprehensive error handling for:
- Missing environment variables
- Invalid YAML configuration
- Reddit API exceptions
- Video processing failures
- File system errors

### Development Environment
Uses devenv.nix for reproducible development environment with Python tooling (black, isort, mypy, pyright) and FFmpeg pre-configured.