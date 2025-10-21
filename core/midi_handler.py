# SPDX-FileCopyrightText: binar1 2025
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import shutil
import json
from datetime import datetime
from utils.folderico import copy_folderico_files
from utils.file_ops import detect_genre


# ─── Preview Logic: Generate Treeview Rows ───────────────────
def get_preview_data(source, structure, naming):
    if not source:
        return []

    preview_rows = []

    for folder_path, dirs, files in os.walk(source):
        if any(f.lower().endswith((".mid", ".midi")) for f in files):
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


# ─── Organizing Logic ────────────────────────────────────────
def organize_midi_folder(
    source_folder,
    output_folder,
    mode="flat",
    structure="Flat",
    naming="Pack-MIDI",
    dry_run=False,
    copy_icons=True,
):
    print(f"Scanning for MIDI folders in: {source_folder}")
    print(f"Dry run is {'ON' if dry_run else 'OFF'}")

    if not os.path.exists(source_folder):
        print(f"Source folder does not exist: {source_folder}")
        return

    # ─── Prepare Log File ─────────────────────────────────────
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(output_folder, f"copy_log_{timestamp}.txt")
    log_lines = [f"{'Dry run' if dry_run else 'Actual copy'} session\n"]

    for root, dirs, files in os.walk(source_folder):
        midi_files = [f for f in files if f.lower().endswith(".mid")]

        if midi_files:
            # ─── Genre Detection and Folder Naming ───────────────
            rel_path = os.path.relpath(root, source_folder)
            pack_name = rel_path.split(os.sep)[0] if os.sep in rel_path else rel_path
            genre = detect_genre(pack_name)
            folder_name = os.path.basename(root)

            if naming == "Pack-MIDI":
                combined_name = f"{pack_name}-{folder_name}"
            elif naming == "Genre-Pack":
                combined_name = f"{genre}-{pack_name}"
            else:
                combined_name = folder_name

            if structure == "Flat":
                target_folder = os.path.join(output_folder, combined_name)
            else:
                target_folder = os.path.join(output_folder, genre, combined_name)
                # ─── Copy Folderico Files from Pack Root ─────────────────────
            pack_root = os.path.join(source_folder, pack_name)

            if copy_icons and not dry_run:
                # Copy all .ico files
                for file in os.listdir(pack_root):
                    if file.lower().endswith(".ico"):
                        icon_src = os.path.join(pack_root, file)
                        icon_dst = os.path.join(target_folder, file)
                        try:
                            shutil.copy2(icon_src, icon_dst)
                            print(f"Copied icon file: {icon_src} → {icon_dst}")
                            log_lines.append(f"{icon_src} → {icon_dst}")
                        except Exception as e:
                            print(f"Error copying icon file: {e}")

            if dry_run:
                print(f"[Dry Run] Would create: {target_folder}")
            else:
                os.makedirs(target_folder, exist_ok=True)

            for file in files:
                if file.lower().endswith((".mid", ".ico", ".ini")):
                    src_path = os.path.join(root, file)
                    dst_path = os.path.join(target_folder, file)

                    if dry_run:
                        print(f"[Dry Run] Would copy: {src_path} → {dst_path}")
                    else:
                        try:
                            shutil.copy2(src_path, dst_path)
                            print(f"Copied: {src_path} → {dst_path}")
                        except Exception as e:
                            print(f"Error copying {file}: {e}")
                    log_lines.append(f"{src_path} → {dst_path}")

            # ─── Copy Folderico Files from Pack Root ─────────────────────
            if copy_icons and not dry_run:
                # Copy all .ico files
                for file in os.listdir(pack_root):
                    if file.lower().endswith(".ico"):
                        icon_src = os.path.join(pack_root, file)
            icon_dst = os.path.join(target_folder, file)
            try:
                shutil.copy2(icon_src, icon_dst)
                print(f"Copied icon file: {icon_src} → {icon_dst}")
                log_lines.append(f"{icon_src} → {icon_dst}")
            except Exception as e:
                print(f"Error copying icon file: {e}")

            # Copy desktop.ini


if os.path.exists(ini_src):
    try:
        shutil.copy2(ini_src, ini_dst)
        print(f"Copied desktop.ini: {ini_src} → {ini_dst}")
        log_lines.append(f"{ini_src} → {ini_dst}")
    except Exception as e:
        print(f"Error copying desktop.ini: {e}")
    # ─── Write Log File ───────────────────────────────────────
    try:
        with open(log_path, "w", encoding="utf-8") as log_file:
            log_file.write("\n".join(log_lines))
        print(f"Log saved to: {log_path}")
    except Exception as e:
        print(f"Error writing log file: {e}")

    # ─── Save Genre Colors to Settings ────────────────────────
    settings_path = os.path.join(os.path.dirname(__file__), "..", "settings.json")
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
    except Exception:
        settings = {}

    settings["genre_colors"] = settings.get("genre_colors", {})
    settings["genre_colors"].update(GENRE_COLORS)

    try:
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
        print("Genre colors saved to settings.json")
    except Exception as e:
        print(f"Error saving genre colors: {e}")
