# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import matplotlib.pyplot as plt
import numpy as np
#import wave
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

#print(len(t))

tfd= fft(datap)

print(len(tfd))

plt.subplot(211)
plt.plot(t,datap)

spectre=np.absolute(tfd)*2/n
freq=np.arange(taille)*1.0/5

#plt.plot(freq,spectre)

#plt.figure(figsize=(30,4))
for i in range(0,taille-2,2):
    tfd[i]=tfd[i]-50000

itfd=ifft(tfd)
plt.subplot(212)
plt.plot(t,itfd)
#type(data[3])

#plt.plot(t,y)
#grid()
#plt.show()