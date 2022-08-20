import sys, os
import pandas as pd

# filenames
##input_dir_path = 'C:\\Users\\Amit PC\\Desktop\\cre\\Bangalore Index\\ECs\\curatedexcel'
input_dir_path = r'C:\Users\Amit\Desktop\Env C'
fileext=input_dir_path.split('\\')[-1]
allfilenames = os.listdir(input_dir_path)
file=[]
for filenames in allfilenames:
    if filenames.find('.xlsx')!=-1 and filenames.find('~')==-1:
        file.append(input_dir_path+'\\'+filenames)
        print (filenames)


# read them in
excels = [pd.ExcelFile(name) for name in file]

# turn them into dataframes
frames = [x.parse(x.sheet_names[0], header=None,index_col=None) for x in excels]

# delete the first row for all frames except the first
# i.e. remove the header row -- assumes it's the first
frames[:] = [df[:] for df in frames[:]]

# concatenate them..
combined = pd.concat(frames)

# write it out
combined.to_excel(input_dir_path+"\\Combined-"+fileext+".xlsx", header=False, index=False)
