from urllib.parse import urlparse, urlunparse
from feed import Feed
from discord_embed import discord_embed2


class TwitterFeed(Feed):
    def __init__(self, url, webhooks, include_retweets=True):
        super().__init__(url, webhooks)
        self.include_retweets = include_retweets

    def prepare_content(self):
        feed_owner = self.feed_data_dict.feed.get("title", "[unknown]")  # -> username / @username
        feed_owner_accountname = feed_owner.split(" / ")[-1]  # -> @username
        feed_owner_link = f"https://twitter.com/{feed_owner_accountname.replace('@', '')}"

        for item in self.feed_items[:5]:
            post_author = item.item_root.get("author")  # @username
            post_author_url = f"https://twitter.com/{post_author.replace('@', '')}" if post_author else ""
            post_url = item.item_root.get("link", "")
            post_url = urlunparse(urlparse(post_url)._replace(netloc="fxtwitter.com"))  # enables an embed view for twitter posts
            # TODO: differntiate between platforms (timestamp)
            # post_date = item.get_pubdate().strftime("%b %d, %Y %H:%M:%S")
            post_date = int(item.get_pubdate().timestamp())  # used with special discord syntax <t:timestamp>
            is_retweet = feed_owner.find(post_author) == -1 if feed_owner and post_author else False

            if is_retweet and not self.include_retweets:
                continue

            if is_retweet:
                output = f"♻️ [{feed_owner_accountname}](<{feed_owner_link}>) retweeted [{post_author}](<{post_author_url}>) at <t:{post_date}> \n{post_url}"
            else:
                output = f"📢 [{feed_owner_accountname}](<{feed_owner_link}>) tweeted at <t:{post_date}> \n{post_url}"

                # TODO: implement custom embed
                # output = discord_embed2({
                #     "feed_owner": feed_owner_accountname,
                #     "feed_owner_link": feed_owner_link,
                #     "post_title": feed_owner,
                #     "post_url": post_url,
                #     "post_description": "Lorem Ipsum",
                #     "enclosure": "",
                #     "post_date": str(item.get_pubdate()),
                # })

            self.final_items_to_be_posted.append(output)

        return self
