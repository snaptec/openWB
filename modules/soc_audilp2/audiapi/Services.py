from abc import abstractmethod, ABCMeta

from audiapi.API import Token, API
from audiapi.model.Vehicle import VehiclesResponse, Vehicle

class Service(metaclass=ABCMeta):
    BASE_URL = 'https://msg.audi.de/fs-car'
    COMPANY = 'Audi'
    COUNTRY = 'DE'

    def __init__(self, api: API):
        self._api = api
        """
        API for communicating

        :type _api: API
        """

    def url(self, part, **format_data):
        """
        Builds a full URL using the given parts

        :param part URL part which should be added at the end
        :param format_data: Format arguments
        :return: URL
        :rtype: str
        """
        url = self.BASE_URL + '/' + self._get_path()
        if self._use_company():
            url += '/' + self.COMPANY + '/' + self.COUNTRY
        url += part
        return url.format(**format_data)

    def _use_company(self):
        return True

    @abstractmethod
    def _get_path(self):
        """
        Returns the url path for this service

        :return: URL path
        :rtype: str
        """
        pass


class VehicleService(Service, metaclass=ABCMeta):
    def __init__(self, api: API, vehicle: Vehicle):
        super().__init__(api)
        self._vehicle = vehicle
        """
        Current vehicle

        :type _vehicle: Vehicle
        """

    def url(self, part, **format_data):
        return super().url(part, **format_data, vin=self._vehicle.vin)


class AuthorizationService(Service):
    """
    Auth flow (?):
    --service, operation-->
    <--PinAuthInfoResponse--
    --  PinChallenge    --> (?)
    ....

    Complete:
    PinChallenge+data -- CompleteAuthenticationRequest -->
    """

    def request_auth(self, vehicle: Vehicle, service: str, operation: str):
        headers = {'Content-Length': '0', 'Content-Type': 'application/json; charset=UTF-8'}
        url = self.url('/vehicles/{vin}/services/{service}/operations/{operation}/request',
                       vin=vehicle.vin, service=service, operation=operation)

        data = {}  # Yes send empty data - no idea why
        return self._api.put(url, data=data, headers=headers)

    def complete_auth(self):
        """
        Completes the auth request
        """
        data = {}
        return self._api.post(self.url('/complete'), data)

    def _get_path(self):
        return 'rolesrights/authorization/v1'


class CarFinderService(VehicleService):
    """
    Requires special permissions - might be for rental car companies
    """

    def find(self):
        """
        Returns the position of the car
        """
        return self._api.get(self.url('/vehicles/{vin}/position'))

    def _get_path(self):
        return 'bs/cf/v1'


class CarService(Service):
    def get_vehicles(self):
        """
        Returns all cars registered for the current account

        :return: VehiclesResponse
        :rtype: VehiclesResponse
        """

        data = self._api.get(self.url('/vehicles'))
        response = VehiclesResponse()
        response.parse(data)
        return response

    def get_vehicle_data(self, vehicle: Vehicle):
        """
        Returns the vehicle data for the given vehicle

        :param vehicle: Vehicle with CSID
        :return: Vehicle data
        """
        return self._api.get(self.url('/vehicle/{csid}'.format(csid=vehicle.csid)))

    def _get_path(self):
        return 'myaudi/carservice/v2'


class ClimateService(Service):
    def _get_path(self):
        return 'bs/rs/v1'


class DiebstahlwarnanlageService(Service):
    def _get_path(self):
        return 'bs/dwap/v1'


class GeofenceService(Service):
    """
    USA only - Restrict car area
    """

    def _get_path(self):
        return 'bs/geofencing/v1'


class LockUnlockService(VehicleService):
    """
    Locks and unlocks the car
    """

    def get_actions(self):
        """
        Returns all available actions
        """
        return self._api.get(self.url("/vehicles/{vin}/actions"))

    # TODO: Lock and unlock request

    def _get_path(self):
        return 'bs/rlu/v1'


class LogonService(Service):
    """
    General API logon service
    """

    def login(self, user: str, password: str, persist_token: bool = True):
        """
        Creates a new session using the given credentials

        :param user: User
        :param password: Password
        :param persist_token: True if the token should be persisted in the file system after login
        """
        token = self.__login_request(user, password)
        self._api.use_token(token)
        if persist_token:
            token.persist()

    def restore_token(self):
        """
        Tries to restore the latest persisted auth token

        :return: True if token could be restored
        :rtype: bool
        """
        token = Token.load()
        if token is None or not token.valid():
            return False
        self._api.use_token(token)
        return True

    def __login_request(self, user: str, password: str):
        """
        Requests a login token for the given user

        :param user: User
        :param password: Password
        :return: Token
        :rtype: Token
        """
        data = {'grant_type': 'password',
                'username': user,
                'password': password}
        reply = self._api.post(self.url('/token'), data, use_json=False)
        return Token.parse(reply)

    def _get_path(self):
        return 'core/auth/v1'


