import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os
#FECHA: 27/OCUTBRE/2024

#--------------------------------------------------------------------
#TODAS LAS FUNCIONES RETORNAN LOS ARREGLOS DE TIPO NUMPY

"""
Para correr el programa tienes que 
estar en la cartpeta del proyecto esto se 
debe a que hay una ruta especifica 
donde se guarda el histograma
"""
#--------------------------------------------------------------------
def frecuencia_pixeles_grises(imagen_gris):
    # Asegúrate de que la imagen esté en formato uint8
    imagen_gris = imagen_gris.astype(np.uint8)
    # Usar np.bincount para contar las frecuencias de cada valor de píxel
    frecuencias = np.bincount(imagen_gris.flatten(), minlength=256)
    # Normalizar las frecuencias dividiendo por el número total de píxeles
    tam = imagen_gris.shape
    total_pixeles = tam[0] * tam[1]
    frecuencias_normalizadas = frecuencias / total_pixeles
    # Calcular la frecuencia acumulada
    frecuencia_acumulada = np.cumsum(frecuencias_normalizadas)
    #retorna la frecuencia acumulada para el uso en la ecualizacion Uniforme
    return frecuencia_acumulada


def ordenarImagen(imagen):
    #PONER LA IMAGEN EN ORDEN RGB
    img_rgb = cv.cvtColor(imagen, cv.COLOR_BGR2RGB)
    return img_rgb

def redondear_personalizado(numero):
    #FUNCION PARA REDONDEAR NUMERO
    decimal = numero - int(numero)
    #Si el numero es menor 0.4 se redondeara para abajo
    if decimal <= 0.4:
        return int(numero)
    #Si el numero es 0.6 se redondeara para arriba
    elif decimal >= 0.6:
        return int(numero) + 1
    else:
        return round(numero)
    
def expancion_imagen(imagen,max = 255,min = 0):
    MAX = max
    MIN = min
    # fmin es el valor minimo de gris en la imagen
    fmin = np.min(imagen)
    #fmax es el valor maximo de gris en la imagen
    fmax = np.max(imagen)
    #se aplica la formula de expancion
    imagen_expansion = ((imagen - fmin)/(fmax - fmin)) * (MAX - MIN)  + MIN
    
    imagen_expansion = np.clip(imagen_expansion, MIN, MAX).astype(np.uint8)
    
    return imagen_expansion

def contraccion_imagen(imagen,max = 255,min = 0):
    MAX = max
    MIN = min
    fmin = np.min(imagen)
    fmax = np.max(imagen)
    #se aplica la imagen de contraccion
    imagen_contraccion = redondear_personalizado(((MAX - MIN)/(fmax -fmin)))*(imagen-fmin) + MIN
    imagen_contraccion = np.clip(imagen_contraccion, MIN, MAX).astype(np.uint8)
    return imagen_contraccion

    
def e_uniforme(frecuencia,imagen):
    lista = []
    MAX = 255
    MIN = 0
    fmin = np.min(imagen)
    fmax = np.max(imagen)
    tam = imagen.shape

    #Se multiplica el ancho por el alto para que solo tengamos una lista de una sola dimension y sea facil trabajar
    imagen = imagen.reshape(tam[0]*tam[1])
    list(imagen)
    # en el for se usa la formula de ecualizacion uniforme
    for i in imagen:
        u = (fmax - fmin)*frecuencia[i] + fmin
        u = redondear_personalizado(u)
        u = round(u, 2)
        lista.append(u)
    lista = np.array(lista).reshape(tam[0],tam[1])
    return lista

#En esta clase guardaremos las imagenes que se vayan definiendo
class Crear_imagen(object):
    def __init__ (self,imagen):
        self.imagen = imagen
        self.ruta = ''
    #Guarda el arreglo de alguna operacion que hiciste
    def guardarImagen(self,ruta):
            self.ruta = ruta
            cv.imwrite(ruta,self.imagen)
    #Devuelve la ruta de la imagen
    def dar_ruta(self):
        return self.ruta
    def dar_imagen(self):
        return self.imagen

