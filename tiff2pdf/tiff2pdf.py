import img2pdf
import os
folder2convert=r'C:\Python\Scripts\tif2pdf\xyz'
filelist=os.listdir(folder2convert)
for filename in filelist:
    image_file= os.path.join(folder2convert, filename)
    output_file = image_file.replace('.tif','.pdf')
    with open(output_file,"wb") as f:
       f.write(img2pdf.convert(image_file)) 
