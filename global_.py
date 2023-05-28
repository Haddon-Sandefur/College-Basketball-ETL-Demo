#Global variables are stored here as needed.
import os


#First run of season boolean 
#If "CBB_Links.json" is in path, return True
priorRunBoolean = os.path.isfile("cbb_Links.json")
#If "CBB_data.txt" is in path, return True
priorDataBoolean = os.path.isfile("cbb_DataRaw.txt")