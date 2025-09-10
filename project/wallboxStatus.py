from wallbox import Wallbox, Statuses
import os
import json
import time

def secrets() -> tuple:
    """
    Returns:
    username, password
    """
    directoryFolder = 'credentials'
    inverterFile = 'wallboxConfig.json'
    scriptDirectory = os.path.dirname(os.path.abspath(__file__))
    parentDirectory = os.path.abspath(os.path.join(scriptDirectory, os.pardir))

    filePath = os.path.join(parentDirectory, directoryFolder, inverterFile)

    with open(filePath, 'r') as file:
        securityData = json.load(file)

    username = securityData['Username']
    password = securityData['Password']
    charger_id = securityData['Charger_Id']

    return username, password, charger_id

def checkStatus() -> str:
    """
    Returns:
    - Wallbox charger status
    """
    username,password,charger_id = secrets()

    wallbox_client = Wallbox(username, password)
    wallbox_client.authenticate()
    time.sleep(15) #times out if we make too many client calls - 3 in a row is too many!

    # Retrieve the list of chargers
    # chargers = wallbox_client.getChargersList()
    # if not chargers:
    #     raise Exception("No chargers found for this account.")

    # charger_id = chargers[0]
    # print(charger_id)    

    # Fetch the status of the charger
    charger_status = wallbox_client.getChargerStatus(charger_id)

    print(Statuses(charger_status['status_id']).name)
    return Statuses(charger_status['status_id']).name

if __name__ == '__main__':
    checkStatus()