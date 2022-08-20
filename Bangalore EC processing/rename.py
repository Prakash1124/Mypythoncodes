import os
folder1=r'F:\Bangalore EC\watermarkremovedpdf'
folder2=r'F:\Bangalore EC\excel'
files1=os.listdir(folder1)
files2=os.listdir(folder2)
files3=[]
for file in files2:
    filex=file.replace('.xlsx','.pdf')
    files3.append(filex)
for file in files1:
    if file in files3:
        filefrom=os.path.join(folder1,file)
        newfilename='Done--'+file
        fileto=os.path.join(folder1,newfilename)
        os.rename(filefrom,fileto)
