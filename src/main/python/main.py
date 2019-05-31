import sys
from fbs_runtime.application_context import ApplicationContext

from start_screen import StartScreen

if __name__ == "__main__":
    app = ApplicationContext()
    s = StartScreen()
    s.show()
    sys.exit(app.app.exec_())