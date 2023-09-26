import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

pasta = r'C:\Users\guilh\OneDrive\Documents\Fusion360\NCProgram'

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.nc'):
            arquivo = event.src_path
            time.sleep(1)

            with open(arquivo, 'r') as g:
                linhas = g.readlines()

            startlines = (linhas[8], 'G90 G17\n', 'G21\n', linhas[3], 'S20000 M03\n', 'G04 H3\n', linhas[14])

            endlines = ('M5\n', 'G0 Z200.\n', 'M9\n', 'M30\n')

            linhas = linhas[16 : -9]

            program = list(list(startlines) + list(linhas) + list(endlines))
  
            with open(arquivo, 'w') as g:
                g.writelines(program)

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=pasta, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
