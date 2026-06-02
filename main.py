import os
import sys
import json
import subprocess
from datetime import datetime

# Настройка окружения Kivy для мобильного экрана
from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# Цветовая палитра Premium Cyber Dark из вашего оригинального кода
BG_COLOR = "#0D0E15"
SIDEBAR_COLOR = "#151722"
CARD_COLOR = "#1E2030"
CONSOLES_BG = "#06070B"
ACCENT_BLUE = "#2b719e"
ACCENT_GREEN = "#10B981"
ACCENT_RED = "#EF4444"
TEXT_MUTED = "#888A96"

# Конфигурации Xray серверов (перенесены из вашего кода)
SELF_VPN_CONFIGS = {
    "Italy 2 🇮🇹 [Durev VPN]": {
        "outbounds": [{"protocol": "vless", "settings": {"vnext": [{"address": "158.160.169.247", "port": 8443}]}}],
        "remarks": "Italy 2 🇮🇹 Durev VPN"
    },
    "Lithuania 2 🇱🇹 [Durev VPN]": {
        "outbounds": [{"protocol": "vless", "settings": {"vnext": [{"address": "51.250.84.37", "port": 8443}]}}],
        "remarks": "Lithuania 2 🇱🇹 Durev VPN"
    }
}

class MainScreen(Screen):
    """ Главный экран: запуск DPI обхода и вывод системного журнала """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Индикатор статуса
        self.status_box = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        self.status_label = Label(
            text="Система деактивирована", 
            color=get_color_from_hex(TEXT_MUTED), 
            font_size='16sp', 
            halign='left'
        )
        self.status_box.add_widget(self.status_label)
        layout.add_widget(self.status_box)
        
        # Кнопка переключения обхода
        self.btn_toggle = Button(
            text="АКТИВИРОВАТЬ ОБХОД", 
            background_normal='',
            background_color=get_color_from_hex(ACCENT_BLUE),
            font_size='16sp', bold=True,
            size_hint_y=0.15
        )
        self.btn_toggle.bind(on_press=self.toggle_bypass)
        layout.add_widget(self.btn_toggle)
        
        # Системный журнал (Логгер)
        layout.add_widget(Label(
            text="СИСТЕМНЫЙ ЖУРНАЛ (ЛОГИ):", 
            color=get_color_from_hex(TEXT_MUTED), 
            font_size='12sp', 
            size_hint_y=0.05, 
            halign='left'
        ))
        
        self.logger = TextInput(
            text="", 
            readonly=True, 
            font_name="Roboto", 
            font_size='12sp',
            background_color=get_color_from_hex(CONSOLES_BG),
            foreground_color=[1, 1, 1, 1],
            size_hint_y=0.55
        )
        layout.add_widget(self.logger)
        
        # Панель навигации
        layout.add_widget(self.create_nav_bar())
        self.add_widget(layout)

    def log_message(self, message):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.logger.text += f"[{current_time}] {message}\n"

    def toggle_bypass(self, instance):
        if not self.app.is_running:
            self.app.start_dpi_process(self)
        else:
            self.app.stop_dpi_process(self)

    def create_nav_bar(self):
        nav = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=5)
        btn1 = Button(text="Главная", background_color=get_color_from_hex(CARD_COLOR))
        btn2 = Button(text="Режимы", background_color=get_color_from_hex(SIDEBAR_COLOR), on_press=lambda x: setattr(self.manager, 'current', 'dpi'))
        btn3 = Button(text="Proxy", background_color=get_color_from_hex(SIDEBAR_COLOR), on_press=lambda x: setattr(self.manager, 'current', 'proxy'))
        btn4 = Button(text="VPN", background_color=get_color_from_hex(SIDEBAR_COLOR), on_press=lambda x: setattr(self.manager, 'current', 'vpn'))
        nav.add_widget(btn1)
        nav.add_widget(btn2)
        nav.add_widget(btn3)
        nav.add_widget(btn4)
        return nav


