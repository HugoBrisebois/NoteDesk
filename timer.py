import tkinter as tk
from tkinter import ttk, messagebox
from timer_stats import TimerStats

class Timer(ttk.Frame):
    def __init__(self, parent=None, task_manager=None):
        super().__init__(parent)
        self.timer_running = False
        self.time_left = 0
        self.task_manager = task_manager
        self.current_task = None
        self.stats = TimerStats()
        self.task_var = tk.StringVar()  # Initialize task_var for all instances

        # Input frame
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Minutes:").grid(row=0, column=0)
        self.minutes_entry = tk.Entry(input_frame, width=5)
        self.minutes_entry.grid(row=0, column=1, padx=5)
        self.minutes_entry.insert(0, "5")

        tk.Label(input_frame, text="Seconds:").grid(row=0, column=2)
        self.seconds_entry = tk.Entry(input_frame, width=5)
        self.seconds_entry.grid(row=0, column=3, padx=5)
        self.seconds_entry.insert(0, "0")

        # Display
        self.time_var = tk.StringVar()
        self.time_var.set("05:00")
        self.time_label = tk.Label(self, textvariable=self.time_var, 
                                  font=('Arial', 24))
        self.time_label.pack(pady=20)

        # Progress bar (optional)
        self.progress = ttk.Progressbar(self, length=200, mode='determinate')
        self.progress.pack(pady=10)

        # Task selection
        if self.task_manager:
            task_frame = ttk.Frame(self)
            task_frame.pack(pady=10)
            tk.Label(task_frame, text="Link to task:").pack(side='left')
            self.task_var = tk.StringVar()
            self.task_combo = ttk.Combobox(task_frame, textvariable=self.task_var)
            self.task_combo.pack(side='left', padx=5)
            self.update_task_list()

        # Stats display
        self.stats_var = tk.StringVar()
        self.update_stats()
        tk.Label(self, textvariable=self.stats_var).pack(pady=5)

        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        self.set_btn = tk.Button(button_frame, text="Set Timer", 
                                command=self.set_timer)
        self.set_btn.pack(side='left', padx=5)

        self.start_btn = tk.Button(button_frame, text="Start", 
                                  command=self.start_timer)
        self.start_btn.pack(side='left', padx=5)

        self.stop_btn = tk.Button(button_frame, text="Stop", 
                                 command=self.stop_timer)
        self.stop_btn.pack(side='left', padx=5)

    def update_task_list(self):
        if not self.task_manager:
            return
        tasks = self.task_manager.get_all_tasks()
        self.task_combo['values'] = [f"{i}: {task.title}" for i, task in enumerate(tasks)]

    def get_selected_task_id(self):
        if not hasattr(self, 'task_var') or not self.task_var.get():
            return None
        try:
            task_value = self.task_var.get()
            if ':' not in task_value:
                return None
            return int(task_value.split(':')[0])
        except:
            return None

    def update_stats(self):
        stats = self.stats.get_daily_stats()
        self.stats_var.set(f"Today's focus time: {stats['total_duration']}")

    def set_timer(self):
        try:
            minutes = int(self.minutes_entry.get() or 0)
            seconds = int(self.seconds_entry.get() or 0)
            self.time_left = minutes * 60 + seconds
            self.initial_time = self.time_left
            self.update_display()
            self.update_progress()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

    def start_timer(self):
        if not self.timer_running and self.time_left > 0:
            self.timer_running = True
            self.countdown()

    def stop_timer(self):
        if self.timer_running:
            initial_time = int(self.minutes_entry.get()) * 60 + int(self.seconds_entry.get())
            elapsed_time = initial_time - self.time_left
            task_id = self.get_selected_task_id()
            self.stats.record_session(elapsed_time, task_id)
            self.update_stats()
        self.timer_running = False

    def countdown(self):
        if self.timer_running and self.time_left > 0:
            self.update_display()
            self.update_progress()
            self.time_left -= 1
            self.after(1000, self.countdown)
        elif self.time_left <= 0:
            self.timer_running = False
            self.time_var.set("00:00")
            self.progress['value'] = 100
            messagebox.showinfo("Timer", "Time's up!")

    def update_display(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        time_string = f"{minutes:02d}:{seconds:02d}"
        self.time_var.set(time_string)

    def update_progress(self):
        if hasattr(self, 'initial_time') and self.initial_time > 0:
            progress_percent = ((self.initial_time - self.time_left) / self.initial_time) * 100
            self.progress['value'] = progress_percent

# No main block needed for embeddable widget