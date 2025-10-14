import os
import shutil
import json
from tkinter import messagebox
from utils.file_ops import detect_genre

def get_preview_data(source, structure, naming):
    if not source:
        messagebox.showerror("Error", "Please select a source folder.")
        return []

    preview_rows = []

    for folder_path, dirs, files in os.walk(source):
        if any(f.lower().endswith(('.mid', '.midi')) for f in files):
            relative_path = os.path.relpath(folder_path, source)
            parts = relative_path.split(os.sep)
            pack_name = parts[0] if parts else "UnknownPack"
            folder_name = os.path.basename(folder_path)
            genre = detect_genre(pack_name)

            if naming == "Pack-MIDI":
                combined_name = f"{pack_name}-{folder_name}"
            elif naming == "Genre-Pack":
                combined_name = f"{genre}-{pack_name}"
            else:
                combined_name = folder_name

            if structure == "Flat":
                dest_path = combined_name
            else:
                dest_path = os.path.join(genre, combined_name)

            preview_rows.append((folder_path, dest_path))

    return preview_rows


    messagebox.showinfo("Preview", preview_text or "No MIDI folders found.")

def organize_midi_folders(source, destination, structure, naming, dry_run):
    if not source or not destination:
        messagebox.showerror("Error", "Please select both source and destination folders.")
        return

    folders_to_copy = []
    for folder_path, dirs, files in os.walk(source):
        if any(f.lower().endswith(('.mid', '.midi')) for f in files):
            folders_to_copy.append(folder_path)

    if not folders_to_copy:
        messagebox.showinfo("No MIDI", "No folders with MIDI files found.")
        return

    copied_folders = set()
    log_path = os.path.join(destination, "copy_log.txt")

    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"{'Dry run' if dry_run else 'Actual copy'} session\n\n")

        for folder_path in folders_to_copy:
            relative_path = os.path.relpath(folder_path, source)
            parts = relative_path.split(os.sep)
            pack_name = parts[0] if parts else "UnknownPack"
            folder_name = os.path.basename(folder_path)
            genre = detect_genre(pack_name)

            if naming == "Pack-MIDI":
                combined_name = f"{pack_name}-{folder_name}"
            elif naming == "Genre-Pack":
                combined_name = f"{genre}-{pack_name}"
            else:
                combined_name = folder_name

            if structure == "Flat":
                dest_path = os.path.join(destination, combined_name)
            else:
                dest_path = os.path.join(destination, genre, combined_name)

            log_file.write(f"{folder_path} → {dest_path}\n")
            copied_folders.add(folder_path)

            if not dry_run:
                os.makedirs(dest_path, exist_ok=True)
                for item in os.listdir(folder_path):
                    s = os.path.join(folder_path, item)
                    d = os.path.join(dest_path, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d)

    messagebox.showinfo("Done", f"{'Simulated' if dry_run else 'Copied'} {len(copied_folders)} MIDI folders.\nLog saved to copy_log.txt")
