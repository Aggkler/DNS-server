from dns import DNS
import socket

LOCALHOST = "localhost"
DEFAULT_PORT = 8053


def main():
    dns_server = DNS()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LOCALHOST, DEFAULT_PORT))

    try:
        while True:
            query, addr = sock.recvfrom(2048)
            rdata = dns_server.process(query)
            if rdata:
                sock.sendto(rdata, addr)
    except KeyboardInterrupt:
        dns_server.cache.save_cache("cache")
        sock.close()


if __name__ == "__main__":
    main()