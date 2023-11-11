# Feed to Webhook

A basic script that fetches RSS feeds and calls a webhook.  
It's meant to run on a Raspberry Pi and get activated by a cronjob.

## Config

Specify the feeds you want to subscribe to along with a webhook url in the [config.yaml](./config_template.yaml) file.  
Make sure to rename `config_template.yaml` to `config.yaml` and place it in the `bot/` directory.  
Additionally you can provide a webhook that gets called if a feed could not be loaded.

The script will edit the config file to store the last post date for each feed so it knows if something new was posted since the last update.

### Twitter Feeds

Some platforms, like Discord or Telegram, don't show previews for Twitter links. But there's a cool service called [FixTweet](https://github.com/FixTweet/FixTweet) that can help with that.

Since Twitter.com doesn't offer (free) RSS feeds, you could use a community-run [Nitter](https://github.com/zedeus/nitter) instance to get your RSS feeds. You can find a list of instances here <https://status.d420.de/>.

#### Important

These public nitter instances shouldn't be used for scraping, as mentioned here <https://status.d420.de/about#api>.  
If you plan to use this script on a larger scale, you might want to think about hosting your own nitter instance.

### RSS Feeds

This script also supports generic RSS feeds to be posted to discord.

## Todo / Ideas

- add error handling for posting to webhooks
- "max post history" config setting (how many posts are made max)
