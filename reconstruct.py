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
   #a=np.fft.ifftn(V)
   #PAS POSSIBLE CAR ON NE PREND PAS EN COMPTE Q+N/2 DANS LE CALCUL DE IDFT
   L=len(V)
   l=len(V[0])
   a=np.zeros((L,l)) #Construit une matrice vide de mêmes dimensions que V
   
   #Puis on reconstruit le signal :
   v=np.zeros(n)
   for i in range(0, n-1):
       m = int(i/pas)
       q = i-m*pas
       v[i] = a[m,q] + a[m+1, q-pas]
   return 
