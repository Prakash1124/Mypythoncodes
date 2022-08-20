import os
import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
import re

#----------- Specify the folder path where files are kept(note there is \\ at end----------------------

input_path='F:\\Bangalore EC\\excel\\'
output_path='F:\\Bangalore EC\\curatedexcel\\'

#-------------------------------------------------------------------------------------------------------

#All the files in the folder
filenamelist=os.listdir(input_path)
filenamelist.sort()
lenlist=len(filenamelist)

#loop over all the files
for c in range(lenlist):
    input_file=filenamelist[c]
    #prints the current file name being processed
    print (c,input_file)
    if (input_file[:9]=='Converted'):
        continue
    #slight code to check if file in list a redundant one
    if input_file.find('.xlsx')!=-1 and input_file.find('~')==-1:
        input_file=input_file[:input_file.find('.xlsx')]
        output_file=input_file+ '- done'


        fromfile=input_path+input_file+'.xlsx'
        renamedfile=input_path+'Converted - '+input_file+'.xlsx'
        tofile=output_path+output_file+'.xlsx'
        strtrow=5

        df = pd.DataFrame({'A' : []})
        df1 = pd.DataFrame({'A' : []})
        #reading file into dataframe and removing the header carried from pdf
        df=pd.read_excel(
            fromfile,    # name of excel sheet
            names=['A','B','C','D','E','F','G','H','I'],       # new column header
            skiprows=range(strtrow-3),   # list of rows you want to omit at the beginning
            usecols='A:I'       # columns to parse (note the excel-like syntax)
        )

        if len(df['A'])==0:
            continue
        
        #filling all blank cells in first columns with preceding value
        df['A']=df['A'].ffill()
        
        #remove any text from date column
        df['C'] = df['C'].str.replace('[^\0-9]', '')
        df['C'] = df['C'].str.strip()

        #converting rest all to text
        df = df.fillna('')
        for xc in 'BCDEFGHI':
            df[xc]=df[xc].astype(str)

        #concatenating the rows of table
        df1=df.groupby(['A']).agg(lambda x: ' '.join(x)).reset_index()

        #replace any character from date
        df1['C']=df1['C'].replace('n','', regex=True)
        df1['C']=df1['C'].replace('l','', regex=True)
        df1['C']=df1['C'].replace('r','', regex=True)
        df1['C']=df1['C'].str.strip()
        df1['C'] = pd.to_datetime(df1['C'],format='%d/%m/%Y', errors='coerce')

        #change the second last column of pdf to numeric
        df1['H'] = pd.to_numeric(df1['H'])

        #replace any type of carraige return so that data becomes congruent
        df1 = df1.replace(r'\n',' ', regex=True)
        df1 = df1.replace(r'\r',' ', regex=True)

        #replace consecutive spaces with just 1
        df1.B = df1.B.replace('\s+', ' ', regex=True)

        #extract article name
        df1['J'] = df1['D'].str.extract(r'Article Name:(.*?)Market', expand=False)
        df1['J'] = df1['J'].str.strip()

        #extract market value
        df1['K'] = df1['D'].str.extract(r'Market Value:(.*?)Consideration Amount', expand=False)
        df1['K'] = df1['K'].str.replace(r'[^\d+]','',regex=True)
        df1['K'] = pd.to_numeric(df1['K'])

        #extract consideration amount
        df1['L'] = df1['D'].str.split('Consideration Amount:', expand=False)
        df1['L'] = df1['L'].str[-1]
        df1['L'] = df1['L'].str.replace(r'[^\d+]','',regex=True)
        df1['L'] = pd.to_numeric(df1['L'])

        #extracting the note
        df1['AB'], df1['S'] = df1['B'].str.split('Note:', 1).str
        df1['AB'] = df1['AB'].str.strip()
        df1['S'] = df1['S'].str.strip()

        #extract property description
        df1['AC'], df1['AD'] = df1['AB'].str.split('Property Schedule Description:', 1).str
        df1['AD'] = df1['AD'].str.strip()
        df1['AC'] = df1['AC'].str.strip()

##        #replacing directions with its correct spelling
##        df1['AD']=df1['AD'].str.replace(r'\[(L.*?K)\]','[LAND MARK]',regex=True)
##        df1['AD']=df1['AD'].str.replace(r'\[(E.*?T)\]','[EAST]',regex=True)
##        df1['AD']=df1['AD'].str.replace(r'\[(W.*?T)\]','[WEST]',regex=True)
##        df1['AD']=df1['AD'].str.replace(r'\[(N.*?H)\]','[NORTH]',regex=True)
##        df1['AD']=df1['AD'].str.replace(r'\[(S.*?H)\]','[SOUTH]',regex=True)

        #finding the directional property details
        df1['AE'] = df1['AD'].str.extract(r'LAND MARK(.*?)EAST', expand=False).str[1:-1]
        df1['O'] = df1['AD'].str.extract(r'EAST(.*?)WEST', expand=False).str[1:-1]
        df1['P'] = df1['AD'].str.extract(r'WEST(.*?)SOUTH', expand=False).str[1:-1]
        df1['Q'] = df1['AD'].str.extract(r'SOUTH(.*?)NORTH', expand=False).str[1:-1]
        df1['R'] = df1['AD'].str.extract(r'NORTH(.*?)', expand=False).str[1:]
       

        df1['O'] = df1['O'].str.strip()
        df1['P'] = df1['P'].str.strip()
        df1['Q'] = df1['Q'].str.strip()
        df1['R'] = df1['R'].str.strip()
        df1['AE'] = df1['AE'].str.strip()


        #seperating the location from its kannada equivalent
        df1['T'] = df1['AC'].replace(r'[^\x00-\x7F]+','$', regex=True)
        df1['U'] = df1['T'].str.split('$').str[-1]
        df1['U'] = df1['U'].str.lstrip('!@#$^&%*()+=-[]\/{}|:<>?').str.strip()

        #filename as per database
        df1['V'],df1['AF'] = df1['I'].str.split('-',1).str
        df1['AG'],df1['Z'] = df1['AF'].str.rsplit('-',1).str
        df1['AH'],df1['Y'] = df1['AG'].str.rsplit('-',1).str
        df1['AI'],df1['X'] = df1['AH'].str.rsplit('-',1).str
        df1['W']=df1['AI'].str.replace('-','')
        df1['AA']=df1['V']+df1['W']+'-'+df1['X']+'-'+df1['Y']+df1['Z']
        df1['I'] = df1['I'].str.strip()

        #arranging the dataframe
        df1=df1[['C','U','I','AE','O','P','Q','R','S','J','K','L','E','F','G','H','AA']]

        #saving the file
        writer = ExcelWriter(tofile)
        df1.to_excel(writer,'Sheet1',index=False,header=False)
        writer.save()

        #printing the loaction name for manual check
        st=set(df1['U'])
        print(st)

        #renaming the file which has been converted
        os.rename(fromfile,renamedfile)

        
