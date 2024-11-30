import cv2 as cv
import tkinter as tk
from tkinter import ttk
from threading import Thread

class VideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Camera Reverse Feed")
        self.root.geometry("600x300")
        self.root.configure(bg='#333')

        # Create title label
        self.title_label = ttk.Label(root, text="Live Camera Reverse Feed", font=("Arial", 18), background='#333', foreground='white')
        self.title_label.pack(pady=20)

        # Create a frame for buttons
        self.button_frame = ttk.Frame(root, padding=10)
        self.button_frame.pack(pady=20, fill="x")

        # Start button
        self.start_button = ttk.Button(self.button_frame, text="Start", command=self.start_capture, width=15, style="Accent.TButton")
        self.start_button.grid(row=0, column=0, padx=10)

        # Stop button
        self.stop_button = ttk.Button(self.button_frame, text="Stop", command=self.stop_capture, width=15, style="Danger.TButton")
        self.stop_button.grid(row=0, column=1, padx=10)

        # Play Reversed button
        self.reverse_button = ttk.Button(self.button_frame, text="Play Reversed", command=self.play_reversed, width=15, style="Primary.TButton")
        self.reverse_button.grid(row=0, column=2, padx=10)

        # Quit button
        self.quit_button = ttk.Button(self.button_frame, text="Quit", command=self.quit_app, width=15, style="Secondary.TButton")
        self.quit_button.grid(row=1, column=0, columnspan=3, pady=10)

        # Configure styles for buttons
        self.style = ttk.Style()
        self.style.configure("Accent.TButton", font=("Arial", 14), background='#28a745', foreground='white')
        self.style.configure("Danger.TButton", font=("Arial", 14), background='#dc3545', foreground='white')
        self.style.configure("Primary.TButton", font=("Arial", 14), background='#007bff', foreground='white')
        self.style.configure("Secondary.TButton", font=("Arial", 14), background='#6c757d', foreground='white')

        # Variables for controlling video playback and capturing
        self.capture_thread = None
        self.is_capturing = False
        self.is_playing_reversed = False
        self.frames_list = []  # List to store frames captured
        self.current_frame_index = 0

    def start_capture(self):
        if not self.is_capturing:
            self.is_capturing = True
            self.capture_thread = Thread(target=self.capture_video)
            self.capture_thread.daemon = True
            self.capture_thread.start()

    def capture_video(self):
        capture = cv.VideoCapture(0)  # Open the camera feed
        self.frames_list = []  # Reset frames list

        while self.is_capturing:
            ret, frame = capture.read()
            if ret:
                self.frames_list.append(frame)  # Add frames to list
                cv.imshow('Video Feed', frame)  # Show the video feed in OpenCV window

            if cv.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to stop
                break
        
        capture.release()
        cv.destroyAllWindows()

    def stop_capture(self):
        self.is_capturing = False  # Stop the video capture

    def play_reversed(self):
        if not self.is_capturing and self.frames_list:
            self.is_playing_reversed = True
            self.frames_list.reverse()  # Reverse the captured frames
            self.current_frame_index = 0  # Start from the first reversed frame
            self.update_reversed_frame()

    def update_reversed_frame(self):
        if self.is_playing_reversed and self.current_frame_index < len(self.frames_list):
            frame = self.frames_list[self.current_frame_index]

            cv.imshow('Reversed Video Feed', frame)  # Show the reversed frames

            self.current_frame_index += 1
            cv.waitKey(30)  # Faster playback (adjust as needed)

            # Call the update method again to continue playing the reversed video
            self.update_reversed_frame()
        else:
            self.is_playing_reversed = False  # Stop when all frames are played

    def quit_app(self):
        self.is_capturing = False
        self.is_playing_reversed = False
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root)
    root.mainloop()
