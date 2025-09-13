import asyncio
from project.inverterFunctions import controlMain, chargeTimes, chargeNow
from project.wallboxStatus import checkStatus

def control() -> None:
    try:
        status = checkStatus()
    except Exception as e:
        print(f"Failed to get status: {e}")
        asyncio.run(controlMain(0, chargeTimes)) #set to default charge times on fail

    if status == 'CHARGING':
        asyncio.run(controlMain(1, None)) #update the time
        asyncio.run(controlMain(0, chargeNow))
    else:
        asyncio.run(controlMain(0, chargeTimes))

    return None

if __name__ == '__main__':
    control()