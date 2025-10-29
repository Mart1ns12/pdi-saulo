import tkinter as tk
from tkinter import scrolledtext, ttk
from views.histogram_canvas import HistogramCanvas

class ControlPanel:
    def __init__(self, root, controller):
        self.controller = controller
        self.frame = tk.Frame(root, bg="#333", width=300)
        self.frame.pack_propagate(False)
        
        # Variáveis para sliders
        self.brightness_var = tk.DoubleVar(value=0)
        self.contrast_var = tk.DoubleVar(value=1.0)
        self.threshold_var = tk.IntVar(value=128)
        
        self._create_histogram_section()
        self._create_sliders_section()
        self._create_buttons_section()
        self._create_quantize_section()
        self._create_log_section()

    def _create_histogram_section(self):
        """Cria seção do histograma"""
        hist_frame = tk.Frame(self.frame, bg="#333")
        hist_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(hist_frame, text="Histograma", fg="white", bg="#333", font=("Arial", 10, "bold")).pack()
        
        # Canvas do histograma
        self.histogram_canvas = HistogramCanvas(hist_frame)

    def _create_sliders_section(self):
        """Cria seção dos sliders"""
        sliders_frame = tk.Frame(self.frame, bg="#333")
        sliders_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Label(sliders_frame, text="Controles", fg="white", bg="#333", font=("Arial", 10, "bold")).pack()
        
        # Slider de Brilho
        brightness_frame = tk.Frame(sliders_frame, bg="#333")
        brightness_frame.pack(fill="x", pady=2)
        
        tk.Label(brightness_frame, text="Brilho:", fg="white", bg="#333", font=("Arial", 9)).pack(side="left")
        self.brightness_scale = tk.Scale(
            brightness_frame, from_=-100, to=100, orient="horizontal",
            variable=self.brightness_var, bg="#444", fg="white", 
            highlightbackground="#333", command=self._on_brightness_change
        )
        self.brightness_scale.pack(side="right", fill="x", expand=True)
        
        # Slider de Contraste
        contrast_frame = tk.Frame(sliders_frame, bg="#333")
        contrast_frame.pack(fill="x", pady=2)
        
        tk.Label(contrast_frame, text="Contraste:", fg="white", bg="#333", font=("Arial", 9)).pack(side="left")
        self.contrast_scale = tk.Scale(
            contrast_frame, from_=0.5, to=3.0, resolution=0.1, orient="horizontal",
            variable=self.contrast_var, bg="#444", fg="white",
            highlightbackground="#333", command=self._on_contrast_change
        )
        self.contrast_scale.pack(side="right", fill="x", expand=True)
        
        # Slider de Threshold
        threshold_frame = tk.Frame(sliders_frame, bg="#333")
        threshold_frame.pack(fill="x", pady=2)
        
        tk.Label(threshold_frame, text="Threshold:", fg="white", bg="#333", font=("Arial", 9)).pack(side="left")
        self.threshold_scale = tk.Scale(
            threshold_frame, from_=0, to=255, orient="horizontal",
            variable=self.threshold_var, bg="#444", fg="white",
            highlightbackground="#333", command=self._on_threshold_change
        )
        self.threshold_scale.pack(side="right", fill="x", expand=True)

    def _create_buttons_section(self):
        """Cria seção dos botões"""
        buttons_frame = tk.Frame(self.frame, bg="#333")
        buttons_frame.pack(fill="x", padx=5, pady=5)
        
        # Botão Reset
        self.reset_btn = tk.Button(
            buttons_frame, text="Reset", command=self._reset_all,
            bg="#666", fg="white", font=("Arial", 9, "bold")
        )
        self.reset_btn.pack(fill="x", pady=2)
        
        # Botão Aplicar Ajustes
        self.apply_btn = tk.Button(
            buttons_frame, text="Aplicar Ajustes", command=self._apply_adjustments,
            bg="#4CAF50", fg="white", font=("Arial", 9, "bold")
        )
        self.apply_btn.pack(fill="x", pady=2)
        
        # Botão Equalizar Histograma
        self.equalize_btn = tk.Button(
            buttons_frame, text="Equalizar Histograma", command=self._equalize_histogram,
            bg="#2196F3", fg="white", font=("Arial", 9, "bold")
        )
        self.equalize_btn.pack(fill="x", pady=2)

    def _create_quantize_section(self):
        """Cria seção da quantização (tons de cinza)"""
        q_frame = tk.Frame(self.frame, bg="#333")
        q_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(q_frame, text="Quantização (tons de cinza)", fg="white", bg="#333", font=("Arial", 10, "bold")).pack(anchor="w")

        row = tk.Frame(q_frame, bg="#333")
        row.pack(fill="x", pady=2)

        tk.Label(row, text="N níveis:", fg="white", bg="#333", font=("Arial", 9)).pack(side="left")
        self.num_levels_var = tk.IntVar(value=4)
        self.num_levels_spin = tk.Spinbox(
            row, from_=2, to=16, textvariable=self.num_levels_var, width=5,
            bg="#444", fg="white", insertbackground="white"
        )
        self.num_levels_spin.pack(side="left", padx=6)

        apply_btn = tk.Button(
            q_frame, text="Aplicar Quantização", command=self._apply_quantize,
            bg="#795548", fg="white", font=("Arial", 9, "bold")
        )
        apply_btn.pack(fill="x", pady=2)

    def _apply_quantize(self):
        if hasattr(self.controller, 'apply_quantize_gray'):
            n = self.num_levels_var.get()
            self.controller.apply_quantize_gray(n)

    def _create_log_section(self):
        """Cria seção do log"""
        log_frame = tk.Frame(self.frame, bg="#333")
        log_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        tk.Label(log_frame, text="Histórico de Ações", fg="white", bg="#333", font=("Arial", 10, "bold")).pack()
        self.log_area = scrolledtext.ScrolledText(log_frame, width=35, height=15, bg="#111", fg="white")
        self.log_area.pack(fill="both", expand=True, pady=2)

    def _on_brightness_change(self, value):
        """Callback para mudança no slider de brilho"""
        if hasattr(self.controller, 'update_brightness'):
            self.controller.update_brightness(float(value))

    def _on_contrast_change(self, value):
        """Callback para mudança no slider de contraste"""
        if hasattr(self.controller, 'update_contrast'):
            self.controller.update_contrast(float(value))

    def _on_threshold_change(self, value):
        """Callback para mudança no slider de threshold"""
        if hasattr(self.controller, 'update_threshold'):
            self.controller.update_threshold(int(value))

    def _reset_all(self):
        """Reset todos os controles"""
        self.brightness_var.set(0)
        self.contrast_var.set(1.0)
        self.threshold_var.set(128)
        
        if hasattr(self.controller, 'reset_image'):
            self.controller.reset_image()

    def _apply_adjustments(self):
        """Aplica todos os ajustes"""
        if hasattr(self.controller, 'apply_brightness_contrast'):
            brightness = self.brightness_var.get()
            contrast = self.contrast_var.get()
            self.controller.apply_brightness_contrast(brightness, contrast)

    def _equalize_histogram(self):
        """Aplica equalização de histograma"""
        if hasattr(self.controller, 'apply_equalization'):
            self.controller.apply_equalization()

    def update_histogram(self, image):
        """Atualiza o histograma"""
        if hasattr(self, 'histogram_canvas'):
            self.histogram_canvas.update_histogram(image)

    def add_log(self, text):
        """Adiciona entrada ao log"""
        self.log_area.insert(tk.END, f"> {text}\n")
        self.log_area.see(tk.END)
