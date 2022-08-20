import os
import shutil


mainfolder=r'F:\Bangalore EC\zip2folder'
x=os.listdir(mainfolder)
for i in range(len(x)):
    folder=os.path.join(mainfolder,x[i])
    files=os.listdir(folder)
    for file in files:
        filefrom=os.path.join(folder,file)
        newfilename=str(i)+'-'+file
        fileto=os.path.join(folder,newfilename)
        
        os.rename(filefrom,fileto)


for root, dirs, files in os.walk(mainfolder):  # replace the . with your starting directory
   for file in files:
      path_file = os.path.join(root,file)
      shutil.copy2(path_file,'F:\\Bangalore EC\\originalpdf')
