# Feed to Webhook

A script that fetches RSS feeds and sends them to Discord using webhooks.  

>📌  
> On the initial run, nothing is posted to your webhooks.  
> It retrieves the latest update from each feed and then starts monitoring for new posts.  

## Usage

> ❗ Made with Python 3.9 to ensure compatibility with most Raspberry Pis.

- Download this project, optionally create a [virtual environment](https://docs.python.org/3/library/venv.html) and run `pip install -r requirements.txt` to install dependencies  
- In `src/` edit `config.json` to add your feeds and webhooks
- On a Raspberry Pi you can use `crontab -e` to create a cronjob  
  E.g. `*/15 * * * * python3 {path_to_project}/src/main.py` (*every 15th minute*)  
  [Crontab Guru](https://crontab.guru/) can help with the syntax
****
## Config

Add the feeds you want to subscribe to along with a webhook url to `config.json`.  

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

``` json
{
  "feeds": [
    {
      "url": "https://www.example.com/feed.rss",
      "webhooks": [
          "https://discord.com/api/webhooks/0123456789/acbdefghijklmnopqrstuvwxyz"
      ],
      "embed_color": "BAD455"
    },
  ],
  "error_webhook": "https://discord.com/api/webhooks/0123456789/acbdefghijklmnopqrstuvwxyz"
}
```
---

## Resources

- Discord Webhooks guide <https://birdie0.github.io/discord-webhooks-guide/>

See [requirements.txt](requirements.txt) for a list of dependencies.
