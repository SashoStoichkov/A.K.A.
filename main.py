import os
import sys
from fbs_runtime.application_context import ApplicationContext

import screens
import collection
import const

if __name__ == "__main__":
    # os.chdir('/home/alex/A.K.A./src/main/python')
    col = collection.Loader(const.DB_NAME).load()
    screens.init(col)
    app = ApplicationContext()
    s = screens.StartScreen()
    s.show()
    sys.exit(app.app.exec_())
