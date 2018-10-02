# DONE: List processes.
# DONE: Stop and continue processes.
# DONE: Add Qt interface.
# DONE: Add macoS app icon.

# TODO: Add menu & hotkeys.
# TODO: Preserve selection on refresh.
# TODO: Refresh process list every time window focused.
# TODO: Split into model, view, controller.
# TODO: Package and install to /Applications.
# TODO: Filter processes by name.
# TODO: Stop process and its descendents together.
# TODO: Save process lists between sesssions.
# TODO: Understand which processes start out paused.
#       https://stackoverflow.com/questions/17005901/determine-if-process-is-paused-with-sigstop-on-os-x-with-c
#       Commit to psutil & PR.
# TODO: Port to C++.
# TODO: Port to Swift.
# TODO: Design webpages and port to Electron.


import psutil

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon


def selected_processes():
    return map(lambda item: item.proc, list_view.selectedItems())


def on_stop():
    for proc in selected_processes():
        proc.suspend()


def on_cont():
    for proc in selected_processes():
        proc.resume()


def on_refresh():
    processes = psutil.process_iter()
    processes = sorted(processes, key=lambda proc: proc.name().lower())

    list_view.clear()

    for proc in processes:
        item = QListWidgetItem(proc.name())
        item.proc = proc
        list_view.addItem(item)


def selection_changed():
    enabled = len(list_view.selectedItems()) > 0
    stop.setEnabled(enabled)
    cont.setEnabled(enabled)


# Construct GUI
app = QApplication([])
app.setApplicationName('Stopper')
app.setWindowIcon(QIcon('icon.png'))

list_view = QListWidget()
list_view.setSelectionMode(list_view.ExtendedSelection)

stop = QPushButton('Stop')
cont = QPushButton('Continue')
refresh = QPushButton('Refresh')

hbox = QHBoxLayout()
hbox.addWidget(stop)
hbox.addWidget(cont)
hbox.addWidget(refresh)
hbox.addStretch()

vbox = QVBoxLayout()
vbox.addWidget(list_view)
vbox.addLayout(hbox)

window = QWidget()
window.setWindowTitle('Stopper')
window.setLayout(vbox)

list_view.itemSelectionChanged.connect(selection_changed)
stop.clicked.connect(on_stop)
cont.clicked.connect(on_cont)
refresh.clicked.connect(on_refresh)

# Populate
on_refresh()
selection_changed()

# Show
window.show()
app.exec_()