class DPIScreen(Screen):
    """ Экран 2: Выбор стратегий и пресетов обхода DPI """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        
        layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        layout.add_widget(Label(text="Конфигурация стратегий обхода", font_size='18sp', bold=True, size_hint_y=0.1))
        
        layout.add_widget(Label(text="Выберите режим оптимизации DPI:", color=get_color_from_hex(TEXT_MUTED), size_hint_y=0.05))
        
        # Селектор стратегий (заменяет OptionMenu из tkinter)
        self.spinner = Spinner(
            text="YouTube Fix (ALT3)",
            values=("YouTube Fix (ALT3)", "Discord & YT Full", "Alternative (Zapret)"),
            background_color=get_color_from_hex(ACCENT_BLUE),
            size_hint_y=0.1
        )
        self.spinner.bind(text=self.on_preset_change)
        layout.add_widget(self.spinner)
        
        layout.add_widget(BoxLayout(size_hint_y=0.65)) # Заглушка
        
        # Навигация назад
        btn_back = Button(text="Назад на главную", background_color=get_color_from_hex(CARD_COLOR), size_hint_y=0.1, on_press=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def on_preset_change(self, spinner, text):
        self.app.selected_preset = text


class ProxyScreen(Screen):
    """ Экран 3: Настройки Telegram Proxy """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        layout.add_widget(Label(text="Telegram Proxy MTProto", font_size='18sp', bold=True, size_hint_y=0.1))
        
        card = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=0.7)
        card.add_widget(Label(text="Сервер: 177267374371.ir.fulle7.info", color=[1,1,1,1]))
        card.add_widget(Label(text="Порт: 8443", color=[1,1,1,1]))
        
        btn_connect = Button(text="Подключить прокси в Telegram", background_color=get_color_from_hex(ACCENT_BLUE), size_hint_y=0.2)
        btn_connect.bind(on_press=self.open_tg_proxy)
        card.add_widget(btn_connect)
        layout.add_widget(card)
        
        btn_back = Button(text="Назад на главную", background_color=get_color_from_hex(CARD_COLOR), size_hint_y=0.1, on_press=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def open_tg_proxy(self, instance):
        import webbrowser
        # Генерация ссылки из оригинального кода
        webbrowser.open("https://t.me/proxy?server=177267374371.ir.fulle7.info&port=8443&secret=EERighJJvXrFGRMCIMJdCQ==")


class VPNScreen(Screen):
    """ Экран 4: Управление VPN (Xray Core) """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        layout.add_widget(Label(text="VPN Сеть (Xray Core)", font_size='18sp', bold=True, size_hint_y=0.1))
        
        self.vpn_spinner = Spinner(
            text="Italy 2 🇮🇹 [Durev VPN]",
            values=list(SELF_VPN_CONFIGS.keys()),
            background_color=get_color_from_hex(ACCENT_GREEN),
            size_hint_y=0.1
        )
        layout.add_widget(self.vpn_spinner)
        
        self.btn_vpn = Button(text="ПОДКЛЮЧИТЬ VPN", background_color=get_color_from_hex(ACCENT_GREEN), size_hint_y=0.15)
        layout.add_widget(self.btn_vpn)
        
        layout.add_widget(BoxLayout(size_hint_y=0.55))
        
        btn_back = Button(text="Назад на главную", background_color=get_color_from_hex(CARD_COLOR), size_hint_y=0.1, on_press=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(btn_back)
        self.add_widget(layout)


class BypassAndroidApp(App):
    """ Основной класс Android-приложения """
    def build(self):
        Window.clearcolor = get_color_from_hex(BG_COLOR)
        
        self.is_running = False
        self.dpi_process = None
        self.selected_preset = "YouTube Fix (ALT3)"
        
        # Определяем директорию приложения на Android для хранения бинарных файлов
        self.bin_dir = os.path.dirname(os.path.abspath(__file__))
        
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(DPIScreen(name='dpi'))
        sm.add_widget(ProxyScreen(name='proxy'))
        sm.add_widget(VPNScreen(name='vpn'))
        return sm

    def start_dpi_process(self, screen):
        screen.log_message(f"Инициализация стратегии: {self.selected_preset}")
        
        # Путь к мобильному исполняемому файлу (например, скомпилированному bye_bye_dpi под android)
        binary_path = os.path.join(self.bin_dir, "byebyedpi")
        
        # Проверяем наличие файла
        if not os.path.exists(binary_path):
            screen.log_message("[ОШИБКА] Бинарный файл 'byebyedpi' не найден в ресурсах приложения!")
            return

        try:
            # Выдаем права на исполнение файлу (критично на Android Linux-платформе)
            os.chmod(binary_path, 0o755)
            
            # Подбор аргументов под пресет
            args = [binary_path, "-e", "1", "-f", "1"]
            if "ALT3" in self.selected_preset:
                args += ["-mix"]
                
            # Запуск бинарника в фоновом процессе субпроцесса
            self.dpi_process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.is_running = True
            screen.status_label.text = "Защита активна. Трафик фильтруется"
            screen.status_label.color = get_color_from_hex(ACCENT_GREEN)
            screen.btn_toggle.text = "ОСТАНОВИТЬ ОБХОД"
            screen.btn_toggle.background_color = get_color_from_hex(ACCENT_RED)
            screen.log_message("[УСПЕШНО] Служба обхода DPI запущена.")
        except Exception as e:
            screen.log_message(f"[КРИТИЧЕСКАЯ ОШИБКА]: {str(e)}")

    def stop_dpi_process(self, screen):
        screen.log_message("Остановка процессов...")
        if self.dpi_process:
            self.dpi_process.terminate()
            self.dpi_process = None
            
        self.is_running = False
        screen.status_label.text = "Система деактивирована"
        screen.status_label.color = get_color_from_hex(TEXT_MUTED)
        screen.btn_toggle.text = "АКТИВИРОВАТЬ ОБХОД"
        screen.btn_toggle.background_color = get_color_from_hex(ACCENT_BLUE)
        screen.log_message("Обход полностью остановлен.")

    def on_stop(self):
        # Автоматическое убийство процессов при закрытии приложения
        if self.dpi_process:
            self.dpi_process.terminate()


if __name__ == "__main__":
    BypassAndroidApp().run()