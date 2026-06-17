from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, RoundedRectangle


class PecasDecorativas(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(120), dp(100))
        self.bind(pos=self._desenhar, size=self._desenhar)

    def _desenhar(self, *args):
        self.canvas.clear()
        cx = self.center_x
        cy = self.center_y
        r = dp(32)

        with self.canvas:
            # Peça branca 
            Color(0, 0, 0, 0.12)
            Ellipse(pos=(cx - r + dp(15), cy - r + dp(8)), size=(r*2, r*2))
            Color(0.96, 0.96, 0.96, 1)
            Ellipse(pos=(cx - r + dp(13), cy - r + dp(10)), size=(r*2, r*2))
            Color(0.82, 0.82, 0.82, 1)
            Line(circle=(cx + dp(13), cy + dp(10), r * 0.52), width=dp(2.5))

            # Peça preta 
            Color(0, 0, 0, 0.22)
            Ellipse(pos=(cx - r - dp(11), cy - r - dp(9)), size=(r*2, r*2))
            Color(0.13, 0.11, 0.10, 1)
            Ellipse(pos=(cx - r - dp(13), cy - r - dp(7)), size=(r*2, r*2))
            Color(0.27, 0.23, 0.21, 1)
            Line(circle=(cx - dp(13), cy - dp(7), r * 0.52), width=dp(2.5))


class BotaoEscuro(Widget):

    def __init__(self, text, on_press_cb, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(260), dp(52))
        self._text = text
        self._cb = on_press_cb
        self.bind(pos=self._desenhar, size=self._desenhar)

    def _desenhar(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.10, 0.09, 0.08, 1)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(26)]
            )

        self.canvas.after.clear()
        from kivy.core.text import Label as CoreLabel
        lbl = CoreLabel(text=self._text, font_size=dp(15), bold=True)
        lbl.refresh()
        texture = lbl.texture
        with self.canvas.after:
            Color(1, 1, 1, 1)
            from kivy.graphics import Rectangle
            Rectangle(
                texture=texture,
                pos=(
                    self.center_x - texture.width / 2,
                    self.center_y - texture.height / 2,
                ),
                size=texture.size,
            )

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._cb()
            return True
        return super().on_touch_down(touch)


class MenuScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (1, 1, 1, 1)
        self._build()

    def _build(self):
        raiz = MDBoxLayout(
            orientation="vertical",
            spacing=0,
            padding=[dp(40), dp(48), dp(40), dp(48)],
        )

        # Título
        raiz.add_widget(MDLabel(
            text="DAMAS",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="H1",
            bold=True,
            size_hint_y=None,
            height=dp(110),
        ))

        # Peças decorativas
        container = MDFloatLayout(size_hint_y=None, height=dp(110))
        pecas = PecasDecorativas(pos_hint={"center_x": 0.5, "center_y": 0.5})
        container.add_widget(pecas)
        raiz.add_widget(container)

        raiz.add_widget(Widget(size_hint_y=None, height=dp(20)))

        # Botões
        def add_btn(texto, cb):
            box = MDFloatLayout(size_hint_y=None, height=dp(52))
            btn = BotaoEscuro(
                text=texto,
                on_press_cb=cb,
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            )
            box.add_widget(btn)
            raiz.add_widget(box)
            raiz.add_widget(Widget(size_hint_y=None, height=dp(14)))

        add_btn("NOVO JOGO",      lambda: setattr(self.manager, "current", "config"))
        add_btn("CONFIGURAÇÕES",  lambda: setattr(self.manager, "current", "theme"))
        add_btn("SAIR",           lambda: __import__(
            "kivy.app", fromlist=["App"]).App.get_running_app().stop())

        raiz.add_widget(Widget())
        self.add_widget(raiz)