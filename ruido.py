#aver amigo pruébalos, si no funcionan pásame el código con los cambios y yo debugeo 
import numpy as np
def agregar_ruidoSP(self, probabilidad):
        alto, ancho = self.img.shape[:2]
        imagen_ruidosa = self.img.copy()

        # Cantidad de píxeles afectados
        cantidad_ruido = int(probabilidad * imagen_ruidosa.size // imagen_ruidosa.shape[-1])

        # Píxeles de "sal" (blancos)
        coords_sal = [np.random.randint(0, dim - 1, cantidad_ruido) for dim in imagen_ruidosa.shape[:2]]
        imagen_ruidosa[coords_sal[0], coords_sal[1]] = 255

        # Píxeles de "pimienta" (negros)
        coords_pimienta = [np.random.randint(0, dim - 1, cantidad_ruido) for dim in imagen_ruidosa.shape[:2]]
        imagen_ruidosa[coords_pimienta[0], coords_pimienta[1]] = 0

        return imagen_ruidosa

    
    
def agregar_ruido_gaussiano(self, media, desviacion):
        ruido = np.random.normal(media, desviacion, self.img.shape).astype(np.float32)
        imagen_ruidosa = self.img.astype(np.float32) + ruido
        imagen_ruidosa = np.clip(imagen_ruidosa, 0, 255).astype(np.uint8)
        return imagen_ruidosa