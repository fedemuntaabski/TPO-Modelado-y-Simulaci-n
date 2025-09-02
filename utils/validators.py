"""
Validadores de Entrada
Valida y verifica la entrada de datos del usuario

Características:
- Validación de funciones matemáticas
- Verificación de parámetros numéricos
- Validación de rangos e intervalos
- Detección de errores comunes
"""

import numpy as np
import re
from typing import Union, Tuple, List

class InputValidator:
    """
    Clase para validar entradas del usuario
    """
    
    @staticmethod
    def validate_function(expression: str) -> Tuple[bool, str]:
        """
        Valida una expresión de función matemática
        
        Args:
            expression: Expresión a validar
            
        Returns:
            Tupla (es_válida, mensaje_error)
        """
        if not expression or not expression.strip():
            return False, "La expresión no puede estar vacía"
        
        # Verificar caracteres válidos
        valid_chars = set('xytabcdefghijklmnopqrstuvwxyz0123456789+-*/()^.,_ ')
        if not all(c.lower() in valid_chars for c in expression):
            return False, "La expresión contiene caracteres no válidos"
        
        # Verificar balance de paréntesis
        if expression.count('(') != expression.count(')'):
            return False, "Los paréntesis no están balanceados"
        
        # Verificar que no termine con operador
        if expression.strip().endswith(('+', '-', '*', '/', '^')):
            return False, "La expresión no puede terminar con un operador"
        
        # Verificar que no empiece con operador (excepto -)
        if expression.strip().startswith(('*', '/', '^')):
            return False, "La expresión no puede empezar con ese operador"
        
        # Verificar operadores consecutivos
        operators = ['+', '-', '*', '/', '^']
        for i in range(len(expression) - 1):
            if expression[i] in operators and expression[i+1] in operators:
                if not (expression[i] in '+-' and expression[i+1] in '+-'):
                    return False, "No se permiten operadores consecutivos"
        
        return True, ""
    
    @staticmethod
    def validate_interval(a: Union[str, float], b: Union[str, float]) -> Tuple[bool, str, float, float]:
        """
        Valida un intervalo [a, b]
        
        Args:
            a, b: Límites del intervalo
            
        Returns:
            Tupla (es_válido, mensaje_error, a_convertido, b_convertido)
        """
        try:
            a_val = float(a)
            b_val = float(b)
        except (ValueError, TypeError):
            return False, "Los límites deben ser números válidos", 0, 0
        
        if not np.isfinite(a_val) or not np.isfinite(b_val):
            return False, "Los límites deben ser números finitos", 0, 0
        
        if a_val >= b_val:
            return False, "El límite inferior debe ser menor que el superior", 0, 0
        
        return True, "", a_val, b_val
    
    @staticmethod
    def validate_positive_integer(value: Union[str, int]) -> Tuple[bool, str, int]:
        """
        Valida que un valor sea un entero positivo
        
        Args:
            value: Valor a validar
            
        Returns:
            Tupla (es_válido, mensaje_error, valor_convertido)
        """
        try:
            val = int(value)
        except (ValueError, TypeError):
            return False, "Debe ser un número entero", 0
        
        if val <= 0:
            return False, "Debe ser un número positivo", 0
        
        if val > 100000:
            return False, "El valor es demasiado grande (máximo 100,000)", 0
        
        return True, "", val
    
    @staticmethod
    def validate_positive_float(value: Union[str, float], 
                               min_val: float = 0, 
                               max_val: float = np.inf) -> Tuple[bool, str, float]:
        """
        Valida que un valor sea un float positivo en un rango
        
        Args:
            value: Valor a validar
            min_val: Valor mínimo permitido
            max_val: Valor máximo permitido
            
        Returns:
            Tupla (es_válido, mensaje_error, valor_convertido)
        """
        try:
            val = float(value)
        except (ValueError, TypeError):
            return False, "Debe ser un número válido", 0.0
        
        if not np.isfinite(val):
            return False, "Debe ser un número finito", 0.0
        
        if val < min_val:
            return False, f"Debe ser mayor o igual a {min_val}", 0.0
        
        if val > max_val:
            return False, f"Debe ser menor o igual a {max_val}", 0.0
        
        return True, "", val
    
    @staticmethod
    def validate_point_list(points_str: str) -> Tuple[bool, str, List[Tuple[float, float]]]:
        """
        Valida una lista de puntos en formato "(x1,y1), (x2,y2), ..."
        
        Args:
            points_str: String con puntos
            
        Returns:
            Tupla (es_válido, mensaje_error, lista_puntos)
        """
        if not points_str.strip():
            return False, "La lista de puntos no puede estar vacía", []
        
        try:
            # Remover espacios y dividir por puntos
            clean_str = points_str.replace(' ', '')
            
            # Buscar patrones (x,y)
            pattern = r'\\(([^,]+),([^)]+)\\)'
            matches = re.findall(pattern, clean_str)
            
            if not matches:
                return False, "Formato incorrecto. Use: (x1,y1), (x2,y2), ...", []
            
            points = []
            for x_str, y_str in matches:
                x = float(x_str)
                y = float(y_str)
                
                if not (np.isfinite(x) and np.isfinite(y)):
                    return False, "Todos los puntos deben ser números finitos", []
                
                points.append((x, y))
            
            if len(points) < 2:
                return False, "Se necesitan al menos 2 puntos", []
            
            # Verificar que no hay puntos duplicados en x
            x_values = [p[0] for p in points]
            if len(set(x_values)) != len(x_values):
                return False, "No puede haber valores x duplicados", []
            
            return True, "", points
        
        except ValueError:
            return False, "Error al convertir coordenadas a números", []
        except Exception:
            return False, "Error en el formato de puntos", []
    
    @staticmethod
    def validate_tolerance(tol: Union[str, float]) -> Tuple[bool, str, float]:
        """
        Valida una tolerancia para métodos numéricos
        
        Args:
            tol: Valor de tolerancia
            
        Returns:
            Tupla (es_válida, mensaje_error, tolerancia_convertida)
        """
        try:
            tol_val = float(tol)
        except (ValueError, TypeError):
            return False, "La tolerancia debe ser un número válido", 0.0
        
        if tol_val <= 0:
            return False, "La tolerancia debe ser positiva", 0.0
        
        if tol_val >= 1:
            return False, "La tolerancia debe ser menor que 1", 0.0
        
        if tol_val < 1e-15:
            return False, "La tolerancia es demasiado pequeña (mínimo 1e-15)", 0.0
        
        return True, "", tol_val
    
    @staticmethod
    def validate_step_size(h: Union[str, float]) -> Tuple[bool, str, float]:
        """
        Valida el tamaño de paso para diferencias finitas
        
        Args:
            h: Tamaño de paso
            
        Returns:
            Tupla (es_válido, mensaje_error, h_convertido)
        """
        try:
            h_val = float(h)
        except (ValueError, TypeError):
            return False, "El paso debe ser un número válido", 0.0
        
        if h_val <= 0:
            return False, "El paso debe ser positivo", 0.0
        
        if h_val >= 1:
            return False, "El paso es demasiado grande (máximo 1)", 0.0
        
        if h_val < 1e-10:
            return False, "El paso es demasiado pequeño (mínimo 1e-10)", 0.0
        
        return True, "", h_val
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitiza un nombre de archivo para que sea válido
        
        Args:
            filename: Nombre de archivo original
            
        Returns:
            Nombre de archivo sanitizado
        """
        # Remover caracteres no válidos
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Limitar longitud
        if len(filename) > 100:
            filename = filename[:100]
        
        # Asegurar que no esté vacío
        if not filename.strip():
            filename = "output"
        
        return filename.strip()
