import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class HistogramCanvas:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        
        # Cria figura do matplotlib
        self.fig = Figure(figsize=(4, 3), dpi=100, facecolor='#333')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#333')
        
        # Configurações do gráfico
        self.ax.tick_params(colors='white', labelsize=8)
        self.ax.set_xlabel('Intensidade', color='white', fontsize=9)
        self.ax.set_ylabel('Frequência', color='white', fontsize=9)
        self.ax.set_title('Histograma', color='white', fontsize=10)
        
        # Cria canvas do Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, self.parent_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Dados do histograma
        self.histogram_data = None
        self.image_type = None

    def update_histogram(self, image):
        """Atualiza o histograma com base na imagem fornecida"""
        if image is None:
            self.clear_histogram()
            return
        
        # Limpa o gráfico anterior
        self.ax.clear()
        self.ax.set_facecolor('#333')
        
        # Determina o tipo de imagem
        if len(image.shape) == 3:
            self._plot_color_histogram(image)
        else:
            self._plot_grayscale_histogram(image)
        
        # Atualiza o canvas
        self.canvas.draw()

    def _plot_grayscale_histogram(self, image):
        """Plota histograma para imagem em escala de cinza"""
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        self.ax.plot(hist, color='white', linewidth=1)
        self.ax.set_xlabel('Intensidade', color='white', fontsize=9)
        self.ax.set_ylabel('Frequência', color='white', fontsize=9)
        self.ax.set_title('Histograma - Escala de Cinza', color='white', fontsize=10)
        self.ax.set_xlim(0, 255)
        self.ax.grid(True, alpha=0.3, color='gray')

    def _plot_color_histogram(self, image):
        """Plota histograma para imagem colorida (3 canais)"""
        colors = ['blue', 'green', 'red']
        labels = ['Canal B', 'Canal G', 'Canal R']
        
        for i, (color, label) in enumerate(zip(colors, labels)):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            self.ax.plot(hist, color=color, linewidth=1, label=label, alpha=0.8)
        
        self.ax.set_xlabel('Intensidade', color='white', fontsize=9)
        self.ax.set_ylabel('Frequência', color='white', fontsize=9)
        self.ax.set_title('Histograma - Canais RGB', color='white', fontsize=10)
        self.ax.set_xlim(0, 255)
        self.ax.legend(fontsize=8, loc='upper right')
        self.ax.grid(True, alpha=0.3, color='gray')

    def plot_histogram_data(self, histogram_data, title="Histograma"):
        """Plota histograma a partir de dados fornecidos"""
        self.ax.clear()
        self.ax.set_facecolor('#333')
        
        if isinstance(histogram_data, list):
            # Múltiplos canais
            colors = ['blue', 'green', 'red']
            labels = ['Canal B', 'Canal G', 'Canal R']
            
            for i, (color, label) in enumerate(zip(colors, labels)):
                if i < len(histogram_data):
                    channel_name, hist = histogram_data[i]
                    self.ax.plot(hist, color=color, linewidth=1, label=label, alpha=0.8)
            
            self.ax.legend(fontsize=8, loc='upper right')
        else:
            # Canal único
            self.ax.plot(histogram_data, color='white', linewidth=1)
        
        self.ax.set_xlabel('Intensidade', color='white', fontsize=9)
        self.ax.set_ylabel('Frequência', color='white', fontsize=9)
        self.ax.set_title(title, color='white', fontsize=10)
        self.ax.set_xlim(0, 255)
        self.ax.grid(True, alpha=0.3, color='gray')
        
        self.canvas.draw()

    def clear_histogram(self):
        """Limpa o histograma"""
        self.ax.clear()
        self.ax.set_facecolor('#333')
        self.ax.set_xlabel('Intensidade', color='white', fontsize=9)
        self.ax.set_ylabel('Frequência', color='white', fontsize=9)
        self.ax.set_title('Histograma', color='white', fontsize=10)
        self.ax.text(0.5, 0.5, 'Nenhuma imagem carregada', 
                    transform=self.ax.transAxes, ha='center', va='center',
                    color='gray', fontsize=12)
        self.canvas.draw()

    def get_histogram_stats(self, image):
        """Retorna estatísticas do histograma"""
        if image is None:
            return None
        
        if len(image.shape) == 3:
            stats = {}
            colors = ['B', 'G', 'R']
            for i, color in enumerate(colors):
                hist = cv2.calcHist([image], [i], None, [256], [0, 256])
                stats[color] = {
                    'mean': np.mean(hist),
                    'std': np.std(hist),
                    'min': np.min(hist),
                    'max': np.max(hist)
                }
            return stats
        else:
            hist = cv2.calcHist([image], [0], None, [256], [0, 256])
            return {
                'mean': np.mean(hist),
                'std': np.std(hist),
                'min': np.min(hist),
                'max': np.max(hist)
            }

# Import necessário para cv2
import cv2