class MobileKeyService(Service):
    """
    Manages keyless access for the car
    """

    def _get_path(self):
        return '// Not implemented in MMI app'


class OperationListService(VehicleService):
    """
    Provides access to all permissions one can set for telemetrics and MMI (connect).
    This will also tell you how long your licences are valid,
    and when the service reaches it's final EOL date
    """

    def get_operations(self):
        """
        Returns all services available and their license status
        """
        return self._api.get(self.url('/vehicles/{vin}/operations'))

    def _get_path(self):
        return 'rolesrights/operationlist/v2'


class PictureNavigationService(VehicleService):
    def get_all(self):
        # Returns 404 for some reason - might need to wireshark the correct path
        return self._api.get(self.url('/vehicles/{vin}/all'))

    def _get_path(self):
        return 'audi/b2c/picturenav/v1'


class PoiNavigationService(Service):
    def _get_path(self):
        return 'audi/b2c/poinav/v1'


class OnlineDestinationsService(VehicleService):
    def get_pois(self):
        return self._api.get(self.url('/vehicles/{vin}/pois'))

    def _get_path(self):
        return ''  # TODO



class PushNotificationService(Service):
    """
    Registers push notifications (of some sort)
    """

    PLATFORM_GOOGLE = 'google'
    APP_ID = 'de.audi.mmiapp'

    def register(self, platform: str, app_id: str, token: str):
        """
        Registers a push notification service
        :param platform: Platform
        :param app_id: App ID
        :param token: Google messaging service token
        :return:
        """
        self._api.post(self.url('/subscriptions/{platform}/{app_id}/{token}', platform=platform, app_id=app_id,
                                token=token), data={})

    def _get_path(self):
        return 'fns/subscription/v1'


class RemoteBatteryChargeService(Service):
    """
    For EV only - timer for choosing when the battery should be charged
    """

    def _get_path(self):
        return 'bs/batterycharge/v1'

class UserInfoService(Service):
    """
    General user information
    """

    def get_info(self):
        return self._api.get(self.url('/userInfo'))

    def _get_path(self):
        return 'core/auth/v1'


class UserManagementService(VehicleService):
    """
    Manages car pairing stuff
    """

    def get_paring_status(self):
        return self._api.get(self.url('/vehicles/{vin}/pairing'))

    def _get_path(self):
        return 'usermanagement/users/v1'


class ValetAlertService(Service):
    """
    USA only - Alerting for invalid car usage
    """

    def get_alerts(self):
        return self._api.get(self.url('/vehicles/{vin}/valetAlerts'))

    def get_definition(self):
        return self._api.get(self.url('/vehicles/{vin}/valetAlertDefinition'))

    def get_request_status(self, request_id: str):
        return self._api.get(self.url('/vehicles/{vin}/valetAlertDefinition/{id}/status', id=request_id))

    def set_definition(self, definition):
        # TODO: Implement definition
        return self._api.post(self.url('/vehicles/{vin}/valetAlertDefinition', data={}))

    def _get_path(self):
        return 'bs/valetalert/v1'


class VehicleManagementService(VehicleService):
    """
    Information about the vehicle management system
    """

    def get_information(self):
        """
        Returns information about the connection system of the vehicle
        (such as embedded sim)
        """
        return self._api.get(self.url('/vehicles/{vin}'))

    def _get_path(self):
        return 'vehicleMgmt/vehicledata/v2'


class VehicleStatusReportService(VehicleService):
    """
    General status of the vehicle
    """

    def get_request_status(self, request_id: str):
        """
        Returns the status of the request with the given ID

        :param request_id: Request ID
        :return: RequestStatus
        :rtype: RequestStatus
        """
        data = self._api.get(self.url('/vehicles/{vin}/requests/{request_id}/jobstatus', request_id=request_id))
        return RequestStatus(data)

    def get_requested_current_vehicle_data(self, request_id: str):
        """
        Returns the vehicle report of the request with the given ID

        :param request_id: Request ID
        :return: VehicleDataResponse
        :rtype: VehicleDataResponse
        """
        data = self._api.get(self.url('/vehicles/{vin}/requests/{request_id}/status', request_id=request_id))
        return VehicleDataResponse(data)

    def request_current_vehicle_data(self):
        """
        Requests the latest report data from the vehicle

        :return: CurrentVehicleDataResponse
        :rtype: CurrentVehicleDataResponse
        """
        data = self._api.post(self.url('/vehicles/{vin}/requests'))
        return CurrentVehicleDataResponse(data)

    def get_stored_vehicle_data(self):
        """
        Returns the last vehicle data received

        :return: VehicleDataResponse
        :rtype: VehicleDataResponse
        """
        data = self._api.get(self.url('/vehicles/{vin}/status'))
        return VehicleDataResponse(data)

    def _get_path(self):
        return 'bs/vsr/v1'
