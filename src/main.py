from domain.event_system.event_system import EventSystem
from infrastructure.application.app import Application
from infrastructure.main_window.main_window import MainWindow


if __name__ == '__main__':
    evt_sys = EventSystem()
    main_window = MainWindow(800, 600, evt_sys)
    app = Application(main_window)

    app.run()
