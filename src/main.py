"""
ASCII Video Player - Standalone Windows App
A retro-style Windows application that converts any video file or HTML file into real-time ASCII art.
Version: 1.1.0
Author: Cheez-Noodlez1
"""

import sys
__version__ = "1.1.0"
__author__ = "Cheez-Noodlez1"
import cv2
import numpy as np
import os
import time
from typing import Optional, Tuple

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QFileDialog, QHBoxLayout, QTextEdit
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal

# Standard ASCII characters ordered by "brightness"
ASCII_CHARS = "@%#*+=-:. "


class VideoThread(QThread):
    """Thread to process video frames or HTML content and send them to the UI."""
    frame_ready = pyqtSignal(str, QColor)

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.is_running = True
        self.color_mode = "Matrix Green"
        self.temp_audio = "temp_audio.wav"

    def run(self) -> None:
        """Main loop for processing video frames or static HTML content."""
        if self.file_path.lower().endswith(('.html', '.htm')):
            self._process_html()
            return

        # Video processing logic
        has_audio = False
        try:
            # Conditional imports for optional audio support
            from moviepy.editor import VideoFileClip
            import pygame

            video = VideoFileClip(self.file_path)
            if video.audio:
                video.audio.write_audiofile(
                    self.temp_audio, codec='pcm_s16le', verbose=False, logger=None
                )
                pygame.mixer.init()
                pygame.mixer.music.load(self.temp_audio)
                has_audio = True
        except ImportError:
            print("Audio extraction skipped: moviepy or pygame not installed.")
        except Exception as e:
            print(f"Audio extraction failed: {e}")

        cap = cv2.VideoCapture(self.file_path)
        if not cap.isOpened():
            print(f"Failed to open video: {self.file_path}")
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
                    continue  # Skip frame to catch up

            # Process the frame
            content, color = self._process_frame(frame)
            self.frame_ready.emit(content, color)

            frame_count += 1
            time.sleep(max(0, delay - 0.01))  # Basic delay adjustment

        cap.release()
        if has_audio:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            try:
                os.remove(self.temp_audio)
            except OSError:
                pass

    def _process_html(self) -> None:
        """Read HTML file, convert to text, and emit."""
        try:
            import html2text
            with open(self.file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            h = html2text.HTML2Text()
            h.ignore_links = False
            text = h.handle(html_content)
            
            color = QColor(0, 255, 0) if self.color_mode == "Matrix Green" else QColor(200, 200, 200)
            self.frame_ready.emit(text, color)
        except Exception as e:
            self.frame_ready.emit(f"Error loading HTML: {e}", QColor(255, 0, 0))

    def _process_frame(self, frame: np.ndarray) -> Tuple[str, QColor]:
        """Convert a video frame to ASCII art."""
        height, width = frame.shape[:2]
        new_width = 80
        new_height = int((height / width) * new_width * 0.5)
        resized_frame = cv2.resize(frame, (new_width, new_height))

        if self.color_mode == "True Color":
            html_frame = (
                "<pre style='line-height: 0.8; font-family: Courier New; font-size: 6pt;'>"
            )
            for y in range(new_height):
                for x in range(new_width):
                    b, g, r = resized_frame[y, x]
                    pixel_val = int(0.299 * r + 0.587 * g + 0.114 * b)
                    char_idx = int(pixel_val / 256 * len(ASCII_CHARS))
                    html_frame += (
                        f"<span style='color: rgb({r},{g},{b});'>"
                        f"{ASCII_CHARS[char_idx]}</span>"
                    )
                html_frame += "<br>"
            html_frame += "</pre>"
            return html_frame, QColor(255, 255, 255)
        else:
            ascii_frame = ""
            gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
            for y in range(new_height):
                for x in range(new_width):
                    char_idx = int(gray_frame[y, x] / 256 * len(ASCII_CHARS))
                    ascii_frame += ASCII_CHARS[char_idx]
                ascii_frame += "\n"
            
            color = QColor(0, 255, 0) if self.color_mode == "Matrix Green" else QColor(200, 200, 200)
            return ascii_frame, color

    def stop(self) -> None:
        """Signal the thread to stop processing."""
        self.is_running = False


class ASCIIVideoPlayer(QMainWindow):
    """Main UI Window for the ASCII Video Player."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASCII Video Player")
        self.resize(1000, 800)
        self.setStyleSheet("background-color: #000000; color: #00FF00;")

        self._setup_ui()
        self.video_thread: Optional[VideoThread] = None
        self.current_mode = "Matrix Green"

        # Drag and Drop support
        self.setAcceptDrops(True)

    def _setup_ui(self) -> None:
        """Initialize the user interface components."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # ASCII Display Area
        self.ascii_display = QTextEdit()
        self.ascii_display.setReadOnly(True)
        self.ascii_display.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.ascii_display.setFont(QFont("Courier New", 6))
        self.ascii_display.setStyleSheet("background-color: black; border: none;")
        self.ascii_display.setPlaceholderText("Drop a video or HTML file to start...")
        layout.addWidget(self.ascii_display)

        # Controls
        controls_layout = QHBoxLayout()

        self.btn_open = QPushButton("Open File")
        self.btn_open.clicked.connect(self.open_file)
        self.btn_open.setStyleSheet(
            "padding: 10px; background-color: #1a1a1a; "
            "border: 1px solid #00FF00; border-radius: 5px;"
        )
        controls_layout.addWidget(self.btn_open)

        self.btn_mode = QPushButton("Switch Color: Matrix")
        self.btn_mode.clicked.connect(self.toggle_color_mode)
        self.btn_mode.setStyleSheet(
            "padding: 10px; background-color: #1a1a1a; "
            "border: 1px solid #00FF00; border-radius: 5px;"
        )
        controls_layout.addWidget(self.btn_mode)

        layout.addLayout(controls_layout)

    def dragEnterEvent(self, event) -> None:
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event) -> None:
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            self.start_playback(files[0])

    def open_file(self) -> None:
        """Open a file dialog to select a video or HTML file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Supported Files (*.mp4 *.avi *.mov *.mkv *.html *.htm)"
        )
        if file_path:
            self.start_playback(file_path)

    def start_playback(self, path: str) -> None:
        """Initialize and start the playback thread."""
        if self.video_thread:
            self.video_thread.stop()
            self.video_thread.wait()

        self.video_thread = VideoThread(path)
        self.video_thread.color_mode = self.current_mode
        self.video_thread.frame_ready.connect(self.update_display)
        self.video_thread.start()

    def update_display(self, content: str, color: QColor) -> None:
        """Update the UI with new ASCII frame content."""
        if self.current_mode == "True Color":
            self.ascii_display.setHtml(content)
        else:
            self.ascii_display.setText(content)
            self.ascii_display.setStyleSheet(f"color: {color.name()};")

    def toggle_color_mode(self) -> None:
        """Cycle through available color modes."""
        modes = ["Matrix Green", "Grayscale", "True Color"]
        idx = (modes.index(self.current_mode) + 1) % len(modes)
        self.current_mode = modes[idx]
        self.btn_mode.setText(f"Switch Color: {self.current_mode.split()[0]}")
        if self.video_thread:
            self.video_thread.color_mode = self.current_mode


def run_in_terminal(file_path: str):
    """Render the file or URL directly to the terminal."""
    # Check if it's a URL
    is_url = file_path.startswith(('http://', 'https://'))
    
    if not is_url and not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    if is_url or file_path.lower().endswith(('.html', '.htm')):
        try:
            import html2text
            import requests
            
            if is_url:
                response = requests.get(file_path)
                response.raise_for_status()
                html_content = response.text
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
            
            h = html2text.HTML2Text()
            print(h.handle(html_content))
        except ImportError:
            print("Error: html2text or requests not installed. Run 'pip install html2text requests'")
        except Exception as e:
            print(f"Error reading HTML: {e}")
        return

    # Video Terminal Rendering
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        print(f"Failed to open video: {file_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = 1.0 / fps if fps > 0 else 0.033

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            height, width = frame.shape[:2]
            new_width = 80
            new_height = int((height / width) * new_width * 0.5)
            resized_frame = cv2.resize(frame, (new_width, new_height))
            gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

            ascii_frame = ""
            for y in range(new_height):
                for x in range(new_width):
                    char_idx = int(gray_frame[y, x] / 256 * len(ASCII_CHARS))
                    ascii_frame += ASCII_CHARS[char_idx]
                ascii_frame += "\n"

            # Clear screen and print
            os.system('cls' if os.name == 'nt' else 'clear')
            print(ascii_frame)
            time.sleep(delay)
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()


def main():
    """Application entry point."""
    # Handle version request
    if "--version" in sys.argv or "-v" in sys.argv:
        print(f"ASCII Video Player v{__version__}")
        print(f"Created by {__author__}")
        return

    # Check if running in terminal mode (no GUI requested or via CLI)
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        
        # If "--terminal" flag is present, run in terminal
        if "--terminal" in sys.argv:
            run_in_terminal(file_path)
            return

    app = QApplication(sys.argv)
    window = ASCIIVideoPlayer()
    window.show()

    # Handle Command Line Arguments for GUI startup
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            # Check for 'true' or 'truecolor' flag
            if any(arg.lower() in ["true", "truecolor"] for arg in sys.argv):
                window.current_mode = "True Color"
                window.btn_mode.setText("Switch Color: True")

            # Start playback instantly
            window.start_playback(file_path)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
