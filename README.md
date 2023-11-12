# Feed to Webhook

A simple script that fetches RSS feeds and sends their content to webhooks.  
It's meant to run on a Raspberry Pi and get activated by a cronjob.

## Config

Specify the feeds you want to subscribe to along with a webhook url in `config.yaml`.  
Additionally you can provide an error webhook that gets called if a feed could not be loaded.  

> ❗ Make sure to place `config.yaml` in the `bot/` directory.

``` yaml
rss_feeds:
  - url: https://example.com/rss.xml
    webhooks:
      - https://discord.com/api/webhooks/0123456789/acbdefghijklmnopqrstuvwxyz
    embed_color: fe0000
  
twitter_feeds:
  - url: https://nitter.example.com/some_user/rss
    webhooks:
      - https://discord.com/api/webhooks/0123456789/acbdefghijklmnopqrstuvwxyz
      - https://discord.com/api/webhooks/0123456789/acbdefghijklmnopqrstuvwxyz
    include_retweets: true

error_webhook: https://discord.com/api/webhooks/0123456789/acbdefghijklmnopqrstuvwxyz
```

<details>
  <summary>👀 Config documentation</summary>

<br>

The config is divided into three main sections: `rss_feeds`, `twitter_feeds`, and `error_webhook`.

### rss_feeds

- `url`: URL of the RSS feed.
- `webhooks`: A list of webhook URLs. When a new item is found in the RSS feed, a message will be sent to each of these webhooks.
- `embed_color`: The color to be used for the embed in the Discord message. This should be a hexadecimal color code without `#`.
- [`last_item_date`]: *The date and time of the last post in the feed. Added automatically.*

### twitter_feeds

- `url`: URL of the Twitter feed. [See below about twitter feeds](#twitter-feeds)
- `webhooks`: A list of webhook URLs. When a new tweet is found, a message will be sent to each of these webhooks.
- `include_retweets`: A boolean value that determines whether retweets should be included.
- [`last_item_date`]: *The date and time of the last post in the feed. Added automatically.*

### error_webhook

This section contains a single webhook URL. If an error occurs while processing the feeds, a message will be sent to this webhook.

</details>

---

### Twitter Feeds

Since Twitter.com doesn't offer (free) RSS feeds, you could use a community-run [Nitter](https://github.com/zedeus/nitter) instance to get your RSS feeds. You can find a list of instances here <https://status.d420.de/>.  

Some platforms, like Discord or Telegram, don't show previews for Twitter links. But there's a cool service called [FixTweet](https://github.com/FixTweet/FixTweet) that can help with that.

#### Important

These public nitter instances shouldn't be used for scraping, as mentioned here <https://status.d420.de/about#api>.  
If you plan to use this script on a larger scale, you might want to think about hosting your own nitter instance.

### RSS Feeds

This script also supports generic RSS feeds to be posted to discord.

## Resources

- Discord Webhooks guide <https://birdie0.github.io/discord-webhooks-guide/>

## Todo / Ideas

- General
  - add error handling for posting to webhooks
  - "max post history" config setting (how many posts are made max; default is 5)
  - option to override bot name and avatar in discord (global and per feed)
- Twitter Feeds
  - custom embed color for twitter feed
  - show post publish date
