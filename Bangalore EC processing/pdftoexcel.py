import tabula
import pandas as pd
import re
import os
import openpyxl
wronglist=[]
#----------- Specify the folder path where files are kept(note there is \\ at end----------------------

inpath='F:\\Bangalore EC\\watermarkremovedpdf\\'
outpath='F:\\Bangalore EC\\excel\\'

#---------------------------------------------------------------------------------------------------

#All the files in the folder

filenamelist=os.listdir(inpath)
filenamelist.sort()
lenlist=len(filenamelist)

#loop over all the files
for c in range(lenlist):
    
    file=filenamelist[c][:-4]
    print (c,'---',file)
    infile=inpath+file+'.pdf'

    if (file[:4]=='Done'):
        continue
    #Reading pdf through tabula(a wrapper built on Java
    df = tabula.read_pdf(infile, encoding='utf-8', spreadsheet=True,pages='all',pandas_options={'header':None})
   
    #Writing it in excel
    outfile=outpath+file+'.xlsx'
    writer = pd.ExcelWriter(outfile)
    df.to_excel(writer,'Sheet1',index=False,header=False)
    writer.save()

    renamedfile=inpath+'Done--'+file+'.pdf'
    os.rename(infile,renamedfile)

    #opening file to check if column count is more than 9
    wb = openpyxl.load_workbook(outfile)
    sheet = wb.worksheets[0]
    column_count = sheet.max_column
    if column_count>9:
        wronglist.append(file)

#if any particular file has more than 9 columns then its name is printed
for q in wronglist:
    print ('Physically check file.There are more columns than required ',q)
