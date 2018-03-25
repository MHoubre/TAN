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

t=np.arange(len(data))/rate
print(len(t))

tfd= fft(data)
spectre=np.absolute(tfd)*2/n
freq=np.arange(n)*1.0/5

plt.plot(freq,spectre)
#plt.figure(figsize=(30,4))
#type(data[3])

#plt.plot(t,y)
#grid()
#plt.show()