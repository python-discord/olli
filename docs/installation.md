---
layout: default
nav_order: 2
---

# Installation

## Docker

Olli is available as a Docker image hosted at `ghcr.io/python-discord/olli`.

There are several tags available (`ghcr.io/python-discord/olli:{tag}`):
- `:main` will track to the latest main commit to Olli.
- `:latest` will track to the latest release of Olli.
- `:<semver>` (e.g. `:0.0.1`) will track to a specific release of Olli.
- `:<sha>` will track to a specific commit to a specific commit to Olli.

Head to [ghcr.io/python-discord/olli](https://ghcr.io/python-discord/olli) to see all available versions.

Once you have a container image you need to configure it by placing a config file in a location described in [Configuration](./configuration.md).

## PyPI

Olli is available on PyPI under the [`olli`](https://pypi.org/project/olli/) package.

Install it with `pip install olli`. The PyPI version **only supports Python 3.9+**.

You should then be able to run `olli` (or sometimes `python -m olli`) to start Olli.

Once installed follow [Configuration](./configuration.md) to configure Olli to report.
