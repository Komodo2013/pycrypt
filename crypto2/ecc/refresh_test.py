import requests
import time
import pyaudio
import numpy as np

def play_sonar_ping(frequency, duration, ping_rate):
    samples = (np.sin(2 * np.pi * frequency * np.arange(duration * 44100) / 44100)).astype(np.float32)
    modulator = np.sin(2 * np.pi * ping_rate * np.arange(duration * 44100) / 44100)
    modulated = samples * modulator * .0000000001

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)
    stream.write(modulated.tobytes())

    stream.stop_stream()
    stream.close()
    p.terminate()


def refresh_browser(url, refresh_interval):
    while True:
        tim = time.ctime()
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"{tim}: Website is accessible. Response code: 200 OK")
                play_sonar_ping(500, .05, 30)
            elif response.status_code == 404:
                print(f"{tim}: 404")
            elif response.status_code == 502:
                print(f"{tim}: 502")
            else:
                print(f"{tim}: Website is accessible, but an unexpected response code was received: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"{tim}: Error connecting to the website:", e)

        time.sleep(refresh_interval)


if __name__ == "__main__":
    play_sonar_ping(500, .05, 30)
    url = "https://lcr.churchofjesuschrist.org/?lang=eng"
    refresh_interval = 20  # Refresh interval in seconds

    refresh_browser(url, refresh_interval)
