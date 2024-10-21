import tkinter as tk
from tkinter import filedialog, messagebox
import cv2 as cv
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import Ecualizacion_Uniforme as eu

"""Asegurarse de tener las librerias descargadas para su uso
    de no ser asi ejecutar
    pip install cv2
    pip install matplotlib
    pip install Pillow

"""

# ------------------------------------------------------
# Panel de Tkinter donde seleccionas imágenes y aplicas funciones
def guardar_imagen(imagen,ruta):
    img = eu.Crear_imagen(imagen)
    n_ruta = filedialog.askdirectory()
    print(n_ruta)
    n_ruta = n_ruta + f'/{ruta}.jpg'
    img.guardarImagen(n_ruta)
    ruta_img = img.dar_ruta()
    return  eu.Imagen(ruta_img)

class Editor:
    def __init__(self, root):
        self.root = root
        root.title("Aplicación de Procesamiento de Imágenes")

        # Crear el marco principal de la ventana
        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Crear un frame para las imágenes
        image_frame = tk.Frame(root)
        image_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # -----------------------------
        # Sección de Etiquetas de Imagen
        # -----------------------------

        self.image_label3 = tk.Label(image_frame)
        self.image_label3.pack(side=tk.TOP, padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.image_label1 = tk.Label(image_frame)
        self.image_label1.pack(side=tk.TOP, padx=10, pady=10, expand=True, fill=tk.BOTH)

        self.image_label2 = tk.Label(image_frame)
        self.image_label2.pack(side=tk.TOP, padx=10, pady=10, expand=True, fill=tk.BOTH)

        # -----------------------------
        # Sección de Carga de Imágenes
        # -----------------------------

        carga_frame = tk.LabelFrame(button_frame, text="Carga de Imágenes", padx=10, pady=10)
        carga_frame.grid(row=0, column=0, sticky="ew", pady=5)
        self.toggle_carga_button = tk.Button(carga_frame, text="Mostrar/Ocultar Carga de Imágenes", command=self.toggle_carga)
        self.toggle_carga_button.grid(row=0, column=0, pady=5, sticky="ew")
        # Marco para la carga de imágenes
        self.carga_oculta_frame = tk.Frame(carga_frame)
        self.load_button = tk.Button(self.carga_oculta_frame, text="Cargar Primera Imagen", command=self.cargar_imagen)
        self.load_button.grid(row=0, column=0, pady=5, sticky="ew")
        self.load_button2 = tk.Button(self.carga_oculta_frame, text="Cargar Segunda Imagen", command=self.cargar_imagen2)
        self.load_button2.grid(row=1, column=0, pady=5, sticky="ew")
        # Agregar el marco de carga oculta al marco de carga
        self.carga_oculta_frame.grid(row=1, column=0, sticky="ew")
        # -----------------------------
        # Sección de Operaciones de Imagen
        # -----------------------------

        self.operaciones_frame = tk.LabelFrame(button_frame, text="Operaciones", padx=10, pady=10)
        self.operaciones_frame.grid(row=1, column=0, sticky="ew", pady=5)
        self.toggle_operaciones_button = tk.Button(self.operaciones_frame, text="Mostrar/Ocultar Operaciones", command=self.toggle_operaciones)
        self.toggle_operaciones_button.grid(row=0, column=0, pady=5, sticky="ew")
        # Marco para las operaciones ocultas
        self.operaciones_ocultas_frame = tk.Frame(self.operaciones_frame)


        self.expansion_button = tk.Button(self.operaciones_ocultas_frame, text="Aplicar Expansión", command=self.aplicar_expansion)
        self.expansion_button.grid(row=0, column=0, pady=5, sticky="ew")
        self.label_expancion = tk.Label(self.operaciones_ocultas_frame, text="Valores MAX,MIN EXPANCION(Ejemplo:255,0):")
        self.label_expancion.grid(row=1, column=0, pady=5, sticky="w")
        self.entrada_expancion = tk.Entry(self.operaciones_ocultas_frame)
        self.entrada_expancion.grid(row=2, column=0, pady=5, sticky="ew")


        self.contraction_button = tk.Button(self.operaciones_ocultas_frame, text="Aplicar Contracción", command=self.aplicar_contraccion)
        self.contraction_button.grid(row=3, column=0, pady=5, sticky="ew")
        self.label_contraccion = tk.Label(self.operaciones_ocultas_frame, text="Valor de MAX,MIN CONTRACION(Ejemplo:255,0):")
        self.label_contraccion.grid(row=4, column=0, pady=5, sticky="w")
        self.entrada_contraccion = tk.Entry(self.operaciones_ocultas_frame)
        self.entrada_contraccion.grid(row=5, column=0, pady=5, sticky="ew")


        self.desplazamiento = tk.Button(self.operaciones_ocultas_frame, text="Desplazamiento (Color)", command=self.aplicar_desplazamiento)
        self.desplazamiento.grid(row=6, column=0, pady=5, sticky="ew")
        self.label_desplazamiento = tk.Label(self.operaciones_ocultas_frame, text="Valor de Desplazamiento:")
        self.label_desplazamiento.grid(row=7, column=0, pady=5, sticky="w")
        self.entrada_desplazamiento = tk.Entry(self.operaciones_ocultas_frame)
        self.entrada_desplazamiento.grid(row=8, column=0, pady=5, sticky="ew")

        #"""SUMA O RESTA POR MEDIO DE UN ESCALARE DE UNA IMAGEN"""
        self.suma = tk.Button(self.operaciones_ocultas_frame, text="Suma o resta (suma:_,resta:-3)", command=self.aplicar_suma_resta_escalar)
        self.suma.grid(row=9, column=0, pady=5, sticky="ew")
        self.label_suma = tk.Label(self.operaciones_ocultas_frame, text="Valor del Escalar:")
        self.label_suma.grid(row=10, column=0, pady=5, sticky="w")
        self.entrada_suma = tk.Entry(self.operaciones_ocultas_frame)
        self.entrada_suma.grid(row=11, column=0, pady=5, sticky="ew")

        #"""UMBRALIZADO DE UNA IMAGEN"""
        self.umbralizado = tk.Button(self.operaciones_ocultas_frame, text="Umbralizado de una imagen", command=self.aplicar_umbralizado)
        self.umbralizado.grid(row=12, column=0, pady=5, sticky="ew")
        self.label_umbralizado = tk.Label(self.operaciones_ocultas_frame, text="Valor del Escalar -> Umbral:")
        self.label_umbralizado.grid(row=13, column=0, pady=5, sticky="w")
        self.entrada_umbralizado = tk.Entry(self.operaciones_ocultas_frame)
        self.entrada_umbralizado.grid(row=14, column=0, pady=5, sticky="ew")
        #Ecualizacion de una imagen
        self.equalize_button = tk.Button(self.operaciones_ocultas_frame, text="Ecualización Uniforme (Color)", command=self.aplicar_EU)
        self.equalize_button.grid(row=15, column=0, pady=5, sticky="ew")
        #Histograma de la imagen 
        self.histograma_button = tk.Button(self.operaciones_ocultas_frame, text="Histograma (Color)", command=self.aplicar_histograma_color)
        self.histograma_button.grid(row=16, column=0, pady=5, sticky="ew")

        # Agregar el marco de operaciones ocultas al marco de operaciones
        self.operaciones_ocultas_frame.grid(row=1, column=0, sticky="ew")

        # -----------------------------
        # Sección de Operaciones Lógicas
        # -----------------------------
        self.logicas_frame = tk.LabelFrame(button_frame, text="Operaciones Lógicas", padx=10, pady=10)
        self.logicas_frame.grid(row=2, column=0, sticky="ew", pady=5)
        self.toggle_logicas_button = tk.Button(self.logicas_frame, text="Mostrar/Ocultar Operaciones Lógicas", command=self.toggle_logicas)
        self.toggle_logicas_button.grid(row=0, column=0, pady=5, sticky="ew")

        # Marco para las operaciones lógicas ocultas
        self.operaciones_logicas_frame = tk.Frame(self.logicas_frame)
        # Botones para las operaciones lógicas-----------------

        self.operacion_or_button = tk.Button(self.operaciones_logicas_frame, text="Aplicar Operación OR", command=self.aplicar_operacion_or)
        self.operacion_or_button.grid(row=0, column=0, pady=5, sticky="ew")

        self.operacion_and_button = tk.Button(self.operaciones_logicas_frame, text="Aplicar Operación AND", command=self.aplicar_operacion_and)
        self.operacion_and_button.grid(row=1, column=0, pady=5, sticky="ew")

        self.operacion_xor_button = tk.Button(self.operaciones_logicas_frame, text="Aplicar Operación XOR", command=self.aplicar_operacion_xor)
        self.operacion_xor_button.grid(row=2, column=0, pady=5, sticky="ew")
        
        # """operaciones artimeticas"""
        #PARA AGREGAR UN CUADRO PARA UN NUEVA OPERACION ES COPIAR ESTO
        self.suma_dos_imagenes_button = tk.Button(self.operaciones_logicas_frame, text="Aplicar Suma de Dos Img", command=self.aplicar_suma_dos_imagenes)
        self.suma_dos_imagenes_button.grid(row=3, column=0, pady=5, sticky="ew")

        self.resta_dos_imagenes_button = tk.Button(self.operaciones_logicas_frame, text="Aplicar Resta de Dos Img", command=self.aplicar_resta_dos_imagenes)
        self.resta_dos_imagenes_button.grid(row=4, column=0, pady=5, sticky="ew")
        #"""OPERACION MULTIPLICACION"""
        self.mul_dos_imagenes_button = tk.Button(self.operaciones_logicas_frame, text="Aplicar Mul de Dos Img", command=self.aplicar_mul_dos_imagenes)
        self.mul_dos_imagenes_button.grid(row=5, column=0, pady=5, sticky="ew")
        # """DAR EL GRIS DE UNA IMAGEN DE COLOR """
        self.gris_imagenes_button = tk.Button(self.operaciones_logicas_frame, text="Aplicar gris a Imagen", command=self.aplicar_gris)
        self.gris_imagenes_button.grid(row=6, column=0, pady=5, sticky="ew")
        # Agregar el marco de operaciones lógicas ocultas al marco de operaciones lógicas
        # """DAR EL INVERSO DE LA IMAGEN"""
        self.inverso_imagenes_button = tk.Button(self.operaciones_logicas_frame, text="Aplicar inverso a Imagen", command=self.aplicar_inverso)
        self.inverso_imagenes_button.grid(row=7, column=0, pady=5, sticky="ew")
        #EXTRACCION DE CANALES
        self.inverso_imagenes_button = tk.Button(self.operaciones_logicas_frame, text="Aplicar Extraccion de Canales", command=self.aplicar_extraccion_canales)
        self.inverso_imagenes_button.grid(row=8, column=0, pady=5, sticky="ew")
        self.operaciones_logicas_frame.grid(row=1, column=0, sticky="ew")

        
        # Inicialización de Imágenes
        self.original_image = None
        self.original_image_2 = None
        self.processed_image = None

    def toggle_carga(self):
        # Mostrar u ocultar el marco de carga oculta
        if self.carga_oculta_frame.winfo_ismapped():
            self.carga_oculta_frame.grid_remove()
        else:
            self.carga_oculta_frame.grid()

    def toggle_operaciones(self):
        # Mostrar u ocultar el marco de operaciones ocultas
        if self.operaciones_ocultas_frame.winfo_ismapped():
            self.operaciones_ocultas_frame.grid_remove()
        else:
            self.operaciones_ocultas_frame.grid()

    def toggle_logicas(self):
        # Mostrar u ocultar el marco de operaciones lógicas ocultas
        if self.operaciones_logicas_frame.winfo_ismapped():
            self.operaciones_logicas_frame.grid_remove()
        else:
            self.operaciones_logicas_frame.grid()





    def cargar_imagen2(self):
        # Abrir un archivo de imagen
        file_path = filedialog.askopenfilename()
        print(file_path)
        if file_path:
            self.imagen2 = eu.Imagen(file_path)
            self.original_image_2 = self.imagen2
            self.display_image(self.imagen2,self.image_label2)

    def cargar_imagen(self):
        # Abrir un archivo de imagen
        file_path = filedialog.askopenfilename()
        print(file_path)
        if file_path:
            self.imagen1 = eu.Imagen(file_path)
            self.original_image = self.imagen1
            print(self.imagen1)
            self.display_image(self.imagen1,self.image_label1)

    def display_image(self, img, label):
        # Verificar si la imagen está en formato BGR y convertirla a RGB
        imagen = img.dar_arreglo()
        tam = imagen.shape
        print(tam)
        tam1 = tam[0]//2
        tam2 = tam[1]//2
    # Verificar si la imagen está en formato BGR y convertirla a RGB
        if len(imagen.shape) == 3 and imagen.shape[2] == 3:  # Si la imagen tiene 3 canales de color
            imagen = cv.cvtColor(imagen, cv.COLOR_BGR2RGB)

        if(tam[0]>600 and tam[1]> 1200):
            imagen = cv.resize(imagen, (tam2,tam1)) 

        img_pil = Image.fromarray(imagen)
        # Convertir la imagen PIL a un formato que Tkinter pueda mostrar
        img_tk = ImageTk.PhotoImage(img_pil)
        # Actualizar la etiqueta de la GUI con la imagen
        label.configure(image=img_tk)
        label.image = img_tk

    # def display_image(self, img):
    #     #A ESTA FUNCION SIMEPRE LE TIENE QUE LLEGAR UN OBJETO IMAGEN()--------------
    #     imagen = img.dar_arreglo()
    #     tam = imagen.shape
    # # Verificar si la imagen está en formato BGR y convertirla a RGB
    #     if len(imagen.shape) == 3 and imagen.shape[2] == 3:  # Si la imagen tiene 3 canales de color
    #         imagen = cv.cvtColor(imagen, cv.COLOR_BGR2RGB)
    #         print(imagen)
    #         tam1 = tam[0]//2
    #         tam2 = tam[1]//2
    #         imagen = cv.resize(imagen, (tam1,tam2,3)) 
    #     else:
    #         tam1 = tam[0]//2
    #         tam2 = tam[1]//2
    #         imagen = cv.resize(imagen, (tam1,tam2))
    #     # Convertir el arreglo numpy a una imagen PIL
    #     img_pil = Image.fromarray(imagen)
    #     # Convertir la imagen PIL a un formato que Tkinter pueda mostrar
    #     img_tk = ImageTk.PhotoImage(img_pil)
    #     # Actualizar la etiqueta de la GUI con la imagen
    #     self.image_label.configure(image=img_tk)
    #     self.image_label.image = img_tk 

    
    



    def aplicar_expansion(self):
        if self.original_image is not None:
            try:
                maximo_input = self.entrada_expancion.get()                
                expancion_image = eu.Operacion(self.original_image)
                # Comprobar si maximo_input está vacío y manejarlo adecuadamente
                if maximo_input:  # Si hay un valor ingresado
                    maximo = tuple(map(int, maximo_input.split(',')))  # Convertir a tupla de enteros
                    expancion_image = expancion_image.operacion_expancion_color(maximo[0], maximo[1])
                else:  # Si no se ingresó ningún valor
                    expancion_image = expancion_image.operacion_expancion_color()  # Llama sin argumentos
                
                img_cargada = guardar_imagen(expancion_image, 'Expansion')
                self.display_image(img_cargada,self.image_label3)
            except ValueError:
                messagebox.showerror("Error", "Introduce un número válido para el desplazamiento")
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")


    def aplicar_contraccion(self):
        if self.original_image is not None:
            try:
                maximo_input = self.entrada_contraccion.get()
                print(maximo_input)
                
                contraccion_image = eu.Operacion(self.original_image)
                
                # Comprobar si maximo_input está vacío y manejarlo adecuadamente
                if maximo_input:  # Si hay un valor ingresado
                    maximo = tuple(map(int, maximo_input.split(',')))  # Convertir a tupla de enteros
                    contraccion_image = contraccion_image.operacion_contraccion_color(maximo[0], maximo[1])
                else:  # Si no se ingresó ningún valor
                    contraccion_image = contraccion_image.operacion_contraccion_color()  # Llama sin argumentos
                #Devolver objeto Imagen() para pasarlo a display_imgage
                img_cargada = guardar_imagen(contraccion_image, 'Contraccion')
                self.display_image(img_cargada,self.image_label3)
            except ValueError:
                messagebox.showerror("Error", "Introduce un número válido para el desplazamiento")
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
    
    def aplicar_desplazamiento(self):
        if self.original_image is not None:
            try:
                #Necesitamos tomar un valor de desplazamiento que se define en la interfaz
                valor_desplazamiento = self.entrada_desplazamiento.get()  # Obtener valor de desplazamiento
                desplazamiento_image = eu.Operacion(self.original_image)
                if valor_desplazamiento:
                    desplazamiento_image = desplazamiento_image.desplazamiento(int(valor_desplazamiento))
                else:
                    desplazamiento_image = desplazamiento_image.desplazamiento()  # Usar el valor
                img_cargada = guardar_imagen(desplazamiento_image, 'Desplazamiento')
                self.display_image(img_cargada,self.image_label3)
            except ValueError:
                messagebox.showerror("Error", "Introduce un número válido para el desplazamiento")
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")

    def aplicar_suma_resta_escalar(self):
        if self.original_image is not None:
            try:
                #Necesitamos tomar un valor de desplazamiento que se define en la interfaz
                suma_resta = self.entrada_suma.get()  # Obtener valor de desplazamiento
                suma_imagen = eu.Operacion(self.original_image)
                if suma_resta:
                    suma_imagen = suma_imagen.suma_escalar(int(suma_resta))  # Usar el valor
                else:
                    suma_imagen = suma_imagen.suma_escalar()
                img_cargada = guardar_imagen(suma_imagen, 'Suma_escalar')
                self.display_image(img_cargada,self.image_label3)
            except ValueError:
                messagebox.showerror("Error", "Introduce un número válido para el desplazamiento")
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
    def aplicar_umbralizado(self):
        if self.original_image is not None:
            try:
                #Necesitamos tomar un valor de desplazamiento que se define en la interfaz
                umbral = self.entrada_umbralizado.get() # Obtener valor de desplazamiento
                print(umbral)
                umbralizado = eu.Operacion(self.original_image)
                if umbral:
                    umbralizado = umbralizado.operacion_umbralizado(int(umbral))  # Usar el valor
                else:
                    umbralizado = umbralizado.operacion_umbralizado()
                img_cargada = guardar_imagen(umbralizado, 'umbralizado')
                self.display_image(img_cargada,self.image_label3)
            except ValueError:
                messagebox.showerror("Error", "Introduce un número válido para el desplazamiento")
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
        
    def aplicar_EU(self):
        if self.original_image is not None:
            #Llamamos a la clase Operacion
            ecualizacion_uni_image = eu.Operacion(self.original_image)
            #Llamamos a la operacion ecualizacion Uniforme
            ecualizacion_uni_image = ecualizacion_uni_image.ecualizacion_Uniforme_color()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            img_cargada = guardar_imagen(ecualizacion_uni_image,'Ecualizacion_Uni')
            
            self.display_image(img_cargada,self.image_label3)
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
    
    def aplicar_operacion_or(self):
        if self.original_image is not None and self.original_image_2 is not None :
            #Llamamos a la clase Operacion
            operacion_or = eu.Operacion(self.original_image, self.original_image_2)
            #Llamamos a la operacion OR
            operacion_or = operacion_or.operacion_or()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            img_cargada = guardar_imagen(operacion_or,'Operacion_OR')
            
            self.display_image(img_cargada,self.image_label3)
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")

    def aplicar_operacion_and(self):
        #Deben haber dos imagenes cargadas para que puedas realizar la operacion 
        if self.original_image is not None and self.original_image_2 is not None:
            #Llamamos a la clase Operacion
            operacion_and = eu.Operacion(self.original_image, self.original_image_2)
            #Llamamos a la operacion AND
            operacion_and = operacion_and.operacion_and()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            img_cargada = guardar_imagen(operacion_and,'Operacion_AND')
            
            self.display_image(img_cargada,self.image_label3)
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
        
    def aplicar_operacion_xor(self):
        if self.original_image is not None and self.original_image_2 is not None:
            #Llamamos a la clase Operacion
            operacion_xor = eu.Operacion(self.original_image, self.original_image_2)
            #Llamamos a la operacion XOR
            operacion_xor = operacion_xor.operacion_xor()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            img_cargada = guardar_imagen(operacion_xor,'Operacion_XOR')
            
            self.display_image(img_cargada,self.image_label3)
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")

    #----------------------------------------OPERACIONS ARITMETICAS---------------------------------------------------------------
    def aplicar_suma_dos_imagenes(self):
        if self.original_image is not None and self.original_image_2 is not None :
            #Llamamos a la clase Operacion
            suma_dos_img = eu.Operacion(self.original_image, self.original_image_2)
            #Llamamos a la operacion SUMA
            suma_dos_img = suma_dos_img.suma_dos_img()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            img_cargada = guardar_imagen(suma_dos_img,'suma_dos_img')
            
            self.display_image(img_cargada,self.image_label3)
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
    def aplicar_resta_dos_imagenes(self):
        if self.original_image is not None and self.original_image_2 is not None :
            #Llamamos a la clase Operacion
            resta_dos_img = eu.Operacion(self.original_image, self.original_image_2)
            #Llamamos a la operacion RESTA
            resta_dos_img = resta_dos_img.resta_dos_img()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            img_cargada = guardar_imagen(resta_dos_img,'resta_dos_img')
            
            self.display_image(img_cargada,self.image_label3)
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
        
    def aplicar_mul_dos_imagenes(self):
        if self.original_image is not None and self.original_image_2 is not None :
            #Llamamos a la clase Operacion
            mul_dos_img = eu.Operacion(self.original_image, self.original_image_2)
            #Llamamos a la operacion MULTIPLICACION
            mul_dos_img = mul_dos_img.mul_dos_img()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            img_cargada = guardar_imagen(mul_dos_img,'mul_dos_img')
            
            self.display_image(img_cargada,self.image_label3)
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
        #-------------------------------------------------------------------------------------------------------
    def aplicar_gris(self):
        if self.original_image is not None:
            #Llamamos a la clase Operacion
            mul_dos_img = eu.Operacion(self.original_image)
            #Llamamos a la operacion MULTIPLICACION
            mul_dos_img = mul_dos_img.operacion_gris()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            img_cargada = guardar_imagen(mul_dos_img,'gris_imagen')
            
            self.display_image(img_cargada,self.image_label3)
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
    def aplicar_inverso(self):
        if self.original_image is not None:
            #Llamamos a la clase Operacion
            mul_dos_img = eu.Operacion(self.original_image)
            #Llamamos a la operacion INVERSO
            mul_dos_img = mul_dos_img.operacion_inverso()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            img_cargada = guardar_imagen(mul_dos_img,'inverso_imagen')
        
            self.display_image(img_cargada,self.image_label3)
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")

    def aplicar_extraccion_canales(self):
        if self.original_image is not None:
            #Llamamos a la clase Operacion
            mul_dos_img = eu.Operacion(self.original_image)
            #Llamamos a la operacion INVERSO
            b,g,r = mul_dos_img.extraccion_canales()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            #"""SOLO MOSTRARA LA IMAGEN DEL CANAL ROJO"
            img_cargada = guardar_imagen(b,'g')
            img_cargada = guardar_imagen(g,'b')
            img_cargada = guardar_imagen(r,'r')
        
            self.display_image(img_cargada,self.image_label3)
            messagebox.showerror("AVISO", "Solo esta mostrando el canal rojo pero todas fueron guardadas")
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
    
    def aplicar_histograma_color(self):
        if self.original_image is not None:
            print(self.original_image)
            # Crear el histograma
            histograma = eu.Operacion(self.original_image)
            histograma = histograma.hacer_histograma_colores('histograma')
            print(histograma)
                        
            # Crear la imagen a partir del histograma
            if(histograma !=None):
                img_cargada = eu.Imagen(histograma)
                # Asegúrate de que estás usando un Label específico para el histograma
                self.display_image(img_cargada, self.image_label3)
        
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
# ------------------------------------------------------
# Ejecutar la aplicación
if __name__ == "__main__":
    panel = tk.Tk()
    aplicacion = Editor(panel)
    panel.mainloop()
