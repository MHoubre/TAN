import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.io.wavfile as wave
import scipy.signal as sig
from scipy import fft, ifft

fe, data = wave.read('/home/mael/Téléchargements/la_mono.wav')

n=len(data)
print(n)
taille=int(len(data)/10)


datap=data[0:taille]

t=np.arange(len(datap))
t=t/fe

T=1*fe


def sampling(sound,instant, width):
    w=sig.hanning(int(width)) #fenêtre de largeur width
    cut=[]
    if int(instant+(width/2)) < len(sound) and int((instant-(width/2))) >=0 :    
        sample=sound[int((instant-(width/2))):int(instant+(width/2))]
#        print(len(sample))
        cut = w*sample
    return cut

#s=sampling(data,2*fe,20000)
#ts=np.arange(len(s))   
#plt.plot(ts,s)
samples=[]
width=44100
#print((len(data)/width)-2)


#Fonction qui parcourt le morceau et le découpe.
#arguments, morceau et nombre d'echantillons
#samples number = (len/largeur_des_echantillons)-2
def stocking_samples(sound, samples_number):
    for i in range(1,samples_number+1):
        samp=sampling(sound,(i/samples_number)*fe,int(len(sound)/samples_number))
        samples.append(samp)
        
    return samples
#--------------------------------------------------------
#test  
sample=stocking_samples(data,2041)
#print(len(sample))
#---------------------------------------------------------------
#samp=sampling(data,1*fe,1000)
def short_term_transform(samples):
    transform=[]
    for i in range(len(samples)):
        #tr= np.asarray(samples[i])
        transform.append(np.fft.fft(samples[i],2048))
        
    return transform
    
transf= short_term_transform(sample)