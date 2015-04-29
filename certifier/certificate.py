
import argparse
import socket
import time

from datetime import datetime, timedelta

from exception import CertifierException, CertifierWarningException

from OpenSSL import SSL

# TODO: this check could be a bit more useful, as it returns codes listed
#   here; https://www.openssl.org/docs/apps/verify.html#DIAGNOSTICS
#   But for now, we're just focused on expiration
def pyopenssl_check_callback(connection, x509, errnum, errdepth, ok):
    ''' callback for pyopenssl ssl check'''

    return True

def get_expiry(host, port=443):

    try:

        # Check the DNS name
        socket.getaddrinfo(host, port)[0][4][0]

        # Connect to the host and get the certificate, keep a short timeout for
        #   infrastructure that we inevitably won't have access to.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((host, port))


        # Set up the SSL context
        ctx = SSL.Context(SSL.TLSv1_METHOD)
        verify_retval = ctx.set_verify(SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT,
                       pyopenssl_check_callback)
        ctx.set_options(SSL.OP_NO_SSLv2)

        # Make the connection get the cert
        ssl_sock = SSL.Connection(ctx, sock)
        ssl_sock.setblocking(1)
        ssl_sock.set_connect_state()
        ssl_sock.set_tlsext_host_name(host)
        ssl_sock.do_handshake()

        x509 = ssl_sock.get_peer_certificate()

        # print '********************************'
        # print dir(x509)
        # print x509.get_notAfter()
        # print x509.get_subject()
        # print x509.get_issuer()
        # print x509.has_expired()
        # print x509.get_signature_algorithm()

        if x509.has_expired():
            raise CertifierException(host, "Cert is expired!")

        # Pull the certs `notAfter` date into a datetime object
        expire_date = datetime.strptime(x509.get_notAfter(), "%Y%m%d%H%M%SZ")
        ssl_sock.shutdown()

        return expire_date

    except SSL.Error as e:
        raise
