import tkinter as tk
from tkinter import ttk
import json
from ..configuracion import COLOR_PALETTE, ICONS

class ConsultasComponent:
    """Mostrar consultas registradas por los auxiliares."""
    def __init__(self, parent):
        self.parent = parent
        self.colors = COLOR_PALETTE
        self.tree = None

    def _load_consultas(self):
        try:
            with open("db/solicitudes.json", "r", encoding="utf-8") as f:
                datos = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            datos = []
        return [d for d in datos if d.get('tipo') == 'consulta']

    def create_consultas_tab(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=f"{ICONS.get('clinical', '🩺')} Consultas")

        self.tree = ttk.Treeview(tab, columns=("Fecha", "Cliente", "Descripción", "Contacto"), show='headings', height=15)
        for col in ("Fecha", "Cliente", "Descripción", "Contacto"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='w', width=150)
        self.tree.pack(fill='both', expand=True, padx=20, pady=20)
        self.refresh()

    def refresh(self):
        consultas = self._load_consultas()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for c in consultas:
            desc = c.get('descripcion', '')[:50] + ('...' if len(c.get('descripcion', '')) > 50 else '')
            self.tree.insert('', 'end', values=(c.get('fecha'), c.get('cliente'), desc, c.get('contacto', ''))) 