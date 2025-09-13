from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
import sys

class FaceUI(QLabel):
    def __init__(self, screen_width=800, screen_height=480):
        super().__init__()
        self.setWindowTitle("Ember Eyes")
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setAlignment(Qt.AlignCenter)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.movie = None
        self.set_emotion("neutral")

    def set_emotion(self, emotion: str):
        """Change the displayed GIF based on emotion."""
        gif_path = f"assets/gifs/{emotion.lower()}.gif"
        self.movie = QMovie(gif_path)
        self.setMovie(self.movie)
        self.movie.start()

    def show_face(self):
        """Run fullscreen window."""
        self.showFullScreen()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    face = FaceUI()
    face.show_face()
    sys.exit(app.exec_())
