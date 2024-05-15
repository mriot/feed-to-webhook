# FTW - Feed to Webhook

Simple RSS feed aggregator for tiny servers like a Raspberry Pi, sending new posts to Discord webhooks.

<img src="https://github.com/mriot/feed-to-webhook/assets/24588573/ae48bf39-09c1-43ca-a0eb-cb59f5ebf4a5" height="400">

## Setup

> 📌 Made with Python 3.9 to ensure compatibility with most Raspberry Pis.

- Download this project, optionally create a [virtual environment](https://docs.python.org/3/library/venv.html) and run `pip install -r requirements.txt` to install dependencies  
- Edit `config.json` to add your feeds and [webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
- Run `python3 src/main.py` to let it create the `feed_timestamps.json` file
- Check the console output for any errors
- On a Raspberry Pi you can use `crontab -e` to create a cronjob  
  E.g. `*/15 * * * * python3 {path_to_project}/src/main.py` (*every 15th minute*)  
  [Crontab Guru](https://crontab.guru/) can help with the syntax

## Config

Add the feeds you want to subscribe to along with one or more webhook urls to `config.json`.  

#### Feeds

| Parameter     | Description                                       | Default                 |
| ------------- | ------------------------------------------------- | ----------------------- |
| `url`         | URL of the RSS feed.                              | -                       |
| `webhooks`    | List of webhook URLs to which new posts are sent. | -                       |
| `embed_color` | Color for Discord embed (hex code, without `#`).  | `738adb` (discord blue) |

#### Misc options

| Parameter       | Description                                                                       | Default |
| --------------- | --------------------------------------------------------------------------------- | ------- |
| `error_webhook` | A single webhook URL. If an error occurs, a message will be sent to this webhook. | -       |

#### Example config

> 📌 You can use C-style comments in the config. Both `//` and `/* */` are supported.

``` json
{
    "feeds": [
        {
            "url": "https://www.example.com/feed.rss",
            "webhooks": [
                "https://discord.com/api/webhooks/0123456789/acbdefghijklmnopqrstuvwxyz",
                "https://discord.com/api/webhooks/9876543210/acbdefghijklmnopqrstuvwxyz"
            ],
            "embed_color": "BAD455"
        }
    ],
    "error_webhook": "https://discord.com/api/webhooks/0123456789/acbdefghijklmnopqrstuvwxyz"
}
```
---

## Resources

- Discord Webhooks guide <https://birdie0.github.io/discord-webhooks-guide/>

See [requirements.txt](requirements.txt) for a list of dependencies.
