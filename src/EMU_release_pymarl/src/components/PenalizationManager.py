import numpy as np
from sklearn.neighbors import BallTree,KDTree
import os
import gc

class PenalizationManager:
  
       
    def __init__(self, umbral_visitas=0, penalizacion_maxima=0.5, beta_penalizacion=0.1):
        self.umbral_visitas = 0 # Límite de visitas antes de penalizar
        self.penalizacion_maxima = 0.5  # Penalización máxima
        self.beta_penalizacion = 0.1  # Controla la curva de penalización

    def penalizacion_sigmoide(self, Ncall):
        """Aplica una penalización sigmoide basada en el número de visitas a un estado."""
        if Ncall > self.umbral_visitas:
            numero=self.penalizacion_maxima / (1 + np.exp(-self.beta_penalizacion * (Ncall - self.umbral_visitas)))
            print ("penalizacion :",numero )
            return numero
        
        return 0  # Sin penalización

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
