def populate_tree():
    tree.delete(*tree.get_children())
    rows = get_preview_data(source_var.get(), structure_var.get(), naming_var.get())

    genre_filter = genre_filter_var.get()
    pack_keyword = pack_filter_var.get().lower()

    filtered_rows = []
    for src, dest in rows:
        pack_name = os.path.basename(os.path.dirname(src)).lower()
        genre = pack_name.split("-")[0] if "-" in pack_name else ""

        if genre_filter != "All" and genre.lower() != genre_filter.lower():
            continue
        if pack_keyword and pack_keyword not in pack_name:
            continue

        filtered_rows.append((src, dest))

    if not filtered_rows:
        messagebox.showinfo("Preview", "No matching folders found.")
        return

    pack_nodes = {}
    for src, dest in filtered_rows:
        pack_name = os.path.basename(os.path.dirname(src))
        folder_name = os.path.basename(src)

        genre_color = get_genre_color(pack_name)
        genre_tag = pack_name

        if pack_name not in pack_nodes:
            pack_nodes[pack_name] = tree.insert(
                "", "end", text=pack_name, values=("", ""), tags=(genre_tag,)
            )
            if genre_color:
                tree.tag_configure(genre_tag, background=genre_color)

        tree.insert(
            pack_nodes[pack_name], "end", text="", values=(folder_name, dest)
        )def populate_tree():
    tree.delete(*tree.get_children())
    rows = get_preview_data(source_var.get(), structure_var.get(), naming_var.get())

    genre_filter = genre_filter_var.get()
    pack_keyword = pack_filter_var.get().lower()

    filtered_rows = []
    for src, dest in rows:
        pack_name = os.path.basename(os.path.dirname(src)).lower()
        genre = pack_name.split("-")[0] if "-" in pack_name else ""

        if genre_filter != "All" and genre.lower() != genre_filter.lower():
            continue
        if pack_keyword and pack_keyword not in pack_name:
            continue

        filtered_rows.append((src, dest))

    if not filtered_rows:
        messagebox.showinfo("Preview", "No matching folders found.")
        return

    pack_nodes = {}
    for src, dest in filtered_rows:
        pack_name = os.path.basename(os.path.dirname(src))
        folder_name = os.path.basename(src)

        genre_color = get_genre_color(pack_name)
        genre_tag = pack_name

        if pack_name not in pack_nodes:
            pack_nodes[pack_name] = tree.insert(
                "", "end", text=pack_name, values=("", ""), tags=(genre_tag,)
            )
            if genre_color:
                tree.tag_configure(genre_tag, background=genre_color)

        tree.insert(
            pack_nodes[pack_name], "end", text="", values=(folder_name, dest)
        )