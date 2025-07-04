"""
Clinical history component for AgroVet Plus application.
"""

import tkinter as tk
from tkinter import ttk
from .configuracion import COLOR_PALETTE, ICONS
from HU.HistoriaClinica import HistoriaClinica


class ClinicalHistoryComponent:
    """Componente para la gestión del historial clínico."""
    
    def __init__(self, parent):
        self.parent = parent
        self.colors = COLOR_PALETTE
        self.records_frame = None
        
    def create_clinical_history_tab(self, notebook):
        """Crear la pestaña de historial clínico."""
        clinical_frame = ttk.Frame(notebook)
        notebook.add(clinical_frame, text=f"{ICONS['clinical']} Historial Clínico")
        
        # Controles
        controls = tk.Frame(clinical_frame, bg=self.colors['light_gray'])
        controls.pack(fill='x', pady=10)
        
        tk.Button(controls, text=f"{ICONS['add']} Registrar/Actualizar Diagnóstico", 
                  command=self.open_clinical_entry_window,
                  bg=self.colors['primary'], fg=self.colors['white'],
                  font=('Arial', 11, 'bold'), relief='flat').pack(side='left', padx=10)
        
        tk.Button(controls, text=f"{ICONS['update']} Refrescar Historias", 
                  command=self.refresh_clinical_histories,
                  bg=self.colors['success'], fg=self.colors['white'],
                  font=('Arial', 11, 'bold'), relief='flat').pack(side='left')
        
        # Contenedor scrollable para historiales clínicos
        content_frame = ttk.Frame(clinical_frame)
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        canvas = tk.Canvas(content_frame, bg=self.colors['light_gray'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient='vertical', command=canvas.yview)
        records_container = ttk.Frame(canvas)
        
        records_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=records_container, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.records_frame = records_container
        self.refresh_clinical_histories()
        
        return clinical_frame

    def refresh_clinical_histories(self):
        """Refrescar los historiales clínicos mostrados."""
        # Limpiar registros anteriores
        for widget in self.records_frame.winfo_children():
            widget.destroy()
        
        if not HistoriaClinica.historiales:
            label = tk.Label(self.records_frame, text="No hay historiales clínicos registrados.", 
                             font=('Arial', 11), bg=self.colors['light_gray'])
            label.pack(pady=20)
        else:
            for h in HistoriaClinica.historiales:
                # Frame para cada historial
                frame = ttk.Frame(self.records_frame, padding=10)
                frame.pack(fill='x', expand=True, pady=10)
                
                # Título del historial
                title = f"Cliente ID: {h.get_id_cliente()} - {h.get_nombre_cliente()} / Mascota: {h.get_nombre_mascota()}"
                tk.Label(frame, text=title, font=('Arial', 12, 'bold'), 
                        bg=self.colors['white']).pack(anchor='w')
                
                # Registros del historial
                for i, reg in enumerate(h.get_registros(), 1):
                    reg_frame = ttk.Frame(frame, padding=10)
                    reg_frame.pack(fill='x', expand=True, pady=(5, 0))
                    
                    # Fecha y hora
                    fecha_hora = f"{reg['fecha']} {reg['hora']}"
                    tk.Label(reg_frame, text=fecha_hora, font=('Arial', 10, 'italic'), 
                            bg=self.colors['light_gray']).pack(anchor='w')
                    
                    # Diagnóstico y tratamiento
                    diag_trat = f"Diagnóstico: {reg['diagnostico']} | Tratamiento: {reg['tratamiento']}"
                    tk.Label(reg_frame, text=diag_trat, font=('Arial', 10), 
                            bg=self.colors['white']).pack(anchor='w')
                    
                    # Comentarios (si existen)
                    if reg.get('comentarios'):
                        tk.Label(reg_frame, text=f"Comentarios: {reg['comentarios']}", font=('Arial', 10, 'italic'), 
                                bg=self.colors['light_gray']).pack(anchor='w')
                
                # Separador entre historiales
                ttk.Separator(self.records_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Hacer scroll al final
        self.records_frame.master.yview_moveto(1.0)

    def open_clinical_entry_window(self):
        """Abrir ventana para entrada clínica."""
        from .dialogs import ClinicalEntryWindow
        ClinicalEntryWindow(self.parent, self.refresh_clinical_histories)
