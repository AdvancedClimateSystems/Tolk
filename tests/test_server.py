""" :class:`tolk.Handler` doesn't have own tests because it is tested when
tests of :class:`tolk.Dispatcher` are executed.

See test coverage if you don't believe me.
"""
import socket

import pytest
import errno
from mock import Mock, patch
from tolk import Handler


class TestHandler:
    def test_handle_raise_socket_error(self):
        """
        Test if socket error has been re-raised when `errno` was
        different than `errno.EPIPE`.

        """
        mock_request = Mock()
        mock_request.sendall = Mock(side_effect=socket.error())

        with pytest.raises(socket.error) as exinfo:
            Handler(mock_request, Mock(), Mock()).handle()


    def test_handle_epipe_socket_error(self):
        """
        Test if None has been returned when 'errno' was `errno.EPIPE`.

        """
        mock_request = Mock()
        mock_request.sendall = Mock(side_effect=socket.error(errno.EPIPE, 'Raise socket error EPIPE'))

        assert Handler(mock_request, Mock(), Mock()).handle() is None
