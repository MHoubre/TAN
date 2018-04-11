# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import matplotlib.pyplot as plt
import numpy as np
import wave
import math
import binascii
import pygame
from pygame.locals import *
import scipy.io.wavfile as wave
from scipy import *

pygame.init()
pygame.mixer.init()
rate, data = wave.read('/home/mael/Téléchargements/la_mono.wav')

n=len(data)
taille=int(len(data)/20)

datap=data[0:taille]

t=np.arange(len(datap))/rate

bruit=np.random.normal(0,0.5,len(datap))
#print(len(t))

tfd= fft(datap)

print(len(tfd))

plt.subplot(211)
plt.plot(t,datap)

plt.subplot(212)
plt.plot(t,bruit)

sig_bruit = datap+bruit

tfd2= fft(sig_bruit)

spectre=np.absolute(tfd2)*2/taille
freq=np.arange(taille)*1.0/5

#plt.plot(freq,spectre)

#plt.figure(figsize=(30,4))

itfd=ifft(tfd2)
#plt.subplot(212)
#plt.plot(t,itfd)