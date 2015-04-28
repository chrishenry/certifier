
import argparse
import socket
import time

from datetime import datetime, timedelta

from exception import CertifierException, CertifierWarningException

from OpenSSL import SSL
PYOPENSSL = True

CA_CERTS = "/etc/ssl/certs/ca-certificates.crt"
HOST = ""

# TODO: this check could be a bit more useful, as it returns codes listed
#   here; https://www.openssl.org/docs/apps/verify.html#DIAGNOSTICS
#   But for now, we're just focused on expiration
def pyopenssl_check_callback(connection, x509, errnum, errdepth, ok):
    ''' callback for pyopenssl ssl check'''

    return True

def verify(host, days_before_expiry=60):
    global HOST

    HOST = host
    PORT = 443

    try:

        # Check the DNS name
        socket.getaddrinfo(HOST, PORT)[0][4][0]

        # Connect to the host and get the certificate
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))

        # Set up the SSL context
        ctx = SSL.Context(SSL.TLSv1_METHOD)
        verify_retval = ctx.set_verify(SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT,
                       pyopenssl_check_callback)
        ctx.set_options(SSL.OP_NO_SSLv2)

        # Make the connection get the cert
        ssl_sock = SSL.Connection(ctx, sock)
        ssl_sock.set_connect_state()
        ssl_sock.set_tlsext_host_name(HOST)
        ssl_sock.do_handshake()

        x509 = ssl_sock.get_peer_certificate()

        if x509.has_expired():
            raise CertifierException(HOST, "Cert is expired!")

        # Pull the certs `notAfter` date into a datetime object
        expire_date = datetime.strptime(x509.get_notAfter(), "%Y%m%d%H%M%SZ")

        # If today + `days_before_expiry` is after the expiry, scream.
        danger_date = datetime.now() + timedelta(days=days_before_expiry)

        if danger_date > expire_date:
            raise CertifierWarningException(HOST, "Expires on %s" % expire_date)

        return expire_date

        ssl_sock.shutdown()

    except SSL.Error as e:
        raise
