import sys
from fbs_runtime.application_context import ApplicationContext

import screens

if __name__ == "__main__":
    app = ApplicationContext()
    s = screens.StartScreen()
    s.show()
    sys.exit(app.app.exec_())