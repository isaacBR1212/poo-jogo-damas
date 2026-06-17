from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, Ellipse

from app.models.tema import TEMAS_DISPONIVEIS


class AmostraTema(MDCard):

    def __init__(self, tema, controller, theme_screen, **kwargs):
        super().__init__(**kwargs)
        self.tema = tema
        self.controller = controller
        self.theme_screen = theme_screen

        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(110)
        self.padding = dp(10)
        self.spacing = dp(6)
        self.ripple_behavior = True
        self.elevation = 2 if tema is not controller.tema else 6

        # Área de prévia (desenhada no canva)
        self.preview = MDBoxLayout(size_hint_y=None, height=dp(60))
        self.preview.bind(size=self._desenhar_preview, pos=self._desenhar_preview)
        self.add_widget(self.preview)

        self.add_widget(MDLabel(
            text=tema.nome,
            halign="center",
            theme_text_color="Primary",
            bold=True,
            size_hint_y=None,
            height=dp(24),
        ))

    def _desenhar_preview(self, *args):
        self.preview.canvas.clear()
        w, h = self.preview.size
        x, y = self.preview.pos
        if w <= 0:
            return

        meio = w / 2
        with self.preview.canvas:
            Color(*self.tema.casa_clara)
            Rectangle(pos=(x, y), size=(meio, h))
            Color(*self.tema.casa_escura)
            Rectangle(pos=(x + meio, y), size=(meio, h))

            r = h * 0.32
            Color(*self.tema.peca_j1)
            Ellipse(pos=(x + meio/2 - r, y + h/2 - r), size=(r*2, r*2))

            Color(*self.tema.peca_j2)
            Ellipse(pos=(x + meio + meio/2 - r, y + h/2 - r), size=(r*2, r*2))

    def on_release(self):
        self.controller.definir_tema(self.tema)
        self.theme_screen._atualizar_selecao()


class ThemeScreen(MDScreen):

    def __init__(self, controller, **kwargs):
        self.controller = controller
        self._cards = []
        super().__init__(**kwargs)
        self._build()

    def _build(self):
        raiz = MDBoxLayout(orientation="vertical")

        barra = MDTopAppBar(
            title="Personalizar Tema",
            left_action_items=[["arrow-left", lambda x: self._voltar()]],
        )
        raiz.add_widget(barra)

        lista = MDBoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(14),
        )

        for tema in TEMAS_DISPONIVEIS:
            card = AmostraTema(tema, self.controller, self)
            self._cards.append(card)
            lista.add_widget(card)

        raiz.add_widget(lista)
        self.add_widget(raiz)

    def _atualizar_selecao(self):
        for card in self._cards:
            card.elevation = 6 if card.tema is self.controller.tema else 2

    def _voltar(self):
        if self.controller.game:
            self.manager.current = "board"
        else:
            self.manager.current = "menu"