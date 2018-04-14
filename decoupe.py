import matplotlib.pyplot as plt
import numpy as np
import wave
import math
import binascii
import pygame
from pygame.locals import *
import scipy.io.wavfile as wave
import scipy.signal as sig

pygame.init()
pygame.mixer.init()
fe, data = wave.read('/home/mael/Téléchargements/la_mono.wav')

n=len(data)
taille=int(len(data)/10)


datap=data[0:taille]

t=np.arange(len(datap))
t=t/fe


def sampling(sound,instant, width):
    w=sig.hanning(int(width)) #fenêtre de largeur width
        
    sample=sound[int((instant-(width/2))):int(instant+(width/2))]
    
    cut = w*sample
    
    return cut
    
#echantillon = sample*w
#plt.plot(t,datap)
#plt.show()