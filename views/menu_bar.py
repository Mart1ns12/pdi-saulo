import tkinter as tk

class MenuBar:
    def __init__(self, root, controller):
        self.controller = controller
        self.menubar = tk.Menu(root)

        # Menu Arquivo
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Abrir", command=controller.open_image)
        file_menu.add_command(label="Salvar como...", command=controller.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=root.quit)
        self.menubar.add_cascade(label="Arquivo", menu=file_menu)

        # Menu Conversão de Cores
        color_menu = tk.Menu(self.menubar, tearoff=0)
        color_menu.add_command(label="RGB → RGBA", command=controller.convert_to_rgba)
        color_menu.add_command(label="RGB → CMYK", command=controller.convert_to_cmyk)
        color_menu.add_command(label="RGB → HSV", command=controller.convert_to_hsv)
        color_menu.add_command(label="RGB → LAB", command=controller.convert_to_lab)
        color_menu.add_separator()
        color_menu.add_command(label="Converter para tons de cinza", command=controller.convert_to_gray)
        self.menubar.add_cascade(label="Conversão de Cores", menu=color_menu)

        # Menu Ajustes
        adjustments_menu = tk.Menu(self.menubar, tearoff=0)
        adjustments_menu.add_command(label="Ajustar Brilho", command=controller.show_brightness_dialog)
        adjustments_menu.add_command(label="Ajustar Contraste", command=controller.show_contrast_dialog)
        adjustments_menu.add_command(label="Brilho e Contraste", command=controller.show_brightness_contrast_dialog)
        adjustments_menu.add_separator()
        adjustments_menu.add_command(label="Equalizar Histograma", command=controller.apply_equalization)
        self.menubar.add_cascade(label="Ajustes", menu=adjustments_menu)

        # Menu Segmentação
        segmentation_menu = tk.Menu(self.menubar, tearoff=0)
        segmentation_menu.add_command(label="Limiarização Binária", command=controller.show_binary_threshold_dialog)
        segmentation_menu.add_command(label="Limiarização Otsu", command=controller.apply_otsu_threshold)
        segmentation_menu.add_command(label="Limiarização Adaptativa (Média)", command=controller.apply_adaptive_threshold_mean)
        segmentation_menu.add_command(label="Limiarização Adaptativa (Gaussiana)", command=controller.apply_adaptive_threshold_gaussian)
        self.menubar.add_cascade(label="Segmentação", menu=segmentation_menu)

        # Menu Detecção de Bordas
        edges_menu = tk.Menu(self.menubar, tearoff=0)
        edges_menu.add_command(label="Sobel...", command=controller.show_sobel_dialog)
        edges_menu.add_command(label="Laplaciano...", command=controller.show_laplacian_dialog)
        edges_menu.add_command(label="Canny...", command=controller.show_canny_dialog)
        self.menubar.add_cascade(label="Detecção de Bordas", menu=edges_menu)

        # Menu Filtros (mantido para compatibilidade)
        filter_menu = tk.Menu(self.menubar, tearoff=0)
        filter_menu.add_command(label="Converter para tons de cinza", command=controller.convert_to_gray)
        filter_menu.add_command(label="Equalizar histograma", command=controller.apply_equalization)
        self.menubar.add_cascade(label="Filtros", menu=filter_menu)
