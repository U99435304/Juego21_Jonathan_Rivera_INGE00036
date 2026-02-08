# Actividad Integradora: Juego de Blackjack (21) 🃏
**Materia:** INGE00036 - Algoritmos y Estructuras de Datos  
**Alumno:** Jonathan Rivera

## 📌 Descripción del Proyecto
Este proyecto consiste en el diseño e implementación de un sistema de procesamiento de datos lineales mediante el modelo de **TDA (Tipos de Datos Abstractos)**. La solución resuelve la gestión de un mazo de cartas mediante una **estructura de Pila (Stack)**, garantizando el control de flujo de información bajo el paradigma de acceso restringido **LIFO** (Last In, First Out).

El desarrollo responde a los requerimientos técnicos de la materia **Algoritmos y Estructuras de Datos**, enfocándose en la optimización de la memoria mediante el uso de **punteros dinámicos** y la reducción de complejidad algorítmica en los procesos de búsqueda y cálculo de puntajes. No se trata solo de un juego, sino de una simulación de manejo de estados y persistencia temporal de datos en una interfaz gráfica.

---

## 🚀 Descargas (Ejecutable para Windows)
Para facilitar la revisión, se ha generado una versión compilada que no requiere la instalación de Python.

👉 **[DESCARGAR](https://github.com/U99435304/Juego21_Jonathan_Rivera_INGE00036/releases/download/V1.0/Juego21_Jonathan_Rivera_INGE00036.exe)** *(Busca el archivo en la sección de "Releases" a la derecha de este repositorio)*

### ⚠️ Instrucciones de Ejecución Segura
Al ser un software de autoría propia y no contar con una firma digital comercial, Windows SmartScreen podría mostrar una advertencia. Para ejecutarlo de forma segura:
1. Haga doble clic en el archivo `Juego21_Jonathan_Rivera_INGE00036.exe`.
2. Si aparece la ventana azul de SmartScreen, haga clic en **"Más información"**.
3. Seleccione el botón **"Ejecutar de todas formas"**.

---

## 🛠️ Estructuras de Datos Aplicadas
Con el fin de demostrar eficiencia y desempeño en el manejo de memoria:

1. **Pila (Stack):** El mazo principal se gestiona bajo el principio **LIFO**.
2. **Arreglo Lineal:** Se utiliza un arreglo de 52 posiciones para la baraja base.
3. **Puntero (TOP):** Un índice controla el tope de la pila para una extracción optimizada.
4. **Listas Dinámicas:** Utilizadas para las manos del jugador y la IA, permitiendo crecimiento dinámico.

## 🎮 Características Técnicas
- **Operación POP():** Cada carta pedida ejecuta una extracción del tope de la pila.
- **Lógica de IA:** El Crupier utiliza un algoritmo de **desigualdad estricta** para sus decisiones.
- **Interfaz Gráfica:** Implementada con `Tkinter`, incluye un monitor de log para auditoría de procesos.

## 💻 Ejecución para Desarrolladores
Si prefiere ejecutar el código fuente:
1. Clone este repositorio.
2. Ejecute:
   ```bash
   python main.py