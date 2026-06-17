from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line


class PecasDecorativas(Widget):

    def __init__(self, **kwargs):
        kwargs.setdefault("size_hint", (None, None))
        kwargs.setdefault("size", (dp(140), dp(110)))
        super().__init__(**kwargs)
        self.bind(pos=self._desenhar, size=self._desenhar)

    def _desenhar(self, *args):
        self.canvas.clear()
        cx = self.center_x
        cy = self.center_y
        r = dp(30)

        with self.canvas:
            # Peça branca 
            Color(0, 0, 0, 0.12)
            Ellipse(pos=(cx - r + dp(18), cy - r + dp(10)), size=(r*2, r*2))
            Color(0.96, 0.96, 0.96, 1)
            Ellipse(pos=(cx - r + dp(16), cy - r + dp(12)), size=(r*2, r*2))
            Color(0.82, 0.82, 0.82, 1)
            Line(circle=(cx + dp(16), cy + dp(12), r * 0.52), width=dp(2.5))

            # Peça preta 
            Color(0, 0, 0, 0.22)
            Ellipse(pos=(cx - r - dp(16), cy - r - dp(10)), size=(r*2, r*2))
            Color(0.13, 0.11, 0.10, 1)
            Ellipse(pos=(cx - r - dp(18), cy - r - dp(8)), size=(r*2, r*2))
            Color(0.27, 0.23, 0.21, 1)
            Line(circle=(cx - dp(18), cy - dp(8), r * 0.52), width=dp(2.5))


class MenuScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (1, 1, 1, 1)
        self._build()

    def _build(self):
        raiz = MDBoxLayout(
            orientation="vertical",
            spacing=0,
            padding=[dp(40), dp(40), dp(40), dp(40)],
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
            height=dp(100),
        ))

        raiz.add_widget(Widget(size_hint_y=None, height=dp(10)))

        
        linha_pecas = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(120),
        )
        linha_pecas.add_widget(Widget())   
        pecas = PecasDecorativas()
        linha_pecas.add_widget(pecas)
        linha_pecas.add_widget(Widget())  
        raiz.add_widget(linha_pecas)

        raiz.add_widget(Widget(size_hint_y=None, height=dp(30)))

        # Botões
        def cria_botao(texto, callback):
            return MDRaisedButton(
                text=texto,
                size_hint=(None, None),
                size=(dp(260), dp(52)),
                pos_hint={"center_x": 0.5},
                md_bg_color=(0.10, 0.09, 0.08, 1),
                text_color=(1, 1, 1, 1),
                font_size=dp(15),
                elevation=0,
                on_release=callback,
            )

        raiz.add_widget(cria_botao(
            "NOVO JOGO",
            lambda *a: setattr(self.manager, "current", "config")
        ))
        raiz.add_widget(Widget(size_hint_y=None, height=dp(14)))

        raiz.add_widget(cria_botao(
            "CONFIGURAÇÕES",
            lambda *a: setattr(self.manager, "current", "theme")
        ))
        raiz.add_widget(Widget(size_hint_y=None, height=dp(14)))

        raiz.add_widget(cria_botao(
            "SAIR",
            lambda *a: __import__("kivy.app", fromlist=["App"]).App.get_running_app().stop()
        ))

        
        raiz.add_widget(Widget(size_hint_y=1))

        self.add_widget(raiz)