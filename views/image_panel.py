import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

class ImagePanel:
    def __init__(self, root):
        self.frame = tk.Frame(root, bg="#222")
        
        # Frame para imagem original (lado esquerdo)
        self.original_frame = tk.Frame(self.frame, bg="#222")
        self.original_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        tk.Label(self.original_frame, text="Imagem Original", fg="white", bg="#222", font=("Arial", 10, "bold")).pack()
        self.original_label = Label(self.original_frame, bg="#222")
        self.original_label.pack(pady=5, fill="both", expand=True)
        
        # Frame para imagem processada (lado direito)
        self.processed_frame = tk.Frame(self.frame, bg="#222")
        self.processed_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        tk.Label(self.processed_frame, text="Imagem Processada", fg="white", bg="#222", font=("Arial", 10, "bold")).pack()
        self.processed_label = Label(self.processed_frame, bg="#222")
        self.processed_label.pack(pady=5, fill="both", expand=True)


    def _get_max_image_size(self):
        """Calcula o tamanho máximo para as imagens baseado no espaço disponível"""
        # Obtém o tamanho do frame pai
        frame_width = self.frame.winfo_width()
        frame_height = self.frame.winfo_height()
        
        # Se ainda não foi renderizado, usa valores padrão
        if frame_width <= 1 or frame_height <= 1:
            return 400, 300
        
        # Calcula o espaço disponível para cada imagem (metade do espaço menos margens)
        max_width = (frame_width - 20) // 2  
        max_height = frame_height - 80 
        
        return max_width, max_height

    def show_original_image(self, image):
        """Exibe a imagem original no painel esquerdo"""
        self.original_label.config(image=image)
        self.original_label.image = image 

    def show_processed_image(self, image):
        """Exibe a imagem processada no painel direito"""
        self.processed_label.config(image=image)
        self.processed_label.image = image 

    def show_image(self, image):
        """Método de compatibilidade - exibe na imagem processada"""
        self.show_processed_image(image)
