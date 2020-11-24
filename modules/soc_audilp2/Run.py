import json
import sys
from audiapi.API import API
from audiapi.Services import LogonService, CarService

def main():
    api = API()
    logon_service = LogonService(api)
    if not logon_service.restore_token():
        # We need to login
        logon_service.login(sys.argv[1], sys.argv[2])

    car_service = CarService(api)
    vehicles_response = car_service.get_vehicles()
    for vehicle in vehicles_response.vehicles:
        print(str(vehicle))
    
if __name__ == '__main__':
    main()
