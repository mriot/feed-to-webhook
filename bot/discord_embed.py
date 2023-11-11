def discord_embed(post_title, post_url, post_description, enclosure):
    return [
        {
            "title": post_title,
            "url": post_url,
            "description": post_description,
            "image": {
                "url": enclosure
            },
            "footer": {
                "text": "Posted at 2021-01-01 00:00:00"
            }
        }
    ]
