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

Olli uses TOML for it's configuration, below the headings such as `olli` correspond to the outer block and the keys inside to the inner block. For example, the `olli` configuration section has a key `interval_minutes`, which in code looks like:

```toml
[olli]
interval_minutes = 5
```

Configuration is validated on startup and if a key is missing or otherwise incorrectly formatted Olli will refuse to start with an error.

# File location

Olli searches several locations for a config file to simplify deployment.

An Olli config file can reside at:
- `olli.toml` (in the current working directory)
- `/config/olli.toml`
- `/olli/config.toml`
- `/etc/olli/config.toml`

The order above is the order that Olli searches for configuration files.

# Sections

## `olli`

`interval_minutes` (required): The interval that Olli should poll during, for example if this is set to 5 then Olli will search the logs for the past 5 minutes every 5 minutes and report.

### Tokens

Olli takes in a list of tokens to scan for, and each token has a set of configuration options. In the configuration file a set of tokens looks like:
```toml
[[olli.tokens]]
token = "ERROR"
color = "#ff5f5f"

[[olli.tokens]]
token = "INFO"
# When no color is provided it falls back to blurple.
```

Tokens accept a `token` and `color` key, the first one is required. `token` represents the phrase that should be searched for and `color` is a hex color (**with** hashtag) that will be used for the generated embeds.

## `loki`

`api_url`: The base URL of your Loki instance, for example `"http://localhost:3100/"`.

`jobs`: A list of jobs to filter for logs in, only services in this list will be searched for tokens. An example might be `jobs = ["default/bot", "default/site"]`.

`max_logs`: This is passed on to Loki to define the maximum number of logs that should be returned, it defaults to 5,000 (raised from the 100 default of Loki).

## `discord`

`webhook_url`: This should be a Discord webhook which Olli will POST to when a service has hit a token filter in the last interval. It is optional but if not specified **must be provided in the `WEBHOOK_URL` environment variable.**

# Putting it together

All together, a configuration file for Olli might look somethinng along the lines of:

```toml
[olli]
interval_minutes = 5

[loki]
api_url = "http://localhost:3100/"
jobs = [
    "default/bot"
]

[discord]
# The only Discord configuration option is webhook_url, which you can
# either specify here or in an environment variable called WEBHOOK_URL
# with the config file taking precedence.

[[olli.tokens]]
token = "ERROR"
color = "#ff5f5f"

[[olli.tokens]]
token = "WARN"
color = "#ffe24d"

[[olli.tokens]]
token = "INFO"
```
