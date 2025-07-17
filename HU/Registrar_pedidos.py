"""
Módulo de registro de pedidos (orientado a objetos).
- Carga inventario desde db/productos.json usando HU.Inventario
- Gestiona pedidos y actualiza stock.
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from typing import List, Dict

from HU.Inventario import Inventario, Producto


class Pedido:
    def __init__(self, cliente: str, producto: Producto, cantidad: int):
        self.cliente = cliente
        self.producto = producto
        self.cantidad = cantidad
        self.fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.estado = "Solicitado"  # Estado inicial para pedidos de aprovisionamiento

    def to_dict(self) -> Dict:
        return {
            "cliente": self.cliente,
            "producto": self.producto.get_nombre(),
            "cantidad": self.cantidad,
            "fecha": self.fecha,
            "estado": self.estado,
        }


class GestorPedidos:
    def __init__(self, archivo_pedidos="db/pedidos.json"):
        # Inicializar inventario
        self.inventario = Inventario()
        self.inventario.cargar_desde_json()
        # Archivo para persistir pedidos
        from pathlib import Path
        self.archivo_pedidos = archivo_pedidos
        Path(self.archivo_pedidos).parent.mkdir(parents=True, exist_ok=True)
        # Cargar pedidos existentes
        self.pedidos: List[Pedido] = []
        self._cargar_pedidos()
        # Diccionario rápido {nombre: Producto}
        self.inventario_dict = {p.get_nombre(): p for p in self.inventario.productos}

    # ---------------- Lógica de negocio -----------------
    def registrar_pedido(self, cliente: str, nombre_producto: str, cantidad: int) -> Pedido:
        if nombre_producto not in self.inventario_dict:
            raise ValueError("Producto no encontrado")
        producto = self.inventario_dict[nombre_producto]
        if cantidad <= 0:
            raise ValueError("Cantidad inválida")
        # Para pedidos de aprovisionamiento no se descuenta stock al registrar
        pedido = Pedido(cliente, producto, cantidad)
        self.pedidos.append(pedido)
        # Guardar en disco
        self._guardar_pedidos()
        return pedido
    def procesar_pedido(self, indice: int) -> Pedido:
        """Marcar pedido como recibido y actualizar stock."""
        if indice < 0 or indice >= len(self.pedidos):
            raise IndexError("Pedido no encontrado")
        pedido = self.pedidos[indice]
        if pedido.estado != "Solicitado":
            raise ValueError("El pedido ya fue procesado")
        # Incrementar stock al recibir mercancía
        producto = pedido.producto
        producto.set_cantidad(producto.get_cantidad() + pedido.cantidad)
        self.inventario.guardar_en_json()
        pedido.estado = "Recibido"
        return pedido

    def listar_pedidos(self) -> List[Pedido]:
        return self.pedidos
    
    def procesar_pedido(self, indice: int) -> Pedido:
        """Marcar un pedido como recibido y actualizar stock."""
        if indice < 0 or indice >= len(self.pedidos):
            raise IndexError("Pedido no encontrado")
        pedido = self.pedidos[indice]
        if pedido.estado != "Solicitado":
            raise ValueError("El pedido ya fue procesado")
        # Incrementar stock al recibir mercancía
        producto = pedido.producto
        producto.set_cantidad(producto.get_cantidad() + pedido.cantidad)
        self.inventario.guardar_en_json()
        pedido.estado = "Recibido"
        # Guardar cambios en pedidos
        self._guardar_pedidos()
        return pedido
    
    # -------- Persistencia de pedidos --------
    def _guardar_pedidos(self):
        import json
        with open(self.archivo_pedidos, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.pedidos], f, indent=4, ensure_ascii=False)
    
    def _cargar_pedidos(self):
        import json
        from pathlib import Path
        if not Path(self.archivo_pedidos).exists():
            return
        try:
            with open(self.archivo_pedidos, "r", encoding="utf-8") as f:
                data = json.load(f)
            for d in data:
                # Reconstruir pedido
                nombre_producto = d.get("producto")
                producto = next((p for p in self.inventario.productos if p.get_nombre() == nombre_producto), None)
                if not producto:
                    continue
                pedido = Pedido(d.get("cliente"), producto, d.get("cantidad"))
                pedido.fecha = d.get("fecha")
                pedido.estado = d.get("estado", pedido.estado)
                self.pedidos.append(pedido)
        except Exception:
            # Si falla, iniciar sin pedidos
            self.pedidos.clear()


# ---------------- Interfaz gráfica simple -----------------
class RegistroPedidosGUI:
    def __init__(self, gestor: GestorPedidos):
        self.gestor = gestor
        self.root = tk.Tk()
        self.root.title("Registro de Pedidos - AgroVet Plus")
        self.root.geometry("500x380")
        self._crear_widgets()
        self.root.mainloop()

    def _crear_widgets(self):
        tk.Label(self.root, text="Nombre del Cliente:").pack()
        self.cliente_entry = tk.Entry(self.root, width=40)
        self.cliente_entry.pack()

        tk.Label(self.root, text="Producto:").pack()
        self.producto_var = tk.StringVar()
        nombres_productos = list(self.gestor.inventario_dict.keys())
        self.producto_menu = tk.OptionMenu(self.root, self.producto_var, *nombres_productos)
        self.producto_menu.pack()

        tk.Label(self.root, text="Cantidad:").pack()
        self.cantidad_entry = tk.Entry(self.root, width=10)
        self.cantidad_entry.pack()

        tk.Button(self.root, text="Registrar Pedido", command=self._registrar).pack(pady=10)
        tk.Button(self.root, text="Ver Pedidos", command=self._ver_pedidos).pack()

    def _registrar(self):
        cliente = self.cliente_entry.get().strip()
        cantidad_str = self.cantidad_entry.get().strip()
        nombre_producto = self.producto_var.get()

        # Validaciones básicas de UI
        if not cliente or not cantidad_str or not nombre_producto:
            messagebox.showerror("Campos obligatorios", "Por favor complete todos los campos.")
            return
        if not cantidad_str.isdigit():
            messagebox.showerror("Error", "La cantidad debe ser un número.")
            return
        cantidad = int(cantidad_str)

        try:
            pedido = self.gestor.registrar_pedido(cliente, nombre_producto, cantidad)
            messagebox.showinfo("Éxito", f"Pedido registrado:\n{pedido.to_dict()}")
            # Limpiar campos
            self.cliente_entry.delete(0, tk.END)
            self.cantidad_entry.delete(0, tk.END)
            self.producto_var.set("")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _ver_pedidos(self):
        pedidos = self.gestor.listar_pedidos()
        if not pedidos:
            messagebox.showinfo("Pedidos", "No hay pedidos registrados aún.")
            return
        ventana = tk.Toplevel(self.root)
        ventana.title("Pedidos Registrados")
        ventana.geometry("600x350")
        texto = tk.Text(ventana, width=85, height=18)
        texto.pack()
        for i, p in enumerate(pedidos, 1):
            d = p.to_dict()
            texto.insert(tk.END, f"{i}. {d['cliente']} - {d['producto']} x{d['cantidad']} ({d['fecha']})\n")
        texto.config(state='disabled')


if __name__ == "__main__":
    gestor = GestorPedidos()
    RegistroPedidosGUI(gestor)
