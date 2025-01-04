import tkinter as tk
from tkinter import filedialog, messagebox
import cv2 as cv
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import Ecualizacion_Uniforme as eu
import os
import tkinter.font as font
#FECHA: 27/OCUTBRE/2024
# © 2024 Leonardo. Todos los derechos reservados.
# Este código está protegido por las leyes de derechos de autor. 
# Prohibida su distribución sin el permiso explícito del autor.

"""Asegurarse de tener las librerias descargadas para su uso
    de no ser asi ejecutar
    pip install cv2
    pip install matplotlib
    pip install Pillow

"""
# Ultimo cambio echo fue el 01/11/2024

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
        button_frame = tk.Frame(root, bg="#516680", relief="groove", borderwidth=2)
        button_frame.pack(side=tk.LEFT, padx=15, pady=15, fill="y")

        # Crear un frame para las imágenes
        image_frame = tk.Frame(root, bg="#516680", relief="ridge", borderwidth=2)
        image_frame.pack(anchor='center', padx=15, pady=15, fill="both", expand=True)

        # -----------------------------
        # Sección de Etiquetas de Imagen
        # -----------------------------
        
        f = font.Font(size=35)

        root.configure(bg="#0D3054")
        image_subframe1 = tk.Frame(image_frame, width=300, height=300, bg="#BCD5FF", relief="groove", borderwidth=2)
        image_subframe1.grid(row=0, column=0, padx=15, pady=15, sticky="NW")

        image_subframe2 = tk.Frame(image_frame, width=300, height=300, bg="#BCD5FF", relief="groove", borderwidth=2)
        image_subframe2.grid(row=1, column=0, padx=15, pady=15, sticky="SW")

        image_subframe3 = tk.Frame(image_frame, width=300, height=600, bg="#BCD5FF", relief="groove", borderwidth=2)
        image_subframe3.grid(row=0, column=1, rowspan=2, padx=15, pady=15, sticky="E")

        # Etiquetas de texto e imagen con fuente y colores mejorados
        self.text_label1 = tk.Label(image_subframe1, text="Imagen 1", font=("Arial", 12, "bold"), bg="#ffffff")
        self.text_label1.pack(side=tk.TOP, pady=(10, 5))  # Espacio superior ajustado

        self.image_label1 = tk.Label(image_subframe1, text="Vista Previa Imagen 1", bg="#e6e6e6")
        self.image_label1.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.text_label2 = tk.Label(image_subframe2, text="Imagen 2", font=("Arial", 12, "bold"), bg="#ffffff")
        self.text_label2.pack(side=tk.TOP, pady=(10, 5))

        self.image_label2 = tk.Label(image_subframe2, text="Vista Previa Imagen 2", bg="#e6e6e6")
        self.image_label2.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.text_label3 = tk.Label(image_subframe3, text="Resultado", font=("Arial", 12, "bold"), bg="#ffffff")
        self.text_label3.pack(side=tk.TOP, pady=(10, 5))

        self.image_label3 = tk.Label(image_subframe3, text="Vista Previa Imagen 3", bg="#e6e6e6")
        self.image_label3.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Configuración de expansión y distribución uniforme
        image_frame.grid_rowconfigure(0, weight=1)
        image_frame.grid_rowconfigure(1, weight=1)
        image_frame.grid_columnconfigure(0, weight=1)
        image_frame.grid_columnconfigure(1, weight=1)
        # -----------------------------
        # Sección de Carga de Imágenes
        # -----------------------------
        

        carga_frame = tk.LabelFrame(button_frame, text="Carga de Imágenes", padx=10, pady=10,bg="#BECACE",fg="#000000")
        carga_frame.grid(row=0, column=0, sticky="ew", pady=5)
        self.toggle_carga_button = tk.Button(carga_frame, text="Mostrar/Ocultar Carga de Imágenes", command=self.toggle_carga,bg="#BBBFBF",fg="#000000")
        self.toggle_carga_button['font'] = f = font.Font(size=10)
        self.toggle_carga_button.grid(row=0, column=0, pady=5, sticky="ew")
        # Marco para la carga de imágenes
        self.carga_oculta_frame = tk.Frame(carga_frame,bg="#BECACE")
        self.load_button = tk.Button(self.carga_oculta_frame, text="Cargar Primera Imagen", command=self.cargar_imagen)
        self.load_button.grid(row=0, column=0, pady=5, sticky="ew")
        self.load_button2 = tk.Button(self.carga_oculta_frame, text="Cargar Segunda Imagen", command=self.cargar_imagen2)
        self.load_button2.grid(row=1, column=0, pady=5, sticky="ew")
        # Agregar el marco de carga oculta al marco de carga
        self.carga_oculta_frame.grid(row=1, column=0, sticky="ew")
        # -----------------------------
        # Sección de Operaciones de Imagen
        # -----------------------------

        self.operaciones_frame = tk.LabelFrame(button_frame, text="Operaciones", padx=10, pady=10,bg="#BECACE",fg="#000000")
        self.operaciones_frame.grid(row=1, column=0, sticky="ew", pady=5)
        self.toggle_operaciones_button = tk.Button(self.operaciones_frame, text="Mostrar/Ocultar Operaciones", command=self.toggle_operaciones,bg="#BBBFBF",fg="#000000")
        self.toggle_operaciones_button['font'] = f = font.Font(size=10)
        self.toggle_operaciones_button.grid(row=0, column=0, pady=5, sticky="ew")
        # Marco para las operaciones ocultas
        self.operaciones_ocultas_frame = tk.Frame(self.operaciones_frame,bg="#BECACE")


        
        self.label_expancion = tk.Label(self.operaciones_ocultas_frame, text="Valores MAX,MIN EXPANCION(Ejemplo:255,0):")
        self.label_expancion.grid(row=0, column=0, pady=5, sticky="w")
        self.entrada_expancion = tk.Entry(self.operaciones_ocultas_frame)
        self.entrada_expancion.grid(row=1, column=0, pady=5, sticky="ew")
        self.expansion_button = tk.Button(self.operaciones_ocultas_frame, text="Aplicar Expansión", command=self.aplicar_expansion)
        self.expansion_button.grid(row=2, column=0, pady=5, sticky="ew")


        
        self.label_contraccion = tk.Label(self.operaciones_ocultas_frame, text="Valor de MAX,MIN CONTRACION(Ejemplo:255,0):")
        self.label_contraccion.grid(row=3, column=0, pady=5, sticky="w")
        self.entrada_contraccion = tk.Entry(self.operaciones_ocultas_frame)
        self.entrada_contraccion.grid(row=4, column=0, pady=5, sticky="ew")
        self.contraction_button = tk.Button(self.operaciones_ocultas_frame, text="Aplicar Contracción", command=self.aplicar_contraccion)
        self.contraction_button.grid(row=5, column=0, pady=5, sticky="ew")


        
        self.label_desplazamiento = tk.Label(self.operaciones_ocultas_frame, text="Valor de Desplazamiento:")
        self.label_desplazamiento.grid(row=6, column=0, pady=5, sticky="w")
        self.entrada_desplazamiento = tk.Entry(self.operaciones_ocultas_frame)
        self.entrada_desplazamiento.grid(row=7, column=0, pady=5, sticky="ew")
        self.desplazamiento = tk.Button(self.operaciones_ocultas_frame, text="Desplazamiento (Color)", command=self.aplicar_desplazamiento)
        self.desplazamiento.grid(row=8, column=0, pady=5, sticky="ew")

        #"""SUMA O RESTA POR MEDIO DE UN ESCALARE DE UNA IMAGEN"""
        self.label_suma = tk.Label(self.operaciones_ocultas_frame, text="Valor del Escalar:")
        self.label_suma.grid(row=9, column=0, pady=5, sticky="w")
        self.entrada_suma = tk.Entry(self.operaciones_ocultas_frame)
        self.entrada_suma.grid(row=10, column=0, pady=5, sticky="ew")
        self.suma = tk.Button(self.operaciones_ocultas_frame, text="Suma o resta (suma:_,resta:-3)", command=self.aplicar_suma_resta_escalar)
        self.suma.grid(row=11, column=0, pady=5, sticky="ew")

        #"""UMBRALIZADO DE UNA IMAGEN"""
        self.label_umbralizado = tk.Label(self.operaciones_ocultas_frame, text="Valor del Escalar -> Umbral:")
        self.label_umbralizado.grid(row=12, column=0, pady=5, sticky="w")
        self.entrada_umbralizado = tk.Entry(self.operaciones_ocultas_frame)
        self.entrada_umbralizado.grid(row=13, column=0, pady=5, sticky="ew")
        self.umbralizado = tk.Button(self.operaciones_ocultas_frame, text="Umbralizado de una imagen", command=self.aplicar_umbralizado)
        self.umbralizado.grid(row=14, column=0, pady=5, sticky="ew")
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
        self.logicas_frame = tk.LabelFrame(button_frame, text="Operaciones Lógicas", padx=10, pady=10,bg="#BECACE",fg="#000000")
        self.logicas_frame.grid(row=2, column=0, sticky="ew", pady=5)
        self.toggle_logicas_button = tk.Button(self.logicas_frame, text="Mostrar/Ocultar Operaciones Lógicas", command=self.toggle_logicas,bg="#BBBFBF",fg="#000000")
        self.toggle_carga_button['font'] = f = font.Font(size=10)
        self.toggle_logicas_button.grid(row=0, column=0, pady=5, sticky="ew")
        
        # Marco para las operaciones lógicas ocultas
        self.operaciones_logicas_frame = tk.Frame(self.logicas_frame,bg="#BECACE")
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
        self.extraccion_imagenes_button = tk.Button(self.operaciones_logicas_frame, text="Aplicar Extraccion de Canales", command=self.aplicar_extraccion_canales)
        self.extraccion_imagenes_button.grid(row=8, column=0, pady=5, sticky="ew")
        self.operaciones_logicas_frame.grid(row=1, column=0, sticky="ew")


        
        
        self.filtro_frame = tk.LabelFrame(button_frame, text="Operaciones Filtro", padx=10, pady=10,bg="#BECACE",fg="#000000")
        self.filtro_frame.grid(row=3, column=0, sticky="ew", pady=5)
        self.toggle_filtro_button = tk.Button(self.filtro_frame, text="Mostrar/Ocultar Operaciones de Ruido", command=self.toggle_filtro,bg="#BBBFBF",fg="#000000")
        self.toggle_carga_button['font'] = f = font.Font(size=10)
        self.toggle_filtro_button.grid(row=0, column=0, pady=5, sticky="ew")

        # Marco para las operaciones de filtro aqui ocultas
        self.operaciones_filtro_frame = tk.Frame(self.filtro_frame,bg="#BECACE")

        self.filtro_mediana_imagenes_button = tk.Button(self.operaciones_filtro_frame, text="Aplicar Filtro Mediana", command=self.aplicar_filtro_mediana)
        self.filtro_mediana_imagenes_button.grid(row=0, column=0, pady=5, sticky="ew")
        #Aplicacion de Filtro Prewit
        self.filtro_prewit_imagenes_button = tk.Button(self.operaciones_filtro_frame, text="Aplicar Filtro Prewit", command=self.aplicar_filtro_prewit)
        self.filtro_prewit_imagenes_button.grid(row=1, column=0, pady=5, sticky="ew")

        self.minimo_histograma_imagenes_button = tk.Button(self.operaciones_filtro_frame, text="Aplicar minimo del histograma", command=self.aplicar_minimo_histograma)
        self.minimo_histograma_imagenes_button.grid(row=6, column=0, pady=5, sticky="ew")



        # Botones para las operaciones de filtro y ruido-----------------
        #"""Rudio Gaussiano para las imagenes que se pusieron"
        self.label_ruido_gaussiano = tk.Label(self.operaciones_filtro_frame, text="Valor de media,desviacion (Ejemplo:0,25):")
        self.label_ruido_gaussiano.grid(row=2, column=0, pady=5, sticky="w")
        self.entrada_ruido_gaussiano = tk.Entry(self.operaciones_filtro_frame)
        self.entrada_ruido_gaussiano.grid(row=3, column=0, pady=5, sticky="ew")
        self.ruido_gaussiano_button = tk.Button(self.operaciones_filtro_frame, text="Aplicar ruido gaussiano", command=self.aplicar_ruido_gaussiano)
        self.ruido_gaussiano_button.grid(row=4, column=0, pady=5, sticky="ew")
        # """Aplicar ruido sal y pimienta en las imagenes """
        self.label_ruido_sp = tk.Label(self.operaciones_filtro_frame, text="Valor de probabilidad:(0.05)")
        self.label_ruido_sp.grid(row=5, column=0, pady=5, sticky="w")
        self.entrada_ruido_sp = tk.Entry(self.operaciones_filtro_frame)
        # Aplica ruido sal y pimienta a la imagen
        self.entrada_ruido_sp.grid(row=6, column=0, pady=5, sticky="ew")
        self.ruido_sp = tk.Button(self.operaciones_filtro_frame, text="Ruido sal y pimienta", command=self.aplicar_ruido_sp)
        self.ruido_sp.grid(row=7, column=0, pady=5, sticky="ew")

        # Aplicas la Umbralizacion por minimo del histograma
        self.minimo_histograma_imagenes_button = tk.Button(self.operaciones_filtro_frame, text="Aplicar minimo del histograma", command=self.aplicar_minimo_histograma)
        self.minimo_histograma_imagenes_button.grid(row=8, column=0, pady=5, sticky="ew")

        self.operaciones_filtro_frame.grid(row=1, column=0, sticky="ew")
        



        self.filtro_frame = tk.LabelFrame(button_frame, text="Segmentacion de Imagen", padx=10, pady=10,bg="#BECACE",fg="#000000")
        self.filtro_frame.grid(row=4, column=0, sticky="ew", pady=5)
        self.toggle_filtro_button = tk.Button(self.filtro_frame, text="Mostrar/Ocultar Segmentacipon", command=self.toggle_segmentacion,bg="#BBBFBF",fg="#000000")
        self.toggle_carga_button['font'] = f = font.Font(size=10)
        self.toggle_filtro_button.grid(row=0, column=0, pady=5, sticky="ew")
        # Marco para las operaciones de filtro aqui ocultas
        self.operaciones_segmentacion_frame = tk.Frame(self.filtro_frame,bg="#BECACE")
        self.segmentacion_imagenes_button = tk.Button(self.operaciones_segmentacion_frame, text="Aplicar Segmentacion a Imagen", command=self.aplicar_segmentacion)
        self.segmentacion_imagenes_button.grid(row=0, column=0, pady=5, sticky="ew")
        self.operaciones_filtro_frame.grid(row=1, column=0, sticky="ew")


        # self.morfologia_frame = tk.LabelFrame(button_frame, text="M de Imagen", padx=10, pady=10,bg="#BECACE",fg="#000000")
        # self.morfologia_frame.grid(row=5, column=0, sticky="ew", pady=5)
        # self.toggle_morfologia_button = tk.Button(self.morfologia_frame, text="Mostrar/Ocultar M-D", command=self.toggle_morfologia,bg="#BBBFBF",fg="#000000")
        # self.toggle_carga_button['font'] = f = font.Font(size=10)
        # self.toggle_morfologia_button.grid(row=0, column=0, pady=5, sticky="ew")
        # # Marco para las operaciones de filtro aqui ocultas
        # self.operaciones_morfologia_frame = tk.Frame(self.morfologia_frame,bg="#BECACE")

        # # Se aplica la dilatacion a una imagen binaria
        # self.dilatacion_imagenes_button = tk.Button(self.operaciones_morfologia_frame, text="Aplicar Dilatacion", command=self.aplicar_dilatacion)
        # self.dilatacion_imagenes_button.grid(row=0, column=0, pady=5, sticky="ew")
    
        # self.erosion_imagenes_button = tk.Button(self.operaciones_morfologia_frame, text="Aplicar Erosion", command=self.aplicar_erosion)
        # self.erosion_imagenes_button.grid(row=1, column=0, pady=5, sticky="ew")
        
        # self.apertura_imagenes_button = tk.Button(self.operaciones_morfologia_frame, text="Aplicar Apertura", command=self.aplicar_apertura)
        # self.apertura_imagenes_button.grid(row=2, column=0, pady=5, sticky="ew")
        
        # self.cierre_imagenes_button = tk.Button(self.operaciones_morfologia_frame, text="Aplicar Cierre", command=self.aplicar_cierre)
        # self.cierre_imagenes_button.grid(row=3, column=0, pady=5, sticky="ew")

        # self.tophat_imagenes_button = tk.Button(self.operaciones_morfologia_frame, text="Aplicar top-hat", command=self.aplicar_tophat)
        # self.tophat_imagenes_button.grid(row=4, column=0, pady=5, sticky="ew")

        # self.bothat_imagenes_button = tk.Button(self.operaciones_morfologia_frame, text="Aplicar bot-hat", command=self.aplicar_bothat)
        # self.bothat_imagenes_button.grid(row=5, column=0, pady=5, sticky="ew")

            
        # self.operaciones_morfologia_frame.grid(row=1, column=0, sticky="ew")













        
        # Inicialización de Imágenes
        self.original_image = None
        self.original_image_2 = None
        self.processed_image = None
    # def toggle_morfologia(self):
    #     # Mostrar u ocultar el marco de carga oculta
    #     if self.operaciones_morfologia_frame.winfo_ismapped():
    #         self.operaciones_morfologia_frame.grid_remove()
    #     else:
    #         self.operaciones_morfologia_frame.grid()
    def toggle_segmentacion(self):
        # Mostrar u ocultar el marco de carga oculta
        if self.operaciones_segmentacion_frame.winfo_ismapped():
            self.operaciones_segmentacion_frame.grid_remove()
        else:
            self.operaciones_segmentacion_frame.grid()
    def toggle_filtro(self):
        # Mostrar u ocultar el marco de carga oculta
        if self.operaciones_filtro_frame.winfo_ismapped():
            self.operaciones_filtro_frame.grid_remove()
        else:
            self.operaciones_filtro_frame.grid()

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
            self.display_image(self.imagen2.dar_arreglo(),self.image_label2)

    def cargar_imagen(self):
        # Abrir un archivo de imagen
        file_path = filedialog.askopenfilename()
        print(file_path)
        if file_path:
            self.imagen1 = eu.Imagen(file_path)
            self.original_image = self.imagen1
            print(self.imagen1)
            self.display_image(self.imagen1.dar_arreglo(),self.image_label1)
    def display_image(self, img, label):
        # Verificar si la imagen está en formato BGR y convertirla a RGB
        imagen = img
        tam = imagen.shape
        
        # Convertir BGR a RGB si es necesario
        if len(imagen.shape) == 3 and imagen.shape[2] == 3:
            imagen = cv.cvtColor(imagen, cv.COLOR_BGR2RGB)

        # Redimensionar la imagen si es necesario
        tam1, tam2 = tam[0], tam[1]
        if tam1 >= 500 and tam2 >= 640 or (tam1 >= 640 and tam2 >= 500):
            tam1 //= 2
            tam2 //= 2
            print(tam)
            imagen = cv.resize(imagen, (tam2, tam1))
        elif tam1 > 600 and tam2 > 1000 or (tam1 > 1000 and tam2 > 800):
            tam1 //= 3
            tam2 //= 3
            imagen = cv.resize(imagen, (tam2, tam1))

        img_pil = Image.fromarray(imagen)
        img_tk = ImageTk.PhotoImage(img_pil)

        # Actualizar la etiqueta de imagen
        label.configure(image=img_tk)
        label.image = img_tk  # Mantener una referencia a la imagen para evitar que se recoja
        

        # image_rgb = cv.cvtColor(image_cv, cv.COLOR_BGR2RGB)
        # image_pil = Image.fromarray(image_rgb)
        # self.current_image = ImageTk.PhotoImage(image_pil)
        # self.image_label1.config(image=self.current_image)


    def aplicar_expansion(self):
        if self.original_image is not None:
            try:
                maximo_input = self.entrada_expancion.get()                
                expancion_image = eu.Operacion(self.original_image.dar_arreglo())
                # Comprobar si maximo_input está vacío y manejarlo adecuadamente
                if maximo_input:  # Si hay un valor ingresado
                    maximo = tuple(map(int, maximo_input.split(',')))  # Convertir a tupla de enteros
                    expancion_image = expancion_image.operacion_expancion_color(maximo[0], maximo[1])
                else:  # Si no se ingresó ningún valor
                    expancion_image = expancion_image.operacion_expancion_color()  # Llama sin argumentos
                
                img_cargada = guardar_imagen(expancion_image, 'Expansion')
                
                self.display_image(img_cargada.dar_arreglo(),self.image_label3)
            except ValueError:
                messagebox.showerror("Error", "Introduce un número válido para el desplazamiento")
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")


    def aplicar_contraccion(self):
        if self.original_image is not None:
            try:
                maximo_input = self.entrada_contraccion.get()
                print(maximo_input)
                
                contraccion_image = eu.Operacion(self.original_image.dar_arreglo())
                
                # Comprobar si maximo_input está vacío y manejarlo adecuadamente
                if maximo_input:  # Si hay un valor ingresado
                    maximo = tuple(map(int, maximo_input.split(',')))  # Convertir a tupla de enteros
                    contraccion_image = contraccion_image.operacion_contraccion_color(maximo[0], maximo[1])
                else:  # Si no se ingresó ningún valor
                    contraccion_image = contraccion_image.operacion_contraccion_color()  # Llama sin argumentos
                #Devolver objeto Imagen() para pasarlo a display_imgage
                img_cargada = guardar_imagen(contraccion_image, 'Contraccion')
                self.display_image(img_cargada.dar_arreglo(),self.image_label3)
            except ValueError:
                messagebox.showerror("Error", "Introduce un número válido para el desplazamiento")
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")

    def aplicar_ruido_gaussiano(self):
        if self.original_image is not None:
            try:
                maximo_input = self.entrada_ruido_gaussiano.get()
                print(maximo_input)
                
                ruido_gaussiano_image = eu.Operacion(self.original_image.dar_arreglo())
                
                # Comprobar si maximo_input está vacío y manejarlo adecuadamente
                if maximo_input:  # Si hay un valor ingresado
                    maximo = tuple(map(int, maximo_input.split(',')))  # Convertir a tupla de enteros
                    ruido_gaussiano_image = ruido_gaussiano_image.ruido_gaussiano(maximo[0], maximo[1])
                else:  # Si no se ingresó ningún valor
                    ruido_gaussiano_image = ruido_gaussiano_image.ruido_gaussiano()  # Llama sin argumentos
                #Devolver objeto Imagen() para pasarlo a display_imgage
                img_cargada = guardar_imagen(ruido_gaussiano_image, 'ruido_gaussiano')
                self.display_image(img_cargada.dar_arreglo(),self.image_label3)
            except ValueError:
                messagebox.showerror("Error", "Introduce un número válido para el desplazamiento")
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
    
    def aplicar_ruido_sp(self):
            if self.original_image is not None:
                try:
                    #Necesitamos tomar un valor de desplazamiento que se define en la interfaz
                    ruido = self.entrada_ruido_sp.get() # Obtener valor de desplazamiento
                    ruidoSP = eu.Operacion(self.original_image.dar_arreglo())
                    if ruido:
                        ruidoSP = ruidoSP.ruidoSP(float(ruido))  # Usar el valor
                    else:
                        ruidoSP = ruidoSP.ruidoSP()
                    img_cargada = guardar_imagen(ruidoSP, 'ruido_sal_pimienta')
                    self.display_image(img_cargada.dar_arreglo(),self.image_label3)
                except ValueError:
                    messagebox.showerror("Error", "Introduce un número válido para el desplazamiento")
            else:
                messagebox.showerror("Error", "Cargar una imagen primero")
            
        
    def aplicar_desplazamiento(self):
        if self.original_image is not None:
            try:
                #Necesitamos tomar un valor de desplazamiento que se define en la interfaz
                valor_desplazamiento = self.entrada_desplazamiento.get()  # Obtener valor de desplazamiento
                desplazamiento_image = eu.Operacion(self.original_image.dar_arreglo())
                if valor_desplazamiento:
                    desplazamiento_image = desplazamiento_image.desplazamiento(int(valor_desplazamiento))
                else:
                    desplazamiento_image = desplazamiento_image.desplazamiento()  # Usar el valor
                img_cargada = guardar_imagen(desplazamiento_image, 'Desplazamiento')
                self.display_image(img_cargada.dar_arreglo(),self.image_label3)
            except ValueError:
                messagebox.showerror("Error", "Introduce un número válido para el desplazamiento")
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")

    def aplicar_suma_resta_escalar(self):
        if self.original_image is not None:
            try:
                #Necesitamos tomar un valor de desplazamiento que se define en la interfaz
                suma_resta = self.entrada_suma.get()  # Obtener valor de desplazamiento
                suma_imagen = eu.Operacion(self.original_image.dar_arreglo())
                if suma_resta:
                    suma_imagen = suma_imagen.suma_escalar(int(suma_resta))  # Usar el valor
                else:
                    suma_imagen = suma_imagen.suma_escalar()
                img_cargada = guardar_imagen(suma_imagen, 'Suma_escalar')
                self.display_image(img_cargada.dar_arreglo(),self.image_label3)
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
                umbralizado = eu.Operacion(self.original_image.dar_arreglo())
                if umbral:
                    umbralizado = umbralizado.operacion_umbralizado(int(umbral))  # Usar el valor
                else:
                    umbralizado = umbralizado.operacion_umbralizado()
                img_cargada = guardar_imagen(umbralizado, 'umbralizado')
                self.display_image(img_cargada.dar_arreglo(),self.image_label3)
            except ValueError:
                messagebox.showerror("Error", "Introduce un número válido para el desplazamiento")
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
        
    def aplicar_EU(self):
        if self.original_image is not None:
            #Llamamos a la clase Operacion
            ecualizacion_uni_image = eu.Operacion(self.original_image.dar_arreglo())
            #Llamamos a la operacion ecualizacion Uniforme
            ecualizacion_uni_image = ecualizacion_uni_image.ecualizacion_Uniforme_color()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            img_cargada = guardar_imagen(ecualizacion_uni_image,'Ecualizacion_Uni')
            
            self.display_image(img_cargada.dar_arreglo(),self.image_label3)
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
    
    def aplicar_operacion_or(self):
        if self.original_image is not None and self.original_image_2 is not None :
            #Llamamos a la clase Operacion
            operacion_or = eu.Operacion(self.original_image.dar_arreglo(), self.original_image_2.dar_arreglo())
            #Llamamos a la operacion OR
            operacion_or = operacion_or.operacion_or()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            img_cargada = guardar_imagen(operacion_or,'Operacion_OR')
            
            self.display_image(img_cargada.dar_arreglo(),self.image_label3)
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")

    def aplicar_operacion_and(self):
        #Deben haber dos imagenes cargadas para que puedas realizar la operacion 
        if self.original_image is not None and self.original_image_2 is not None:
            #Llamamos a la clase Operacion
            operacion_and = eu.Operacion(self.original_image.dar_arreglo(), self.original_image_2.dar_arreglo())
            #Llamamos a la operacion AND
            operacion_and = operacion_and.operacion_and()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            img_cargada = guardar_imagen(operacion_and,'Operacion_AND')
            
            self.display_image(img_cargada.dar_arreglo(),self.image_label3)
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
        
    def aplicar_operacion_xor(self):
        if self.original_image is not None and self.original_image_2 is not None:
            #Llamamos a la clase Operacion
            operacion_xor = eu.Operacion(self.original_image.dar_arreglo(), self.original_image_2.dar_arreglo())
            #Llamamos a la operacion XOR
            operacion_xor = operacion_xor.operacion_xor()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            img_cargada = guardar_imagen(operacion_xor,'Operacion_XOR')
            
            self.display_image(img_cargada.dar_arreglo(),self.image_label3)
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")

    #----------------------------------------OPERACIONS ARITMETICAS---------------------------------------------------------------
    def aplicar_suma_dos_imagenes(self):
        if self.original_image is not None and self.original_image_2 is not None :
            #Llamamos a la clase Operacion
            suma_dos_img = eu.Operacion(self.original_image.dar_arreglo(), self.original_image_2.dar_arreglo())
            #Llamamos a la operacion SUMA
            suma_dos_img = suma_dos_img.suma_dos_img()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            img_cargada = guardar_imagen(suma_dos_img,'suma_dos_img')
            
            self.display_image(img_cargada.dar_arreglo(),self.image_label3)
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
    def aplicar_resta_dos_imagenes(self):
        if self.original_image is not None and self.original_image_2 is not None :
            #Llamamos a la clase Operacion
            resta_dos_img = eu.Operacion(self.original_image.dar_arreglo(), self.original_image_2.dar_arreglo())
            #Llamamos a la operacion RESTA
            resta_dos_img = resta_dos_img.resta_dos_img()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            img_cargada = guardar_imagen(resta_dos_img,'resta_dos_img')
            
            self.display_image(img_cargada.dar_arreglo(),self.image_label3)
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
        
    def aplicar_mul_dos_imagenes(self):
        if self.original_image is not None and self.original_image_2 is not None :
            #Llamamos a la clase Operacion
            mul_dos_img = eu.Operacion(self.original_image.dar_arreglo(), self.original_image_2.dar_arreglo())
            #Llamamos a la operacion MULTIPLICACION
            mul_dos_img = mul_dos_img.mul_dos_img()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            img_cargada = guardar_imagen(mul_dos_img,'mul_dos_img')
            
            self.display_image(img_cargada.dar_arreglo(),self.image_label3)
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
        #-------------------------------------------------------------------------------------------------------
    def aplicar_gris(self):
        if self.original_image is not None:
            #Llamamos a la clase Operacion
            mul_dos_img = eu.Operacion(self.original_image.dar_arreglo())
            #Llamamos a la operacion MULTIPLICACION
            mul_dos_img = mul_dos_img.operacion_gris()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            img_cargada = guardar_imagen(mul_dos_img,'gris_imagen')
            
            self.display_image(img_cargada.dar_arreglo(),self.image_label3)
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
    def aplicar_inverso(self):
        if self.original_image is not None:
            #Llamamos a la clase Operacion
            mul_dos_img = eu.Operacion(self.original_image.dar_arreglo())
            #Llamamos a la operacion INVERSO
            mul_dos_img = mul_dos_img.operacion_inverso()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            img_cargada = guardar_imagen(mul_dos_img,'inverso_imagen')
        
            self.display_image(img_cargada.dar_arreglo(),self.image_label3)
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")

    def aplicar_extraccion_canales(self):
        if self.original_image is not None:
            #Llamamos a la clase Operacion
            mul_dos_img = eu.Operacion(self.original_image.dar_arreglo())
            #Llamamos a la operacion INVERSO
            b,g,r = mul_dos_img.extraccion_canales()
            #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
            #"""SOLO MOSTRARA LA IMAGEN DEL CANAL ROJO"
            img_cargada = guardar_imagen(b,'b')
            img_cargada = guardar_imagen(g,'g')
            img_cargada = guardar_imagen(r,'r')
        
            self.display_image(img_cargada.dar_arreglo(),self.image_label3)
            messagebox.showerror("AVISO", "Solo esta mostrando el canal rojo pero todas fueron guardadas")
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")
    
    def aplicar_histograma_color(self):
        if self.original_image is not None:
            print(self.original_image)
            # Crear el histograma
            histograma = eu.Operacion(self.original_image.dar_arreglo())
            histograma = histograma.hacer_histograma_colores('histograma')
            print(histograma)
                        
            # Crear la imagen a partir del histograma
            if(histograma !=None):
                img_cargada = eu.Imagen(histograma)
                # Asegúrate de que estás usando un Label específico para el histograma
                self.display_image(img_cargada.dar_arreglo(), self.image_label3)
        
        else:
            messagebox.showerror("Error", "Cargar una imagen primero")

    def aplicar_filtro_mediana(self):
            if self.original_image is not None:
                #Llamamos a la clase Operacion
                f_mediana = eu.Operacion(self.original_image.dar_arreglo())
                #Llamamos a la operacion INVERSO
                f_mediana = f_mediana.filtro_mediana()
                #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
                img_cargada = guardar_imagen(f_mediana,'filtro_mediana')
            
                self.display_image(img_cargada.dar_arreglo(),self.image_label3)
            else:
                messagebox.showerror("Error", "Cargar una imagen primero")

    def aplicar_filtro_prewit(self):
            if self.original_image is not None:
                #Llamamos a la clase Operacion
                f_prewitt = eu.Operacion(self.original_image.dar_arreglo())
                #Llamamos a la operacion INVERSO
                f_prewitt = f_prewitt.filtro_prewitt()
                #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
                img_cargada = guardar_imagen(f_prewitt,'filtro_prewitt')
            
                self.display_image(img_cargada.dar_arreglo(),self.image_label3)
            else:
                messagebox.showerror("Error", "Cargar una imagen primero")

    def aplicar_minimo_histograma(self):
        if self.original_image is not None:
                #Llamamos a la clase Operacion
                m_histograma= eu.Operacion(self.original_image.dar_arreglo())
                #Llamamos a la operacion INVERSO
                m_histograma = m_histograma.minimo_histograma()
                #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
                img_cargada = guardar_imagen(m_histograma,'minimo_histograma')
            
                self.display_image(img_cargada.dar_arreglo(),self.image_label3)
        else:
                messagebox.showerror("Error", "Cargar una imagen primero")

    def aplicar_segmentacion(self):
        if self.original_image is not None:
                #Llamamos a la clase Operacion
            m_histograma = eu.Operacion(self.original_image.dar_arreglo())
            imagen_original = m_histograma.operacion_gris()
            # Paso 1: Convertir a escala de grises
            imagen = m_histograma.operacion_gris()
            self.display_image(imagen, self.image_label3)
            self.root.update()
            img_cargada = guardar_imagen(imagen,'imagen_gris_1')

            # Paso 2: Aplicar filtro promedio varias veces
            for i in range(0, 4):
                operacion = eu.Operacion(imagen)
                imagen = operacion.filtro_promedio()
                print(f"Filtro promedio iteración {i+1}: {imagen.shape}")  # Depuración
            self.display_image(imagen, self.image_label3)
            self.root.update()
            img_cargada = guardar_imagen(imagen,'filtro_promedio_2')


            # Paso 3: Aplicar filtro mínimo varias veces
            for i in range(0, 3):
                operacion = eu.Operacion(imagen)
                imagen = operacion.filtro_minimo()
                print(f"Filtro mínimo iteración {i+1}: {imagen.shape}")  # Depuración
            self.display_image(imagen, self.image_label3)
            self.root.update()
            img_cargada = guardar_imagen(imagen,'filtro_minimo_3')

            # Paso 4: Aplicar filtro mediana varias veces
            for i in range(0, 20):
                operacion = eu.Operacion(imagen)
                imagen = operacion.filtro_mediana()
                print(f"Filtro mediana iteración {i+1}: {imagen.shape}")  # Depuración
            self.display_image(imagen, self.image_label3)
            self.root.update()
            img_cargada = guardar_imagen(imagen,'filtro_mediana_4')


            # Paso 5: Reaplicar filtro promedio
            for i in range(0, 3):
                operacion = eu.Operacion(imagen)
                imagen = operacion.filtro_promedio()
            self.display_image(imagen, self.image_label3)
            self.root.update()
            img_cargada = guardar_imagen(imagen,'filtro_promedio_6')


            # Paso 6: Umbralizado
            operacion = eu.Operacion(imagen)
            imagen = operacion.operacion_umbralizado(71)
            self.display_image(imagen, self.image_label3)
            self.root.update()
            img_cargada = guardar_imagen(imagen,'umbralizado_7')


            # Paso 7: Filtros adicionales (máximo y mediana)
            for i in range(0, 3):
                operacion = eu.Operacion(imagen)
                imagen = operacion.filtro_maximo()
            self.display_image(imagen, self.image_label3)
            self.root.update()
            img_cargada = guardar_imagen(imagen,'filtro_maxiomo_8')

            for i in range(0, 13):
                operacion = eu.Operacion(imagen)
                imagen = operacion.filtro_mediana()
            self.display_image(imagen, self.image_label3)
            self.root.update()
            img_cargada = guardar_imagen(imagen,'filtro_mediana_9')


            # Paso 8: Filtro mínimo final
            for i in range(0, 1):
                operacion = eu.Operacion(imagen)
                imagen = operacion.filtro_minimo()

            self.display_image(imagen, self.image_label3)
            img_cargada = guardar_imagen(imagen,'filtro_minimo_10')




            imagen_r = eu.Operacion(self.original_image.dar_arreglo())
            _,_,imagen_r = imagen_r.extraccion_canales()
            self.display_image(imagen_r, self.image_label3)
            self.root.update()
            img_cargada = guardar_imagen(imagen_r,'canal_rojo_11')

            operacion = eu.Operacion(imagen_r)
            imagen_gris = operacion.operacion_gris()
            self.display_image(imagen_gris, self.image_label3)
            self.root.update()
            img_cargada = guardar_imagen(imagen_gris,'operacion_gris_12')


            for i in range(0, 3):
                operacion = eu.Operacion(imagen_gris)
                imagen_gris = operacion.filtro_maximo()
            self.display_image(imagen_gris, self.image_label3)
            self.root.update()
            img_cargada = guardar_imagen(imagen_gris,'filtro_maximo_13')


            for i in range(0, 20):
                operacion = eu.Operacion(imagen_gris)
                imagen_gris = operacion.filtro_mediana()
            self.display_image(imagen_gris, self.image_label3)
            self.root.update()
            img_cargada = guardar_imagen(imagen_gris,'filtro_mediana_14')


            operacion = eu.Operacion(imagen_gris)
            imagen_gris = operacion.operacion_umbralizado(12)
            self.display_image(imagen_gris, self.image_label3)
            self.root.update()
            img_cargada = guardar_imagen(imagen_gris,'umbralizado_15')
            
            operacion = eu.Operacion(imagen_gris)
            imagen_gris = operacion.operacion_inverso()
            self.display_image(imagen_gris, self.image_label3)
            self.root.update()
            img_cargada = guardar_imagen(imagen_gris,'inverso_16')

            # imagen_gris = cv.imread("placa/filtro_maximo_17.jpg")
            # # imagen_gris = cv.cvtColor(imagen_gris,cv.COLOR_BGR2GRAY)
            for i in range(0, 38):
                operacion = eu.Operacion(imagen_gris)
                imagen_gris = operacion.filtro_maximo()
            self.display_image(imagen_gris, self.image_label3) 
            self.root.update()
            img_cargada = guardar_imagen(imagen_gris,'filtro_maximo_17')


            operacion = eu.Operacion(imagen,imagen_gris)
            imagen_gris = operacion.operacion_or()
            self.display_image(imagen_gris, self.image_label3)
            self.root.update()
            img_cargada = guardar_imagen(imagen_gris,'operacion_or_18')

            for i in range(0, 6):
                operacion = eu.Operacion(imagen_gris)
                imagen_gris = operacion.filtro_mediana()
            
            self.display_image(imagen_gris, self.image_label3)
            self.root.update()
            img_cargada = guardar_imagen(imagen_gris,'operacion_mediana_19')

            operacion = eu.Operacion(imagen_gris)
            imagen_gris = operacion.operacion_inverso()
            self.display_image(imagen_gris, self.image_label3)
            self.root.update()
            img_cargada = guardar_imagen(imagen_gris,'umbralizado_total')

            operacion = eu.Operacion(imagen_gris)
            imagen_gris = operacion.filtro_prewitt()
            self.display_image(imagen_gris, self.image_label3)
            self.root.update()
            
            img_cargada = guardar_imagen(imagen_gris,'umbralizado_total_prewitt')


            operacion = eu.Operacion(imagen_original,imagen_gris)
            imagen_gris = operacion.operacion_or()
            self.display_image(imagen_gris, self.image_label3)
            self.root.update()
            
            img_cargada = guardar_imagen(imagen_gris,'umbralizado_total_or')

            

        else:
                messagebox.showerror("Error", "Cargar una imagen primero")





    def aplicar_dilatacion(self):
            if self.original_image is not None:
                #Llamamos a la clase Operacion
                f_dilatacion = eu.Operacion(self.original_image.dar_arreglo())
                #Llamamos a la operacion INVERSO
                f_dilatacion = f_dilatacion.operacion_dilatacion()
                #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
                img_cargada = guardar_imagen(f_dilatacion,'dilatacion')
            
                self.display_image(img_cargada.dar_arreglo(),self.image_label3)
            else:
                messagebox.showerror("Error", "Cargar una imagen primero")
    def aplicar_erosion(self):
            if self.original_image is not None:
                #Llamamos a la clase Operacion
                f_erosion = eu.Operacion(self.original_image.dar_arreglo())
                #Llamamos a la operacion INVERSO
                f_erosion = f_erosion.operacion_erosion()
                #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
                img_cargada = guardar_imagen(f_erosion,'erosion')
            
                self.display_image(img_cargada.dar_arreglo(),self.image_label3)
            else:
                messagebox.showerror("Error", "Cargar una imagen primero")
    def aplicar_apertura(self):
            if self.original_image is not None:
                #Llamamos a la clase Operacion
                apertura = eu.Operacion(self.original_image.dar_arreglo())
                #Llamamos a la operacion INVERSO
                apertura = apertura.operacion_apertura()
                #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
                img_cargada = guardar_imagen(apertura,'apertura')
            
                self.display_image(img_cargada.dar_arreglo(),self.image_label3)
            else:
                messagebox.showerror("Error", "Cargar una imagen primero")
    def aplicar_cierre(self):
            if self.original_image is not None:
                #Llamamos a la clase Operacion
                cierre = eu.Operacion(self.original_image.dar_arreglo())
                #Llamamos a la operacion INVERSO
                cierre = cierre.operacion_cierre()
                #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
                img_cargada = guardar_imagen(cierre,'cierre')
            
                self.display_image(img_cargada.dar_arreglo(),self.image_label3)
            else:
                messagebox.showerror("Error", "Cargar una imagen primero")

    def aplicar_tophat(self):
            if self.original_image is not None:
                #Llamamos a la clase Operacion
                cierre = eu.Operacion(self.original_image.dar_arreglo())
                #Llamamos a la operacion INVERSO
                cierre = cierre.tophat()
                #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
                img_cargada = guardar_imagen(cierre,'tophat')
            
                self.display_image(img_cargada.dar_arreglo(),self.image_label3)
            else:
                messagebox.showerror("Error", "Cargar una imagen primero")
    def aplicar_bothat(self):
            if self.original_image is not None:
                #Llamamos a la clase Operacion
                cierre = eu.Operacion(self.original_image.dar_arreglo())
                #Llamamos a la operacion INVERSO
                cierre = cierre.bothat()
                #Guardamos el objeto Imagen en "img_cargada" para darsela a display_image
                img_cargada = guardar_imagen(cierre,'bothat')
            
                self.display_image(img_cargada.dar_arreglo(),self.image_label3)
            else:
                messagebox.showerror("Error", "Cargar una imagen primero")
# ------------------------------------------------------
# Ejecutar la aplicación
if __name__ == "__main__":
    panel = tk.Tk()
    aplicacion = Editor(panel)
    panel.mainloop()
