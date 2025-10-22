from tkinter import Tk, filedialog, messagebox, simpledialog
from models.model import Model
from views.view import View

class Controller:
    def __init__(self):
        self.root = Tk()
        self.root.title("PDI Studio - Sistema Interativo de Processamento de Imagens")
        self.root.geometry("1600x900")

        # Model
        self.model = Model()

        # View
        self.view = View(self.root, controller=self)

    # ========== Métodos principais ==========
    def run(self):
        self.root.mainloop()

    def open_image(self):
        path = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Arquivos de imagem", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if path:
            # Carrega imagem original
            original_image = self.model.load_image(path)
            if original_image:
                # Exibe imagem original e processada
                self.view.image_panel.show_original_image(original_image)
                self.view.image_panel.show_processed_image(original_image)
                
                # Atualiza histograma
                self.view.control_panel.update_histogram(self.model.processed)
                
                self.view.log_action(f"Imagem carregada: {path}")

    def save_image(self):
        if self.model.processed is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")]
        )
        if path:
            self.model.save_image(path)
            self.view.log_action(f"Imagem salva em: {path}")

    def reset_image(self):
        """Reset imagem para estado original"""
        original_image = self.model.get_original_tk_image()
        processed_image = self.model.reset_image()
        
        if original_image and processed_image:
            self.view.image_panel.show_original_image(original_image)
            self.view.image_panel.show_processed_image(processed_image)
            self.view.control_panel.update_histogram(self.model.processed)
            self.view.log_action("Imagem resetada para estado original.")

    # ========== Conversões de Cores ==========
    def convert_to_rgba(self):
        result = self.model.convert_to_rgba()
        if result:
            self.view.image_panel.show_processed_image(result)
            self.view.control_panel.update_histogram(self.model.processed)
            self.view.log_action("Conversão RGB → RGBA aplicada.")

    def convert_to_cmyk(self):
        result = self.model.convert_to_cmyk()
        if result:
            self.view.image_panel.show_processed_image(result)
            self.view.control_panel.update_histogram(self.model.processed)
            self.view.log_action("Conversão RGB → CMYK aplicada.")

    def convert_to_hsv(self):
        result = self.model.convert_to_hsv()
        if result:
            self.view.image_panel.show_processed_image(result)
            self.view.control_panel.update_histogram(self.model.processed)
            self.view.log_action("Conversão RGB → HSV aplicada.")

    def convert_to_lab(self):
        result = self.model.convert_to_lab()
        if result:
            self.view.image_panel.show_processed_image(result)
            self.view.control_panel.update_histogram(self.model.processed)
            self.view.log_action("Conversão RGB → LAB aplicada.")

    def convert_to_gray(self):
        result = self.model.convert_to_gray()
        if result:
            self.view.image_panel.show_processed_image(result)
            self.view.control_panel.update_histogram(self.model.processed)
            self.view.log_action("Conversão para tons de cinza aplicada.")

    # ========== Ajustes de Histograma ==========
    def apply_equalization(self):
        result = self.model.equalize_histogram()
        if result:
            self.view.image_panel.show_processed_image(result)
            self.view.control_panel.update_histogram(self.model.processed)
            self.view.log_action("Equalização de histograma aplicada.")

    def update_brightness(self, brightness):
        """Atualiza brilho em tempo real - sempre a partir da imagem original"""
        # Pega os valores atuais de contraste e threshold
        contrast = self.view.control_panel.contrast_var.get()
        
        # Se contraste não está no padrão, aplica ambos
        if contrast != 1.0:
            result = self.model.adjust_brightness_contrast(brightness, contrast)
        else:
            result = self.model.adjust_brightness(brightness)
        
        if result:
            self.view.image_panel.show_processed_image(result)
            self.view.control_panel.update_histogram(self.model.processed)

    def update_contrast(self, contrast):
        """Atualiza contraste em tempo real - sempre a partir da imagem original"""
        # Pega os valores atuais de brilho
        brightness = self.view.control_panel.brightness_var.get()
        
        # Se brilho não está no padrão, aplica ambos
        if brightness != 0:
            result = self.model.adjust_brightness_contrast(brightness, contrast)
        else:
            result = self.model.adjust_contrast(contrast)
        
        if result:
            self.view.image_panel.show_processed_image(result)
            self.view.control_panel.update_histogram(self.model.processed)

    def apply_brightness_contrast(self, brightness, contrast):
        """Aplica brilho e contraste simultaneamente"""
        result = self.model.adjust_brightness_contrast(brightness, contrast)
        if result:
            self.view.image_panel.show_processed_image(result)
            self.view.control_panel.update_histogram(self.model.processed)
            self.view.log_action(f"Brilho: {brightness}, Contraste: {contrast} aplicados.")

    def update_threshold(self, threshold):
        """Atualiza threshold em tempo real - sempre a partir da imagem original"""
        result = self.model.apply_binary_threshold(threshold)
        if result:
            self.view.image_panel.show_processed_image(result)
            self.view.control_panel.update_histogram(self.model.processed)

    # ========== Diálogos de Ajuste ==========
    def show_brightness_dialog(self):
        brightness = simpledialog.askfloat("Ajustar Brilho", "Digite o valor de brilho (-100 a +100):", 
                                          minvalue=-100, maxvalue=100, initialvalue=0)
        if brightness is not None:
            result = self.model.adjust_brightness(brightness)
            if result:
                self.view.image_panel.show_processed_image(result)
                self.view.control_panel.update_histogram(self.model.processed)
                self.view.log_action(f"Brilho ajustado para: {brightness}")

    def show_contrast_dialog(self):
        contrast = simpledialog.askfloat("Ajustar Contraste", "Digite o valor de contraste (0.5 a 3.0):", 
                                       minvalue=0.5, maxvalue=3.0, initialvalue=1.0)
        if contrast is not None:
            result = self.model.adjust_contrast(contrast)
            if result:
                self.view.image_panel.show_processed_image(result)
                self.view.control_panel.update_histogram(self.model.processed)
                self.view.log_action(f"Contraste ajustado para: {contrast}")

    def show_brightness_contrast_dialog(self):
        brightness = simpledialog.askfloat("Ajustar Brilho", "Digite o valor de brilho (-100 a +100):", 
                                          minvalue=-100, maxvalue=100, initialvalue=0)
        if brightness is not None:
            contrast = simpledialog.askfloat("Ajustar Contraste", "Digite o valor de contraste (0.5 a 3.0):", 
                                           minvalue=0.5, maxvalue=3.0, initialvalue=1.0)
            if contrast is not None:
                result = self.model.adjust_brightness_contrast(brightness, contrast)
                if result:
                    self.view.image_panel.show_processed_image(result)
                    self.view.control_panel.update_histogram(self.model.processed)
                    self.view.log_action(f"Brilho: {brightness}, Contraste: {contrast} aplicados.")

    def show_binary_threshold_dialog(self):
        threshold = simpledialog.askinteger("Limiarização Binária", "Digite o valor de threshold (0 a 255):", 
                                           minvalue=0, maxvalue=255, initialvalue=128)
        if threshold is not None:
            result = self.model.apply_binary_threshold(threshold)
            if result:
                self.view.image_panel.show_processed_image(result)
                self.view.control_panel.update_histogram(self.model.processed)
                self.view.log_action(f"Limiarização binária aplicada com threshold: {threshold}")

    # ========== Operações de Limiarização ==========
    def apply_otsu_threshold(self):
        result = self.model.apply_otsu_threshold()
        if result:
            self.view.image_panel.show_processed_image(result)
            self.view.control_panel.update_histogram(self.model.processed)
            self.view.log_action("Limiarização Otsu aplicada.")

    def apply_adaptive_threshold_mean(self):
        result = self.model.apply_adaptive_threshold('mean')
        if result:
            self.view.image_panel.show_processed_image(result)
            self.view.control_panel.update_histogram(self.model.processed)
            self.view.log_action("Limiarização adaptativa (média) aplicada.")

    def apply_adaptive_threshold_gaussian(self):
        result = self.model.apply_adaptive_threshold('gaussian')
        if result:
            self.view.image_panel.show_processed_image(result)
            self.view.control_panel.update_histogram(self.model.processed)
            self.view.log_action("Limiarização adaptativa (Gaussiana) aplicada.")

    # ========== Métodos de compatibilidade ==========
    def apply_gray(self):
        self.convert_to_gray()

    def display_image(self, image):
        self.view.image_panel.show_processed_image(image)

    def log_action(self, text):
        self.view.control_panel.add_log(text)
