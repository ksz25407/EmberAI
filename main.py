import logging
import sqlite3
import sys
from asr.vosk_asr import VoskASR
from tts.coqui_tts import speak
from llm.vicuna_llm import VicunaLLM
from memory.short_term import ShortTermMemory
from face.face_ui import FaceUI
from face.animator import Animator
from face.emotions import Emotions
from button import listening_state
from config import MODEL_PATH

# ================== Setup ==================
logging.basicConfig(
    filename='/mnt/ssd/logs/ai_companion.log',
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Setup SQLite cache
conn = sqlite3.connect('/mnt/ssd/cache.db')
conn.execute("""
CREATE TABLE IF NOT EXISTS responses (
    context TEXT PRIMARY KEY,
    response TEXT
)
""")

# Initialize components
asr = VoskASR(MODEL_PATH)
llm = VicunaLLM()
memory = ShortTermMemory()
face_ui = FaceUI()
animator = Animator()
emotions = Emotions()


# ================== Main Loop ==================
def process_environment():
    with asr.stream() as stream:
        while True:
            try:
                data = stream.read(1024)
                if not listening_state.get("state"):
                    continue

                if asr.recognize(data):
                    text = asr.get_text()
                    if not text.strip():
                        continue

                    logging.info(f"Heard: {text}")
                    memory.add(text)

                    # Build context
                    context = f"Audio: {memory.get_context()}"

                    # Check cache
                    cursor = conn.execute("SELECT response FROM responses WHERE context=?", (context,))
                    cached = cursor.fetchone()

                    if cached:
                        response = cached[0]
                    else:
                        response = llm.generate_response(context)
                        conn.execute("INSERT OR REPLACE INTO responses (context, response) VALUES (?, ?)", (context, response))
                        conn.commit()

                    logging.info(f"AI: {response}")

                    # Speak + Animate
                    speak(response)
                    emotion = emotions.detect_emotion(response)
                    animator.set_emotion(emotion)
                    animator.update(face_ui.screen)

            except Exception as e:
                logging.error(f"Error in loop: {e}", exc_info=True)


# ================== Run ==================
if __name__ == "__main__":
    try:
        process_environment()
    except KeyboardInterrupt:
        logging.info("Shutting down by user")
    except Exception as e:
        logging.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        conn.close()
        face_ui.cleanup()
