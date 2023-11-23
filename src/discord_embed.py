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
