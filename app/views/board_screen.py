from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.widget import Widget


#  Cores do tabuleiro 
COR_CASA_CLARA  = (0.94, 0.85, 0.71, 1)   
COR_CASA_ESCURA = (0.55, 0.37, 0.24, 1)   
COR_SELECIONADA = (0.20, 0.75, 0.45, 1)   
COR_DESTINO     = (0.95, 0.80, 0.20, 0.7) 
COR_PECA_J1     = (0.95, 0.95, 0.90, 1)   
COR_PECA_J2     = (0.15, 0.12, 0.10, 1)  


class CasaWidget(Widget):
    """Widget de uma casa do tabuleiro 8×8."""

    def __init__(self, linha, col, controller, board_screen, **kwargs):
        super().__init__(**kwargs)
        self.linha = linha
        self.col = col
        self.controller = controller
        self.board_screen = board_screen
        self.bind(size=self._desenhar, pos=self._desenhar)

    def _desenhar(self, *args):
        self.canvas.clear()
        w, h = self.size
        x, y = self.pos
        t = self.board_screen

        eh_escura = (self.linha + self.col) % 2 == 1

        # Cor de fundo da casa
        if (self.linha, self.col) == t.selecionado:
            cor_fundo = COR_SELECIONADA
        elif (self.linha, self.col) in t.destinos_possiveis:
            cor_fundo = COR_DESTINO
        elif eh_escura:
            cor_fundo = COR_CASA_ESCURA
        else:
            cor_fundo = COR_CASA_CLARA

        with self.canvas:
            Color(*cor_fundo)
            Rectangle(pos=self.pos, size=self.size)

            # Desenha a peça se houver
            peca = self.controller.get_tabuleiro()[self.linha][self.col]
            if peca:
                margem = w * 0.12
                diametro = w - 2 * margem

                
                Color(0, 0, 0, 0.25)
                Ellipse(
                    pos=(x + margem + 2, y + margem - 2),
                    size=(diametro, diametro)
                )

                # Corpo da peça
                if peca.jogador == 1:
                    Color(*COR_PECA_J1)
                else:
                    Color(*COR_PECA_J2)
                Ellipse(
                    pos=(x + margem, y + margem),
                    size=(diametro, diametro)
                )

                # Anel da dama
                from app.models.damas import PecaDamas
                if isinstance(peca, PecaDamas) and peca.dama:
                    Color(0.85, 0.65, 0.10, 1)   # dourado
                    espessura = diametro * 0.12
                    Ellipse(
                        pos=(x + margem + espessura, y + margem + espessura),
                        size=(diametro - 2*espessura, diametro - 2*espessura)
                    )
                    if peca.jogador == 1:
                        Color(*COR_PECA_J1)
                    else:
                        Color(*COR_PECA_J2)
                    Ellipse(
                        pos=(x + margem + espessura*2, y + margem + espessura*2),
                        size=(diametro - 4*espessura, diametro - 4*espessura)
                    )

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        self.board_screen.tratar_toque(self.linha, self.col)
        return True


