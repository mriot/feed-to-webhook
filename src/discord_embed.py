def discord_embed(data):
    return [
        {
            "author": {
                "name": data.get("feed_owner"),
                "url": data.get("feed_owner_link"),
                # "icon_url": "https://i.imgur.com/R66g1Pe.jpg"
            },
            "title": data.get("post_title"),
            "url": data.get("post_url", ""),
            "description": data.get("post_description"),
            # "color": data.get("color", 0x00FF00),
            "image": {
                "url": data.get("enclosure")
            },
            "timestamp": data.get('post_date', ''),
        }
    ]


# TODO
def discord_embed2(data):
    keys = ["feed_owner", "feed_owner_link", "post_title", "post_url", "post_description", "enclosure", "post_date"]
    embed_dict = {key: data.get(key, '') for key in keys if key in data}

    embed = {
        "author": {
            "name": embed_dict.get("feed_owner"),
            "url": embed_dict.get("feed_owner_link"),
        },
        "title": embed_dict.get("post_title"),
        "url": embed_dict.get("post_url"),
        "description": embed_dict.get("post_description"),
        # "image": {
        #     "url": embed_dict.get("enclosure")
        # },
        "timestamp": embed_dict.get('post_date'),
    }

    # Remove keys with empty values
    embed = {key: value for key, value in embed.items() if value}

    return [embed]
