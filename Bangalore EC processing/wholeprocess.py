import subprocess
subprocess.call("removeAcap.py", shell=True)
subprocess.call("watermarkremover.py", shell=True)
subprocess.call("pdftoexcel.py", shell=True)
subprocess.call("exceltocuratedexcel.py", shell=True)
subprocess.call("combinecuratedxlsx.py", shell=True)
