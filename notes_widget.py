import tkinter as tk
from tkinter import ttk, messagebox
from notes_db import NotesDatabase

class NotesWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = NotesDatabase()
        self.current_note_id = None
        self.create_widgets()

    def create_widgets(self):
        # Left side - Notes list
        left_frame = ttk.Frame(self)
        left_frame.pack(side='left', fill='both', padx=5, pady=5)

        # Notes list
        self.notes_list = tk.Listbox(left_frame, width=40, height=20)
        self.notes_list.pack(fill='both', expand=True)
        self.notes_list.bind('<<ListboxSelect>>', self.on_select_note)

        # Right side - Note editor
        right_frame = ttk.Frame(self)
        right_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)

        # Title
        ttk.Label(right_frame, text="Title:").pack(anchor='w')
        self.title_entry = ttk.Entry(right_frame)
        self.title_entry.pack(fill='x', pady=(0, 10))

        # Content
        ttk.Label(right_frame, text="Content:").pack(anchor='w')
        self.content_text = tk.Text(right_frame, height=15)
        self.content_text.pack(fill='both', expand=True)

        # Buttons
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill='x', pady=10)

        ttk.Button(button_frame, text="New Note", command=self.new_note).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Save", command=self.save_note).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_note).pack(side='left', padx=5)

        self.refresh_notes_list()

    def refresh_notes_list(self):
        self.notes_list.delete(0, tk.END)
        notes = self.db.get_all_notes()
        for note in notes:
            self.notes_list.insert(tk.END, f"{note[1]} (ID: {note[0]})")

    def new_note(self):
        self.current_note_id = None
        self.title_entry.delete(0, tk.END)
        self.content_text.delete('1.0', tk.END)

    def save_note(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get('1.0', tk.END).strip()

        if not title:
            messagebox.showerror("Error", "Title is required!")
            return

        if self.current_note_id is None:
            self.db.add_note(title, content)
        else:
            self.db.update_note(self.current_note_id, title, content)

        self.refresh_notes_list()
        messagebox.showinfo("Success", "Note saved successfully!")

    def delete_note(self):
        if self.current_note_id is None:
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this note?"):
            self.db.delete_note(self.current_note_id)
            self.new_note()
            self.refresh_notes_list()

    def on_select_note(self, event):
        if not self.notes_list.curselection():
            return

        selection = self.notes_list.get(self.notes_list.curselection())
        note_id = int(selection.split("ID: ")[-1][:-1])
        note = self.db.get_note(note_id)
        
        self.current_note_id = note[0]
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, note[1])
        self.content_text.delete('1.0', tk.END)
        self.content_text.insert('1.0', note[2])