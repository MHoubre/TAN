import numpy as np
import scipy.io.wavfile as wave
import scipy.signal as sig
import sounddevice as sd

from matplotlib import pyplot as plt
from reconstruct import reconst

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


if __name__ == "__main__":

    fe, data = wave.read('test_voix.wav')
    fe2, la = wave.read('0838.wav')
#    print(n, fe)
    la = la[0:len(data)]
    data = data[0:len(la)]
    f, t, Zxx = sig.stft(data, nperseg=2048) #partie 1 :/
    f2, t2, E = sig.stft(la, nperseg=2048) 

    H = vocal_frequency_response_estimation(Zxx)

    V = apply_vocal_spectrum(E, H)

    t, R = sig.istft(V) # partie reconstruction :/

    R = R / 100000 #On devra peut etre appliquer un facteur 

    wave.write("chasse-eau-baptiste.wav", fe, R)
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
