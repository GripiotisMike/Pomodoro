# Import necessary libraries
from tkinter import *
import math
from tkinter import messagebox

# ---------------------------- CONSTANTS ------------------------------- #
# Define color constants for the UI
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

# Define time constants (in minutes)
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# Variables to track the state of the timer
reps = 0  # The number of repetitions of work/break cycles
timer = None  # To hold the timer object for canceling it
marks = ""  # Holds check marks to indicate completed work sessions

# ---------------------------- TIMER RESET ------------------------------- #
def reset():
    global reps
    global timer
    global marks
    marks = ""  # Reset the check marks
    reps = 0  # Reset repetitions
    window.after_cancel(timer)  # Cancel any ongoing timer
    canvas.itemconfig(timer_text, text="00:00")  # Reset the time display to 00:00
    timer_label.config(text="Timer")  # Reset the timer label
    check_marks.config(text="")  # Clear the check marks

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    global marks
    marks = ""  # Clear marks for a new session
    reps += 1  # Increment the repetition count
    
    # Convert the minutes to seconds for countdown
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    
    # Check the repetition count to determine whether it's work or break time
    if reps % 8 == 0:
        count_down(long_break_sec)  # Long break every 8th repetition
        timer_label.config(text="BIG BREAK!", fg=RED)  # Update label to indicate break time
        messagebox.showinfo("Time for your long break!")  # Display a messagebox alert
    elif reps % 2 == 0 and reps != 8:
        count_down(short_break_sec)  # Short break after every even repetition
        timer_label.config(text="Break!", fg=PINK)  # Update label to indicate break time
        messagebox.showinfo("Time for a break")  # Display a messagebox alert
    else:
        count_down(work_sec)  # Start work session
        timer_label.config(text="Work Work Work", fg=GREEN)  # Update label for work time
        messagebox.showinfo("Time to get back to work!")  # Display a messagebox alert

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer
    global marks
    
    # Convert the time in seconds to minutes and seconds
    count_min = math.floor(count / 60)
    count_sec = count % 60
    
    # Add leading zeros if the time is less than 10
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    if count_min < 10:
        count_min = f"0{count_min}"
    
    # Update the timer display on the canvas
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    
    # If time is not yet zero, continue countdown
    if count > 0:
        timer = window.after(1000, count_down, count - 1)  # Call the function every second
    else:
        start_timer()  # Once countdown is finished, start the next session
        # Add check marks after every work session
        for i in range(math.floor(reps / 2)):
            marks += "✓"
        check_marks.config(text=marks)  # Display check marks for completed work sessions

# ---------------------------- UI SETUP ------------------------------- #
# Create the main window for the application
window = Tk()
window.title("Pomodoro")  # Set the window title
window.config(padx=100, pady=50, bg=YELLOW)  # Set the padding and background color

# Create the canvas to display the tomato image and timer text
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")  # Load the tomato image
canvas.create_image(100, 112, image=tomato_img)  # Place the image on the canvas
timer_text = canvas.create_text(100, 135, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)  # Place the canvas in the grid at row 1, column 1

# Create the timer label that will display the current timer status
timer_label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 35, "bold"))
timer_label.grid(row=0, column=1)  # Place it in the grid at row 0, column 1

# Create buttons for start and reset actions
start_button = Button(text="Start", command=start_timer)
start_button.grid(row=2, column=0)  # Place it in row 2, column 0

reset_button = Button(text="Reset", command=reset)
reset_button.grid(row=2, column=2)  # Place it in row 2, column 2

# Label to display check marks after completing work sessions
check_marks = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20, "bold"))
check_marks.grid(row=3, column=1)  # Place it in row 3, column 1

# Start the tkinter main loop to run the Pomodoro application
window.mainloop()
