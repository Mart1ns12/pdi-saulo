import cv2
import numpy as np


class EdgeModel:
    def __init__(self):
        pass

    def _to_gray(self, image_bgr: np.ndarray) -> np.ndarray:
        if image_bgr is None:
            return None
        if len(image_bgr.shape) == 2:
            return image_bgr
        return cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    def detect_sobel_edges(self, image_bgr: np.ndarray, ksize: int = 3) -> np.ndarray:
        gray = self._to_gray(image_bgr)
        if gray is None:
            return None
        dx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
        dy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
        mag = cv2.magnitude(dx, dy)
        mag = np.uint8(np.clip(mag / (mag.max() + 1e-8) * 255.0, 0, 255))
        return mag

    def detect_laplacian_edges(self, image_bgr: np.ndarray, ksize: int = 3) -> np.ndarray:
        gray = self._to_gray(image_bgr)
        if gray is None:
            return None
        lap = cv2.Laplacian(gray, cv2.CV_64F, ksize=ksize)
        edges = cv2.convertScaleAbs(lap)
        return edges

    def detect_canny_edges(self, image_bgr: np.ndarray, threshold1: int = 100, threshold2: int = 200, blur_ksize: int = 3) -> np.ndarray:
        gray = self._to_gray(image_bgr)
        if gray is None:
            return None
        if blur_ksize is not None and int(blur_ksize) > 1:
            k = int(blur_ksize)
            if k % 2 == 0:
                k += 1
            gray = cv2.GaussianBlur(gray, (k, k), 0)
        edges = cv2.Canny(gray, threshold1, threshold2)
        return edges

    def overlay_edges_on_image(self, image_bgr: np.ndarray, edges_uint8: np.ndarray, color=(0, 0, 255), alpha: float = 0.8) -> np.ndarray:
        if image_bgr is None or edges_uint8 is None:
            return image_bgr
        if len(edges_uint8.shape) == 2:
            mask = edges_uint8 > 0
            overlay = image_bgr.copy()
            colored = np.zeros_like(image_bgr)
            colored[:, :] = color
            overlay[mask] = colored[mask]
        else:
            overlay = edges_uint8
        blended = cv2.addWeighted(image_bgr, alpha, overlay, 1 - alpha, 0)
        return blended


