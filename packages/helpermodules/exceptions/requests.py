from requests import HTTPError
from requests.exceptions import ConnectionError

from helpermodules.exceptions.registry import ExceptionRegistry


def handle_connection_error(e: ConnectionError):
    return "Die Verbindung zum Server {} ist fehlgeschlagen. Überprüfe Adresse und Netzwerk.".format(e.request.url)


def handle_http_error(e: HTTPError):
    code = e.response.status_code
    if 400 <= code < 500:
        if code == 401:
            return "HTTP 401: Authentifizierung fehlgeschlagen. Überprüfe die Zugangsdaten"
        return "HTTP {}: Client-Fehler. Überprüfe die Konfiguration.".format(code)
    if 500 <= code < 600:
        return "HTTP {}: Server-Fehler. Versuche es später erneut.".format(code)
    return "HTTP {}: Unbekannter Fehler an Host {}".format(code, e.request.url)


def register_request_exception_handlers(registry: ExceptionRegistry) -> None:
    registry.add(ConnectionError, handle_connection_error)
    registry.add(HTTPError, handle_http_error)
