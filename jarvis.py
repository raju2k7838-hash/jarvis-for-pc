import datetime
import os
import tempfile
import wave
import numpy as np
import pyttsx3
import pywhatkit
import speech_recognition as sr
import sounddevice as sd
import webbrowser
import pyautogui
import wikipedia

# Text-to-Speech Engine Setup
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 175)


def speak(audio):
  print(f'JARVIS: {audio}')
  engine.say(audio)
  engine.runAndWait()


def wish_me():
  hour = int(datetime.datetime.now().hour)
  if hour >= 0 and hour < 12:
    speak('Good morning Suraj, have a great day!')
  elif hour >= 12 and hour < 18:
    speak('Good afternoon!')
  else:
    speak('Good evening!')
  speak('I am Jarvis. Ready for your command.')


def open_website(site_name):
  known_sites = {
      'google': 'https://www.google.com',
      'youtube': 'https://www.youtube.com',
      'wikipedia': 'https://www.wikipedia.org',
      'facebook': 'https://www.facebook.com',
      'instagram': 'https://www.instagram.com',
      'github': 'https://github.com',
  }
  site_name = site_name.strip().lower()
  url = known_sites.get(site_name, site_name)
  if not url.startswith(('http://', 'https://')):
    if '.' not in url:
      url = f'https://www.{url}.com'
    else:
      url = f'https://{url}'
  webbrowser.open(url)


def take_command():
  # पहले वॉइस से कोशिश करेंगे
  duration = 7  # सुनने का समय बढ़ाकर 7 सेकंड किया
  fs = 44100
  print(
      '\n[Listening via Microphone... Speak now or press Enter to type manually]'
  )

  try:
    audio_data = sd.rec(
        int(duration * fs), samplerate=fs, channels=1, dtype='int16'
    )
    sd.wait()

    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
      temp_filename = temp_audio.name

    wf = wave.open(temp_filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(fs)
    wf.writeframes(audio_data.tobytes())
    wf.close()

    r = sr.Recognizer()
    with sr.AudioFile(temp_filename) as source:
      audio = r.record(source)

    print('Recognizing...')
    query = r.recognize_google(audio, language='en-in')
    print(f'User said (Voice): {query}\n')

    try:
      os.remove(temp_filename)
    except:
      pass

    return query.lower()

  except Exception as e:
    # अगर आवाज़ समझ नहीं आई, तो कीबोर्ड से टाइप करने का ऑप्शन देंगे
    print(f"Audio error: {type(e).__name__}: {e}")
    manual_query = input('Type your command here (or press Enter to retry): ')
    if manual_query.strip() == '':
      return 'none'
    return manual_query.lower()


if __name__ == '__main__':
  wish_me()
  while True:
    query = take_command()

    if 'wikipedia' in query:
      speak('Searching Wikipedia...')
      query = query.replace('wikipedia', '')
      results = wikipedia.summary(query, sentences=2)
      speak('According to Wikipedia:')
      print(results)
      speak(results)

    elif query.startswith('open '):
      site_name = query.removeprefix('open ').strip()
      speak(f'Opening {site_name}...')
      open_website(site_name)

    elif query.startswith('play '):
      song = query.removeprefix('play ').strip()
      song = song.removesuffix(' on youtube').strip()
      speak(f'Playing {song} on YouTube')
      pywhatkit.playonyt(song)

    elif 'open youtube' in query:
      speak('Opening YouTube...')
      webbrowser.open('https://www.youtube.com')

    elif 'open google' in query:
      speak('Opening Google...')
      webbrowser.open('https://www.google.com')

    elif 'open notepad' in query:
      speak('Opening Notepad...')
      os.system('notepad')

    elif 'time' in query:
      strTime = datetime.datetime.now().strftime('%H:%M:%S')
      speak(f'Sir, the current time is {strTime}')

    elif 'take screenshot' in query:
      speak('Taking screenshot...')
      img = pyautogui.screenshot()
      img.save('screenshot.png')
      speak('Screenshot saved successfully.')

    elif 'volume up' in query:
      speak('Increasing volume...')
      for _ in range(5):
        pyautogui.press('volumeup')

    elif 'exit' in query or 'quit' in query or 'stop' in query:
      speak('Shutting down Jarvis. Goodbye Suraj!')
      break