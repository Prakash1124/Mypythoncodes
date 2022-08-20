
toremovefolders=['F:\\Bangalore EC\\originalpdf2',
                 'F:\\Bangalore EC\\watermarkremovedpdf',
                 'F:\\Bangalore EC\\excel',
                 'F:\\Bangalore EC\\curatedexcel']


import os
import glob
for folder in toremovefolders:
    files = glob.glob(folder+'\\*')
    for f in files:
        os.remove(f)
