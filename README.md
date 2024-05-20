# FTW - Feed to Webhook

This RSS feed aggregator is designed to run on a Raspberry Pi or a similar device, allowing you to monitor RSS feeds and send new posts to [Discord webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks). It's lightweight, easy to set up, and does not require a database whatsoever.

The frequency of how often feeds are checked is set through a [cronjob](https://en.wikipedia.org/wiki/Cron) schedule, which can be adjusted to your liking.

## Features

- Flexible, can parse a wide range of feed types
- [ETag and Last-Modified](https://feedparser.readthedocs.io/en/latest/http-etag.html) support to reduce bandwidth usage
- Customizable embed colors and icons for each feed
- Optional error webhook to get notified of any issues
- Does not consume any resources outside the scheduled runs

## Setup

> 📌 Made with Python 3.9 to ensure compatibility with most Raspberry Pis.

- Download this project and run `pip install -r requirements.txt` to install dependencies  
- Edit `config.json` to add your feeds and webhooks
- Run `python src/main.py` once to let it create a `timestamps.json` file
- Check the console output for any errors
- On a Raspberry Pi you can use `crontab -e` to create a cronjob  
  E.g. `*/15 * * * * python3 {path_to_project}/src/main.py` (*every 15th minute*)  
  [Crontab Guru](https://crontab.guru/) can help with the syntax

## Config

#### Feeds

> 📌 Only `url` and `webhooks` are required.

| Parameter     | Description                                           | Default                    |
| ------------- | ----------------------------------------------------- | -------------------------- |
| `url`         | URL of the RSS feed.                                  | -                          |
| `webhooks`    | List of webhook URLs to which new posts are sent.     | -                          |
| `embed_color` | Color for Discord embed (hex code, without `#`).      | `738ADB` (discord blue)    |
| `icon_url`    | Alternative icon that will be displayed in the embed. | Usually the feed's favicon |

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

## Embed design

Most embeds consist of an icon along with the feed's title, a heading to the article, some text, and an image. In the footer, you'll find the feed's source and the date of the article.

- The icon typically comes from the feed itself (or defaults to the website's favicon), but you can override this in the config to use a custom icon.

- If any images are found within the article, the first one will be used as the embed's image.

### Example

![example embed](https://github.com/mriot/feed-to-webhook/assets/24588573/2de472c9-1429-4119-bb74-a68a9ba93fbc)

---

## Resources

- Discord Webhooks guide <https://birdie0.github.io/discord-webhooks-guide/>

See [requirements.txt](requirements.txt) for a list of dependencies.
