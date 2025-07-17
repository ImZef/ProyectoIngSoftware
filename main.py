#!/usr/bin/env python3
"""
Launcher para la aplicación AgroVet Plus
Este archivo permite ejecutar tanto la interfaz gráfica como la de consola
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox
from HU.Inventario import Inventario
from GUI.main import main as gui_main
from comandos import main as console_main

def main():
    """Punto de entrada principal simplificado.

    Ahora delega directamente a la interfaz unificada definida en ``GUI.app``
    (importada como ``gui_main``). Esa interfaz gráfica ya permite al usuario
    escoger tanto el tipo de interfaz (GUI o Consola) como el rol antes de
    continuar, por lo que el lanzador anterior (AgroVetLauncher) resulta
    redundante.
    """

    # Llamar a la interfaz unificada. Si el usuario elige "Consola" dentro de
    # la ventana de selección, ``gui_main`` se encargará de lanzar
    # ``comandos.main`` automáticamente.
    gui_main()

if __name__ == "__main__":
    main()
