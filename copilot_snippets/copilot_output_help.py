# ─────────────────────────────────────────────────────────────
# Function: show_output_mode_help
# ─────────────────────────────────────────────────────────────
def show_output_mode_help():
    messagebox.showinfo(
        "Output Mode Options",
        "Flat: All folders go directly into the destination.\n"
        "Nested by Genre: Folders are grouped by genre.\n"
        "Nested by Pack: Folders are grouped by pack name."
    )

# ─────────────────────────────────────────────────────────────
# GUI: Output Mode Help Button
# ─────────────────────────────────────────────────────────────
ctk.CTkButton(root, text="ℹ️", width=30, command=show_output_mode_help).grid(row=6, column=2, padx=5)