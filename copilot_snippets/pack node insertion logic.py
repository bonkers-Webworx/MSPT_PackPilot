genre_color = get_genre_color(pack_name)
genre_tag = pack_name  # Unique tag per pack

if pack_name not in pack_nodes:
    pack_nodes[pack_name] = tree.insert(
        "", "end", text=pack_name, values=("", ""), tags=(genre_tag,)
    )
    if genre_color:
        tree.tag_configure(genre_tag, background=genre_color)