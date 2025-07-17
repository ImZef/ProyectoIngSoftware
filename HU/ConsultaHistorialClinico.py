"""
HU10: Consultar historial clínico del cliente
Historia de Usuario para el rol de Médico Veterinario
Solo contiene lógica de negocio, sin interfaz gráfica.
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

from db import get_db_path
from .HistoriaClinica import HistoriaClinica
from .Venta import Venta


class ConsultaHistorialClinico:
    """Lógica de negocio para consultar historial clínico completo del cliente."""
    
    def __init__(self):
        self.historiales_clinicos = []
        self.compras_cliente = []
        self.cargar_datos_sistema()
        
    def cargar_datos_sistema(self):
        """Cargar todos los datos del sistema."""
        try:
            # Cargar historiales clínicos
            HistoriaClinica.cargar_historiales()
            
            # Cargar ventas
            Venta.cargar_desde_json()
            
        except Exception as e:
            raise Exception(f"Error al cargar datos del sistema: {str(e)}")
            
    def obtener_lista_clientes(self) -> List[str]:
        """Obtener lista única de todos los clientes del sistema."""
        try:
            clientes = set()
            
            # Clientes de historiales clínicos
            for historial in HistoriaClinica.historiales:
                clientes.add(historial.get_nombre_cliente())
            
            # Clientes de ventas
            for venta in Venta.ventas:
                clientes.add(venta.cliente)
            
            return sorted(list(clientes))
            
        except Exception as e:
            raise Exception(f"Error al obtener lista de clientes: {str(e)}")
            
    def buscar_clientes_por_termino(self, termino: str) -> List[str]:
        """Buscar clientes que coincidan con el término de búsqueda."""
        try:
            termino_lower = termino.lower()
            clientes_filtrados = []
            
            # Filtrar de historiales clínicos
            for historial in HistoriaClinica.historiales:
                nombre = historial.get_nombre_cliente().lower()
                if termino_lower in nombre:
                    clientes_filtrados.append(historial.get_nombre_cliente())
            
            # Filtrar de ventas
            for venta in Venta.ventas:
                nombre = venta.cliente.lower()
                if termino_lower in nombre:
                    clientes_filtrados.append(venta.cliente)
            
            # Eliminar duplicados y ordenar
            return sorted(list(set(clientes_filtrados)))
            
        except Exception as e:
            raise Exception(f"Error al buscar clientes: {str(e)}")
            
    def obtener_historial_completo_cliente(self, nombre_cliente: str) -> Tuple[List, List]:
        """
        Obtener historial completo del cliente.
        Retorna tupla (historiales_clinicos, compras_cliente)
        """
        try:
            historiales_cliente = []
            compras_cliente = []
            
            # Buscar historiales clínicos
            for historial in HistoriaClinica.historiales:
                if historial.get_nombre_cliente().lower() == nombre_cliente.lower():
                    historiales_cliente.append(historial)
            
            # Buscar compras
            for venta in Venta.ventas:
                if venta.cliente.lower() == nombre_cliente.lower():
                    compras_cliente.append(venta)
            
            return historiales_cliente, compras_cliente
            
        except Exception as e:
            raise Exception(f"Error al obtener historial del cliente: {str(e)}")
            
    def procesar_consultas_medicas(self, historiales_cliente: List) -> List[Dict]:
        """Procesar consultas médicas para mostrar en interfaz."""
        consultas = []
        
        for historial in historiales_cliente:
            for registro in historial.get_registros():
                consulta = {
                    'fecha_completa': f"{registro['fecha']} {registro['hora']}",
                    'fecha': registro['fecha'],
                    'hora': registro['hora'],
                    'mascota': historial.get_nombre_mascota(),
                    'diagnostico': registro['diagnostico'],
                    'tratamiento': registro['tratamiento'],
                    'historial_id': historial.get_nombre_cliente()
                }
                consultas.append(consulta)
                
        # Ordenar por fecha (más reciente primero)
        try:
            consultas.sort(key=lambda x: datetime.strptime(x['fecha'], "%d/%m/%Y"), reverse=True)
        except:
            pass  # Si hay error en formato de fecha, mantener orden original
            
        return consultas
        
    def procesar_compras_cliente(self, compras_cliente: List) -> List[Dict]:
        """Procesar compras del cliente para mostrar en interfaz."""
        compras = []
        
        for venta in compras_cliente:
            venta_dict = venta.to_dict()
            productos_str = ", ".join([f"{p['nombre']} (x{p['cantidad']})" 
                                     for p in venta_dict['productos']])
            
            compra = {
                'fecha': venta.fecha_venta.strftime("%d/%m/%Y %H:%M"),
                'fecha_obj': venta.fecha_venta,
                'productos': productos_str,
                'productos_lista': venta_dict['productos'],
                'total': venta.total(),
                'forma_pago': venta.forma_pago,
                'total_formateado': f"${venta.total():,}"
            }
            compras.append(compra)
            
        # Ordenar por fecha (más reciente primero)
        compras.sort(key=lambda x: x['fecha_obj'], reverse=True)
        
        return compras
        
    def generar_estadisticas_cliente(self, historiales_cliente: List, compras_cliente: List) -> Dict:
        """Generar estadísticas del cliente."""
        try:
            total_consultas = sum(len(h.get_registros()) for h in historiales_cliente)
            total_compras = len(compras_cliente)
            mascotas_atendidas = len(set(h.get_nombre_mascota() for h in historiales_cliente))
            total_gastado = sum(venta.total() for venta in compras_cliente) if compras_cliente else 0
            
            return {
                'total_consultas': total_consultas,
                'total_compras': total_compras,
                'mascotas_atendidas': mascotas_atendidas,
                'total_gastado': total_gastado
            }
            
        except Exception as e:
            return {
                'total_consultas': 0,
                'total_compras': 0,
                'mascotas_atendidas': 0,
                'total_gastado': 0
            }
            
    def generar_recomendaciones_inteligentes(self, historiales_cliente: List, compras_cliente: List) -> List[str]:
        """Generar recomendaciones personalizadas basadas en el historial."""
        recomendaciones = []
        
        try:
            # Análisis de diagnósticos frecuentes
            diagnosticos = []
            for historial in historiales_cliente:
                for registro in historial.get_registros():
                    diagnosticos.append(registro['diagnostico'].lower())
            
            # Análisis de productos comprados
            productos_comprados = []
            for venta in compras_cliente:
                for producto in venta.to_dict()['productos']:
                    productos_comprados.append(producto['nombre'].lower())
            
            # Generar recomendaciones inteligentes
            texto_diagnosticos = ' '.join(diagnosticos)
            texto_productos = ' '.join(productos_comprados)
            
            # Recomendaciones basadas en diagnósticos
            if 'desparasit' in texto_diagnosticos:
                recomendaciones.append("Mantener esquema regular de desparasitación cada 3-6 meses")
            
            if 'vacun' in texto_diagnosticos or 'inmuniz' in texto_diagnosticos:
                recomendaciones.append("Verificar calendario de vacunación y mantener al día")
            
            if 'dental' in texto_diagnosticos or 'diente' in texto_diagnosticos:
                recomendaciones.append("Implementar rutina de higiene dental regular")
            
            # Recomendaciones basadas en productos
            if 'vitamina' in texto_productos or 'suplemento' in texto_productos:
                recomendaciones.append("Continuar con suplementación vitamínica según indicaciones")
            
            if 'alimento' in texto_productos or 'comida' in texto_productos:
                recomendaciones.append("Mantener alimentación balanceada y de calidad")
            
            # Recomendaciones temporales
            if historiales_cliente:
                try:
                    # Buscar última consulta
                    ultima_fecha = None
                    for historial in historiales_cliente:
                        for registro in historial.get_registros():
                            fecha_registro = datetime.strptime(registro['fecha'], "%d/%m/%Y")
                            if ultima_fecha is None or fecha_registro > ultima_fecha:
                                ultima_fecha = fecha_registro
                    
                    if ultima_fecha:
                        dias_desde_ultima = (datetime.now() - ultima_fecha).days
                        if dias_desde_ultima > 365:
                            recomendaciones.append("Programar chequeo general - más de un año desde última consulta")
                        elif dias_desde_ultima > 180:
                            recomendaciones.append("Considerar chequeo preventivo")
                            
                except:
                    pass
            
            # Recomendaciones generales si no hay específicas
            if not recomendaciones:
                recomendaciones.extend([
                    "Mantener visitas regulares para chequeos preventivos",
                    "Considerar vacunación según calendario veterinario",
                    "Implementar rutina de desparasitación preventiva"
                ])
            
            return recomendaciones
            
        except Exception as e:
            return ["Mantener visitas regulares para chequeos preventivos"]
            
    def validar_acceso_veterinario(self, rol_usuario: Dict) -> bool:
        """Validar que el usuario tenga permisos para consultar historial clínico."""
        try:
            if not rol_usuario:
                return False
            
            # Acceso permitido si el rol posee el permiso específico o acceso total
            permisos = rol_usuario.get('permisos', [])
            if 'historiales_clinicos' in permisos or 'todas_las_funciones' in permisos:
                return True
            
            # Fallback por id/nombre/tipo para compatibilidad hacia atrás
            tipo_rol = str(rol_usuario.get('tipo', '')).lower()
            id_rol = str(rol_usuario.get('id', '')).lower()
            nombre_rol = str(rol_usuario.get('nombre', '')).lower()
            return any(r in ['veterinario', 'administrador', '4'] for r in [tipo_rol, id_rol, nombre_rol])
        except Exception:
            return False
            
    def buscar_detalle_consulta_especifica(self, fecha: str, mascota: str, diagnostico: str) -> Optional[Dict]:
        """Buscar detalle específico de una consulta."""
        try:
            for historial in HistoriaClinica.historiales:
                if historial.get_nombre_mascota() == mascota:
                    for registro in historial.get_registros():
                        if (registro['fecha'] == fecha and 
                            registro['diagnostico'] == diagnostico):
                            return {
                                'cliente': historial.get_nombre_cliente(),
                                'mascota': historial.get_nombre_mascota(),
                                'especie': historial.get_especie(),
                                'raza': historial.get_raza(),
                                'edad': historial.get_edad(),
                                'genero': historial.get_genero(),
                                'fecha': registro['fecha'],
                                'hora': registro['hora'],
                                'diagnostico': registro['diagnostico'],
                                'tratamiento': registro['tratamiento']
                            }
            return None
            
        except Exception as e:
            return None
            
    def buscar_detalle_compra_especifica(self, fecha: str, cliente: str) -> Optional[Dict]:
        """Buscar detalle específico de una compra."""
        try:
            for venta in Venta.ventas:
                fecha_venta_str = venta.fecha_venta.strftime("%d/%m/%Y %H:%M")
                if fecha_venta_str == fecha and venta.cliente == cliente:
                    venta_dict = venta.to_dict()
                    return {
                        'cliente': venta.cliente,
                        'fecha': fecha_venta_str,
                        'productos': venta_dict['productos'],
                        'total': venta.total(),
                        'forma_pago': venta.forma_pago,
                        'descuento': venta_dict.get('descuento', 0)
                    }
            return None
            
        except Exception as e:
            return None
            
    def verificar_cliente_existe(self, nombre_cliente: str) -> bool:
        """Verificar si existe un cliente en el sistema."""
        clientes = self.obtener_lista_clientes()
        return nombre_cliente in clientes
        
    def generar_resumen_textual(self, nombre_cliente: str, estadisticas: Dict, recomendaciones: List[str]) -> str:
        """Generar resumen textual integrado del cliente."""
        resumen = f"📋 RESUMEN INTEGRADO - {nombre_cliente}\n"
        resumen += "=" * 60 + "\n\n"
        
        # Estadísticas generales
        resumen += "📊 ESTADÍSTICAS GENERALES:\n"
        resumen += f"• Total de consultas médicas: {estadisticas['total_consultas']}\n"
        resumen += f"• Total de compras realizadas: {estadisticas['total_compras']}\n"
        resumen += f"• Mascotas atendidas: {estadisticas['mascotas_atendidas']}\n"
        
        if estadisticas['total_gastado'] > 0:
            resumen += f"• Total gastado: ${estadisticas['total_gastado']:,}\n"
        
        resumen += "\n" + "-" * 40 + "\n\n"
        
        # Recomendaciones personalizadas
        resumen += "💡 RECOMENDACIONES PERSONALIZADAS:\n"
        for rec in recomendaciones:
            resumen += f"• {rec}\n"
        
        resumen += "\n" + "-" * 40 + "\n"
        resumen += f"📅 Reporte generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        resumen += "🏥 AgroVet Plus - Sistema Veterinario\n"
        
        return resumen 