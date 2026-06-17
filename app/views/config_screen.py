from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp


class ConfigScreen(MDScreen):
    """Configurações dos jogadores"""

    def __init__(self, controller, **kwargs):
        self.controller = controller
        super().__init__(**kwargs)
        self._build()

    def _build(self):
        root = MDBoxLayout(
            orientation="vertical",
            spacing=dp(16),
            padding=[dp(40), dp(50), dp(40), dp(50)],
        )

        root.add_widget(MDLabel(
            text="Configurar Partida",
            halign="center",
            theme_text_color="Primary",
            font_style="H5",
            size_hint_y=None,
            height=dp(50),
        ))

        root.add_widget(MDLabel(
            text="Peças brancas (⬤)",
            halign="left",
            theme_text_color="Secondary",
            font_style="Subtitle2",
            size_hint_y=None,
            height=dp(30),
        ))

        self.campo_j1 = MDTextField(
            hint_text="Nome do Jogador 1",
            text="Jogador 1",
            mode="rectangle",
            size_hint_y=None,
            height=dp(50),
        )
        root.add_widget(self.campo_j1)

        root.add_widget(MDLabel(
            text="Peças pretas (⬤)",
            halign="left",
            theme_text_color="Secondary",
            font_style="Subtitle2",
            size_hint_y=None,
            height=dp(30),
        ))

        self.campo_j2 = MDTextField(
            hint_text="Nome do Jogador 2",
            text="Jogador 2",
            mode="rectangle",
            size_hint_y=None,
            height=dp(50),
        )
        root.add_widget(self.campo_j2)

        root.add_widget(MDBoxLayout(size_hint_y=None, height=dp(20)))

        btn_iniciar = MDRaisedButton(
            text="INICIAR JOGO",
            size_hint=(None, None),
            size=(dp(240), dp(50)),
            pos_hint={"center_x": 0.5},
            on_release=self._iniciar,
        )
        root.add_widget(btn_iniciar)

        btn_voltar = MDFlatButton(
            text="VOLTAR",
            size_hint=(None, None),
            size=(dp(240), dp(50)),
            pos_hint={"center_x": 0.5},
            on_release=lambda *a: setattr(self.manager, "current", "menu"),
        )
        root.add_widget(btn_voltar)

        self.add_widget(root)

    def _iniciar(self, *args):
        nome1 = self.campo_j1.text.strip() or "Jogador 1"
        nome2 = self.campo_j2.text.strip() or "Jogador 2"
        self.controller.iniciar_partida(nome1, nome2)
        self.manager.current = "board"