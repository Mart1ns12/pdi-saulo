import tkinter as tk
from tkinter import Label

class ImagePanel:
    def __init__(self, root):
        self.frame = tk.Frame(root, bg="#222")
        
        # Cria um canvas com scrollbar
        self.canvas = tk.Canvas(self.frame, bg="#222", highlightthickness=0)
        
        # Scrollbars vertical e horizontal
        self.v_scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.h_scrollbar = tk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        
        # Configura o canvas para usar as scrollbars
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        
        # Posiciona as scrollbars e o canvas
        self.v_scrollbar.pack(side="right", fill="y")
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Frame interno que conterá as imagens
        self.inner_frame = tk.Frame(self.canvas, bg="#222")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        
        # Frame para imagem original (topo)
        self.original_frame = tk.Frame(self.inner_frame, bg="#222")
        self.original_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(self.original_frame, text="Imagem Original", fg="white", bg="#222", font=("Arial", 10, "bold")).pack()
        self.original_label = Label(self.original_frame, bg="#222")
        self.original_label.pack(pady=5)
        
        # Frame para imagem processada (embaixo)
        self.processed_frame = tk.Frame(self.inner_frame, bg="#222")
        self.processed_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(self.processed_frame, text="Imagem Processada", fg="white", bg="#222", font=("Arial", 10, "bold")).pack()
        self.processed_label = Label(self.processed_frame, bg="#222")
        self.processed_label.pack(pady=5)
        
        # Atualiza a scrollregion quando o frame interno mudar de tamanho
        self.inner_frame.bind("<Configure>", self._on_frame_configure)
        
        # Bind para scroll com o mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_frame_configure(self, event=None):
        """Atualiza a região de scroll quando o conteúdo muda"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        """Permite scroll com a roda do mouse"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def show_original_image(self, image):
        """Exibe a imagem original no painel superior"""
        self.original_label.config(image=image)
        self.original_label.image = image  # mantém referência
        self._on_frame_configure()

    def show_processed_image(self, image):
        """Exibe a imagem processada no painel inferior"""
        self.processed_label.config(image=image)
        self.processed_label.image = image  # mantém referência
        self._on_frame_configure()

    def show_image(self, image):
        """Método de compatibilidade - exibe na imagem processada"""
        self.show_processed_image(image)
