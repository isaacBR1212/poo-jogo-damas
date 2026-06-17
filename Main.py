from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from app.controllers.game_controller import GameController
from app.views.menu_screen import MenuScreen
from app.views.config_screen import ConfigScreen
from app.views.board_screen import BoardScreen
from app.views.theme_screen import ThemeScreen


class DamasApp(MDApp):
    """Ponto de entrada da aplicação KivyMD."""

    def build(self):
        self.theme_cls.primary_palette = "Brown"
        self.theme_cls.accent_palette  = "Amber"
        self.theme_cls.theme_style     = "Light"
        self.title = "Jogo de Damas"

    
        controller = GameController()

        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(ConfigScreen(controller=controller, name="config"))
        sm.add_widget(BoardScreen(controller=controller, name="board"))
        sm.add_widget(ThemeScreen(controller=controller, name="theme"))

        return sm


if __name__ == "__main__":
    DamasApp().run()