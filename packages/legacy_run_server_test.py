import socket
import threading
from pathlib import Path
from unittest.mock import Mock, call

from legacy_run_server import SocketListener


def send_message(path: str, msg: bytes):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(path)
        sock.sendall(msg)


def test_socket_listener_reads_bytes(tmp_path: Path):
    # setup
    socket_path = tmp_path / "socket"
    socket_path_str = str(socket_path)
    condition = threading.Condition()
    mock = Mock()

    def listener(data: bytes):
        mock(data)
        with condition:
            condition.notify()

    # execution
    socket_listener = SocketListener(socket_path, listener)
    thread = threading.Thread(target=socket_listener.handle_connections, daemon=True)
    thread.start()
    send_message(socket_path_str, b"first")
    send_message(socket_path_str, b"second")

    # evaluation
    with condition:
        condition.wait_for(lambda: mock.call_count == 2)
    socket_listener.close()
    mock.assert_has_calls([call(b"first"), call(b"second")], any_order=True)
