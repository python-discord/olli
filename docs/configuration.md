---
layout: default
nav_order: 3
title: Configuration
---

# Configuration
{: .no_toc }

Olli provides several configuration options to alter how the application behaves.

1. TOC
{:toc}

# File Format

Olli uses a .env file or environment variables for it's configuration, see `.env.example` for an example `.env` file. This file must either exist in the project root directory, or environment variables must be made available to the container.

Configuration is validated on startup and if a key is missing or otherwise incorrectly formatted Olli will refuse to start with an error.

# Sections

## `service`

`service_interval_minutes` (required): The interval that Olli should poll during, for example if this is set to 5 then Olli will search the logs for the past 5 minutes every 5 minutes and report.

### Tokens

Olli takes in a list of tokens to scan for, and each token is a JSON dictionary containing a set of configuration options. In the configuration file a set of tokens looks like:
```toml
service_tokens=[{"token":"ERROR","color":"#ff5f5f"},{"token":"WARN","color":"#ffe24d"},{"token":"INFO"}]
# When no color is provided it falls back to blurple.
```

Tokens accept a `token` and `color` key, the first one is required. `token` represents the phrase that should be searched for and `color` is a hex color (**with** hashtag) that will be used for the generated embeds.

Tokens also accept a `case_sensitive` key which defaults to `false`. If you want to match the case as written in the `token` field set `case_sensitive` to `true` in the token config.

## `loki`

`loki_api_url`: The base URL of your Loki instance, for example `http://localhost:3100`.

`loki_jobs`: A list of jobs to filter for logs in, only services in this list will be searched for tokens. An example might be `loki_jobs=default/bot,default/site`.

`loki_max_logs`: This is passed on to Loki to define the maximum number of logs that should be returned, it defaults to 5,000 (raised from the 100 default of Loki).

## `discord`

`discord_webhook_url` (required): This should be a Discord webhook which Olli will POST to when a service has hit a token filter in the last interval.

# Putting it together

All together, a configuration file for Olli might look something along the lines of:

```
loki_api_url=http://localhost:3100
loki_jobs=default/bot,default/site

discord_webhook_url=some_discord_webhook

service_interval_minutes=5
service_tokens=[{"token":"ERROR","color":"#ff5f5f"},{"token":"WARN","color":"#ffe24d"},{"token":"INFO"}]
```
