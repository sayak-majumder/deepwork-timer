import tkinter as tk            # Import the tkinter module for GUI
from tkinter import messagebox  # Import messagebox to show error messages or dialogs

# Define a class for the Pomodoro application.
class PomodoroApp:
    def __init__(self, master):
        # The constructor takes a 'master' widget (our main window)
        self.master = master
        master.title("DWT")  # Set the title of the window

        # State variables to track session data and timer status
        self.total_sessions = 0       # Total number of pomodoro sessions the user wants
        self.current_session = 0      # Which session we're currently in
        self.is_work_session = True   # Boolean flag: True for work, False for break
        self.time_left = 0            # Time left in the current session (in seconds)
        self.is_paused = False        # Boolean to know if the timer is paused
        self.timer_running = False    # Boolean to know if the timer is running

        # Create a title label at the top of the window
        self.label_title = tk.Label(master, text="Deep_Work_Timer", font=("Helvetica", 16))
        self.label_title.pack(pady=10)  # 'pack' adds it to the window with some vertical padding

        # Create a frame to hold the session input elements (label and entry)
        self.session_frame = tk.Frame(master)
        self.session_frame.pack(pady=5)

        # Label prompting the user to enter the number of sessions
        self.label_sessions = tk.Label(self.session_frame, text="Enter number of sessions:")
        self.label_sessions.pack(side=tk.LEFT)  # Place it to the left within the frame

        # Entry widget for user input (number of sessions)
        self.entry_sessions = tk.Entry(self.session_frame, width=5)
        self.entry_sessions.pack(side=tk.LEFT)

        # Start Button to begin the timer after entering sessions
        self.start_button = tk.Button(master, text="Start Session", command=self.start_session)
        self.start_button.pack(pady=5)

        # Label to display the countdown timer (initially 00:00)
        self.timer_label = tk.Label(master, text="00:00", font=("Helvetica", 48))
        self.timer_label.pack(pady=10)

        # Status label to display the current session type (work or break) and number
        self.status_label = tk.Label(master, text="", font=("Helvetica", 14))
        self.status_label.pack(pady=5)

        # Button to pause and resume the timer; initially disabled until the session starts
        self.pause_button = tk.Button(master, text="Pause", state=tk.DISABLED, command=self.pause_resume)
        self.pause_button.pack(pady=5)

        # Button to reset the session; also disabled initially
        self.reset_button = tk.Button(master, text="Reset", state=tk.DISABLED, command=self.reset)
        self.reset_button.pack(pady=5)

    def start_session(self):
        """
        This function is called when the user clicks the Start Session button.
        It reads the number of sessions, sets up the first work session,
        and begins the countdown.
        """
        try:
            self.total_sessions = int(self.entry_sessions.get())  # Convert input to an integer
            if self.total_sessions <= 0:
                raise ValueError  # Raise error if the number is not positive
        except ValueError:
            # Show an error message if input is invalid
            messagebox.showerror("Input Error", "Please enter a positive integer for sessions.")
            return

        # Initialization of the session state
        self.current_session = 1        # Start with the first session
        self.is_work_session = True     # Begin with a work session
        self.start_button.config(state=tk.DISABLED)      # Disable start button to avoid restarting
        self.entry_sessions.config(state=tk.DISABLED)      # Disable entry so user cannot change it mid-session
        self.pause_button.config(state=tk.NORMAL)          # Enable the pause button now that a session is active
        self.reset_button.config(state=tk.NORMAL)          # Enable the reset button

        # Update the status label to show that we are in a work session
        self.status_label.config(text=f"Session {self.current_session} - Work")
        self.time_left = 25 * 60  # Set timer for 25 minutes (25 * 60 seconds)
        self.timer_running = True  # Set the flag indicating the timer is running
        self.countdown()           # Start the countdown timer

    def countdown(self):
        """
        This method manages the countdown timer. It updates the GUI every second,
        and automatically transitions between work and break sessions.
        """
        # If paused or timer not running, do not continue updating the timer.
        if self.is_paused or not self.timer_running:
            return

        # Convert the remaining seconds into minutes and seconds format
        minutes, seconds = divmod(self.time_left, 60)
        # Update the timer label with formatted time (e.g., "24:59")
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

        if self.time_left > 0:
            # Decrease the time left by one second
            self.time_left -= 1
            # Schedule the countdown function to run again after 1000 milliseconds (1 second)
            self.master.after(1000, self.countdown)
        else:
            # When the timer reaches 0, decide what to do next:
            if self.is_work_session:
                # If it's a work session and there are still sessions remaining, start a break
                if self.current_session < self.total_sessions:
                    self.is_work_session = False  # Switch to break session
                    self.status_label.config(text=f"Session {self.current_session} - Break")
                    self.time_left = 5 * 60  # Set timer for 5 minutes (break)
                    self.master.after(1000, self.countdown)
                else:
                    # If it's the last work session, finish all sessions
                    self.finish_sessions()
            else:
                # If it's a break session, increment the session count and start a new work session
                self.current_session += 1
                self.is_work_session = True  # Switch back to work session
                if self.current_session <= self.total_sessions:
                    self.status_label.config(text=f"Session {self.current_session} - Work")
                    self.time_left = 25 * 60  # Reset timer for another 25-minute work session
                    self.master.after(1000, self.countdown)
                else:
                    # If for some reason we exceed the total sessions, finish sessions
                    self.finish_sessions()

    def pause_resume(self):
        """
        Toggles the pause/resume state of the timer.
        If the timer is paused, resume the countdown.
        If running, pause it.
        """
        if self.is_paused:
            # If already paused, then resume countdown
            self.is_paused = False
            self.pause_button.config(text="Pause")
            self.countdown()  # Continue the countdown
        else:
            # Otherwise, pause the timer
            self.is_paused = True
            self.pause_button.config(text="Resume")

    def finish_sessions(self):
        """
        Called when all work sessions are complete.
        Displays a motivational message and offers the option to start a new session.
        """
        self.timer_running = False  # Stop the timer
        self.status_label.config(text="Hurrah! You're one step away from becoming the best version of yourself!")
        self.pause_button.config(state=tk.DISABLED)  # Disable pause button when done
        # Create a new button that allows the user to start a new deep work session (which calls reset)
        self.new_session_button = tk.Button(self.master, text="Start New Deep Work Session", command=self.reset)
        self.new_session_button.pack(pady=10)

    def reset(self):
        """
        Resets the application to its initial state so the user can start over.
        """
        self.timer_running = False  # Stop any running timer
        self.is_paused = False        # Reset pause state
        self.current_session = 0      # Reset current session count
        self.total_sessions = 0       # Reset total sessions
        self.time_left = 0            # Reset timer
        self.timer_label.config(text="00:00")  # Reset the timer display
        self.status_label.config(text="")      # Clear the status label
        self.entry_sessions.config(state=tk.NORMAL)  # Enable the entry field again
        self.start_button.config(state=tk.NORMAL)    # Enable the start button
        self.pause_button.config(state=tk.DISABLED, text="Pause")  # Reset and disable pause button
        self.reset_button.config(state=tk.DISABLED)  # Disable the reset button
        # If the new session button exists, remove it from the GUI
        if hasattr(self, 'new_session_button'):
            self.new_session_button.destroy()

# Main part of the program: Create the window and run the application
if __name__ == "__main__":
    root = tk.Tk()              # Create the main window
    app = PomodoroApp(root)     # Instantiate the PomodoroApp with the main window
    root.mainloop()             # Start the Tkinter event loop (this keeps the window open)
    