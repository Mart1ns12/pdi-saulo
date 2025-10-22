import cv2
import numpy as np
from PIL import Image, ImageTk

class HistogramModel:
    def __init__(self):
        pass

    def calculate_histogram(self, image, channels=None):
        """Calcula histograma da imagem"""
        if len(image.shape) == 3:
            if channels is None:
                # Histograma para cada canal separadamente
                histograms = []
                colors = ['B', 'G', 'R']
                for i in range(3):
                    hist = cv2.calcHist([image], [i], None, [256], [0, 256])
                    histograms.append((colors[i], hist.flatten()))
                return histograms
            else:
                # Histograma para canal específico
                hist = cv2.calcHist([image], [channels], None, [256], [0, 256])
                return hist.flatten()
        else:
            # Imagem em escala de cinza
            hist = cv2.calcHist([image], [0], None, [256], [0, 256])
            return hist.flatten()

    def equalize_histogram(self, image):
        """Aplica equalização de histograma"""
        if len(image.shape) == 3:
            # Para imagens coloridas, equaliza cada canal separadamente
            channels = cv2.split(image)
            equalized_channels = []
            for channel in channels:
                equalized = cv2.equalizeHist(channel)
                equalized_channels.append(equalized)
            return cv2.merge(equalized_channels)
        else:
            # Para imagens em escala de cinza
            return cv2.equalizeHist(image)

    def adjust_brightness(self, image, brightness):
        """Ajusta brilho da imagem (-100 a +100)"""
        # Converte brightness de -100 a +100 para -255 a +255
        brightness_value = int(brightness * 2.55)
        
        if len(image.shape) == 3:
            # Para imagens coloridas
            adjusted = cv2.convertScaleAbs(image, alpha=1.0, beta=brightness_value)
        else:
            # Para imagens em escala de cinza
            adjusted = cv2.convertScaleAbs(image, alpha=1.0, beta=brightness_value)
        
        return adjusted

    def adjust_contrast(self, image, contrast):
        """Ajusta contraste da imagem (0.5 a 3.0)"""
        # Converte contrast de 0.5-3.0 para 0-255
        contrast_value = float(contrast)
        
        if len(image.shape) == 3:
            # Para imagens coloridas
            adjusted = cv2.convertScaleAbs(image, alpha=contrast_value, beta=0)
        else:
            # Para imagens em escala de cinza
            adjusted = cv2.convertScaleAbs(image, alpha=contrast_value, beta=0)
        
        return adjusted

    def adjust_brightness_contrast(self, image, brightness, contrast):
        """Ajusta brilho e contraste simultaneamente"""
        brightness_value = int(brightness * 2.55)
        contrast_value = float(contrast)
        
        if len(image.shape) == 3:
            # Para imagens coloridas
            adjusted = cv2.convertScaleAbs(image, alpha=contrast_value, beta=brightness_value)
        else:
            # Para imagens em escala de cinza
            adjusted = cv2.convertScaleAbs(image, alpha=contrast_value, beta=brightness_value)
        
        return adjusted

    def get_histogram_stats(self, image):
        """Retorna estatísticas do histograma"""
        if len(image.shape) == 3:
            # Para imagens coloridas, calcula para cada canal
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
            # Para imagens em escala de cinza
            hist = cv2.calcHist([image], [0], None, [256], [0, 256])
            return {
                'mean': np.mean(hist),
                'std': np.std(hist),
                'min': np.min(hist),
                'max': np.max(hist)
            }

    def to_tk_image(self, cv_image):
        """Converte imagem OpenCV para formato Tkinter"""
        if len(cv_image.shape) == 3:
            rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        else:
            rgb = cv_image
        
        img = Image.fromarray(rgb)
        return ImageTk.PhotoImage(img)
