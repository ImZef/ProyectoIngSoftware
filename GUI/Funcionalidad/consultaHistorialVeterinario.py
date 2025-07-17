"""
Componente gráfico para consulta de historial clínico - Rol Veterinario
Interfaz gráfica que usa la lógica de negocio de HU/ConsultaHistorialClinico.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from ..configuracion import COLOR_PALETTE, FONTS, ICONS
from HU.ConsultaHistorialClinico import ConsultaHistorialClinico


class ConsultaHistorialVeterinarioGUI:
    """Interfaz gráfica para consultar historial clínico completo del cliente."""
    
    def __init__(self, parent_window):
        self.parent = parent_window
        self.colors = COLOR_PALETTE
        self.window = None
        self.consulta_hu = None
        self.cliente_seleccionado = None
        
    def abrir_consulta_historial(self):
        """Abrir ventana de consulta de historial clínico."""
        try:
            # Inicializar lógica de negocio
            self.consulta_hu = ConsultaHistorialClinico()
            
            # Crear ventana
            self.window = tk.Toplevel(self.parent)
            self.window.title("🏥 Consulta de Historial Clínico - Veterinario")
            self.window.geometry("1000x700")
            self.window.configure(bg=self.colors['light_gray'])
            
            # Centrar ventana
            self.center_window()
            
            # Crear interfaz
            self.crear_interfaz()
            
            # Cargar datos iniciales
            self.cargar_datos_iniciales()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al inicializar consulta de historial: {str(e)}")
            
    def center_window(self):
        """Centrar la ventana en la pantalla."""
        self.window.update_idletasks()
        width = 1000
        height = 700
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def crear_interfaz(self):
        """Crear la interfaz de consulta de historial."""
        # Encabezado
        header_frame = tk.Frame(self.window, bg='#f0f0f0', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame,
                              text="🏥 Consulta de Historial Clínico",
                              font=('Arial', 20, 'bold'),
                              bg='#f0f0f0',
                              fg='#333333')
        title_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Frame principal
        main_frame = tk.Frame(self.window, bg=self.colors['light_gray'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Sección de búsqueda de cliente
        self.crear_seccion_busqueda(main_frame)
        
        # Sección de resultados
        self.crear_seccion_resultados(main_frame)
        
    def crear_seccion_busqueda(self, parent):
        """Crear sección de búsqueda de cliente."""
        search_frame = tk.LabelFrame(parent,
                                   text="🔍 Buscar Cliente",
                                   font=FONTS['subtitle'],
                                   bg=self.colors['white'],
                                   fg=self.colors['dark_gray'],
                                   padx=15,
                                   pady=10)
        search_frame.pack(fill='x', pady=(0, 20))
        
        # Frame interno para búsqueda
        search_content = tk.Frame(search_frame, bg=self.colors['white'])
        search_content.pack(fill='x')
        
        # Campo de búsqueda
        tk.Label(search_content,
                text="👤 Nombre del Cliente:",
                font=FONTS['label'],
                bg=self.colors['white'],
                fg=self.colors['dark_gray']).pack(side='left', padx=(0, 10))
        
        self.search_entry = tk.Entry(search_content,
                                   font=FONTS['text'],
                                   width=30,
                                   relief='solid',
                                   bd=1)
        self.search_entry.pack(side='left', padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.buscar_en_tiempo_real)
        
        # Botones
        tk.Button(search_content,
                 text="🔍 Buscar",
                 font=FONTS['label'],
                 bg=self.colors['primary'],
                 fg=self.colors['white'],
                 command=self.buscar_cliente,
                 padx=15,
                 pady=5,
                 cursor='hand2').pack(side='left', padx=(0, 10))
        
        tk.Button(search_content,
                 text="🗂️ Ver Todos",
                 font=FONTS['label'],
                 bg=self.colors['secondary'],
                 fg=self.colors['dark_gray'],
                 command=self.mostrar_todos_clientes,
                 padx=15,
                 pady=5,
                 cursor='hand2').pack(side='left', padx=(0, 10))
        
        # Lista de clientes
        self.crear_lista_clientes(search_frame)
        
    def crear_lista_clientes(self, parent):
        """Crear lista de clientes disponibles."""
        lista_frame = tk.Frame(parent, bg=self.colors['white'])
        lista_frame.pack(fill='x', pady=(10, 0))
        
        tk.Label(lista_frame,
                text="Clientes disponibles:",
                font=FONTS['label'],
                bg=self.colors['white'],
                fg=self.colors['dark_gray']).pack(anchor='w')
        
        # Combobox para selección de cliente
        self.cliente_var = tk.StringVar()
        self.cliente_combo = ttk.Combobox(lista_frame,
                                        textvariable=self.cliente_var,
                                        font=FONTS['text'],
                                        width=40,
                                        state="readonly")
        self.cliente_combo.pack(anchor='w', pady=(5, 0))
        self.cliente_combo.bind('<<ComboboxSelected>>', self.on_cliente_seleccionado)
        
    def crear_seccion_resultados(self, parent):
        """Crear sección de resultados del historial."""
        results_frame = tk.LabelFrame(parent,
                                    text="📋 Historial del Cliente",
                                    font=FONTS['subtitle'],
                                    bg=self.colors['white'],
                                    fg=self.colors['dark_gray'],
                                    padx=15,
                                    pady=10)
        results_frame.pack(fill='both', expand=True)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Pestaña de consultas médicas
        self.crear_pestana_consultas()
        
        # Pestaña de compras/productos
        self.crear_pestana_compras()
        
        # Pestaña de resumen integrado
        self.crear_pestana_resumen()
        
    def crear_pestana_consultas(self):
        """Crear pestaña de consultas médicas."""
        consultas_frame = ttk.Frame(self.notebook)
        self.notebook.add(consultas_frame, text="🏥 Consultas Médicas")
        
        # Lista de consultas
        self.tree_consultas = ttk.Treeview(consultas_frame,
                                         columns=('Fecha', 'Mascota', 'Diagnóstico', 'Tratamiento'),
                                         show='headings',
                                         height=12)
        
        # Configurar columnas
        self.tree_consultas.heading('Fecha', text='Fecha')
        self.tree_consultas.heading('Mascota', text='Mascota')
        self.tree_consultas.heading('Diagnóstico', text='Diagnóstico')
        self.tree_consultas.heading('Tratamiento', text='Tratamiento')
        
        self.tree_consultas.column('Fecha', width=120, anchor='center')
        self.tree_consultas.column('Mascota', width=150)
        self.tree_consultas.column('Diagnóstico', width=200)
        self.tree_consultas.column('Tratamiento', width=200)
        
        # Scrollbar para consultas
        scroll_consultas = ttk.Scrollbar(consultas_frame, orient='vertical', command=self.tree_consultas.yview)
        self.tree_consultas.configure(yscrollcommand=scroll_consultas.set)
        
        # Empaquetar
        self.tree_consultas.pack(side='left', fill='both', expand=True)
        scroll_consultas.pack(side='right', fill='y')
        
        # Bind para ver detalles
        self.tree_consultas.bind('<Double-1>', self.ver_detalle_consulta)
        
    def crear_pestana_compras(self):
        """Crear pestaña de compras/productos."""
        compras_frame = ttk.Frame(self.notebook)
        self.notebook.add(compras_frame, text="🛒 Historial de Compras")
        
        # Lista de compras
        self.tree_compras = ttk.Treeview(compras_frame,
                                       columns=('Fecha', 'Productos', 'Total', 'Forma_Pago'),
                                       show='headings',
                                       height=12)
        
        # Configurar columnas
        self.tree_compras.heading('Fecha', text='Fecha')
        self.tree_compras.heading('Productos', text='Productos')
        self.tree_compras.heading('Total', text='Total')
        self.tree_compras.heading('Forma_Pago', text='Forma de Pago')
        
        self.tree_compras.column('Fecha', width=150, anchor='center')
        self.tree_compras.column('Productos', width=300)
        self.tree_compras.column('Total', width=100, anchor='e')
        self.tree_compras.column('Forma_Pago', width=120, anchor='center')
        
        # Scrollbar para compras
        scroll_compras = ttk.Scrollbar(compras_frame, orient='vertical', command=self.tree_compras.yview)
        self.tree_compras.configure(yscrollcommand=scroll_compras.set)
        
        # Empaquetar
        self.tree_compras.pack(side='left', fill='both', expand=True)
        scroll_compras.pack(side='right', fill='y')
        
        # Bind para ver detalles
        self.tree_compras.bind('<Double-1>', self.ver_detalle_compra)
        
    def crear_pestana_resumen(self):
        """Crear pestaña de resumen integrado."""
        resumen_frame = ttk.Frame(self.notebook)
        self.notebook.add(resumen_frame, text="📊 Resumen Integrado")
        
        # Text area para resumen
        self.text_resumen = tk.Text(resumen_frame,
                                  font=FONTS['text'],
                                  bg=self.colors['light_gray'],
                                  fg=self.colors['dark_gray'],
                                  wrap='word',
                                  padx=10,
                                  pady=10)
        
        # Scrollbar para resumen
        scroll_resumen = ttk.Scrollbar(resumen_frame, orient='vertical', command=self.text_resumen.yview)
        self.text_resumen.configure(yscrollcommand=scroll_resumen.set)
        
        # Empaquetar
        self.text_resumen.pack(side='left', fill='both', expand=True)
        scroll_resumen.pack(side='right', fill='y')
        
    def cargar_datos_iniciales(self):
        """Cargar datos iniciales de clientes."""
        try:
            # Obtener lista de clientes usando la lógica de negocio
            clientes = self.consulta_hu.obtener_lista_clientes()
            
            # Actualizar combobox
            self.cliente_combo['values'] = clientes
            
            if not clientes:
                self.mostrar_mensaje_sin_datos()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
            
    def buscar_en_tiempo_real(self, event=None):
        """Búsqueda en tiempo real mientras el usuario escribe."""
        termino = self.search_entry.get().lower().strip()
        if len(termino) >= 2:
            self.filtrar_clientes(termino)
        elif len(termino) == 0:
            self.cargar_datos_iniciales()
            
    def filtrar_clientes(self, termino):
        """Filtrar clientes por término de búsqueda."""
        try:
            clientes_filtrados = self.consulta_hu.buscar_clientes_por_termino(termino)
            self.cliente_combo['values'] = clientes_filtrados
            
        except Exception as e:
            print(f"Error al filtrar clientes: {e}")
            
    def buscar_cliente(self):
        """Buscar cliente específico."""
        termino = self.search_entry.get().strip()
        if not termino:
            messagebox.showwarning("Búsqueda", "Ingrese un nombre para buscar")
            return
        
        self.filtrar_clientes(termino.lower())
        
    def mostrar_todos_clientes(self):
        """Mostrar todos los clientes disponibles."""
        self.search_entry.delete(0, tk.END)
        self.cargar_datos_iniciales()
        
    def on_cliente_seleccionado(self, event=None):
        """Evento cuando se selecciona un cliente."""
        cliente_seleccionado = self.cliente_var.get()
        if cliente_seleccionado:
            self.cliente_seleccionado = cliente_seleccionado
            self.cargar_historial_cliente(cliente_seleccionado)
            
    def cargar_historial_cliente(self, nombre_cliente):
        """Cargar historial completo del cliente seleccionado."""
        try:
            # Obtener historial usando la lógica de negocio
            historiales_cliente, compras_cliente = self.consulta_hu.obtener_historial_completo_cliente(nombre_cliente)
            
            # Actualizar pestañas
            self.actualizar_pestana_consultas(historiales_cliente)
            self.actualizar_pestana_compras(compras_cliente)
            self.actualizar_pestana_resumen(nombre_cliente, historiales_cliente, compras_cliente)
            
            # Verificar si hay datos
            if not historiales_cliente and not compras_cliente:
                self.mostrar_mensaje_sin_registros(nombre_cliente)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar historial: {str(e)}")
            
    def actualizar_pestana_consultas(self, historiales_cliente):
        """Actualizar pestaña de consultas médicas."""
        # Limpiar tree
        for item in self.tree_consultas.get_children():
            self.tree_consultas.delete(item)
        
        if not historiales_cliente:
            return
            
        # Procesar consultas usando la lógica de negocio
        consultas = self.consulta_hu.procesar_consultas_medicas(historiales_cliente)
        
        for consulta in consultas:
            self.tree_consultas.insert('', 'end', values=(
                consulta['fecha_completa'],
                consulta['mascota'],
                consulta['diagnostico'],
                consulta['tratamiento']
            ))
                
    def actualizar_pestana_compras(self, compras_cliente):
        """Actualizar pestaña de compras."""
        # Limpiar tree
        for item in self.tree_compras.get_children():
            self.tree_compras.delete(item)
        
        if not compras_cliente:
            return
            
        # Procesar compras usando la lógica de negocio
        compras = self.consulta_hu.procesar_compras_cliente(compras_cliente)
        
        for compra in compras:
            self.tree_compras.insert('', 'end', values=(
                compra['fecha'],
                compra['productos'],
                compra['total_formateado'],
                compra['forma_pago']
            ))
            
    def actualizar_pestana_resumen(self, nombre_cliente, historiales_cliente, compras_cliente):
        """Actualizar pestaña de resumen integrado."""
        self.text_resumen.delete(1.0, tk.END)
        
        if not historiales_cliente and not compras_cliente:
            self.text_resumen.insert(tk.END, "No hay registros disponibles para este cliente.")
            return
        
        # Generar resumen usando la lógica de negocio
        estadisticas = self.consulta_hu.generar_estadisticas_cliente(historiales_cliente, compras_cliente)
        recomendaciones = self.consulta_hu.generar_recomendaciones_inteligentes(historiales_cliente, compras_cliente)
        resumen = self.consulta_hu.generar_resumen_textual(nombre_cliente, estadisticas, recomendaciones)
        
        self.text_resumen.insert(tk.END, resumen)
        
    def ver_detalle_consulta(self, event):
        """Ver detalle de consulta específica."""
        selection = self.tree_consultas.selection()
        if not selection:
            return
        
        item = self.tree_consultas.item(selection[0])
        valores = item['values']
        
        # Crear ventana de detalle
        self.mostrar_detalle_consulta(valores)
        
    def ver_detalle_compra(self, event):
        """Ver detalle de compra específica."""
        selection = self.tree_compras.selection()
        if not selection:
            return
        
        item = self.tree_compras.item(selection[0])
        valores = item['values']
        
        # Crear ventana de detalle
        self.mostrar_detalle_compra(valores)
        
    def mostrar_detalle_consulta(self, valores):
        """Mostrar ventana con detalle de consulta."""
        detalle_window = tk.Toplevel(self.window)
        detalle_window.title("🏥 Detalle de Consulta")
        detalle_window.geometry("500x400")
        detalle_window.configure(bg=self.colors['white'])
        
        # Contenido del detalle
        content = tk.Text(detalle_window, font=FONTS['text'], wrap='word', padx=10, pady=10)
        content.pack(fill='both', expand=True)
        
        detalle_texto = f"""🏥 DETALLE DE CONSULTA MÉDICA
{'='*40}

