import subprocess
import os
from rofi import Rofi
from pathlib import Path
from dotenv import load_dotenv

import sys
SCRIPTS_FOLDER = "{}/scripts/".format(os.getenv('DOTFILES_PATH'))
sys.path.append(SCRIPTS_FOLDER) 

from vscode_projects.list_projects import list_projects

def main():
  dotenv_around_path = Path(SCRIPTS_FOLDER + 'around.env')
  dotenv_path = Path(SCRIPTS_FOLDER + 'local.env')

  load_dotenv(dotenv_path=dotenv_around_path)
  load_dotenv(dotenv_path=dotenv_path)

  meet_url = os.getenv('MEET_URL')
  jira_url = os.getenv('JIRA_URL')
  project_root_directory = os.getenv('PROJECT_ROOT_DIRECTORY')

  rofi = Rofi()   
  options = ["Meetings","Go to Ticket", "My Tickets", "Code"]
  source_output_index, _ = rofi.select("Select Option", options, rofi_args=['-i'])
  
  if source_output_index == 0:
    subprocess.check_output(("google-chrome","{}landing?authuser=1".format(meet_url)))
  
  if source_output_index == 1:  
    rofi_ticket = Rofi()  
    ticket = rofi_ticket.text_entry("Ticket: ")
    subprocess.check_output(("google-chrome","{}browse/{}".format(jira_url, ticket)))

  if source_output_index == 2:
    subprocess.check_output(("google-chrome",jira_url + "browse/AMC-551?jql=resolution%20%3D%20Unresolved%20AND%20assignee%20in%20(membersOf(%22Around%20Users%22))%20AND%20assignee%20%3D%20lwitzke%20ORDER%20BY%20created%20DESC"))

  if source_output_index == 3:
    project = list_projects()
    project.execute(project_root_directory)  

if __name__ == '__main__':
  main()