import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import ContentStream
from PyPDF2.generic import TextStringObject, NameObject
from PyPDF2.utils import b_
import shutil

#----------- Specify the folder path where files are kept(note there is \\ at end----------------------
inpath='F:\\Bangalore EC\\originalpdf\\'
inpath2='F:\\Bangalore EC\\originalpdf2\\'
outpath='F:\\Bangalore EC\\watermarkremovedpdf\\'
wm_text = 'Only For Information'
wm_text2 = '    Draft copy'
replace_with = ''

#---------------------------------------------------------------------------------------------------

#All the files in the folder

filenamelist=os.listdir(inpath)
filenamelist.sort()
lenlist=len(filenamelist)

#loop over all the files
for c in range(lenlist):
    file=filenamelist[c]
    # Load PDF into pyPDF
    openfile = open(inpath+file, "rb")
    source = PdfFileReader(openfile)
    output = PdfFileWriter()

    # For each page
    for page in range(source.getNumPages()):
        # Get the current page and it's contents
        page = source.getPage(page)
        content_object = page["/Contents"].getObject()
        content = ContentStream(content_object, source)

        # Loop over all pdf elements
        for operands, operator in content.operations:
            # You might adapt this part depending on your PDF file for our case binary Tj operator contains watermark

            if operator == b_("Tj"):
                text = operands[0]
                if isinstance(text, TextStringObject) and (text.startswith(wm_text) or text.startswith(wm_text2)):
                    operands[0] = TextStringObject(replace_with)


        # Set the modified content as content object on the page
        page.__setitem__(NameObject('/Contents'), content)

        # Add the page to the output
        output.addPage(page)

    # Write the stream
    outputStream = open(outpath+file, "wb")
    output.write(outputStream)
    
    outputStream.close()
    print(c,file)
    
    openfile.close()
    shutil.move(inpath+file, inpath2+file)