📅 Fecha y Hora: {valores[0]}
🐾 Mascota: {valores[1]}
🩺 Diagnóstico: {valores[2]}
💊 Tratamiento: {valores[3]}

{'='*40}
👨‍⚕️ Dr. Veterinario - AgroVet Plus
"""
        
        content.insert(tk.END, detalle_texto)
        content.config(state='disabled')
        
    def mostrar_detalle_compra(self, valores):
        """Mostrar ventana con detalle de compra."""
        detalle_window = tk.Toplevel(self.window)
        detalle_window.title("🛒 Detalle de Compra")
        detalle_window.geometry("500x400")
        detalle_window.configure(bg=self.colors['white'])
        
        # Contenido del detalle
        content = tk.Text(detalle_window, font=FONTS['text'], wrap='word', padx=10, pady=10)
        content.pack(fill='both', expand=True)
        
        detalle_texto = f"""🛒 DETALLE DE COMPRA
{'='*40}

📅 Fecha: {valores[0]}
📦 Productos: {valores[1]}
💰 Total: {valores[2]}
💳 Forma de Pago: {valores[3]}

{'='*40}
🏪 AgroVet Plus - Sistema de Ventas
"""
        
        content.insert(tk.END, detalle_texto)
        content.config(state='disabled')
        
    def mostrar_mensaje_sin_registros(self, cliente):
        """Mostrar mensaje cuando no hay registros para el cliente."""
        mensaje = f"ℹ️ INFORMACIÓN\n\nNo se encontraron registros para el cliente '{cliente}'.\n\nEsto puede significar que:\n• Es un cliente nuevo\n• No tiene consultas médicas registradas\n• No ha realizado compras en el sistema"
        
        messagebox.showinfo("Sin Registros", mensaje)
        
        # También actualizar el resumen
        self.text_resumen.delete(1.0, tk.END)
        self.text_resumen.insert(tk.END, f"No se encontraron registros para el cliente '{cliente}'.")
        
    def mostrar_mensaje_sin_datos(self):
        """Mostrar mensaje cuando no hay datos en el sistema."""
        messagebox.showinfo("Sin Datos", "No hay clientes registrados en el sistema.\n\nAsegúrese de que existan:\n• Historiales clínicos\n• Registros de ventas")


def abrir_consulta_historial_veterinario(parent_window, rol_usuario=None):
    """Función de utilidad para abrir la consulta de historial clínico."""
    try:
        # Verificar permisos de veterinario usando la lógica de negocio
        consulta_hu = ConsultaHistorialClinico()
        
        if rol_usuario and not consulta_hu.validar_acceso_veterinario(rol_usuario):
            messagebox.showerror("Permiso Denegado", 
                               "❌ Acceso denegado\n\nSolo los usuarios con rol de Veterinario o Administrador pueden acceder a esta funcionalidad.")
            return
        
        # Crear y abrir la ventana
        historial_gui = ConsultaHistorialVeterinarioGUI(parent_window)
        historial_gui.abrir_consulta_historial()
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al abrir consulta de historial: {str(e)}") 