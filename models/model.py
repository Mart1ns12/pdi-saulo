import cv2
from PIL import Image, ImageTk
import numpy as np
from models.color_model import ColorModel
from models.histogram_model import HistogramModel
from models.threshold_model import ThresholdModel
from models.edge_model import EdgeModel

class Model:
    def __init__(self):
        self.original = None
        self.processed = None
        
        # Modelos especializados
        self.color_model = ColorModel()
        self.histogram_model = HistogramModel()
        self.threshold_model = ThresholdModel()
        self.edge_model = EdgeModel()

    def load_image(self, path):
        """Carrega imagem e define como original"""
        self.original = cv2.imread(path)
        self.processed = self.original.copy() if self.original is not None else None
        return self.to_tk_image(self.original) if self.original is not None else None

    def save_image(self, path):
        """Salva a imagem processada"""
        if self.processed is not None:
            cv2.imwrite(path, self.processed)

    def reset_image(self):
        """Reset imagem processada para o estado original"""
        if self.original is not None:
            self.processed = self.original.copy()
            return self.to_tk_image(self.processed)
        return None

    def get_original_tk_image(self):
        """Retorna imagem original em formato Tkinter"""
        return self.to_tk_image(self.original) if self.original is not None else None

    def get_processed_tk_image(self):
        """Retorna imagem processada em formato Tkinter"""
        return self.to_tk_image(self.processed) if self.processed is not None else None

    # ========== Conversões de Cores ==========
    def convert_to_rgba(self):
        if self.processed is not None:
            self.processed = self.color_model.rgb_to_rgba(self.processed)
            return self.to_tk_image(self.processed)
        return None

    def convert_to_cmyk(self):
        if self.processed is not None:
            self.processed = self.color_model.rgb_to_cmyk(self.processed)
            return self.to_tk_image(self.processed)
        return None

    def convert_to_hsv(self):
        if self.processed is not None:
            self.processed = self.color_model.rgb_to_hsv(self.processed)
            return self.to_tk_image(self.processed)
        return None

    def convert_to_lab(self):
        if self.processed is not None:
            self.processed = self.color_model.rgb_to_lab(self.processed)
            return self.to_tk_image(self.processed)
        return None

    def convert_to_gray(self):
        if self.processed is not None:
            self.processed = self.color_model.rgb_to_gray(self.processed)
            return self.to_tk_image(self.processed)
        return None

    # ========== Operações de Histograma ==========
    def equalize_histogram(self):
        if self.processed is not None:
            self.processed = self.histogram_model.equalize_histogram(self.processed)
            return self.to_tk_image(self.processed)
        return None

    def adjust_brightness(self, brightness):
        """Ajusta brilho sempre a partir da imagem original"""
        if self.original is not None:
            self.processed = self.histogram_model.adjust_brightness(self.original.copy(), brightness)
            return self.to_tk_image(self.processed)
        return None

    def adjust_contrast(self, contrast):
        """Ajusta contraste sempre a partir da imagem original"""
        if self.original is not None:
            self.processed = self.histogram_model.adjust_contrast(self.original.copy(), contrast)
            return self.to_tk_image(self.processed)
        return None

    def adjust_brightness_contrast(self, brightness, contrast):
        """Ajusta brilho e contraste sempre a partir da imagem original"""
        if self.original is not None:
            self.processed = self.histogram_model.adjust_brightness_contrast(self.original.copy(), brightness, contrast)
            return self.to_tk_image(self.processed)
        return None

    def calculate_histogram(self):
        if self.processed is not None:
            return self.histogram_model.calculate_histogram(self.processed)
        return None

    # ========== Operações de Limiarização ==========
    def apply_binary_threshold(self, threshold_value):
        """Aplica threshold sempre a partir da imagem original"""
        if self.original is not None:
            self.processed = self.threshold_model.binary_threshold(self.original.copy(), threshold_value)
            return self.to_tk_image(self.processed)
        return None

    def apply_otsu_threshold(self):
        if self.processed is not None:
            self.processed = self.threshold_model.otsu_threshold(self.processed)
            return self.to_tk_image(self.processed)
        return None

    def apply_adaptive_threshold(self, method='mean'):
        if self.processed is not None:
            if method == 'mean':
                self.processed = self.threshold_model.adaptive_threshold_mean(self.processed)
            else:
                self.processed = self.threshold_model.adaptive_threshold_gaussian(self.processed)
            return self.to_tk_image(self.processed)
        return None

    def apply_quantize_threshold(self, num_levels=4):
        """Aplica quantização em N tons de cinza sempre a partir da original"""
        if self.original is not None:
            self.processed = self.threshold_model.quantize_threshold(self.original.copy(), num_levels)
            return self.to_tk_image(self.processed)
        return None

    # ========== Detecção de Bordas (sobreposição na imagem processada) ==========
    def apply_sobel(self, ksize=3):
        if self.processed is not None:
            edges = self.edge_model.detect_sobel_edges(self.processed, ksize=ksize)
            self.processed = self.edge_model.overlay_edges_on_image(self.processed, edges)
            return self.to_tk_image(self.processed)
        return None

    def apply_laplacian(self, ksize=3):
        if self.processed is not None:
            edges = self.edge_model.detect_laplacian_edges(self.processed, ksize=ksize)
            self.processed = self.edge_model.overlay_edges_on_image(self.processed, edges)
            return self.to_tk_image(self.processed)
        return None

    def apply_canny(self, threshold1=100, threshold2=200, blur_ksize=3):
        if self.processed is not None:
            edges = self.edge_model.detect_canny_edges(self.processed, threshold1=threshold1, threshold2=threshold2, blur_ksize=blur_ksize)
            self.processed = self.edge_model.overlay_edges_on_image(self.processed, edges)
            return self.to_tk_image(self.processed)
        return None

    # ========== Conversão ==========
    def to_tk_image(self, cv_image, max_width=None, max_height=None):
        if cv_image is None:
            return None
        
        if len(cv_image.shape) == 3:
            rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        else:
            rgb = cv_image
        
        img = Image.fromarray(rgb)
        
        # Redimensiona se especificado
        if max_width and max_height:
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        return ImageTk.PhotoImage(img)
