import os
folder=r'F:\Bangalore EC\watermarkremovedpdf'
files=os.listdir(folder)
for file in files:
    if 'Done--' in file:
        filefrom=os.path.join(folder,file)
        newfilename=file.replace('Done--','').strip()
        fileto=os.path.join(folder,newfilename)
        os.rename(filefrom,fileto)
