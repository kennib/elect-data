import time
import subprocess
from ftplib import FTP
import emlparse

DELAY = 90 # seconds

FEED_NAME = "results.aec.gov.au"
FEED_ID = 15508
FEED_DETAIL = "Standard"
FEED_TYPE = "Verbose"

# Setup the FTP connection
ftp = FTP(FEED_NAME)
ftp.login()
ftp.cwd("{}/{}/{}".format(FEED_ID, FEED_DETAIL, FEED_TYPE))


# Keep polling the FTP server
retrieved = set()
while True:
    most_recent = ftp.nlst()[-1]

    if most_recent not in retrieved:
        # Retrieve most recent file
        retrieved.add(most_recent)
        url = "ftp://{}/{}/{}/{}/{}".format(FEED_NAME,FEED_ID,
                                         FEED_DETAIL, FEED_TYPE, most_recent)
        subprocess.call(["curl", "--silent", url, "-o", most_recent])
        print("Retrieved", most_recent)
        # Unzip the file
        eml = subprocess.check_output(["unzip", "-Z", "-1", most_recent, "xml/*.xml"]).strip().lstrip('xml/')
        subprocess.call(["unzip", "-qq", "-jf", most_recent, "xml/*.xml"])
        print("Unzipped ", most_recent)
        # Get JSON from EML
        emlparse.eml_to_JSON(eml)
        print("To JSON  ", most_recent)
    else:
        print("Already retrieved the most recent file", most_recent)

    print("Waiting....")
    time.sleep(DELAY)
