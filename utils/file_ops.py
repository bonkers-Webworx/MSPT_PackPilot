def detect_genre(pack_name):
    # Simple genre detection placeholder
    genre_map = {
        "Techno": "Techno",
        "House": "House",
        "Trap": "Trap",
        "Ambient": "Ambient"
    }
    for keyword in genre_map:
        if keyword.lower() in pack_name.lower():
            return genre_map[keyword]
    return "Unknown"
