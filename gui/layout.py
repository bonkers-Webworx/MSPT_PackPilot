import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import tkinter.font as tkfont
import json
import os

from logic.midi import get_preview_data, organize_midi_folders

def show_naming_help():
    messagebox.showinfo("Naming Options", 
        "Pack-MIDI: Combines pack and folder name (e.g., Drums01-KickLoops)\n"
        "Genre-Pack: Combines genre and pack name (e.g., HipHop-Drums01)\n"
        "Folder Only: Uses just the folder name (e.g., KickLoops)"
    )

def launch_gui():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("MSPT PackPilot")
    root.geometry("800x600")

    # Load settings
    settings_path = "settings.json"
    if os.path.exists(settings_path):
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
    else:
        settings = {
            "structure": "Flat",
            "naming": "Pack-MIDI",
            "dry_run": False,
            "font_size": 12
        }

    # Font for Treeview
    tree_font = tkfont.Font(family="Segoe UI", size=settings.get("font_size", 12))
    header_font = tkfont.Font(family="Segoe UI", size=settings.get("font_size", 12) + 2, weight="bold")
    row_height = int(settings.get("font_size", 12) * 1.8)

    style = ttk.Style()
    style.configure("Custom.Treeview", font=tree_font, rowheight=row_height)
    style.configure("Custom.Treeview.Heading", font=header_font)

    # Variables
    source_var = ctk.StringVar()
    destination_var = ctk.StringVar()
    structure_var = ctk.StringVar(value=settings["structure"])
    naming_var = ctk.StringVar(value=settings["naming"])
    dry_run_var = ctk.BooleanVar(value=settings["dry_run"])
    font_size_var = ctk.IntVar(value=settings.get("font_size", 12))
    genre_filter_var = ctk.StringVar(value="All")
    pack_filter_var = ctk.StringVar()
    output_mode_var = ctk.StringVar(value="Flat")

    def save_settings():
        new_settings = {
            "structure": structure_var.get(),
            "naming": naming_var.get(),
            "dry_run": dry_run_var.get(),
            "font_size": font_size_var.get()
        }
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(new_settings, f, indent=4)

    def update_font_size():
        new_size = font_size_var.get()
        tree_font.configure(size=new_size)
        header_font.configure(size=new_size + 2)
        style.configure("Custom.Treeview", rowheight=int(new_size * 1.8))
        style.configure("Custom.Treeview.Heading", font=header_font)

        settings["font_size"] = new_size
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)

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

            if pack_name not in pack_nodes:
                pack_nodes[pack_name] = tree.insert("", "end", text=pack_name, values=("", ""))

            tree.insert(pack_nodes[pack_name], "end", text="", values=(folder_name, dest))

    # Layout
    ctk.CTkLabel(root, text="Source Folder").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ctk.CTkEntry(root, textvariable=source_var, width=400).grid(row=0, column=1)
    ctk.CTkButton(root, text="Browse", command=lambda: source_var.set(filedialog.askdirectory())).grid(row=0, column=2)

    ctk.CTkLabel(root, text="Destination Folder").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    ctk.CTkEntry(root, textvariable=destination_var, width=400).grid(row=1, column=1)
    ctk.CTkButton(root, text="Browse", command=lambda: destination_var.set(filedialog.askdirectory())).grid(row=1, column=2)

    ctk.CTkLabel(root, text="Structure").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    ctk.CTkComboBox(root, variable=structure_var, values=["Flat", "Nested"], width=400).grid(row=2, column=1)

    ctk.CTkLabel(root, text="Naming").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    ctk.CTkComboBox(root, variable=naming_var, values=["Pack-MIDI", "Genre-Pack", "Folder Only"], width=400).grid(row=3, column=1)
    ctk.CTkButton(root, text="ℹ️", width=30, command=show_naming_help).grid(row=3, column=2, padx=5)

    ctk.CTkLabel(root, text="Genre Filter").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    ctk.CTkComboBox(root, variable=genre_filter_var, values=["All", "HipHop", "Trap", "EDM", "House"], width=400).grid(row=4, column=1)

    ctk.CTkLabel(root, text="Pack Name Filter").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    ctk.CTkEntry(root, textvariable=pack_filter_var, width=400).grid(row=5, column=1)

    ctk.CTkLabel(root, text="Output Mode").grid(row=6, column=0, padx=10, pady=5, sticky="w")
    ctk.CTkComboBox(root, variable=output_mode_var, values=["Flat", "Nested by Genre", "Nested by Pack"], width=400).grid(row=6, column=1)

    ctk.CTkLabel(root, text="Font Size").grid(row=7, column=0, padx=10, pady=5, sticky="w")
    font_slider = ctk.CTkSlider(root, from_=10, to=24, variable=font_size_var, number_of_steps=14)
    font_slider.grid(row=7, column=1, sticky="ew")

    ctk.CTkButton(root, text="Preview", command=populate_tree).grid(row=8, column=0, pady=20)
    ctk.CTkButton(root, text="Organize", command=lambda: [save_settings(), organize_midi_folders(
        source_var.get(), destination_var.get(), structure_var.get(), naming_var.get(), dry_run_var.get()
    )]).grid(row=8, column=1)
    ctk.CTkButton(root, text="Apply Font Size", command=update_font_size).grid(row=8, column=2, pady=20)

    # Treeview frame
    tree_frame = ctk.CTkFrame(root)
    tree_frame.grid(row=9, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    tree = ttk.Treeview(tree_frame, columns=("Folder", "Destination"), show="tree headings", style="Custom.Treeview")
    tree.heading("#0", text="Pack")
    tree.heading("Folder", text="Folder")
    tree.heading("Destination", text="Destination Path")
    tree.column("#0", width=150)
    tree.column("Folder", width=200)
    tree.column("Destination", width=400)
    tree.pack(fill="both", expand=True)

    root.grid_rowconfigure(9, weight=1)
    root.grid_columnconfigure(1, weight=1)

    root.mainloop()