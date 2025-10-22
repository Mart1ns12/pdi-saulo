import cv2
import numpy as np
from PIL import Image, ImageTk

class ColorModel:
    def __init__(self):
        pass

    def rgb_to_rgba(self, image):
        """Converte imagem RGB para RGBA adicionando canal alpha"""
        if len(image.shape) == 3 and image.shape[2] == 3:
            # Adiciona canal alpha com valor 255 (opaco)
            alpha_channel = np.ones((image.shape[0], image.shape[1], 1), dtype=image.dtype) * 255
            rgba_image = np.concatenate([image, alpha_channel], axis=2)
            return rgba_image
        return image

    def rgba_to_rgb(self, image):
        """Converte imagem RGBA para RGB removendo canal alpha"""
        if len(image.shape) == 3 and image.shape[2] == 4:
            return image[:, :, :3]
        return image

    def rgb_to_cmyk(self, image):
        """Converte imagem RGB para CMYK"""
        if len(image.shape) == 3 and image.shape[2] == 3:
            # Normaliza para 0-1
            rgb = image.astype(np.float32) / 255.0
            
            # Calcula CMYK
            k = 1 - np.max(rgb, axis=2)
            c = (1 - rgb[:, :, 0] - k) / (1 - k + 1e-8)
            m = (1 - rgb[:, :, 1] - k) / (1 - k + 1e-8)
            y = (1 - rgb[:, :, 2] - k) / (1 - k + 1e-8)
            
            # Converte de volta para 0-255
            cmyk = np.stack([c, m, y, k], axis=2)
            cmyk = np.clip(cmyk * 255, 0, 255).astype(np.uint8)
            return cmyk
        return image

    def cmyk_to_rgb(self, image):
        """Converte imagem CMYK para RGB"""
        if len(image.shape) == 3 and image.shape[2] == 4:
            # Normaliza para 0-1
            cmyk = image.astype(np.float32) / 255.0
            
            # Calcula RGB
            r = (1 - cmyk[:, :, 0]) * (1 - cmyk[:, :, 3])
            g = (1 - cmyk[:, :, 1]) * (1 - cmyk[:, :, 3])
            b = (1 - cmyk[:, :, 2]) * (1 - cmyk[:, :, 3])
            
            # Converte de volta para 0-255
            rgb = np.stack([r, g, b], axis=2)
            rgb = np.clip(rgb * 255, 0, 255).astype(np.uint8)
            return rgb
        return image

    def rgb_to_hsv(self, image):
        """Converte imagem RGB para HSV"""
        if len(image.shape) == 3 and image.shape[2] == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return image

    def hsv_to_rgb(self, image):
        """Converte imagem HSV para RGB"""
        if len(image.shape) == 3 and image.shape[2] == 3:
            return cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
        return image

    def rgb_to_lab(self, image):
        """Converte imagem RGB para LAB"""
        if len(image.shape) == 3 and image.shape[2] == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        return image

    def lab_to_rgb(self, image):
        """Converte imagem LAB para RGB"""
        if len(image.shape) == 3 and image.shape[2] == 3:
            return cv2.cvtColor(image, cv2.COLOR_LAB2BGR)
        return image

    def rgb_to_gray(self, image):
        """Converte imagem RGB para tons de cinza"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Converte de volta para 3 canais para manter consistência
            return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        return image

    def to_tk_image(self, cv_image):
        """Converte imagem OpenCV para formato Tkinter"""
        if len(cv_image.shape) == 3:
            if cv_image.shape[2] == 4:  # RGBA
                rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGRA2RGB)
            else:  # RGB
                rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        else:  # Grayscale
            rgb = cv_image
        
        img = Image.fromarray(rgb)
        return ImageTk.PhotoImage(img)
