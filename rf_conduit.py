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
        #plt.plot(ck)
        #plt.show()
        ck = [f if np.absolute(f) < 0.4 else 0 for f in ck] #va un peu plus vite qu'une boucle, seuil à parametrer
        Ck = np.fft.fft(ck)
        Hk = np.exp(Ck)
        H.append(Hk)
    return H

def apply_vocal_spectrum(E, H):
    V = []

    for i in range(len(E)):
        V.append(E[i] * H[i])

    return V

def apply_transformation(voice, sound):
    data = voice[0:len(sound)]
    sound = sound[0:len(data)]

    fv, tv, zv = sig.stft(voice, nperseg=N)
    fs, ts, zs = sig.stft(sound, nperseg=N)

    H = vocal_frequency_response_estimation(zv)
    V = apply_vocal_spectrum(zs, H)

    t, R = sig.istft(V)

    return R

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    print(len(indata))
    print(indata)
    outdata[:] = indata
    #outdata[:] = apply_transformation(indata, soundarray)



if __name__ == "__main__":
     fe, soundarray = wave.read('0838.wav')
     print(fe)

     with sd.Stream(channels=1, callback=callback, blocksize=N, device=(0, 9)):
         sd.sleep(int(20 * 1000))

#     fe2, la = wave.read('0838.wav')
# #    print(n, fe)
#     la = la[0:len(data)]
#     data = data[0:len(la)]
#     f, t, Zxx = sig.stft(data, nperseg=2048) #partie 1 :/
#     f2, t2, E = sig.stft(la, nperseg=2048)
#
#     H = vocal_frequency_response_estimation(Zxx)
#
#     V = apply_vocal_spectrum(E, H)
#
#     t, R = sig.istft(V) # partie reconstruction :/
#
#     R = R / 100000 #On devra peut etre appliquer un facteur
#
#     wave.write("chasse-eau-baptiste.wav", fe, R)
    # plt.plot(data)
    # plt.figure()
    # plt.plot(H[10])
    # plt.figure()
    # plt.plot(R)
    # plt.show()
    # sd.play(data)
    # sd.wait()
    # sd.play(la)
    # sd.wait()
    # sd.play(R)
    # sd.wait()
