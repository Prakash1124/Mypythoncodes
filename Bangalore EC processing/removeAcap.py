import os
path='F:\\Bangalore EC\\originalpdf\\'
x=os.listdir(path)
y="Â"


for i in range(len(x)):
    fromfile=path+x[i]
    if y in x[i]:
        z=x[i].replace(y,'')
        tofile=path+z
        os.rename(fromfile,tofile)
