import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import StringProperty, BooleanProperty
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader

# ---------------------------
#   JUEGO
# ---------------------------
class Juego(Widget):
    estado = StringProperty("Usa la pala para enterrar los 3 huevos (0/3)")
    completado = BooleanProperty(False)
    parpadeo_activo = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.huevos = []
        self.huevos_descubiertos = set()
        self.arrastrando = False
        self._parpadeo_phase = 0

        # Imagen especial
        self.imagen_central = None
        self.imagen_central_pos = None
        self.imagen_central_visible = True
        self.imagen_central_moviendo = False
        self.imagen_central_activable = False  # Solo se puede activar si los 3 huevos han sido encontrados

        # Sonido
        self.sonido_enterrar = SoundLoader.load("cavando.wav")

        with self.canvas:
            # Crear 3 huevos en posiciones aleatorias
            for i in range(3):
                pos = self._posicion_valida()
                huevo = Rectangle(source="Huevos.png", pos=pos, size=(130, 90))
                self.huevos.append(huevo)

            # Crear la pala
            self.pala = Rectangle(source="pala.png", pos=(200, 300), size=(120, 120))

            # Imagen central (inicial)
            self.imagen_central_pos = self._pos_centro()
            self.imagen_central = Rectangle(source="tortuga triste.png", pos=self.imagen_central_pos, size=(120, 120))

        Clock.schedule_interval(self._animar_huevos, 0.05)
        Clock.schedule_interval(self._animar_imagen_central, 1/60)
        self.bind(size=self._ajustar_imagen_central)

    def _animar_huevos(self, dt):
        if not self.parpadeo_activo:
            for huevo in self.huevos:
                huevo.size = (130, 90)
            return

        self._parpadeo_phase += dt * 2
        scale = 1 + 0.2 * abs(__import__('math').sin(self._parpadeo_phase))
        for i, huevo in enumerate(self.huevos):
            if i in self.huevos_descubiertos:
                huevo.size = (130, 90)
            else:
                huevo.size = (130 * scale, 90 * scale)

    def _animar_imagen_central(self, dt):
        if not self.imagen_central_visible or not self.imagen_central:
            return

        # Solo mover si está en modo moviendo y animaciones activas
        if self.imagen_central_moviendo and self.parpadeo_activo:
            x, y = self.imagen_central.pos
            target_y = self.height * (2/3)
            speed = 3
            if y < target_y:
                y = min(y + speed, target_y)
                self.imagen_central.pos = (x, y)
            else:
                # Desaparece al llegar al 1/3 superior
                self.imagen_central_visible = False
                self.imagen_central.pos = (-999, -999)  # Fuera de pantalla

    def _pos_centro(self):
        cx = self.width / 2 - 60
        cy = self.height / 2 - 60
        return (cx, cy)

    def _posicion_valida(self):
        while True:
            x = random.randint(50, self.width - 150 if self.width > 150 else 400)
            y = random.randint(50, int(self.height * 0.5) - 100 if self.height > 200 else 200)
            nuevo = (x, y)
            if all(not self._se_superpone(nuevo, (100, 80), h.pos, h.size) for h in self.huevos):
                return nuevo

    def _se_superpone(self, pos1, size1, pos2, size2, margen=10):
        x1, y1 = pos1; w1, h1 = size1
        x2, y2 = pos2; w2, h2 = size2
        return not (x1 + w1 + margen < x2 or
                    x1 > x2 + w2 + margen or
                    y1 + h1 + margen < y2 or
                    y1 > y2 + h2 + margen)

    def on_touch_down(self, touch):
        # Pulsar la pala para arrastrar
        if self._colision(self.pala, touch.pos):
            self.arrastrando = True
            return True

        # Pulsar la imagen central solo si es activable y visible
        if self.imagen_central_activable and self.imagen_central_visible and self._colision(self.imagen_central, touch.pos):
            self._activar_imagen_central()
            return True

    def on_touch_move(self, touch):
        if self.arrastrando:
            self.pala.pos = (touch.x - self.pala.size[0] / 2,
                             touch.y - self.pala.size[1] / 2)

            for i, huevo in enumerate(self.huevos):
                if self._colision(self.pala, huevo.pos):
                    if i not in self.huevos_descubiertos:
                        self.huevos_descubiertos.add(i)
                        huevo.source = "Huevos enterrados.png"
                        if self.sonido_enterrar:
                            self.sonido_enterrar.play()

            if len(self.huevos_descubiertos) == len(self.huevos):
                self.estado = "Enterraste los 3 huevos :), ahora la tortuga puede irse, libérala"
                self.completado = True
                self.imagen_central_activable = True  # Ahora se puede activar la imagen central
            else:
                self.estado = f"Huevos enterrados: {len(self.huevos_descubiertos)}/{len(self.huevos)}"

    def on_touch_up(self, touch):
        if self.arrastrando:
            self.arrastrando = False

    def _colision(self, figura, pos):
        x, y = pos
        return (x >= figura.pos[0] and
                x <= figura.pos[0] + figura.size[0] and
                y >= figura.pos[1] and
                y <= figura.pos[1] + figura.size[1])

    def _activar_imagen_central(self):
        if self.imagen_central:
            self.imagen_central.source = "tortuga.png"
            if self.parpadeo_activo:
                self.imagen_central_moviendo = True
                self.imagen_central_activable = False  # Solo se activa una vez
                self.estado = "Felicidades eres el heroe de la playa"
            else:
                # Solo cambia la imagen, no desaparece ni se mueve
                self.estado = "Felicidades eres el heroe de la playa"

    def reset(self):
        self.estado = "Usa la pala para enterrar los 3 huevos (0/3)"
        self.completado = False
        self.huevos_descubiertos.clear()

        for huevo in self.huevos:
            huevo.pos = self._posicion_valida()
            huevo.source = "Huevos.png"

        self.pala.pos = (200, 300)

        # Imagen central vuelve al centro y a la imagen inicial
        if self.imagen_central:
            self.imagen_central.source = "tortuga triste.png"
            self.imagen_central.pos = self._pos_centro()
            self.imagen_central_visible = True
            self.imagen_central_moviendo = False
            self.imagen_central_activable = False

    def _ajustar_imagen_central(self, *args):
        if self.imagen_central:
            self.imagen_central.pos = self._pos_centro()


