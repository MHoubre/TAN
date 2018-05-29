# -*- coding: utf-8 -*-

import numpy as np
import scipy.io.wavfile as wave
import scipy.signal as sig

import sounddevice as sd

from matplotlib import pyplot as plt
from reconstruct import reconst


N = 2048
fe = 44100
T = N / fe

sd.default.samplerate = fe
sd.default.channels = 1

soundarray = None


def plot_fft(s, tf, N=N):
    #fonction pour tracer une fft
    #xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    #plt.plot(xf, 2.0/N * np.abs(tf[0:N//2]))

    freq = np.fft.fftfreq(s.size, d=1/fe)
    plt.plot(freq[0:N//2], np.abs(tf[0:N//2]))
    plt.grid()
    plt.show()

def tf_short_time(x):
    #Scipy génère bien w(s) = hann(s) pour 0 <= s <= N-1
    #on l'appliquera ensuite à chaque découpe
    hw = sig.hann(N)

    length = x.size #longueur du signal

    #Calcule des indices selon une découpe de pas N/2
    #indices = np.arange(start=0, stop=length - N/2, step=N/2, dtype='int')
    indices = np.arange(start=0, stop=length, step=N/2, dtype='int')

    #Echantillons en sortie
    samples = np.zeros((indices.size, N), dtype='complex')

    for m, i in enumerate(indices):
        #Notre échantillon de taile N:
        s = x[i:i+N]
        l = len(s) #sa longeur
        if l < N: #dernier echantillon tronqué
            s = np.pad(s, (0, N-l), 'constant') #zero-padding
            #hw = sig.hann(l) #recalcul de la fenêtre

        #Echantillon fenétré:
        sw = s * hw

        #Calcul de la TF de l'échantillon:
        tf = np.fft.fft(sw)

        #plot_fft(sw, tf)

        samples[m] = tf

    return samples


def vocal_frequency_response_estimation(stf):

    TETA_THRES = 800

    H = np.zeros(stf.shape, dtype='complex')

    for m in range(stf.shape[0]):

        module = np.abs(stf[m])

        module = module + 0.001 #eviter log(0)
        lm = np.log(module)

        cesptre = np.fft.ifft(lm)

        #plot_fft(lm, cesptre)

        freq = np.fft.fftfreq(cesptre.size, d=1/fe)

        #filtrage du cesptre
        for j in range(cesptre.size):
            f = np.abs(freq[j])
            fN = freq[N-1]

            if f >= TETA_THRES:
                cesptre[j] = 0

        #plot_fft(lm, cesptre)

        cexp = np.fft.fft(cesptre)
        H[m] = np.exp(cexp)

    return H

def apply_vocal_spectrum(E, H):

    V = np.zeros(E.shape, dtype='complex')

    for m in range(V.shape[0]):
        V[m] = E[m] * H[m]
        #plot_fft(V[m])

    return V

def reconstruct(V, nmax):
    R = np.zeros(nmax)
    a = np.zeros(V.shape)
    dn = N // 2


    for m in range(V.shape[0]):
        a[m] = np.fft.ifft(V[m])

    #print(nmax, a.shape)

    for n in range(nmax-N):
        m = n // dn
        q = int(n - m * dn)
        #print(m, q + dn, q)
        R[n] = a[m, q] + a[m+1, q+dn]

    return R

def apply_transformation(voice, sound):
    ls = len(sound)
    lv = len(voice)

    if (ls < lv):
        sound = np.pad(sound, (0, lv-ls), 'reflect')
    else:
        sound = sound[:len(voice)]

    tfs_voice = tf_short_time(voice)
    tfs_sound = tf_short_time(sound)

    H = vocal_frequency_response_estimation(tfs_voice)
    V = apply_vocal_spectrum(tfs_sound, H)

    R = reconstruct(V, lv)

    return R / 100000


def callback(indata, outdata, frames, time, status):
    #outdata[:] = indata
    outdata[:, 0] = apply_transformation(indata[:, 0], soundarray)


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
    with sd.Stream(callback=callback, blocksize=N*k):
        sd.sleep(int(sec * 1000))

def test_sound(v_path=None, output=None, data=None):
    global soundarray
    if data is None:
        voice = wave.read(v_path)[1]
    else:
        voice = data

    try:
        voice = voice[:, 0]
    except IndexError:
        pass


    #sd.play(voice, blocking=True)
    #sd.play(soundarray, blocking=True)

    R = apply_transformation(voice, soundarray)
    #R = R / 100000
    if (output is None):
         sd.play(R)
         sd.wait()
    # else:
    #     wave.write("output.wav", fe, R)

def record(path, sec):
    a = sd.rec(4*fe, blocking=True)
    wave.write(path, fe, a)

    return a

if __name__ == "__main__":
    #sd.wait()
    soundarray = wave.read('sons/vent1.wav')[1]

    try:
        soundarray = soundarray[:, 0]
    except IndexError:
        pass
    #sd.play(soundarray, blocking=True)
    a = record("test.wav", 4)
    sd.play(a, blocking=True)
    test_sound(data=a)
    #stream(30, 8)
