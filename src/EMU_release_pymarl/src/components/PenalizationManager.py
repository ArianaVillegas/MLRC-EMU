import numpy as np
from sklearn.neighbors import BallTree,KDTree
import os
import gc

class PenalizationManager:
  
       
    def __init__(self, umbral_visitas=0, penalizacion_maxima=0.5, beta_penalizacion=0.0009):
        self.umbral_visitas = 10
        self.penalizacion_maxima = 0.5
        self.beta_penalizacion = 0.0009 #0.01 # Ajustado para mejor progresión
    def penalizacion_sigmoide(self, Ncall):
        if Ncall > self.umbral_visitas:
             numero= self.penalizacion_maxima / (1 + np.exp(-self.beta_penalizacion * (Ncall - self.umbral_visitas)))
             
             return numero
    
        return 0
    def penalizacion_sigmoide_mejorada(self ,Ncall):
        if Ncall > self.umbral_visitas:
             numero= self.penalizacion_maxima * (1 - np.exp(-self.beta_penalizacion * (Ncall - self.umbral_visitas)))
            
             return numero
        return 0


    def penalizacion_lineal(self, Ncall):
        """Aplica una penalización lineal basada en el número de visitas a un estado."""
        if Ncall > self.umbral_visitas:
            return min(self.penalizacion_maxima, self.beta_penalizacion * (Ncall - self.umbral_visitas))
        return 0

    def penalizacion_exponencial(self, Ncall):
        """Aplica una penalización exponencial."""
        if Ncall > self.umbral_visitas:
            return min(self.penalizacion_maxima, self.penalizacion_maxima * (1 - np.exp(-self.beta_penalizacion * (Ncall - self.umbral_visitas))))
        return 0
    def penalizacion_inversa(self, Ncall):
        """ Penalización inversa. """
        return self.penalizacion_maxima / (1 + Ncall)
 