# ---------------------------
#   PANTALLAS
# ---------------------------
class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=50, spacing=20)

        # Cambia el color aquí (RGBA, valores de 0 a 1)
        with layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(1, 1, 1, 1)  # Blanco, cambia los valores a tu gusto
            self.bg_rect = Rectangle(pos=layout.pos, size=layout.size)

        # Actualiza el tamaño del fondo si la ventana cambia
        layout.bind(pos=self._update_bg, size=self._update_bg)

        self.img = Image(source="NV_LOGO.png")

        layout.add_widget(self.img)
        self.add_widget(layout)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def on_enter(self):
        # Cambiar automáticamente al menú después de 2 segundos
        Clock.schedule_once(self.cambiar, 2)

    def cambiar(self, dt):
        self.manager.current = "menu"



class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="horizontal", spacing=20, padding=50)

        # Sonidos de botones
        self.sonido_boton1 = SoundLoader.load("Inicio.wav")  # Jugar
        self.sonido_boton2 = SoundLoader.load("Salida.wav")  # Salir

        # Fondo con imagen
        with layout.canvas.before:
            from kivy.graphics import Rectangle
            self.bg_rect = Rectangle(source="Fondo del menu.jpg", pos=layout.pos, size=layout.size)

        layout.bind(pos=self._update_bg, size=self._update_bg)

        titulo = Label(text=" Mahahual Aventura ", font_size=32, color=(0 , 0 , 0 , 1), font_name="Roboto-Bold.ttf")
        btn_jugar = Button(text="Jugar", size_hint_y=None, height=60)
        btn_salir = Button(text="Salir", size_hint_y=None, height=60)

        btn_jugar.bind(on_release=lambda *_: self.sonar_boton1_e_ir_a_juego())
        btn_salir.bind(on_release=lambda *_: self.sonar_boton2_y_salir_con_carga())

        layout.add_widget(titulo)
        layout.add_widget(btn_jugar)
        layout.add_widget(btn_salir)

        self.add_widget(layout)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def sonar_boton1_e_ir_a_juego(self):
        if self.sonido_boton1:
            self.sonido_boton1.play()
        self.manager.current = "juego"

    def sonar_boton2_y_salir_con_carga(self):
        if self.sonido_boton2:
            self.sonido_boton2.play()
        self.manager.current = "loading"
        Clock.schedule_once(lambda dt: App.get_running_app().stop(), 1)



