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
import os
import decoupe as dec
import rf_conduit as rf
import reconstruct as rec

#On demande les chemins des fichiers a utiliser 
#(pour que tout le monde puisse utiliser son path perso):
voice_path=str(input("Entrez le chemin de la voix à utiliser :"+"\n"))
sound_path=str(input("Entrez le chemin du son à utiliser :"+"\n"))

#Préparation du fichier son utilisé.
sound_fe, sound_data = wave.read(sound_path)
sound_n=len(sound_data)
sound_taille=int(len(sound_data)/10)
sound_datap=sound_data[0:sound_taille]
sound_t=np.arange(len(sound_datap))
sound_t=sound_t/sound_fe
sound_T=1*sound_fe

#Préparation du fichier voix utilisé.
voice_fe, voice_data = wave.read(voice_path)
voice_n=len(voice_data)
voice_taille=int(len(voice_data)/10)
voice_datap=voice_data[0:voice_taille]
voice_t=np.arange(len(voice_datap))
voice_t=voice_t/voice_fe
voice_T=1*voice_fe

print("\n"+"fréquence et taille de la voix: ")
print(voice_fe)
print(len(voice_data))
print("\n"+"fréquence et taille du son: ")
print(sound_fe)
print(len(sound_data))

#Exemple d'appel d'une fonction d'un autre fichier :
s=dec.sampling(sound_data,2*sound_fe,20000)