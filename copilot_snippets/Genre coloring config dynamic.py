import random

# ─────────────────────────────────────────────────────────────
# Genre coloring config (dynamic)
# ─────────────────────────────────────────────────────────────
GENRE_COLORS = {}

def generate_pastel_color():
    r = random.randint(150, 255)
    g = random.randint(150, 255)
    b = random.randint(150, 255)
    return f'#{r:02X}{g:02X}{b:02X}'

def get_genre_color(name):
    name_lower = name.lower()
    for genre in GENRE_COLORS:
        if genre in name_lower:
            return GENRE_COLORS[genre]

    possible_genre = name_lower.split("-")[0]
    if possible_genre not in GENRE_COLORS:
        GENRE_COLORS[possible_genre] = generate_pastel_color()
    return GENRE_COLORS[possible_genre]