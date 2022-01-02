import subprocess
import os
from dotenv import load_dotenv
from rofi import Rofi
from pathlib import Path

class list_projects:
    
    def __init__(self):
        print("Init")

    def __clean_output(self, output):
        print(output)
        output = str(output).replace("b'","").replace("'","").split("\\n")
        return list(filter(None, output))

    def execute(self, project_root_directory):
        print(project_root_directory)
        rofi = Rofi()
        output = self.__clean_output(subprocess.check_output("ls -la " + project_root_directory + "| awk '{print $9}'" , shell=True))
        source_output_index, _ = rofi.select("Select Option", output)
        
        if source_output_index == -1:
            exit();

        subprocess.check_output("code {}{}/".format(project_root_directory,output[source_output_index]) , shell=True)