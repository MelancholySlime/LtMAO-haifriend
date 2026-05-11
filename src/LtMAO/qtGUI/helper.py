class Keeper:
    def __init__(self):
        pass

from PySide6.QtCore import Signal, QObject

import sys
from threading import Thread
from datetime import datetime
from time import time_ns

class SafeThread:
    cached = {}

    @staticmethod
    def check_safe(thread):
        if thread == None:
            return True
        return False

    @staticmethod
    def start(thread_name, target):
        if thread_name not in SafeThread.cached:
            SafeThread.cached[thread_name] = None
        if SafeThread.check_safe(SafeThread.cached[thread_name]):
            def cmd():
                try:
                    target()
                except:
                    import traceback
                    print(traceback.format_exc())
                SafeThread.cached[thread_name] = None
            SafeThread.cached[thread_name] = Thread(target=cmd, name=thread_name, daemon=True)
            SafeThread.cached[thread_name].start()
        else:
            print(f'{thread_name}: Error: Thread is already running, wait for it to end.')


def link_dnd_cmd(widget, dnd_cmd):
    def dragEvent(e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dropEvent(e):
        if e.mimeData().hasUrls:
            dnd_cmd([url.toLocalFile() for url in e.mimeData().urls()])
            e.accept()
        else:
            e.ignore()

    widget.setAcceptDrops(True)
    widget.dragEnterEvent = dragEvent
    widget.dragMoveEvent = dragEvent
    widget.dropEvent = dropEvent

class Log(QObject):
    logbox_signal = Signal(str)
    statusbar_signal = Signal(str)

    def __init__(self, logbox, statusbar):
        QObject.__init__(self)
        self.logbox = logbox
        self.statusbar = statusbar
        self.logbox_signal.connect(logbox.appendPlainText)
        self.statusbar_signal.connect(statusbar.showMessage)

    def write_log(self, msg):
        msg = f'🗒️ [{datetime.now().time()}] {msg}'
        self.show_statusbar(msg)
        self.write_logbox(msg)
        scrollbar = self.logbox.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def write_logbox(self, msg):
        self.logbox_signal.emit(msg)

    def show_statusbar(self, msg):
        self.statusbar_signal.emit(msg)

def link_main_window(logbox, statusbar):
    log = Log(logbox, statusbar)

    class Writer():
        def write(self, msg):
            msg = msg.strip()
            if msg:
                log.write_log(msg)

        def flush(self):
            pass

    writer = Writer()
    sys.stdout = writer
    sys.stderr = writer

def link_splash(label):
    class Writer():
        def write(self, msg):
            msg = msg.strip()
            if msg:
                label.setText('🗒️ ' + msg)
                label.repaint()

        def flush(self):
            pass

    writer = Writer()
    sys.stdout = writer
    sys.stderr = writer