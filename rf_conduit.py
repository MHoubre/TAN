import numpy as np
import scipy.io.wavfile as wave
import scipy.signal as sig

import sounddevice as sd

from matplotlib import pyplot as plt
from reconstruct import reconst


N=2048
soundarray = None

#
# def tf_short_term(data, N):
#     hw = sig.hanning(N)
#
#     indices = np.arange(start=0, stop=len(data), step=N, dtype='int')
#     samples = []
#     for i in indices:
#         s = data[i:i+N]
#         l = len(s)
#         if l < N: #le dernier echantillon est tronqué on recalcule la bonne
#                   #taille de fenetre
#             hw = sig.hanning(l)
#         samples.append(np.fft.fft(data[i:i+N]*hw, N))
#
#     return samples

def vocal_frequency_response_estimation(samples):
    H = []
    for s in samples:
        a = np.log(np.absolute(s)) #erreur normales ici
        a[a == -np.inf] = 0
        ck = np.fft.ifft(a)
    #    ck[np.absolute(ck) >= 0.5] = 0
        #ck = [f if np.absolute(f) < 0.4 else 0 for f in ck]
        Ck = np.fft.fft(ck)
        Hk = np.exp(Ck)
        H.append(Hk)
    return H

def apply_vocal_spectrum(E, H):
    V = []

    for i in range(len(E)):
        if(len(H) > 1):
            V.append(E[i] * H[i])
        else:
            V.append(E[i] * H[i])

    return V

def apply_transformation(voice, sound):
    ls = len(sound)
    lv = len(voice)

    if (ls < lv):
        sound = np.pad(sound, (0, lv-ls), 'reflect')
    else:
        sound = sound[:len(voice)]

    fv, tv, zv = sig.stft(voice, nperseg=N)
    fs, ts, zs = sig.stft(sound, nperseg=N)

    H = vocal_frequency_response_estimation(zv)
    V = apply_vocal_spectrum(zs, H)

    t, R = sig.istft(V, nperseg=N)

    return R


def callback(indata, outdata, frames, time, status):
    outdata[:, 0] = apply_transformation(indata[:, 0], soundarray)/100

def plot(voice, soundarray, output):

    plt.subplot(231)
    plt.plot(voice)
    plt.subplot(232)
    plt.plot(soundarray)
    plt.subplot(233)
    plt.plot(output)

    plt.subplot(234)
    plt.plot(np.fft.fftshift(np.fft.fft(voice)))
    plt.subplot(235)
    plt.plot(np.fft.fftshift(np.fft.fft(soundarray)))
    plt.subplot(236)
    plt.plot(np.fft.fftshift(np.fft.fft(output)))
    plt.show()

    #plt.plot(output, label)


def stream(sec, k):
    with sd.Stream(channels=1, callback=callback, blocksize=N*k, device=(5,5)):
          sd.sleep(int(sec * 1000))

def test_sound(v_path, output=None):
    global soundarray
    fe, voice = wave.read(v_path)

    try:
        voice = voice[:, 0]
    except IndexError:
        pass

    try:
        soundarray = soundarray[:, 0]
    except IndexError:
        pass

    sd.play(voice)
    sd.wait()
    sd.play(soundarray)
    sd.wait()

    R = apply_transformation(voice, soundarray)
    R = R / 100000

    if (output is None):
        sd.play(R)
        sd.wait()
    else:
        wave.write("output.wav", fe, R)

if __name__ == "__main__":
    #fe, soundarray = wave.read('sons/feu.wav')
    #fe, voice = wave.read('lepadawan.wav')
    soundarray = wave.read('sons/vent1.wav')[1]

    test_sound('lepadawan.wav')
    stream(30, 8)
