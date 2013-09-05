import time
import subprocess
from ftplib import FTP
import emlparse

DELAY = 90 # seconds

FEED_NAME = "results.aec.gov.au"
FEED_ID = 15508
FEED_PRELOAD= "Preload"
FEED_DETAIL = "Standard"
FEED_TYPE = "Verbose"

# Fetches files from the AEC FTP site
# takes a list of files to extract from the most recent zip in the given directory
# takes a list of excluded files not to download
# takes a boolean for vebosity of logging messages
def fetch_files(dir, files=None, types=None, excluded=None, verbose=True):
  if files == None: files = []
  if types == None: types = ["media feed"]*len(files)
  if excluded == None: excluded = []
  
  # Get the name of the most recent file in the gven directory
  most_recent = ftp.nlst()[-1]
  
  # Download it if it is not excluded
  if most_recent not in excluded:
    url = "ftp://{}/{}/{}/{}".format(FEED_NAME, FEED_ID, dir, most_recent)
    subprocess.call(["curl", "--silent", url, "-o", most_recent])
    if verbose:
      print("Retrieved", most_recent)
    # Unzip the file
    eml_files = subprocess.check_output(["unzip", "-Z", "-1", most_recent]+files).splitlines()
    eml_files = [eml.split('/')[-1] for eml in eml_files]
    subprocess.call(["unzip", "-qq", "-jn", most_recent]+files)
    if verbose:
      print("Unzipped ", most_recent)
    # Get JSON from EML
    for eml, type in zip(eml_files, types):
      print("Parsing  ", eml, type)
      emlparse.eml_to_JSON(eml, type)
    if verbose:
      print("To JSON  ", eml_files)
  else:
    if verbose:
      print("Already retrieved the most recent file", most_recent)
  
  if verbose:
    print()
  
  return most_recent

# Setup the FTP connection
ftp = FTP(FEED_NAME)
ftp.login()


# Fetch preload data
ftp.cwd("/{}/{}/{}/".format(FEED_ID, FEED_DETAIL, FEED_PRELOAD))
dir = "{}/{}".format(FEED_DETAIL, FEED_PRELOAD)
fetch_files(dir, files=["xml/eml-*-candidates-*.xml", "xml/eml-*-event-*.xml"],
                 types=["candidates", "electorates"])


# Keep polling the FTP server
ftp.cwd("/{}/{}/{}/".format(FEED_ID, FEED_DETAIL, FEED_TYPE))
retrieved = set()
while True:
  # Fetch the latest results
  dir = "{}/{}".format(FEED_DETAIL, FEED_TYPE)
  new_file = fetch_files(dir, files=["xml/*.xml"], types=["media feed"], excluded=retrieved)
  retrieved.add(new_file)
  
  # Wait a while before fetching the next set of results
  print("Waiting....")
  time.sleep(DELAY)
