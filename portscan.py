import socket
from threading import Thread, Lock


class PortScanner:
    def __init__(self, host, port_range, udp_check_required, tcp_check_required):
        self.host = host
        self.start, self.end = port_range
        self.udp = udp_check_required
        self.tcp = tcp_check_required

        self.print_lock = Lock()

    def run(self):
        treads = []
        for port in range(self.start, self.end + 1):
            try:
                if self.udp:
                    sp = port
                    t = Thread(target=self.scan_udp, args=(sp,))
                    treads.append(t)
                    t.start()
                if self.tcp:
                    sp = port
                    t = Thread(target=self.scan_tcp, args=(sp,))
                    treads.append(t)
                    t.start()
            except KeyboardInterrupt:
                quit()

        for t in treads:
            t.join()

    def scan_tcp(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(10)
                sock.connect((self.host, port))
            with self.print_lock:
                print(f'TCP {port} {socket.getservbyport(port, "tcp").upper()}')
        except (socket.timeout, OSError, ConnectionRefusedError):
            pass
        except PermissionError:
            with self.print_lock:
                print(f'Warning: TCP {port}: permission required')

    def scan_udp(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
                sock.sendto(b'', (self.host, port))
            with self.print_lock:
                print(f'UDP {port} {socket.getservbyport(port, "udp").upper()}')
        except (socket.timeout, OSError):
            pass
        except PermissionError:
            with self.print_lock:
                print(f'Warning: UDP {port}: permission required')
