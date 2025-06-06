import hashlib
import hmac
import base64
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import http.client
import json
import os

url = 'www.soliscloud.com'
port = '13333'
apiMethod = 'POST'

def secrets() -> tuple:
    """
    Returns:
     
    keyId, secretKey, stationId, password, username, inverterSn, inverterId
    """
    directoryFolder = 'credentials'
    inverterFile = 'inverterConfig.json'
    scriptDirectory = os.path.dirname(os.path.abspath(__file__))
    parentDirectory = os.path.abspath(os.path.join(scriptDirectory, os.pardir))

    filePath = os.path.join(parentDirectory, directoryFolder, inverterFile)

    with open(filePath, 'r') as file:
        securityData = json.load(file)

    keyId = securityData['Key Id']
    secretKey = securityData['Secret Key'].encode('utf-8') #bytes literal
    stationId = securityData['Station Id']
    password = securityData['Password']
    username = securityData['Username']
    inverterSn = securityData['Inverter SN']
    inverterId = securityData['Inverter Id']

    return keyId, secretKey, stationId, password, username, inverterSn, inverterId

def contentType() -> str:
    return 'application/json'

def currentDateTime(format: int) -> str:
    """
    Parameters:
    - 0 (int) to return the authentication format
    - 1 (int) to return the update format
    """
    utc_time = datetime.now(timezone.utc)
    now = utc_time.astimezone(ZoneInfo("Europe/London"))
    dttime = None
    if format == 0:
        dttime = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    elif format == 1:
        dttime = now.strftime("%Y-%m-%d %H:%M:%S")
    else:
        raise ValueError("Incorrect (int) value passed to currentDateTime(): {format}\nExpected values are 0,1")
    return dttime

def base64Hash(bodyValue: str) -> str:
    hashValue = base64.b64encode(hashlib.md5(bodyValue.encode('utf-8')).digest()).decode('utf-8')
    return hashValue

def hexMD5(passwordValue: str) -> str:
    hexValue = hashlib.md5(passwordValue.encode('utf-8')).hexdigest()
    return hexValue

def hmacEncrypt(secretKeyValue: str, encryptStrValue: str) -> str:
    h = hmac.new(secretKeyValue, msg=encryptStrValue.encode('utf-8'), digestmod=hashlib.sha1)
    sign = base64.b64encode(h.digest()).decode('utf-8')
    return sign

def authValue(keyIdValue: str, secretKeyValue:str, bodyValue: str, resourceValue: str) -> str:
    """
    Returns:
    - authentication string
    """
    dttime = None
    try: 
        dttime = currentDateTime(0)
    except ValueError as e:
        print(e)

    encryptStr = (apiMethod + "\n"
        + base64Hash(bodyValue) + "\n"
        + contentType() + "\n"
        + dttime + "\n"
        + resourceValue)
    auth = "API " + keyIdValue + ":" + hmacEncrypt(secretKeyValue, encryptStr)
    return auth

async def solisAPICall(resourceValue: str, bodyValue: str, headerValue: str) -> json:
    """
    Parameter:
    - resource path
    - http request body
    - http request header

    Returns:
    - JSON string
    """
    try:
        conn = http.client.HTTPSConnection(url, port)
        conn.request(apiMethod, resourceValue, bodyValue, headerValue)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        data = data.replace(',\n  }','}') #the json result is broken!
        if response.code >= 400:
            print(f'Error: {response.code} - {data}')
        else:
            return json.loads(data) 
    except http.client.HTTPException as e:
        print(f'Error: {e}')
    finally:
        conn.close()