import tkinter as tk
from tkinter import ttk

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Application")
        self.geometry("300x200")
        
        # Main window content
        tk.Label(self, text="Main Application", font=('Arial', 16)).pack(pady=20)
        
        # Button to open timer window
        self.timer_btn = tk.Button(self, text="Open Timer", 
                                  command=self.open_timer_window)
        self.timer_btn.pack(pady=10)
        
        self.timer_window = None  # Keep reference to timer window
    
    def open_timer_window(self):
        # Check if timer window already exists
        if self.timer_window is None or not self.timer_window.winfo_exists():
            self.timer_window = TimerWindow(self)
        else:
            # If window exists, just bring it to front
            self.timer_window.lift()
            self.timer_window.focus_force()

class TimerWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Timer")
        self.geometry("300x200")
        
        # Make window stay on top (optional)
        # self.attributes('-topmost', True)
        
        # Timer variables
        self.time_left = 60
        self.timer_running = False
        self.after_id = None  # Store the after() ID for canceling
        
        # Timer display
        self.time_var = tk.StringVar()
        self.time_var.set("01:00")
        
        self.time_label = tk.Label(self, textvariable=self.time_var, 
                                  font=('Arial', 24))
        self.time_label.pack(pady=20)
        
        # Control buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        
        self.start_btn = tk.Button(button_frame, text="Start", 
                                  command=self.start_timer)
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = tk.Button(button_frame, text="Stop", 
                                 command=self.stop_timer)
        self.stop_btn.pack(side='left', padx=5)
        
        self.reset_btn = tk.Button(button_frame, text="Reset", 
                                  command=self.reset_timer)
        self.reset_btn.pack(side='left', padx=5)
        
        # Close button
        tk.Button(self, text="Close", command=self.destroy).pack(pady=10)
        
        # Handle window closing properly
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.countdown()
    
    def stop_timer(self):
        self.timer_running = False
        if self.after_id:
            self.after_cancel(self.after_id)
    
    def reset_timer(self):
        self.stop_timer()
        self.time_left = 60
        self.update_display()
    
    def countdown(self):
        if self.timer_running and self.time_left > 0:
            self.update_display()
            self.time_left -= 1
            self.after_id = self.after(1000, self.countdown)
        elif self.time_left <= 0:
            self.timer_running = False
            self.time_var.set("00:00")
            self.bell()  # System beep
            tk.messagebox.showinfo("Timer", "Time's up!", parent=self)
    
    def update_display(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        time_string = f"{minutes:02d}:{seconds:02d}"
        self.time_var.set(time_string)
    
    def on_closing(self):
        # Stop the timer when window is closed
        self.stop_timer()
        self.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()