class Imagen(object):
    def __init__(self,ruta_imagen):
        self.ruta_imagen = ruta_imagen

        self.img = cv.imread(self.ruta_imagen)
    
    def guardar(self,name):
        #gurdamos en la carpeta img
        cv.imwrite(f'img/{name}.jpg',self.img)
    #Muestra la imagen
    def showImage(self):
        cv.imshow("Show image",self.img)
        cv.waitKey(0)
        cv.destroyAllWindows()
    #Devuelve el arreglo de la imagen carganda
    def dar_arreglo(self):
        #Para que podamos manipular la imagen tenemmos que cambiar a rgb
        return self.img














class Operacion(object):
    def __init__(self, imagen,imagen2 = None):
        #Esto debe ser el arreglo de la imagen
        self.img = imagen.dar_arreglo()
        #Verifica si existe una imagen2 
        if(imagen2 is not None):
            self.img2 = imagen2.dar_arreglo()
        else:
            self.img2 = None
        #verifica si es una imgen de color
        if len(self.img.shape) == 3:
            print("Esta operacion es con una imagen de color")
            self.gray_img =cv.cvtColor(self.img,cv.COLOR_BGR2GRAY)
            self.b, self.g, self.r = cv.split(self.img)
        #Si no es una imgen de color el self.img pasa a ser self.gray_img
        else:
            self.gray_img = self.img



    def suma_escalar(self,numero = 0):
    #Esta operacion suma un escalar a la imagen
        if(numero >0):
            suma = cv.add(self.img,numero)
        else:
            numero = abs(numero)
            suma = cv.subtract(self.img,numero)
        return suma
    
    def multiplicacion_escalar(self,numero = 0):
    #Esta operacion resta un escala de la imagen
        multiplicacion = cv.multiply(self.img,numero)
        return multiplicacion
    
    def operacion_or(self,tamaño = None):
        #Cambia el tamaño si este se definio en la funcion
        if tamaño is None:
            tamaño = self.img.shape
            print(tamaño)
        img1 = cv.resize(self.img,(tamaño[1],tamaño[0]))
        img2 = cv.resize(self.img2, (tamaño[1],tamaño[0]))
        or_img = cv.bitwise_or(img1,img2)
        return or_img
    
    def operacion_and(self,tamaño = None):
        #Cambia el tamaño si este se definio en la funcion
        if tamaño is None:
            tamaño = self.img.shape
            print(tamaño)
        img1 = cv.resize(self.img,(tamaño[1],tamaño[0]))
        img2 = cv.resize(self.img2, (tamaño[1],tamaño[0]))
        and_img = cv.bitwise_and(img1,img2)
        return and_img
    
    def operacion_xor(self,tamaño = None):
        #Cambia el tamaño si este se definio en la funcion
        if tamaño is None:
            tamaño = self.img.shape
        img1 = cv.resize(self.img,(tamaño[1],tamaño[0]))
        img2 = cv.resize(self.img2, (tamaño[1],tamaño[0]))
        xor_img = cv.bitwise_xor(img1,img2)
        return xor_img
    
    def operacion_gris(self):
        #retorna el arreglo de la imagen en gris
        return self.gray_img
    
    def operacion_umbralizado(self,umbral = 127):
        _, umbralizada = cv.threshold(self.gray_img,umbral,255,cv.THRESH_BINARY)
        return umbralizada
    
    def operacion_contraccion_color(self,max = 255,min = 0):
        #La contraccion para imagenes de color
        b = contraccion_imagen(self.b,max,min)
        g = contraccion_imagen(self.g,max,min)
        r = contraccion_imagen(self.r,max,min)
        bgr = cv.merge([b,g,r])
        return bgr
    def operacion_expancion_color(self,max = 255,min = 0):
        #llama 3 veces a la expancion pero para cada canal de la imagen
        b = expancion_imagen(self.b,max,min)
        g = expancion_imagen(self.g,max,min)
        r = expancion_imagen(self.r,max,min)
        bgr = cv.merge([b,g,r])
        return bgr
    
    
    def desplazamiento_color(self,numero = 0):
        b = self.b + numero
        g =self.g + numero
        r = self.r + numero
        bgr = cv.merge([b,g,r])
        return bgr
    
    #Reutilzamos las operaciones que se hicieron para los grises
    def ecualizacion_Uniforme_color(self):
        #Sacamos la frecuencia relativa de cada canal
        fb = frecuencia_pixeles_grises(self.b)
        fg = frecuencia_pixeles_grises(self.g)
        fr = frecuencia_pixeles_grises(self.r)
        b = e_uniforme(fb,self.b)
        g = e_uniforme(fg,self.g)
        r = e_uniforme(fr,self.r)

        bgr = cv.merge([b,g,r])
        return bgr
    
    def operacion_contraccion(self,max = 255,min = 0):
        #llamamos a la funcion que realiza la contraccion
        contraccion = contraccion_imagen(self.gray_img,max,min)
        return contraccion
    
    def operacion_expancion(self,max = 255,min = 0):
        expancion = expancion_imagen(self.gray_img,max,min)
        return expancion

    def ecualizacion_Uniforme(self):
        #Sacamos la frecuencia relativa de cada pixel
        frecuencia = frecuencia_pixeles_grises(self.gray_img)
        uniforme = e_uniforme(frecuencia,self.gray_img)
        return uniforme
    
    def desplazamiento(self,numero = 0):
        # print(self.img)
        # tam = self.img.shape
        # print(tam)
        # desplazamiento = []
        # for i in self.img:
        #     for j in i:
        #         for k in j:   
        #             # print(k)
        #             if(k + numero >255):
        #                 desplazamiento.append(255)
        #             elif(k + numero < 0):
        #                 desplazamiento.append(0)
        #             else:
        #                 desplazamiento.append(k)
        # desplazamiento = np.array(desplazamiento).reshape((tam[0],tam[1],3))
        # print(desplazamiento)
        # return desplazamiento
        print(self.img)
        tam = self.img.shape
        print(tam)
        # Desplazamiento de la imagen, asegurando que los valores se mantengan entre 0 y 255
        desplazamiento = self.img.astype(np.int32) + numero  # Convertimos a int32 para evitar overflow
        desplazamiento = np.clip(desplazamiento, 0, 255)      # Limitamos a [0, 255]
        return desplazamiento.astype(np.uint8)  # Convertimos de nuevo a uint8
    



    def suma_dos_img(self):
        # Asegurarse de que ambas imágenes tengan el mismo tamaño
        img1= cv.resize(self.img, (self.img2.shape[1], self.img2.shape[0]))
        # Sumar las imágenes usando cv2.add()
        suma = cv.add(img1, self.img2)
        return suma
    
    def resta_dos_img(self):
        img1 = cv.resize(self.img, (self.img2.shape[1], self.img2.shape[0]))

        # Restar las imágenes usando cv2.subtract()
        resta = cv.subtract(img1, self.img2)
        return resta
    def mul_dos_img(self):
        img1 = cv.resize(self.img, (self.img2.shape[1], self.img2.shape[0]))
        # Multiplicar las imágenes en color
        multiplicacion = cv.multiply(img1, self.img2)
        return multiplicacion
    
    def operacion_inverso(self):
        inverso = cv.bitwise_not(self.img)
        return inverso
    
    def extraccion_canales(self):
        if(len(self.img.shape) == 3):
            self.b,self.g,self.r = cv.split(self.img)
            self.b = cv.merge([self.b, np.zeros_like(self.b), np.zeros_like(self.b)])  # Solo azul
            self.g = cv.merge([np.zeros_like(self.g), self.g, np.zeros_like(self.g)])  # Solo verde
            self.r = cv.merge([np.zeros_like(self.r), np.zeros_like(self.r), self.r])  # Solo rojo
            return self.b,self.g,self.r

        else:
            canales_gris = cv.split(self.img)
            return  canales_gris,canales_gris,canales_gris

    def filtro_mediana(self, parametro = None):
        imagen_2 = []
        tam = self.img.shape
        print(tam)
        tam_1 = tam[0]
        tam_2 = tam[1]
        for i in range(tam_1):
            for j in range(tam_2):
                
                if (0 < i < tam_1 - 1) and (0 < j < tam_2 - 1):
                    lista = []
                    lista1 =[]
                    for k in range(0,3):
                        lista.append(self.img[i-1][j-1][k])
                        lista.append(self.img[i-1][j][k])
                        lista.append(self.img[i][j-1][k])
                        lista.append(self.img[i+1][j+1][k])
                        lista.append(self.img[i+1][j][k])
                        lista.append(self.img[i][j+1][k])
                        lista.append(self.img[i+1][j-1][k])
                        lista.append(self.img[i-1][j+1][k])
                        lista.sort()
                        x = lista[4]
                        lista1.append(x)
                        lista = []
                    imagen_2.append(lista1)
                else:
                    imagen_2.append(self.img[i][j])
        imagen_2 = np.array(imagen_2).reshape(tam)
        return imagen_2

    def hacer_histograma_grises(self,nombre_archivo = None):
        # Histograma de la imagen en escala de grises
        if(len(self.img.shape) != 3):
            plt.hist(self.gray_img.ravel(), bins=256, range=[0, 256])
            plt.title('Histograma en Escala de Grises')
            if nombre_archivo:
                plt.savefig(f'img/{nombre_archivo}.jpg')  # Guarda la gráfica en formato PNG
                print(f'Gráfica guardada como {nombre_archivo}.jpg')
            # Histograma de los canales de color
            # plt.show()
    
    def hacer_histograma_colores(self,nombre_archivo = None):
        if(len(self.img.shape) ==3):
            color = ('b', 'g', 'r')
            for i, col in enumerate(color):
                hist = cv.calcHist([self.img], [i], None, [255], [0, 255])
                plt.plot(hist, color=col)
                plt.xlim([0, 255])

            plt.title('Histograma de la Imagen')
            # plt.show()
            if nombre_archivo:
                ruta_g = os.path.abspath('img2') 
                plt.savefig(f'{ruta_g}\{nombre_archivo}.jpg')  # Guarda la gráfica en formato PNG
                print(f'Gráfica guardada como {nombre_archivo}.jpg')
                plt.close() 
                ruta = os.path.abspath(f'img2/{nombre_archivo}.jpg')
                return ruta

        else:
            
                plt.hist(self.gray_img.ravel(), bins=256, range=[0, 256])
                plt.title('Histograma')
                if nombre_archivo:
                    ruta_g = os.path.abspath('img2') 
                    plt.savefig(f'{ruta_g}\{nombre_archivo}.jpg')  # Guarda la gráfica en formato PNG
                    print(f'Gráfica guardada como {nombre_archivo}.jpg')
                    ruta = os.path.abspath(f'/img2/{nombre_archivo}.jpg')
                    return ruta
                
    
    def ruidoSP(self, probabilidad = 0.005):
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


    def ruido_gaussiano(self, media = 0, desviacion = 25):
        ruido = np.random.normal(media, desviacion, self.img.shape).astype(np.float32)
        imagen_ruidosa = self.img.astype(np.float32) + ruido
        imagen_ruidosa = np.clip(imagen_ruidosa, 0, 255).astype(np.uint8)
        return imagen_ruidosa
    

    def dar_arreglo(self):
        #Para que podamos manipular la imagen tenemmos que cambiar a rgb
        return self.img
if __name__ == '__main__':
    imagen = Imagen('img/b.jpg')
    imagen_2 = Imagen('img/b.jpg')
    print(imagen.img)
    print("sdlfjsldf")
    operacion = Operacion(imagen,imagen_2)
    o = operacion.filtro_mediana()
    print(o)