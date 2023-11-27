def discord_embed(data):
    keys = ["feed_title", "feed_link", "post_title", "post_link", "post_description", "embed_color", "post_enclosure", "post_date"]
    embed_dict = {key: data.get(key, '') for key in keys if key in data}

    embed = {
        "author": {
            "name": embed_dict.get("feed_title"),
            "url": embed_dict.get("feed_link"),
            # "icon_url": "https://i.imgur.com/R66g1Pe.jpg"
        },
        "title": embed_dict.get("post_title"),
        "url": embed_dict.get("post_link"),
        "description": embed_dict.get("post_description"),
        "color": int(str(embed_dict.get("embed_color") or "738adb"), 16),
        "image": {
            "url": embed_dict.get("post_enclosure")
        },
        "timestamp": embed_dict.get('post_date'),
    }

    # Remove keys with empty values
    embed = {key: value for key, value in embed.items() if value}

    return [embed]
