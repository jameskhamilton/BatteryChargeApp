import asyncio
from project.inverterFunctions import controlMain, chargeTimes, chargeNow
from project.wallboxStatus import checkStatus

if __name__ == '__main__':

    status = checkStatus()

    if status == 'CHARGING':
        asyncio.run(controlMain(1, None)) #update the time
        asyncio.run(controlMain(0, chargeNow))
    else:    
        asyncio.run(controlMain(0, chargeTimes))
