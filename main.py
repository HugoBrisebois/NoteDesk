import tkinter as tk
from tkinter import ttk
from clock import Timer



class NoteDesk(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Tkinter App")
        self.geometry("650x600")

        # Store references to frames/widgets
        self.content = None
        self.timer_widget = None

        # Create a TaskBar
        self.draw_taskbar()
        self.main_window()

    def draw_taskbar(self):
        taskbar = ttk.Frame(self, width=150, height=600)
        taskbar.pack(side='left', fill='y', anchor='w')
        taskbar.pack_propagate(False)

        # Buttons
        tk.Button(taskbar, text="Home", command=self.show_home).grid(row=0, column=0, sticky="ew")
        tk.Button(taskbar, text="Tasks", command=self.show_tasks).grid(row=1, column=0, sticky="ew")
        tk.Button(taskbar, text="Timers", command=self.show_timer).grid(row=2, column=0, sticky="ew")
        tk.Button(taskbar, text="Notes", command=self.show_notes).grid(row=3, column=0, sticky="ew")
        taskbar.columnconfigure(0, weight=1)

    def main_window(self):
        # Content frame (right side)
        self.content = ttk.Frame(self, width=500, height=600)
        self.content.pack(side='right', fill='both', expand=True, anchor='e')
        self.content.pack_propagate(False)
        self.show_home()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()
        label = tk.Label(self.content, text="Welcome to the Productivity App!", font=("Arial", 18), justify="center")
        label.pack(pady=40)

    def show_tasks(self):
        self.clear_content()
        label = tk.Label(self.content, text="Tasks section coming soon.", font=("Arial", 16), justify="center")
        label.pack(pady=40)

    def show_notes(self):
        self.clear_content()
        from notes_widget import NotesWidget
        notes_widget = NotesWidget(self.content)
        notes_widget.pack(pady=20, padx=20, fill='both', expand=True)

    def show_timer(self):
        self.clear_content()
        from clock import Timer
        self.timer_widget = Timer(self.content)
        self.timer_widget.pack(pady=20)


if __name__ == "__main__":
    app = NoteDesk()
    app.mainloop()