class BoardScreen(MDScreen):
    """Tela principal do jogo ."""

    def __init__(self, controller, **kwargs):
        self.controller = controller
        self.selecionado = None        
        self.destinos_possiveis = []   
        self._dialog = None
        super().__init__(**kwargs)
        self._build()


    def _build(self):
        raiz = MDBoxLayout(orientation="vertical")

        from kivymd.uix.toolbar import MDTopAppBar
        barra = MDTopAppBar(
            title="Jogo de Damas",
            left_action_items=[["arrow-left", lambda x: self._voltar_menu()]],
            right_action_items=[["refresh", lambda x: self._reiniciar()]],
        )
        raiz.add_widget(barra)

       
        centro = MDBoxLayout(orientation="horizontal")

        self.painel = self._criar_painel()
        centro.add_widget(self.painel)

        # Tabuleiro
        self.grade = MDGridLayout(cols=8, rows=8)
        self.casas: list[list[CasaWidget]] = []
        for l in range(8):
            linha_casas = []
            for c in range(8):
                casa = CasaWidget(l, c, self.controller, self)
                self.grade.add_widget(casa)
                linha_casas.append(casa)
            self.casas.append(linha_casas)
        centro.add_widget(self.grade)

        raiz.add_widget(centro)
        self.add_widget(raiz)

        self.controller.on_update = self.atualizar

    def _criar_painel(self):
        painel = MDBoxLayout(
            orientation="vertical",
            size_hint_x=None,
            width=dp(140),
            padding=dp(10),
            spacing=dp(10),
        )

        painel.add_widget(MDLabel(
            text="Vez de:",
            font_style="Caption",
            theme_text_color="Secondary",
            size_hint_y=None, height=dp(20),
        ))

        self.label_turno = MDLabel(
            text="—",
            font_style="Subtitle1",
            theme_text_color="Primary",
            bold=True,
            size_hint_y=None, height=dp(30),
        )
        painel.add_widget(self.label_turno)

        painel.add_widget(MDLabel(
            text="Peças J1:",
            font_style="Caption",
            theme_text_color="Secondary",
            size_hint_y=None, height=dp(20),
        ))
        self.label_j1 = MDLabel(
            text="12",
            font_style="H6",
            size_hint_y=None, height=dp(30),
        )
        painel.add_widget(self.label_j1)

        painel.add_widget(MDLabel(
            text="Peças J2:",
            font_style="Caption",
            theme_text_color="Secondary",
            size_hint_y=None, height=dp(20),
        ))
        self.label_j2 = MDLabel(
            text="12",
            font_style="H6",
            size_hint_y=None, height=dp(30),
        )
        painel.add_widget(self.label_j2)

        
        painel.add_widget(MDBoxLayout())

        return painel

    #  condições: 

    def tratar_toque(self, linha: int, col: int):
        if self.controller.get_fim():
            return

        tabuleiro = self.controller.get_tabuleiro()
        peca_clicada = tabuleiro[linha][col]
        jogador_atual = self.controller.get_numero_jogador_atual()

       
        if peca_clicada and peca_clicada.jogador == jogador_atual:
            self.selecionado = (linha, col)
            self.destinos_possiveis = self.controller.get_jogadas_possiveis(linha, col)
            self.redesenhar()
            return

        
        if self.selecionado and (linha, col) in self.destinos_possiveis:
            ol, oc = self.selecionado
            self.selecionado = None
            self.destinos_possiveis = []
            self.controller.executar_jogada(ol, oc, linha, col)
            return

        
        self.selecionado = None
        self.destinos_possiveis = []
        self.redesenhar()

   

    def atualizar(self):
        """Chamado pelo controller após cada jogada válida."""
        self.label_turno.text = self.controller.get_jogador_atual()
        self.label_j1.text = str(self.controller.get_pecas_count(1))
        self.label_j2.text = str(self.controller.get_pecas_count(2))
        self.redesenhar()

        if self.controller.get_fim():
            self._mostrar_resultado()

    def redesenhar(self):
        for l in range(8):
            for c in range(8):
                self.casas[l][c]._desenhar()

    #  resultado final

    def _mostrar_resultado(self):
        vencedor = self.controller.get_vencedor()
        texto = f"{vencedor} venceu!" if vencedor else "Empate!"

        if self._dialog:
            self._dialog.dismiss()

        self._dialog = MDDialog(
            title="Fim de jogo",
            text=texto,
            buttons=[
                MDFlatButton(
                    text="NOVO JOGO",
                    on_release=lambda *a: self._dialog.dismiss() or setattr(
                        self.manager, "current", "config")
                ),
                MDFlatButton(
                    text="MENU",
                    on_release=lambda *a: self._dialog.dismiss() or setattr(
                        self.manager, "current", "menu")
                ),
            ],
        )
        self._dialog.open()


    def _reiniciar(self):
        self.selecionado = None
        self.destinos_possiveis = []
        self.controller.reiniciar()

    def _voltar_menu(self):
        self.selecionado = None
        self.destinos_possiveis = []
        self.manager.current = "menu"