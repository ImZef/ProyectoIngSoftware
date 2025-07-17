"""
Clinical history component for AgroVet Plus application.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox # Added missing import
from ..configuracion import COLOR_PALETTE, ICONS
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
        
        # Encabezado centrado - Similar al diseño de ventas
        header_frame = tk.Frame(clinical_frame, bg='#f5f5f5', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame,
                              text="🏥 Historial Clínico",
                              font=('Arial', 24, 'bold'),
                              bg='#f5f5f5',
                              fg='#333333')
        title_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Controles
        controls = tk.Frame(clinical_frame, bg=self.colors['light_gray'])
        controls.pack(fill='x', pady=10)
        
        # Botones Registrar y Actualizar
        tk.Button(controls, text=f"{ICONS['add']} Registrar Diagnóstico", 
                  command=self.open_clinical_entry_registrar,
                  bg=self.colors['primary'], fg=self.colors['white'],
                  font=('Arial', 11, 'bold'), relief='flat').pack(side='left', padx=10)

        tk.Button(controls, text=f"{ICONS['update']} Actualizar Diagnóstico", 
                  command=self.open_clinical_entry_actualizar,
                  bg=self.colors['accent'], fg=self.colors['white'],
                  font=('Arial', 11, 'bold'), relief='flat').pack(side='left', padx=10)
        
        # Botón específico para veterinarios (HU10)
        tk.Button(controls, text="🔍 Consultar Historial Cliente", 
                  command=self.open_historial_cliente_veterinario,
                  bg=self.colors['accent'], fg=self.colors['white'],
                  font=('Arial', 11, 'bold'), relief='flat').pack(side='left', padx=10)
        
        # Contenedor scrollable para historiales clínicos
        content_frame = tk.Frame(clinical_frame, bg=self.colors['light_gray'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        canvas = tk.Canvas(content_frame, bg=self.colors['light_gray'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient='vertical', command=canvas.yview)
        records_container = tk.Frame(canvas, bg=self.colors['light_gray'])
        
        records_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=records_container, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Enlazar scroll con rueda del ratón (canvas y contenedor interno)
        self._bind_mousewheel(canvas)
        self._bind_mousewheel(records_container)
        self._bind_mousewheel(content_frame)

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
                frame = tk.Frame(self.records_frame, bg=self.colors['light_gray'], padx=10, pady=10)
                frame.pack(fill='x', expand=True, pady=10)
                
                # Título del historial
                title = f"Cliente ID: {h.get_id_cliente()} - {h.get_nombre_cliente()} / Mascota: {h.get_nombre_mascota()}"
                tk.Label(frame, text=title, font=('Arial', 12, 'bold'), 
                        bg=self.colors['light_gray']).pack(anchor='w')
                
                # Registros del historial
                for i, reg in enumerate(h.get_registros(), 1):
                    reg_frame = tk.Frame(frame, bg=self.colors['light_gray'], padx=10, pady=10)
                    reg_frame.pack(fill='x', expand=True, pady=(5, 0))
                    
                    # Fecha y hora
                    fecha_hora = f"{reg['fecha']} {reg['hora']}"
                    tk.Label(reg_frame, text=fecha_hora, font=('Arial', 10, 'italic'), 
                            bg=self.colors['light_gray']).pack(anchor='w')
                    
                    # Diagnóstico y tratamiento
                    diag_trat = f"Diagnóstico: {reg['diagnostico']} | Tratamiento: {reg['tratamiento']}"
                    tk.Label(reg_frame, text=diag_trat, font=('Arial', 10), 
                            bg=self.colors['light_gray']).pack(anchor='w')
                    
                    # Comentarios (si existen)
                    if reg.get('comentarios'):
                        tk.Label(reg_frame, text=f"Comentarios: {reg['comentarios']}", font=('Arial', 10, 'italic'), 
                                bg=self.colors['light_gray']).pack(anchor='w')
                
                # Separador entre historiales
                ttk.Separator(self.records_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Hacer scroll al final
        self.records_frame.master.yview_moveto(1.0)

    def open_clinical_entry_registrar(self):
        """Registrar nuevo diagnóstico con ID autoincrementado."""
        from ..roles import role_manager
        if not role_manager.has_permission('historiales_clinicos'):
            messagebox.showerror("Permiso Denegado",
                                 "❌ Acceso denegado\n\nSolo los usuarios con rol de Veterinario o Administrador pueden registrar diagnósticos y tratamientos.")
            return

        from .dialogs import ClinicalEntryWindow
        ClinicalEntryWindow(self.parent, self.refresh_clinical_histories, auto_id=True)

    def open_clinical_entry_actualizar(self):
        """Actualizar diagnóstico existente solicitando ID."""
        from ..roles import role_manager
        if not role_manager.has_permission('historiales_clinicos'):
            messagebox.showerror("Permiso Denegado",
                                 "❌ Acceso denegado\n\nSolo los usuarios con rol de Veterinario o Administrador pueden actualizar diagnósticos.")
            return

        from .dialogs import ClinicalEntryWindow
        ClinicalEntryWindow(self.parent, self.refresh_clinical_histories, auto_id=False)

    def open_historial_cliente_veterinario(self):
        """Abrir ventana de consulta de historial clínico para veterinarios (HU10)."""
        try:
            from .consultaHistorialVeterinario import abrir_consulta_historial_veterinario
            from ..roles import role_manager
            
            # Obtener rol actual
            rol_actual = role_manager.get_current_role()
            abrir_consulta_historial_veterinario(self.parent, rol_actual)
        except ImportError as e:
            messagebox.showerror("Error", f"No se pudo cargar la funcionalidad de veterinario: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir consulta de historial: {e}")

    # ------------------ Utilidades ------------------
    def _bind_mousewheel(self, widget):
        """Enlazar desplazamiento con la rueda del ratón al widget dado."""
        # Determinar canvas objetivo
        def _get_scroll_target(w):
            return w if isinstance(w, tk.Canvas) else w.master

        # Windows y macOS
        widget.bind("<MouseWheel>", lambda e, c=_get_scroll_target(widget): c.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        # Linux
        widget.bind("<Button-4>",  lambda e, c=_get_scroll_target(widget): c.yview_scroll(-1, "units"))
        widget.bind("<Button-5>",  lambda e, c=_get_scroll_target(widget): c.yview_scroll(1, "units"))
