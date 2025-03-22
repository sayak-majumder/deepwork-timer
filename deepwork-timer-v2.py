import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import threading

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deep-Work-Timer")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Initialize variables
        self.work_time = 0
        self.break_time = 0
        self.total_sessions = 0
        self.current_session = 0
        self.timer_running = False
        self.paused = False
        self.remaining_time = 0
        self.timer_thread = None
        
        # Create GUI elements
        self.setup_ui()
        
    def setup_ui(self):
        # Title label
        self.title_label = tk.Label(self.root, text=" You're a champion!", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)
        
        # Timer display
        self.time_display = tk.Label(self.root, text="00:00", font=("Arial", 48))
        self.time_display.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Ready to start", font=("Arial", 12))
        self.status_label.pack(pady=5)
        
        # Session counter
        self.session_counter = tk.Label(self.root, text="Session: 0/0", font=("Arial", 12))
        self.session_counter.pack(pady=5)
        
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        # Create buttons
        self.start_button = tk.Button(button_frame, text="Start New Session", command=self.start_new_session, bg="#4CAF50", fg="white", width=15, height=2)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.pause_button = tk.Button(button_frame, text="Pause", command=self.pause_resume, bg="#FFC107", fg="white", width=15, height=2, state=tk.DISABLED)
        self.pause_button.grid(row=0, column=1, padx=5)
        
    def start_new_session(self):
        # Get user input for session parameters
        self.work_time = simpledialog.askinteger("Work Time", "Enter work time in minutes:", minvalue=1, maxvalue=120)
        if self.work_time is None:
            return
            
        self.break_time = simpledialog.askinteger("Break Time", "Enter break time in minutes:", minvalue=1, maxvalue=60)
        if self.break_time is None:
            return
            
        self.total_sessions = simpledialog.askinteger("Sessions", "Enter number of sessions:", minvalue=1, maxvalue=20)
        if self.total_sessions is None:
            return
        
        # Reset counters
        self.current_session = 1
        self.session_counter.config(text=f"Session: {self.current_session}/{self.total_sessions}")
        
        # Start the timer
        self.start_timer()
        
    def start_timer(self):
        # Enable pause button, disable start button
        self.pause_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)
        
        self.timer_running = True
        self.paused = False
        
        # Start timer in a separate thread to keep UI responsive
        self.timer_thread = threading.Thread(target=self.run_timer)
        self.timer_thread.daemon = True
        self.timer_thread.start()
    
    def run_timer(self):
        while self.current_session <= self.total_sessions and self.timer_running:
            # Work phase
            self.status_label.config(text=f"Working - Session {self.current_session}")
            self.root.update()
            self.countdown(self.work_time * 60)
            
            if not self.timer_running:
                break
                
            # Break phase
            if self.current_session < self.total_sessions:
                self.status_label.config(text=f"Break - Session {self.current_session}")
                self.root.update()
                self.countdown(self.break_time * 60)
                
            if not self.timer_running:
                break
                
            self.current_session += 1
            self.session_counter.config(text=f"Session: {self.current_session}/{self.total_sessions}")
            self.root.update()
        
        if self.current_session > self.total_sessions:
            # All sessions completed
            messagebox.showinfo("Congratulations!", "Hurrah! You're one step away from becoming the best version of yourself!")
            
        # Reset UI
        self.reset_ui()
            
    def countdown(self, seconds):
        self.remaining_time = seconds
        
        while self.remaining_time > 0 and self.timer_running:
            if not self.paused:
                mins, secs = divmod(self.remaining_time, 60)
                time_str = f"{mins:02d}:{secs:02d}"
                self.time_display.config(text=time_str)
                self.root.update()
                time.sleep(1)
                self.remaining_time -= 1
            else:
                # When paused, just update UI and wait
                self.root.update()
                time.sleep(0.1)
    
    def pause_resume(self):
        if self.paused:
            self.paused = False
            self.pause_button.config(text="Pause")
            self.status_label.config(text=f"Working - Session {self.current_session}")
        else:
            self.paused = True
            self.pause_button.config(text="Resume")
            self.status_label.config(text="Paused")
    
    def reset_ui(self):
        self.pause_button.config(state=tk.DISABLED, text="Pause")
        self.start_button.config(state=tk.NORMAL)
        self.status_label.config(text="Ready to start")
        self.session_counter.config(text="Session: 0/0")
        self.time_display.config(text="00:00")
        self.timer_running = False
        self.paused = False

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()