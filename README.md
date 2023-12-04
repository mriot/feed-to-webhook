# Feed to Webhook

A script that fetches Twitter and RSS feeds and sends them to Discord using webhooks.  

>📌  
> On the initial run, nothing is posted to your webhooks.  
> It retrieves the latest item from each feed and then starts monitoring for new posts.  

## Usage

> ❗ Requires Python 3.6 or higher

- Download this project, optionally create a [virtual environment](https://docs.python.org/3/library/venv.html) and run `pip install -r requirements.txt` to install dependencies  
- In `src/` rename `config_template.yaml` to `config.yaml` and add your feeds
- On a Raspberry Pi you can use `crontab -e` to create a cronjob  
  E.g. `*/15 * * * * python3 {path_to_project}/src/main.py` (*every 15th minute*)  
  [Crontab Guru](https://crontab.guru/) can help with the syntax

## Config

Add the feeds you want to subscribe to along with a webhook url to `config.yaml`.  
More options can be found in the config documentation below.

<details>
  <summary>👀 Config documentation</summary>

<br>

The config is divided into three main sections: `twitter_feeds`, `rss_feeds` and `error_webhook`.  
Only `url` and `webhooks` are required for each feed.

#### `twitter_feeds`

- `url`: URL of the Twitter feed.
- `webhooks`: A list of webhook URLs. When a new tweet is found, a message will be sent to each of these webhooks.
- `embed_color` [**optional**]: The color to be used for the embed in the Discord message. This should be a hexadecimal color code **without** `#`. Default: `1DA1F2` (twitter blue).
- `exclude_retweets` [**optional**]: A boolean value that determines whether retweets should be excluded. Default: `false`.
- `override_domain` [**optional**]: Set to `False` to disable overriding or provide a domain name, such as `nitter.net`. Default: `twitter.com`.
  - When set to `False`, this option will preserve the original links to the Nitter instance that provides your feed.

#### `rss_feeds`

- `url`: URL of the RSS feed.
- `webhooks`: A list of webhook URLs. When a new item is found, a message will be sent to each of these webhooks.
- `embed_color` [**optional**]: The color to be used for the embed in the Discord message. This should be a hexadecimal color code **without** `#`. Default: `738adb` (discord blue).

#### `error_webhook`

- A single webhook URL. If an error occurs, a message will be sent to this webhook.

</details>

#### Example config

``` yaml
rss_feeds:
  - url: https://example.com/rss.xml
    webhooks:
      - https://discord.com/api/webhooks/0123456789/acbdefghijklmnopqrstuvwxyz
    
  - url: https://example.com/rss2.xml
    webhooks:
      - https://discord.com/api/webhooks/0123456789/acbdefghijklmnopqrstuvwxyz
    embed_color: fe0000


twitter_feeds:
  - url: https://nitter.example.com/some_user/rss
    webhooks:
      - https://discord.com/api/webhooks/0123456789/acbdefghijklmnopqrstuvwxyz
      - https://discord.com/api/webhooks/0123456789/acbdefghijklmnopqrstuvwxyz
    exclude_retweets: true
    embed_color: fe0000
    override_domain: "nitter.net"


error_webhook: https://discord.com/api/webhooks/0123456789/acbdefghijklmnopqrstuvwxyz
```

---

### <img src="https://github.com/mriot/feed-to-webhook/assets/24588573/d1d57576-63ad-4a58-8eb2-e45d2e05e636" height="15" /> Twitter Feeds

Since Twitter.com doesn't offer (free) RSS feeds, you can use a community-run [Nitter](https://github.com/zedeus/nitter) instance instead. You can find a list of instances here <https://status.d420.de/>.  

Note though that some instances might not provide RSS feeds.

> These public nitter instances shouldn't be used for scraping, as mentioned [here](https://status.d420.de/about#api).  
> If you plan to use this script on a larger scale, consider hosting your own Nitter instance.

### <img src="https://github.com/mriot/feed-to-webhook/assets/24588573/8548a7e7-4f34-46f3-9adf-66f627ced6f9" height="15" /> RSS Feeds

This script supports various RSS and Atom versions thanks to [feedparser](https://github.com/kurtmckee/feedparser).

## Resources

- Discord Webhooks guide <https://birdie0.github.io/discord-webhooks-guide/>
- Nitter Instance Uptime & Health <https://status.d420.de/>

See [requirements.txt](requirements.txt) for a list of dependencies.
