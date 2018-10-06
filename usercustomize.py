banner = " Veky's Python ".center(78, '=')

print('/' + banner + '\\')

import sys

oldhook = sys.__interactivehook__

def newhook():
    oldhook()
    print('\\' + banner + '/')

sys.__interactivehook__ = newhook

sys.ps1, sys.ps2 = '> ', '| '
