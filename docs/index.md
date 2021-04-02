---
layout: default
nav_order: 1
---

# Olli

> *Olli searches your Loki logs and relays matching terms to Discord.*

Olli is the tool that bridges the gap between Discord and Loki, providing alerts to a configured Discord webhook when certain search phrases appear in your accumulated Loki logs.

{:refdef: style="text-align: center;"}
![olli demo](https://i.imgur.com/hWMq9xk.png){: width="300" }
{: refdef}

Olli searches for configured terms through the provided Loki data source at a configured interval (see more in [Configuration](./configuration.md)). When it finds that a certain token has been mentioned in the last period it will send a report through to Discord.

To get started with Olli head to the [Installation](./installation.md) page.