class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Sonidos de botones
        self.sonido_boton1 = SoundLoader.load("Inicio.wav")  # Reiniciar, animación
        self.sonido_boton2 = SoundLoader.load("Salida.wav")  # Volver al menú

        # Fondo: solo una imagen que cubre toda la pantalla
        with layout.canvas.before:
            from kivy.graphics import Rectangle
            self.bg_rect = Rectangle(source="Fondo juego.jpg", pos=layout.pos, size=layout.size)

        layout.bind(pos=self._update_bg, size=self._update_bg)

        self.juego = Juego(size_hint=(0.8, 0.7), pos_hint={'x':0.1, 'y':0.2})
        self.label_estado = Label(text=self.juego.estado, font_size=30, size_hint=(0.6, None), height=40, pos_hint={'x':0.2, 'y':0.02}, color=(0, 0, 0, 1))
        self.juego.bind(estado=lambda _, val: setattr(self.label_estado, "text", val))

        btn_reiniciar = Button(text="Reiniciar juego", size_hint=(None, None), size=(150, 60), pos_hint={'x':0.85, 'y':0.1})
        btn_volver = Button(text="Volver al menú", size_hint=(None, None), size=(150, 60), pos_hint={'x':0.85, 'y':0.2})
        self.btn_animacion = Button(
            text="Desactivar animación",
            size_hint=(None, None),
            size=(180, 60),
            pos_hint={'x':0.85, 'y':0.3}
        )
        self.btn_animacion.bind(on_release=self.toggle_parpadeo)

        btn_reiniciar.bind(on_release=lambda *_: self.sonar_boton1_y_reiniciar())
        btn_volver.bind(on_release=lambda *_: self.sonar_boton2_y_volver_menu())

        layout.add_widget(self.label_estado)
        layout.add_widget(self.juego)
        layout.add_widget(btn_reiniciar)
        layout.add_widget(btn_volver)
        layout.add_widget(self.btn_animacion)

        self.add_widget(layout)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def sonar_boton2_y_volver_menu(self):
        if self.sonido_boton2:
            self.sonido_boton2.play()
        self.juego.reset()
        self.manager.current = "menu"

    def sonar_boton1_y_reiniciar(self):
        if self.sonido_boton1:
            self.sonido_boton1.play()
        self.juego.reset()

    def toggle_parpadeo(self, instance):
        if self.sonido_boton1:
            self.sonido_boton1.play()
        self.juego.parpadeo_activo = not self.juego.parpadeo_activo
        instance.text = "Activar animación" if not self.juego.parpadeo_activo else "Desactivar animación"


# ---------------------------
#   APP PRINCIPAL
# ---------------------------
class MiApp(App):
    def build(self):
        self.title = "Mahahual Aventura"
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(LoadingScreen(name="loading"))
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="juego"))

        sm.current = "loading"
        self.sm = sm
        return sm

    def on_stop(self):
        # Antes de cerrar, muestra la pantalla de carga
        if hasattr(self, 'sm'):
            self.sm.current = "loading"
            Clock.schedule_once(lambda dt: None, 1)  # Pequeña pausa opcional


if __name__ == "__main__":
    MiApp().run()
