# ─────────────────────────────────────────────────────────────
# Genre coloring config
# ─────────────────────────────────────────────────────────────
GENRE_COLORS = {
    "trap": "#FFB6C1",
    "lofi": "#ADD8E6",
    "house": "#98FB98",
    "techno": "#FFD700",
    "ambient": "#D8BFD8",
    "drum": "#FFA07A"
}

# ─────────────────────────────────────────────────────────────
# Function: get_genre_color
# ─────────────────────────────────────────────────────────────
def get_genre_color(name):
    """Return a color based on genre keyword in name."""
    name_lower = name.lower()
    for genre, color in GENRE_COLORS.items():
        if genre in name_lower:
            return color
    return None