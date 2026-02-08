import tkinter as tk  # Importa la librería base para interfaces gráficas
from tkinter import messagebox  # Importa el módulo para mostrar cuadros de diálogo (alertas)
import random  # Importa la librería para generar aleatoriedad (mezclar baraja)
""" 
    CLASE PRINCIPAL: Encapsula la lógica del juego y la interfaz gráfica bajo el modelo 
    de Programación Orientada a Objetos, gestionando estados y estructuras de datos. 
    """
class Blackjack:
    """ MÉTODO CONSTRUCTOR: Inicializa la ventana principal y las variables de control de la Pila. """
    def __init__(self, root):
        self.root = root  # Guarda la ventana principal en una variable de instancia
        self.root.title("Juego21_Jonathan_Rivera_INGE00036")  # Establece el título de la ventana
        self.root.geometry("1100x850")  # Define el tamaño inicial de la ventana
        self.root.configure(bg="#1a4a1a")  # Establece el color de fondo verde tipo casino

        # --- CONTENEDOR DE SCROLL ---
        self.main_canvas = tk.Canvas(self.root, bg="#1a4a1a", highlightthickness=0)  # Crea un lienzo que permite desplazamiento
        self.main_canvas.pack(side="left", fill="both", expand=True)  # Empaqueta el lienzo a la izquierda expandiéndose

        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)  # Crea la barra de desplazamiento
        self.scrollbar.pack(side="right", fill="y")  # Empaqueta la barra a la derecha ocupando todo el eje Y

        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)  # Conecta el canvas con el movimiento de la barra
        
        self.scrollable_frame = tk.Frame(self.main_canvas, bg="#1a4a1a")  # Crea el marco interno que contendrá los widgets
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", tags="frame")  # Inserta el marco en el canvas

        # --- LÓGICA DE ESTRUCTURAS ---
        self.palos = ['♠', '♥', '♦', '♣']  # Arreglo con los símbolos de la baraja
        self.valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']  # Arreglo con los rangos de las cartas
        self.baraja = []  # Estructura que funcionará como Pila (Stack) principal
        self.ind_baraja = 0  # Puntero (TOP) que indica la posición actual en la pila
        self.mano_jugador = []  # Lista dinámica para almacenar las cartas del usuario
        self.mano_crupier = []  # Lista dinámica para almacenar las cartas del crupier

        self.setup_ui()  # Llama a la función que construye la interfaz visual
        
        # Eventos para actualización de scroll y dibujo
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)  # Detecta cambios de tamaño para ajustar el scroll
        self.root.bind("<Configure>", lambda e: self.dibujar_pila())  # Redibuja la pila visual si se cambia el tamaño de ventana
        
        self.nueva_mano()  # Inicia el ciclo del juego por primera vez

    """ GESTIÓN DE SCROLL: Recalcula dinámicamente el área de scroll cuando el frame interno cambia de tamaño. """
    def on_frame_configure(self, event=None):
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))  # Recalcula el área total de desplazamiento
        canvas_width = self.main_canvas.winfo_width()  # Obtiene el ancho actual del canvas
        self.main_canvas.itemconfig("frame", width=canvas_width)  # Ajusta el marco interno al ancho del canvas

    """ GENERACIÓN DE DATOS: Construye un arreglo de 52 objetos (cartas) y los mezcla aleatoriamente. """
    def crear_baraja(self):
        mazo = [v + p for p in self.palos for v in self.valores]  # Genera 52 cartas combinando valores y palos
        random.shuffle(mazo)  # Desordena el arreglo de forma aleatoria (mezclar)
        return mazo  # Retorna el mazo listo para ser usado como pila
    
    """ OPERACIÓN DE PILA (POP): Extrae el dato del "TOP" y desplaza el puntero de la estructura. """
    def ejecutar_pop(self):
        if self.ind_baraja < len(self.baraja):  # Verifica que el puntero no exceda el límite de la baraja
            carta = self.baraja[self.ind_baraja]  # Extrae el elemento apuntado por el índice actual
            self.ind_baraja += 1  # Incrementa el puntero (avanza al siguiente elemento de la pila)
            return carta  # Retorna la carta extraída
        return None  # Retorna nada si la pila está vacía

    """ LÓGICA DE ALGORITMO: Evalúa el valor total de una mano considerando la naturaleza dual del As (1 u 11). """
    def calcular_puntos(self, mano):        
        pts, ases = 0, 0  # Inicializa acumuladores de puntos y contador de Ases
        for carta in mano:  # Itera cada carta en la lista dinámica de la mano
            v = carta[:-1]  # Separa el valor del símbolo (ej: '10♠' -> '10')
            if v in ['J', 'Q', 'K']: pts += 10  # Las figuras valen 10 puntos
            elif v == 'A': pts += 11; ases += 1  # El As vale 11 inicialmente
            else: pts += int(v)  # Las cartas numéricas valen su valor entero
        while pts > 21 and ases > 0:  # Si se pasa de 21 y hay Ases, ajusta el valor del As
            pts -= 10; ases -= 1  # El As cambia su valor de 11 a 1 para no perder
        return pts  # Retorna el puntaje final calculado
    
    """ INTERFAZ DE USUARIO: Define la arquitectura de widgets y los contenedores de información estática y dinámica. """
    def setup_ui(self):
        # TÍTULO PRINCIPAL
        tk.Label(self.scrollable_frame, text="♠  ACTIVIDAD INTEGRADORA: BLACKJACK  ♥", font=("Arial", 22, "bold"), 
                 bg="#1a4a1a", fg="#d4af37", pady=10).pack(fill="x")  # Crea y coloca el título superior decorativo

        # PANEL DE INFORMACIÓN ESTÁTICA
        self.frame_info = tk.Frame(self.scrollable_frame, bg="#0d260d", bd=2, relief="ridge")  # Marco para datos del alumno
        self.frame_info.pack(fill="x", padx=20, pady=5)  # Empaqueta el marco de información
        
        info_texto = (
            f"ALUMNO: JONATHAN RIVERA\n"
            f"MATERIA: INGE00036-1330260005\n"
            "----------------------------------------------------------------------\n"
            "ESTRUCTURAS ACTIVAS:\n"
            "• ARREGLO LINEAL: Mazo de 52 celdas. "
            "• PILA (STACK): Acceso LIFO. "
            "• PUNTERO (TOP): Índice dinámico.\n"
            "• LISTAS DINÁMICAS: Manos de jugadores que reciben resultados de POP()."
        )  # Cadena de texto con los detalles técnicos del proyecto
        
        tk.Label(self.frame_info, text=info_texto, bg="#0d260d", fg="#a5d6a7", 
                 font=("Courier New", 10, "bold"), justify="left", pady=10).pack()  # Muestra el texto informativo en pantalla

        self.canvas_pila = tk.Canvas(self.scrollable_frame, height=130, bg="#0d260d", highlightthickness=0)  # Canvas para ver la pila
        self.canvas_pila.pack(fill="x", padx=20, pady=10)  # Empaqueta el visualizador de la estructura de datos

        self.frame_crupier = tk.Frame(self.scrollable_frame, bg="#1a4a1a")  # Contenedor para cartas del crupier
        self.frame_crupier.pack(pady=10)  # Coloca el contenedor en la interfaz
        self.lbl_pts_crupier = tk.Label(self.scrollable_frame, text="Puntos Crupier: ?", bg="#1a4a1a", fg="#cccccc")  # Texto puntos del crupier
        self.lbl_pts_crupier.pack()  # Muestra el puntaje del crupier

        tk.Frame(self.scrollable_frame, height=2, bg="#d4af37").pack(fill="x", padx=100, pady=15)  # Línea divisoria estética

        self.frame_jugador = tk.Frame(self.scrollable_frame, bg="#1a4a1a")  # Contenedor para cartas del jugador
        self.frame_jugador.pack(pady=10)  # Coloca el contenedor del jugador
        self.lbl_pts_jugador = tk.Label(self.scrollable_frame, text="Tus Puntos: 0", bg="#1a4a1a", fg="white", font=("Arial", 14, "bold"))  # Puntos usuario
        self.lbl_pts_jugador.pack()  # Muestra el puntaje del usuario

        self.frame_btns = tk.Frame(self.scrollable_frame, bg="#1a4a1a", pady=10)  # Contenedor para los botones de acción
        self.frame_btns.pack()  # Coloca el panel de control

        btn_style = {"font": ("Arial", 11, "bold"), "width": 14, "height": 2, "fg": "white"}  # Diccionario con estilos comunes para botones
        self.btn_hit = tk.Button(self.frame_btns, text="PEDIR (POP)", bg="#28a745", command=self.hit, **btn_style)  # Botón pedir carta
        self.btn_hit.grid(row=0, column=0, padx=10)  # Posiciona botón en grid
        self.btn_stand = tk.Button(self.frame_btns, text="PLANTARSE", bg="#854c1d", command=self.stand, **btn_style)  # Botón plantarse
        self.btn_stand.grid(row=0, column=1, padx=10)  # Posiciona botón en grid
        self.btn_new = tk.Button(self.frame_btns, text="REPARTIR", bg="#4a69bd", command=self.nueva_mano, **btn_style)  # Botón repartir nueva mano
        self.btn_new.grid(row=0, column=2, padx=10)  # Posiciona botón en grid

        # LOG DE ACCIONES
        self.lbl_log = tk.Label(self.scrollable_frame, text="Esperando inicio...", bg="#000000", fg="#00ff00", 
                                font=("Courier", 10), width=100, height=3, relief="sunken", bd=2)  # Cuadro de log tipo consola
        self.lbl_log.pack(pady=10, padx=20)  # Muestra el monitor de eventos

    """ VISUALIZACIÓN DE DATOS: Renderiza en tiempo real el arreglo lineal y la ubicación del puntero TOP. """
    def dibujar_pila(self):
        self.canvas_pila.delete("all")  # Limpia el canvas antes de redibujar la pila
        ancho_canvas = self.canvas_pila.winfo_width()  # Obtiene el ancho para calcular espaciado
        if ancho_canvas < 100: ancho_canvas = 1060  # Valor por defecto si la ventana aún no carga
        alto_c, ancho_c, y_pos = 70, 25, 35  # Dimensiones de cada "celda" de la pila
        espaciado = (ancho_canvas - 60) / 52  # Calcula la distancia entre cartas según el mazo
        for i, carta in enumerate(self.baraja):  # Recorre todo el arreglo lineal de la baraja
            x = 30 + (i * espaciado)  # Calcula posición X de la celda
            color = "#1a1a1a" if i < self.ind_baraja else ("#ffffff" if i == self.ind_baraja else "#2c3e50")  # Color según estado
            txt_c = "#333" if i < self.ind_baraja else ("blue" if i == self.ind_baraja else "white")  # Color de texto según estado
            self.canvas_pila.create_rectangle(x, y_pos, x + ancho_c, y_pos + alto_c, fill=color, outline="#444")  # Dibuja la celda física
            if i == self.ind_baraja:  # Si el índice coincide con el puntero
                self.canvas_pila.create_text(x + (ancho_c/2), y_pos - 15, text="TOP", fill="#d4af37", font=("Arial", 8, "bold"))  # Marca el TOP de la pila
            self.canvas_pila.create_text(x + (ancho_c/2), y_pos + 15, text=carta[0], fill=txt_c, font=("Arial", 7, "bold"))  # Muestra valor
            self.canvas_pila.create_text(x + (ancho_c/2), y_pos + alto_c - 15, text=carta[-1], fill=txt_c, font=("Arial", 10))  # Muestra palo

    """ RENDERIZADO DE OBJETOS: Crea la representación gráfica de una carta en la interfaz. """
    def crear_carta_visual(self, parent, texto, oculta=False):        
        color = "red" if ('♥' in texto or '♦' in texto) else "black"  # Define color según el palo
        f = tk.Frame(parent, bg="white", width=85, height=125, bd=2, relief="raised")  # Crea el "naipe" físico como un Frame
        f.pack_propagate(False)  # Evita que el frame colapse al tamaño de sus etiquetas internas
        f.pack(side="left", padx=5)  # Alinea la carta a la izquierda con separación
        if oculta:  # Si la carta debe estar boca abajo
            f.configure(bg="#2c3e50")  # Cambia color a oscuro (reverso)
            tk.Label(f, text="??", bg="#2c3e50", fg="white", font=("Arial", 25, "bold")).place(relx=0.5, rely=0.5, anchor="center")  # Marca de incógnita
        else:  # Si la carta es visible
            tk.Label(f, text=texto, bg="white", fg=color, font=("Arial", 11, "bold")).pack(anchor="nw", padx=3)  # Valor en esquina
            tk.Label(f, text=texto[-1], bg="white", fg=color, font=("Arial", 38)).place(relx=0.5, rely=0.5, anchor="center")  # Símbolo central grande
        return f  # Retorna el objeto gráfico de la carta

    """ SINCRONIZACIÓN: Actualiza los elementos visuales de acuerdo al estado de las listas dinámicas (manos). """
    def actualizar_mesa(self, revelar=False):
        self.dibujar_pila()  # Refresca el estado visual de la estructura Stack
        for w in self.frame_jugador.winfo_children(): w.destroy()  # Limpia cartas anteriores del jugador
        for w in self.frame_crupier.winfo_children(): w.destroy()  # Limpia cartas anteriores del crupier
        for c in self.mano_jugador: self.crear_carta_visual(self.frame_jugador, c)  # Dibuja las cartas actuales del jugador
        for i, c in enumerate(self.mano_crupier):  # Dibuja las cartas actuales del crupier
            self.crear_carta_visual(self.frame_crupier, c, oculta=(i==1 and not revelar))  # Mantiene una carta oculta si es necesario
        self.lbl_pts_jugador.config(text=f"Tus Puntos: {self.calcular_puntos(self.mano_jugador)}")  # Actualiza etiqueta de puntos jugador
        pts_c = self.calcular_puntos(self.mano_crupier) if revelar else "?"  # Oculta puntos del crupier si no se ha revelado
        self.lbl_pts_crupier.config(text=f"Puntos Crupier: {pts_c}")  # Actualiza etiqueta de puntos crupier
        # Refresco de Scroll
        self.on_frame_configure()  # Reajusta el área de scroll por si creció el contenido

    """ INICIALIZACIÓN DE RONDA: Resetea el puntero de la pila y vacía las listas dinámicas de las manos. """
    def nueva_mano(self): 
        self.lbl_log.config(text="BARAJANDO ESTRUCTURA... Creando nueva Pila LIFO.")  # Informa al usuario sobre la estructura
        self.btn_hit.config(state="disabled")  # Desactiva botones durante animación
        self.btn_stand.config(state="disabled")  # Desactiva botones durante animación
        self.btn_new.config(state="disabled")  # Desactiva botones durante animación
        self.baraja = self.crear_baraja()  # Reinicializa la pila barajada
        self.ind_baraja = 0  # Resetea el puntero TOP al inicio del arreglo
        self.mano_jugador = []  # Vacía la lista dinámica del jugador
        self.mano_crupier = []  # Vacía la lista dinámica del crupier
        for i in range(2):  # Reparte 2 cartas iniciales a cada uno
            self.root.after(i * 800, self.animar_jugador)  # Programa animación para el jugador
            self.root.after(i * 800 + 400, self.animar_crupier)  # Programa animación para el crupier con un pequeño retraso para efecto visual
        self.root.after(1600, lambda: [  # Después de repartir, habilita botones y actualiza el log
            self.btn_hit.config(state="normal"),  # Habilita botón de pedir carta
            self.btn_stand.config(state="normal"),  # Habilita botón de plantarse
            self.btn_new.config(state="normal"),  # Habilita botón de reiniciar
            self.lbl_log.config(text="CARTAS REPARTIDAS. ¿Pedir (POP) o Plantarse?")  # Informa al usuario que es su turno para decidir la acción
        ])

    """ AUTOMATIZACIÓN: Realiza un POP() y lo añade a la mano del jugador para efectos visuales de inicio. """
    def animar_jugador(self):
        self.mano_jugador.append(self.ejecutar_pop())  # Realiza un POP() y lo agrega a la lista del jugador
        self.actualizar_mesa()  # Refresca la interfaz

    """ Realiza un POP() y lo añade a la mano del crupier para efectos visuales de inicio. """
    def animar_crupier(self):
        self.mano_crupier.append(self.ejecutar_pop())  # Realiza un POP() y lo agrega a la lista del crupier
        self.actualizar_mesa()  # Refresca la interfaz

    """ ACCIÓN JUGADOR: Ejecuta manualmente el POP() de la pila y actualiza el estado del juego. """
    def hit(self):       
        c = self.ejecutar_pop()  # Ejecuta la operación POP() sobre la pila de cartas
        self.mano_jugador.append(c)  # Inserta el elemento en la lista dinámica del jugador
        # ACTUALIZACIÓN DEL LOG
        self.lbl_log.config(text=f"ACCIÓN: POP() -> Se extrae {c} de la Pila.")  # Registra la operación de estructura de datos
        self.actualizar_mesa()  # Refresca la visualización de la mesa
        if self.calcular_puntos(self.mano_jugador) > 21:  # Verifica condición de derrota inmediata
            self.stand()  # Si se pasó, termina su turno automáticamente

    """ CONTROL DE FLUJO: Desactiva la entrada del usuario y activa la lógica de decisión de la IA. """
    def stand(self):
        self.btn_hit.config(state="disabled")  # Desactiva botón de pedir carta para evitar más acciones del jugador
        self.btn_stand.config(state="disabled")  # Desactiva botón de plantarse para evitar más acciones del jugador
        self.btn_new.config(state="disabled")  # Desactiva botón de nueva mano para evitar reinicios durante el turno del crupier
        self.lbl_log.config(text="TURNO DEL CRUPIER: Procesando lógica de la casa...")  # Informa al usuario que es el turno del crupier
        self.turno_crupier()  #  Inicia el proceso de decisión del crupier para su turno, evaluando la mesa y actuando en consecuencia

    """ ALGORITMO: Evalúa el estado de la mesa y decide si extraer más datos de la pila (POP). """
    def turno_crupier(self):
        pj, pc = self.calcular_puntos(self.mano_jugador), self.calcular_puntos(self.mano_crupier)  # Obtiene puntajes actuales
        if pj <= 21 and pc < pj and pc < 21:  # Condición para que el crupier siga pidiendo cartas
            c = self.ejecutar_pop()  # Realiza un POP() para el crupier si las condiciones indican que debe seguir jugando
            # ACTUALIZACIÓN DEL LOG
            self.lbl_log.config(text=f"IA CRUPIER: Tiene {pc}, necesita superar {pj}. POP() -> {c}")  # Muestra proceso interno
            self.mano_crupier.append(c)  # Agrega carta a su lista
            self.actualizar_mesa(revelar=True)  # Refresca mesa revelando cartas
            self.root.after(900, self.turno_crupier)  # Espera un tiempo y vuelve a evaluar decisión
        else:  # Si la IA decide no pedir más o se pasó
            self.lbl_log.config(text=f"IA CRUPIER FINALIZA. Total Crupier: {pc}")  # Informa que el crupier ha terminado su turno
            self.actualizar_mesa(revelar=True)  # Refresca mesa final
            self.veredicto()  # Llama a la función de comparación final

    """ COMPARACIÓN FINAL: Analiza los puntajes finales de ambas estructuras para declarar un ganador. """
    def veredicto(self):
        pj, pc = self.calcular_puntos(self.mano_jugador), self.calcular_puntos(self.mano_crupier)  # Variables de puntaje final
        res_t = f"Tu puntuación: {pj}\nPuntuación Crupier: {pc}\n\n"  # Prepara encabezado del resultado
        
        if pj > 21: m = res_t + "¡PERDISTE! Te pasaste de 21 puntos."  # Condición: Jugador excede límite
        elif pc > 21: m = res_t + "¡GANASTE! La casa se pasó."  # Condición: crupier excede límite
        elif pj < pc: m = res_t + "¡PERDISTE! La casa gana. Puntuación del crupier es superior."  # Condición: crupier tiene mejor puntaje
        else: m = res_t + "¡EMPATE!"  # Condición: Ambos puntajes iguales
        
        self.lbl_log.config(text=f"PARTIDA FINALIZADA. {pj} vs {pc}. Presiona 'REPARTIR'.")  # Log de fin de juego
        messagebox.showinfo("Resultado del Análisis", m)  # Muestra ventana emergente con el ganador
        self.btn_new.config(state="normal")  # Habilita botón para nueva partida
        self.on_frame_configure()  # Ajusta scroll final

if __name__ == "__main__":
    """ PUNTO DE ENTRADA: Inicia la ejecución de la aplicación y el bucle principal de eventos. """
    root = tk.Tk()  # Crea la instancia raíz de Tkinter
    app = Blackjack(root)  # Instancia la clase del juego pasándole la raíz
    root.mainloop()  # Inicia el bucle de espera de eventos de la aplicación