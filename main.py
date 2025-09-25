import tkinter as tk
from tkinter import ttk
from timer import Timer



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

    def show_productivity(self):
        self.clear_content()
        
        # Create a paned window to allow resizable split view
        paned = ttk.PanedWindow(self.content, orient=tk.VERTICAL)
        paned.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tasks section at the top
        tasks_frame = ttk.LabelFrame(paned, text="Tasks")
        from tasks.task_widget import TaskWidget
        tasks_widget = TaskWidget(tasks_frame)
        tasks_widget.pack(pady=5, padx=5, fill='both', expand=True)
        paned.add(tasks_frame)
        
        # Notes section at the bottom
        notes_frame = ttk.LabelFrame(paned, text="Notes")
        from notes.notes_widget import NotesWidget
        notes_widget = NotesWidget(notes_frame)
        notes_widget.pack(pady=5, padx=5, fill='both', expand=True)
        paned.add(notes_frame)

    def show_timer(self):
        self.clear_content()
        from timer import Timer
        self.timer_widget = Timer(self.content)
        self.timer_widget.pack(pady=20)

    def show_tasks(self):
        self.clear_content()
        from tasks.task_widget import TaskWidget
        tasks_widget = TaskWidget(self.content)
        tasks_widget.pack(pady=20, padx=20, fill='both', expand=True)

    def show_notes(self):
        self.clear_content()
        from notes.notes_widget import NotesWidget
        notes_widget = NotesWidget(self.content)
        notes_widget.pack(pady=20, padx=20, fill='both', expand=True)


if __name__ == "__main__":
    app = NoteDesk()
    app.mainloop()

