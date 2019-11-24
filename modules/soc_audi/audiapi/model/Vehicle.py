class Vehicle:
    """
    Represents a single vehicle
    """

    def __init__(self):
        self.vin = ''
        #self.csid = ''
        #self.registered = ''

    def parse(self, data):
        self.vin = data.get('VIN')
        #self.csid = data.get('CSID')
        #self.registered = data.get('registered')

    def __str__(self):
        return str(self.__dict__)


class VehiclesResponse:
    def __init__(self):
        self.vehicles = []
        """
        List of vehicles

        :type vehicles: List[Vehicle]
        """
        self.blacklisted_vins = 0

    def parse(self, data):
        response = data.get('getUserVINsResponse')
        self.blacklisted_vins = response.get('vinsOnBlacklist')
        for item in response.get('CSIDVins'):
            vehicle = Vehicle()
            vehicle.parse(item)
            self.vehicles.append(vehicle)
