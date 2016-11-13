# encoding utf8

import os
import re
from pathlib import Path

def date(file):
    """ un fichier récent a un st_mtime élevé """
    return file.stat().st_mtime
    
for ui in Path('.').glob('*.ui'):
    py = Path(re.sub(r'\.ui$', '.py', str(ui)))

    if py.exists() and date(ui) < date(py): # le py est + jeune : pas besoin de re-générer
        print('{} est plus récent que {}'.format(py, ui))
    else:
        cmd = 'python c:\\tools\Anaconda3\\lib\\site-packages\\pyqt4\\uic\\pyuic.py {} > {}'.format(ui, py)
        print(' !! mise à jour de {} à partir de {}'.format(py, ui))
        # print(cmd)
        os.system(cmd)
