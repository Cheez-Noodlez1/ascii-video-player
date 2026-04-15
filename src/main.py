import sys
import cv2
import numpy as np
import os
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QFileDialog, QHBoxLayout)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal

# Standard ASCII characters ordered by "brightness"
ASCII_CHARS = "@%#*+=-:. "

class VideoThread(QThread):
    """Thread to process video frames and send them to the UI."""
    frame_ready = pyqtSignal(str, QColor)

    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        self.is_running = True
        self.color_mode = "Matrix Green"
        self.temp_audio = "temp_audio.wav"

    def run(self):
        # 1. Extract audio using moviepy (if possible)
        has_audio = False
        try:
            from moviepy.editor import VideoFileClip
            import pygame
            
            video = VideoFileClip(self.video_path)
            if video.audio:
                video.audio.write_audiofile(self.temp_audio, codec='pcm_s16le', verbose=False, logger=None)
                pygame.mixer.init()
                pygame.mixer.music.load(self.temp_audio)
                has_audio = True
        except Exception as e:
            print(f"Audio extraction failed: {e}")

        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        delay = 1.0 / fps if fps > 0 else 0.033
        
        if has_audio:
            pygame.mixer.music.play()
            start_time = time.time()

        frame_count = 0
        while self.is_running:
            ret, frame = cap.read()
            if not ret:
                break

            # Sync with audio/time
            if has_audio:
                elapsed = time.time() - start_time
                target_frame = int(elapsed * fps)
                if frame_count < target_frame:
                    frame_count += 1
                    continue # Skip frame to catch up

            # Resize and Convert
            height, width = frame.shape[:2]
            new_width = 80
            new_height = int((height / width) * new_width * 0.5)
            resized_frame = cv2.resize(frame, (new_width, new_height))

            if self.color_mode == "True Color":
                html_frame = "<pre style='line-height: 0.8; font-family: Courier New; font-size: 6pt;'>"
                for y in range(new_height):
                    for x in range(new_width):
                        b, g, r = resized_frame[y, x]
                        pixel_val = int(0.299*r + 0.587*g + 0.114*b)
                        char_idx = int(pixel_val / 256 * len(ASCII_CHARS))
                        html_frame += f"<span style='color: rgb({r},{g},{b});'>{ASCII_CHARS[char_idx]}</span>"
                    html_frame += "<br>"
                html_frame += "</pre>"
                self.frame_ready.emit(html_frame, QColor(255, 255, 255))
            else:
                ascii_frame = ""
                gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
                for y in range(new_height):
                    for x in range(new_width):
                        char_idx = int(gray_frame[y, x] / 256 * len(ASCII_CHARS))
                        ascii_frame += ASCII_CHARS[char_idx]
                    ascii_frame += "\n"
                color = QColor(0, 255, 0) if self.color_mode == "Matrix Green" else QColor(200, 200, 200)
                self.frame_ready.emit(ascii_frame, color)

            frame_count += 1
            time.sleep(max(0, delay - 0.01)) # Basic delay adjustment

        cap.release()
        if has_audio:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            try: os.remove(self.temp_audio)
            except: pass

    def stop(self):
        self.is_running = False

class ASCIIVideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASCII Video Player")
        self.resize(1000, 800)
        self.setStyleSheet("background-color: #000000; color: #00FF00;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # ASCII Display Area
        from PyQt6.QtWidgets import QTextEdit
        self.ascii_display = QTextEdit()
        self.ascii_display.setReadOnly(True)
        self.ascii_display.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.ascii_display.setFont(QFont("Courier New", 6))
        self.ascii_display.setStyleSheet("background-color: black; border: none;")
        self.ascii_display.setPlaceholderText("Drop a video file to start...")
        layout.addWidget(self.ascii_display)

        # Controls
        controls_layout = QHBoxLayout()
        
        self.btn_open = QPushButton("Open Video")
        self.btn_open.clicked.connect(self.open_file)
        self.btn_open.setStyleSheet("padding: 10px; background-color: #1a1a1a; border: 1px solid #00FF00; border-radius: 5px;")
        controls_layout.addWidget(self.btn_open)

        self.btn_mode = QPushButton("Switch Color: Matrix")
        self.btn_mode.clicked.connect(self.toggle_color_mode)
        self.btn_mode.setStyleSheet("padding: 10px; background-color: #1a1a1a; border: 1px solid #00FF00; border-radius: 5px;")
        controls_layout.addWidget(self.btn_mode)

        layout.addLayout(controls_layout)

        self.video_thread = None
        self.current_mode = "Matrix Green"

        # Drag and Drop support
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            self.start_video(files[0])

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi *.mov *.mkv)")
        if file_path:
            self.start_video(file_path)

    def start_video(self, path):
        if self.video_thread:
            self.video_thread.stop()
            self.video_thread.wait()
        
        self.video_thread = VideoThread(path)
        self.video_thread.color_mode = self.current_mode
        self.video_thread.frame_ready.connect(self.update_display)
        self.video_thread.start()

    def update_display(self, content, color):
        if self.current_mode == "True Color":
            self.ascii_display.setHtml(content)
        else:
            self.ascii_display.setText(content)
            self.ascii_display.setStyleSheet(f"color: {color.name()};")

    def toggle_color_mode(self):
        modes = ["Matrix Green", "Grayscale", "True Color"]
        idx = (modes.index(self.current_mode) + 1) % len(modes)
        self.current_mode = modes[idx]
        self.btn_mode.setText(f"Switch Color: {self.current_mode.split()[0]}")
        if self.video_thread:
            self.video_thread.color_mode = self.current_mode

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ASCIIVideoPlayer()
    window.show()

    # Handle Command Line Arguments (e.g. ascii-stream movie.mp4 true)
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
        if os.path.exists(video_path):
            # Check for 'true' or 'truecolor' flag
            if len(sys.argv) > 2 and sys.argv[2].lower() in ["true", "truecolor"]:
                window.current_mode = "True Color"
                window.btn_mode.setText("Switch Color: True")
            
            # Start playback instantly
            window.start_video(video_path)

    sys.exit(app.exec())
