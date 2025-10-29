import cv2
import numpy as np
from PIL import Image, ImageTk

class ThresholdModel:
    def __init__(self):
        pass

    def binary_threshold(self, image, threshold_value):
        """Aplica limiarização binária simples"""
        if len(image.shape) == 3:
            # Converte para escala de cinza primeiro
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Aplica limiarização binária
        _, binary = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
        
        # Converte de volta para 3 canais para manter consistência
        return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

    def binary_inverse_threshold(self, image, threshold_value):
        """Aplica limiarização binária inversa"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        _, binary = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)
        return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

    def truncate_threshold(self, image, threshold_value):
        """Aplica limiarização truncada"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        _, truncated = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_TRUNC)
        return cv2.cvtColor(truncated, cv2.COLOR_GRAY2BGR)

    def to_zero_threshold(self, image, threshold_value):
        """Aplica limiarização to zero"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        _, to_zero = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_TOZERO)
        return cv2.cvtColor(to_zero, cv2.COLOR_GRAY2BGR)

    def to_zero_inverse_threshold(self, image, threshold_value):
        """Aplica limiarização to zero inversa"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        _, to_zero_inv = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_TOZERO_INV)
        return cv2.cvtColor(to_zero_inv, cv2.COLOR_GRAY2BGR)

    def otsu_threshold(self, image):
        """Aplica limiarização automática usando método Otsu"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return cv2.cvtColor(otsu, cv2.COLOR_GRAY2BGR)

    def adaptive_threshold_mean(self, image, max_value=255, block_size=11, c=2):
        """Aplica limiarização adaptativa usando média"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        adaptive = cv2.adaptiveThreshold(
            gray, max_value, cv2.ADAPTIVE_THRESH_MEAN_C, 
            cv2.THRESH_BINARY, block_size, c
        )
        return cv2.cvtColor(adaptive, cv2.COLOR_GRAY2BGR)

    def adaptive_threshold_gaussian(self, image, max_value=255, block_size=11, c=2):
        """Aplica limiarização adaptativa usando Gaussiana"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        adaptive = cv2.adaptiveThreshold(
            gray, max_value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, block_size, c
        )
        return cv2.cvtColor(adaptive, cv2.COLOR_GRAY2BGR)

    def range_threshold(self, image, lower_value, upper_value):
        """Aplica segmentação por faixa de valores"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Cria máscara para valores dentro da faixa
        mask = cv2.inRange(gray, lower_value, upper_value)
        
        # Aplica máscara
        result = cv2.bitwise_and(gray, gray, mask=mask)
        return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

    def multi_otsu_threshold(self, image, num_classes=3):
        """Aplica limiarização multi-Otsu para segmentação em múltiplas classes"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Calcula histograma
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist = hist.flatten()
        
        # Normaliza histograma
        hist = hist / hist.sum()
        
        # Calcula limiares usando método de Otsu
        thresholds = self._calculate_multi_otsu_thresholds(hist, num_classes)
        
        # Aplica segmentação
        segmented = np.zeros_like(gray)
        for i, threshold in enumerate(thresholds):
            if i == 0:
                mask = gray <= threshold
            elif i == len(thresholds) - 1:
                mask = gray > thresholds[i-1]
            else:
                mask = (gray > thresholds[i-1]) & (gray <= threshold)
            segmented[mask] = int(255 * (i + 1) / num_classes)
        
        return cv2.cvtColor(segmented, cv2.COLOR_GRAY2BGR)

    def _calculate_multi_otsu_thresholds(self, hist, num_classes):
        """Calcula limiares para segmentação multi-Otsu"""
        # Implementação simplificada - em produção, usar biblioteca scikit-image
        # Para este exemplo, dividimos o histograma em partes iguais
        total_pixels = hist.sum()
        pixels_per_class = total_pixels / num_classes
        
        thresholds = []
        cumulative = 0
        for i in range(num_classes - 1):
            cumulative += pixels_per_class
            threshold = np.argmin(np.abs(np.cumsum(hist) - cumulative))
            thresholds.append(threshold)
        
        return thresholds

    def quantize_threshold(self, image, num_levels=4):
        """Quantiza a imagem em N tons de cinza (uniforme).

        - Aceita imagem BGR ou escala de cinza
        - Retorna imagem BGR para manter consistência
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Garante um número válido de níveis
        try:
            num_levels = int(num_levels)
        except Exception:
            num_levels = 4
        num_levels = max(2, min(256, num_levels))

        # Quantização uniforme por divisão inteira
        level_size = max(1, 256 // num_levels)
        quantized = (gray // level_size) * level_size

        return cv2.cvtColor(quantized.astype(np.uint8), cv2.COLOR_GRAY2BGR)

    def to_tk_image(self, cv_image):
        """Converte imagem OpenCV para formato Tkinter"""
        if len(cv_image.shape) == 3:
            rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        else:
            rgb = cv_image
        
        img = Image.fromarray(rgb)
        return ImageTk.PhotoImage(img)
