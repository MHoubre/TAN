# -*- coding: utf-8 -*-
"""
Created on Wed May  2 10:49:35 2018

@author: Auriac - Dautricourt - Houbre - Michaux
"""
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.io.wavfile as wave
import scipy.signal as sig

#Préparation du fichier son utilisé.
sound_fe, sound_data = wave.read("la_mono.wav")
sound_n=len(sound_data)
sound_taille=int(len(sound_data)/10)
sound_datap=sound_data[0:sound_taille]
sound_t=np.arange(len(sound_datap))
sound_t=sound_t/sound_fe
sound_T=1*sound_fe

#Préparation du fichier voix utilisé.
voice_fe, voice_data = wave.read("test_voix.wav")
voice_n=len(voice_data)
voice_taille=int(len(voice_data)/10)
voice_datap=voice_data[0:voice_taille]
voice_t=np.arange(len(voice_datap))
voice_t=voice_t/voice_fe
voice_T=1*voice_fe

print(sound_fe)
print(len(sound_data))
print(voice_fe)
print(len(voice_data))