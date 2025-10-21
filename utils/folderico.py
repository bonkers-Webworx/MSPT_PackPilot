import os
import shutil


def copy_folderico_files(source_folder, target_folder):
    """
    Copies .ico and .ini files from source_folder to target_folder.
    Used to preserve custom folder icons created with Folderico.
    """
    for ext in [".ico", ".ini"]:
        for file in os.listdir(source_folder):
            if file.lower().endswith(ext):
                src_path = os.path.join(source_folder, file)
                dst_path = os.path.join(target_folder, file)
                try:
                    shutil.copy2(src_path, dst_path)
                    print(f"Copied {file} to {target_folder}")
                except Exception as e:
                    print(f"Failed to copy {file}: {e}")
