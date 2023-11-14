# Feed to Webhook

A simple script that fetches twitter and other RSS feeds and sends their content to webhooks.  
It's meant to run on a Raspberry Pi and get activated by a cronjob.

>📌  
> On the initial run, nothing is posted to your webhooks. It retrieves the latest item from each feed and then starts monitoring for new posts.  
> Feed timestamps are automatically saved to `feed_timestamps.yaml`.

## Usage

> ❗ Requires Python 3.6 or higher

- Clone this project, optionally create a [virtual environment](https://docs.python.org/3/library/venv.html) and run `pip install -r requirements.txt` to install dependencies  
- Rename `config_template.yaml` to `config.yaml` and add your feeds
- On a Raspberry Pi you can use `crontab -e` to create a cronjob  
  E.g. `*/15 * * * * python3 {path_to_project}/src/main.py` (*every 15th minute*)  
  [Crontab Guru](https://crontab.guru/) can help with the syntax

## Config

Specify the feeds you want to subscribe to along with a webhook url in `config.yaml`.  
Additionally you can provide an error webhook that gets called if a feed could not be loaded.  

> ❗ Remember to rename `config_template.yaml` to `config.yaml` and make sure it's located in the `src/` directory.

``` yaml
rss_feeds:
  - url: https://example.com/rss.xml
    webhooks:
      - https://discord.com/api/webhooks/0123456789/acbdefghijklmnopqrstuvwxyz
    embed_color: fe0000
  
twitter_feeds:
  - url: https://nitter.example.com/some_user/rss
    webhooks: ### you can specify multiple webhooks ###
      - https://discord.com/api/webhooks/0123456789/acbdefghijklmnopqrstuvwxyz
      - https://discord.com/api/webhooks/0123456789/acbdefghijklmnopqrstuvwxyz
    include_retweets: true

error_webhook: https://discord.com/api/webhooks/0123456789/acbdefghijklmnopqrstuvwxyz
```

<details>
  <summary>👀 Config documentation</summary>

<br>

The config is divided into three main sections: `rss_feeds`, `twitter_feeds`, and `error_webhook`.

### `rss_feeds`

- `url`: URL of the RSS feed.
- `webhooks`: A list of webhook URLs. When a new item is found, a message will be sent to each of these webhooks.
- `embed_color`: The color to be used for the embed in the Discord message. This should be a hexadecimal color code without `#`.

### `twitter_feeds`

- `url`: URL of the Twitter feed.
- `webhooks`: A list of webhook URLs. When a new tweet is found, a message will be sent to each of these webhooks.
- `include_retweets`: A boolean value that determines whether retweets should be included.

### `error_webhook`

This section contains a single webhook URL. If an error occurs while processing the feeds, a message will be sent to this webhook.

</details>

---

### <img src="https://github.com/mriot/feed-to-webhook/assets/24588573/d1d57576-63ad-4a58-8eb2-e45d2e05e636" height="15" /> Twitter Feeds

Since Twitter.com doesn't offer (free) RSS feeds, you could use a community-run [Nitter](https://github.com/zedeus/nitter) instance instead. You can find a list of instances here <https://status.d420.de/>.  

Some platforms, like Discord or Telegram, don't show previews for Twitter links. But there's a cool service called [FixTweet](https://github.com/FixTweet/FixTweet) that can help with that.

> These public nitter instances shouldn't be used for scraping, as mentioned here <https://status.d420.de/about#api>.  
> If you plan to use this script on a larger scale, you might want to think about hosting your own nitter instance.

### <img src="https://github.com/mriot/feed-to-webhook/assets/24588573/8548a7e7-4f34-46f3-9adf-66f627ced6f9" height="15" /> RSS Feeds

This script also supports generic RSS feeds to be posted to discord.

## Resources

- Discord Webhooks guide <https://birdie0.github.io/discord-webhooks-guide/>
- FixTweet <https://github.com/FixTweet/FixTweet>
- Nitter Instance Uptime & Health <https://status.d420.de/>
- Crontab Guru <https://crontab.guru/>

## Todo / Ideas

- General
  - add error handling for posting to webhooks
  - "max post history" config setting (how many posts are made max; default is 5)
  - option to override bot name and avatar in discord (global and per feed)
  - remove/replace timezone info from timestamp (currently str replace)
- Twitter Feeds
  - custom embed color for twitter feed
  - show post publish date
