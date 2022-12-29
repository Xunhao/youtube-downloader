import tkinter as tk
import os
from tkinter import filedialog
from pytube import YouTube
from pytube.exceptions import VideoUnavailable


def download_video():
    # Start of the function should clear any existing prompt
    response_label.config(text='')
    link = link_field.get()  # Attempt to get the user supplied URL
    if 'youtu.be' in link.lower() or 'youtube.com' in link.lower():  # Check if the user supplies a Youtube URL
        download_path = filedialog.askdirectory()
        # When user cancels the operation during folder selection, the variable would be empty
        if len(download_path) == 0:
            response_label.config(text='Cancelled')
            return
    else:
        response_label.config(text='Please enter a valid YouTube URL')
        return

    # Attempt to download video from Youtube
    try:
        yt = YouTube(link_field.get())
        yt.check_availability()  # Check whether the video is available
    except VideoUnavailable:  # Handles any error due to unavailable videos
        response_label.config(
            text='The link you provided cannot be downloaded')
    except Exception as e:
        response_label.config(
            text='An error has occurred. Please check your input!')
    else:
        # Check if the file already exist in the directory
        if os.path.exists(download_path + '/' + yt.title + '.mp4'):
            response_label.config(text='File already exists in folder.')
        yt = yt.streams.get_highest_resolution().download(download_path)
        # Let the user know that the video has been downloaded
        response_label.config(text='Download completed!')


# Set up Tkinter GUI
screen = tk.Tk()
screen.title('YT Ducky Delivery')
screen.geometry('500x400')
screen.resizable(False, False)  # To prevent users from adjusting the window
canvas = tk.Canvas(screen, width=500, height=400, bg='skyblue')
canvas.pack()

# Image logo
current_directory = os.getcwd()
logo_img = tk.PhotoImage(file=current_directory + '/yellow_duck.png')
logo_img = logo_img.subsample(4, 4)  # Resize images
screen.iconphoto(True, logo_img)  # Generate an icon for the window

# Entry
# Allows user to enter a single line of input

# We will use this input field to allow user to provider a YouTube URL
link_field = tk.Entry(
    screen,
    width=40,
    bg='white',
    fg='black',
    selectbackground='black',
    insertbackground='black',  # This changes the cursor colour so that it is visible
    highlightthickness=0
)

# Labels
# Display a box to place text or images

# We will use this label to provide a brief instruction for the user
link_label = tk.Label(
    screen,
    text='Enter Youtube Link Below',
    fg='black',
    bg='skyblue',
    font=('Helvetica', 17)
)

# We will use this label to interact with the user based on the user's action
response_label = tk.Label(
    screen,
    fg='black',
    bg='skyblue',
    font=('Helvetica', 13, 'italic')
)

# Buttons
# Display a button for user to interact

# We will use this button to allow users to kickstart the downloading process
# We will perform user input validation via the function set up above
download_btn = tk.Button(
    screen,
    text='Download',
    highlightbackground='skyblue',  # Blend the border with the bg colour
    command=download_video
)

# Add widgets to window
canvas.create_image(250, 80, image=logo_img)
canvas.create_window(250, 170, window=link_label)
canvas.create_window(250, 220, window=link_field)
canvas.create_window(250, 320, window=response_label)
canvas.create_window(250, 270, window=download_btn)

screen.mainloop()
