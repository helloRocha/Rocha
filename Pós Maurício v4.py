import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

pasta = r'C:\Users\guilh\OneDrive\Documents\Fusion360\NCProgram'

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.txt'):
            arquivo = event.src_path
            time.sleep(1)

            with open(arquivo, 'r') as g:
                linhas = g.readlines()

                tem_compensacao = False

                for linha in linhas:
                    if 'G83' in linha:
                        tem_compensacao = True
                        break

                if tem_compensacao:

                    inifu = linhas[5].split()
                
                    rotfu = linhas[11].split()

                    ciclo = linhas[13].split()
                    
                    avanço = int(ciclo[5].replace('F', '').replace('.', ''))

                    avanço100 = avanço / 100

                    avançostr = str(avanço100)


                    program = (linhas[0], ';' + linhas[1], 'G99\n', 'G54\n',
                    'T00\n', (inifu[1] + ' ' + inifu[2] + ' ' + inifu[3] + '\n'),
                    '\n', ';' + linhas[7], linhas[8], 'M6\n', linhas[10], rotfu[0] + '\n', 
                    (rotfu[1] + ' ' + rotfu[2] + '\n'), linhas[12], ('G74 ' + ciclo[2] + ' ' + (ciclo[4].replace('Q', 'W') + ' ' + ('F' + avançostr )) + '\n'),
                    linhas[15], '\n', linhas[17], 'G54\n', 'T00\n', (inifu[1] + ' ' + inifu[2] + ' ' + inifu[3] + '\n'),
                    'M30\n', '%' )

                else:

                    tem_compensacao = False

                    for linha in linhas:
                            if 'G42' in linha or 'G41' in linha:
                             tem_compensacao = True
                             break

                    if tem_compensacao:
                        aprox = (linhas[5]).split()

                        rot = (linhas[11]).split()

                        lrotu = (linhas[13]).split()

                        lvc = (linhas[14]).split()

                        comp = (linhas[18]).split()


                        startlines = (linhas[0], (';' + linhas[1]), 'G99\n', 'G54\n', 'T00\n',(aprox[1] + ' ' + aprox[2] + ' ' + aprox[3]),
                        '\n', (';' + linhas[7]) , '\n', linhas[8], 'M6\n', linhas[10], rot[0] + '\n', (rot[1] + ' ' + rot[2] + '\n'), 
                        linhas [12], ('G92' + ' ' + lrotu[1] + ' ' + 'M3' + '\n' ), lvc[0] + '\n', lvc[1] + '\n', linhas[15], linhas[16],
                        linhas[17], (comp[0] + '\n'), (comp[1] + ' ' + comp[2] + '\n'))

                        endlines = (rot[0] + '\n', (rot[1] + ' ' + rot[2] + '\n'), '\n', 'M9\n', 'G54\n', 'T00\n', 
                        (aprox[1] + ' ' + aprox[2] + ' ' + aprox[3] + '\n'), 'M30\n', '%')

                        linhas = linhas[19 : -6]

                        program = list(list(startlines) + list(linhas) + list(endlines))
                    
                    else:
                        aprox = (linhas[5]).split()

                        rot = (linhas[11]).split()

                        lrotu = (linhas[13]).split()
            
                        lvc = (linhas[14]).split()


                        startlines = (linhas[0], (';' + linhas[1]), 'G99\n', 'G54\n', 'T00\n',(aprox[1] + ' ' + aprox[2] + ' ' + aprox[3]),
                        '\n', (';' + linhas[7]) , '\n', linhas[8], 'M6\n', linhas[10], rot[0] + '\n', (rot[1] + ' ' + rot[2] + '\n'), linhas [12], 
                        ('G92' + ' ' + lrotu[1] + ' ' + 'M3' + '\n' ), lvc[0] + '\n', lvc[1] + '\n', linhas[15])

                        endlines = (rot[0] + '\n', (rot[1] + ' ' + rot[2] + '\n'), '\n', 'M9\n', 'G54\n', 'T00\n', 
                        (aprox[1] + ' ' + aprox[2] + ' ' + aprox[3] + '\n'), 'M30\n', '%')

                        linhas = linhas[16 : -6]

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