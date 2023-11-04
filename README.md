# Feed to Webhook

A **super basic** script that fetches RSS feeds and calls a webhook.  
It's meant to run on a Raspberry Pi and get triggered by a cronjob.

## Config

Specify the feeds you want to subscribe to along with a webhook url in the [config.json](./config_template.json) file.  
Make sure to rename `config_template.json` to `config.json`.  
Additionally you can provide a webhook that gets called if a feed could not be loaded.

The script will edit the config file to store the last post date for each feed so it knows if something new was posted since the last update.

### Twitter Feeds

Some platforms, like Discord or Telefram, don't show previews for Twitter links. But there's a cool service called [FixTweet](https://github.com/FixTweet/FixTweet) that can help with that.

Add `is_twitter_feed: true` to the feed config to activate this feature.

Since Twitter.com doesn't offer (free) RSS feeds, you could use a community-run [Nitter](https://github.com/zedeus/nitter) instance to get your RSS feeds. You can find a list of instances here <https://status.d420.de/>.

#### Important

These public nitter instances shouldn't be used for scraping, as mentioned here <https://status.d420.de/about#api>.  
If you plan to use this script on a larger scale, you might want to think about hosting your own nitter instance.
