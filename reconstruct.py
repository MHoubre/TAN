# -*- coding: utf-8 -*-
"""
Created on Wed May  2 14:19:46 2018

@author:  Auriac - Dautricourt - Houbre - Michaux
"""
import numpy as np

#reconst prend en argument un tableau à deux entrées V[m,k], le nombre de 
#points du signal de la voix n, le pas de découpage pas et retourne une 
#liste v[n] reconstruite.
def reconst(V, n, pas):
   #On commence par calculer les découpes :
   L=len(V)
   l=len(V[0])
   a=np.zeros((L,l), dtype=complex) #Construit une matrice vide de mêmes dimensions que V
   for i in range(0,L): #Pour chaque ligne (=pour chaque tranche)
      a[i]=np.fft.ifftn(V[i])
   
   #Puis on reconstruit le signal :
   v=np.zeros(n)
   for i in range(0, n):
       m = int(i/pas)
       print(m)
       q = int(i-m*pas)
       print(q)
       v[i] = a[m,q] + a[m+1, q-pas]
   return v