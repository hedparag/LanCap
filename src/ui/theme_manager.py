import winreg
from PySide6.QtWidgets import QApplication

class ThemeManager:
    _current_mode = "system" # system, light, dark

    @classmethod
    def set_theme(cls, mode="system"):
        cls._current_mode = mode
        cls.apply_theme()

    @classmethod
    def apply_theme(cls):
        app = QApplication.instance()
        if not app:
            return

        is_dark = False
        if cls._current_mode == "dark":
            is_dark = True
        elif cls._current_mode == "system":
            is_dark = cls.is_windows_dark_mode()

        from src.ui.styles import get_light_style, get_dark_style
        
        # Apply style globally to the application
        if is_dark:
            app.setStyleSheet(get_dark_style())
        else:
            app.setStyleSheet(get_light_style())

    @classmethod
    def is_windows_dark_mode(cls):
        try:
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            reg_key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(reg_key, "AppsUseLightTheme")
            return value == 0
        except Exception:
            # Fallback to light mode if registry check fails
            return False
