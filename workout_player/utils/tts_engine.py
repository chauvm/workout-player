import pyttsx3

class TtsEngine:
  def __init__(self):
    self._engine = pyttsx3.init()
    """RATE"""
    self._engine.setProperty('rate', 180)
    """VOLUME"""
    # self._engine.setProperty('volume', 1.0)    # setting up volume level  between 0 and 1
    """VOICE"""
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[0].id)   # 0 for male
    # engine.setProperty('voice', voices[1].id)   # 0 for female 
  
  def say(self, message):
    self._engine.say(message)
    self._engine.runAndWait()
    self._engine.stop()