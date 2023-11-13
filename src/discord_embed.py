def discord_embed(data):
    return [
        {
            "author": {
                "name": data["feed_owner"],
                "url": data["feed_owner_link"],
                # "icon_url": "https://i.imgur.com/R66g1Pe.jpg"
            },
            "title": data["post_title"],
            "url": data.get("post_url", ""),
            "description": data["post_description"],
            "color": data["color"],
            "image": {
                "url": data["enclosure"]
            },
            "timestamp": data.get('post_date', ''),
        }
    ]
