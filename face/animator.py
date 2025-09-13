from PyQt5.QtCore import QTimer

class Animator:
    def __init__(self, face_ui):
        self.face_ui = face_ui
        self.current_emotion = "neutral"

        # Timer for auto-blinking (every 6 seconds)
        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self.blink)
        self.blink_timer.start(6000)

    def set_emotion(self, emotion: str):
        """Update emotion with smooth transition."""
        if emotion != self.current_emotion:
            self.current_emotion = emotion
            self.face_ui.set_emotion(emotion)

    def blink(self):
        """Momentary blink effect."""
        if self.current_emotion != "angry":  # Angry face shouldn't blink often
            self.face_ui.set_emotion("blink")
            QTimer.singleShot(200, lambda: self.face_ui.set_emotion(self.current_emotion))
