from discord_embed import discord_embed
from feed import Feed


class RssFeed(Feed):
    def __init__(self, url, webhooks, embed_color=None, summarize=True):
        super().__init__(url, webhooks)
        self.embed_color = embed_color
        self.summarize = summarize

    def summarize_text(self):
        pass

    def prepare_content(self):
        d = self.feed_data_dict

        for item in self.feed_items[:5]:
            output = discord_embed({
                "feed_title": d.feed.get("title"),
                "feed_link": d.feed.get("link"),

                "post_title": item.item_root.get("title"),
                "post_link": item.item_root.get("link"),
                "post_description": item.item_root.get("description"),
                "post_enclosure": item.item_root.get("enclosure"),
                "post_date": str(item.get_pubdate()),

                "embed_color": self.embed_color
            })

            self.final_items_to_be_posted.append(output)

        return self
