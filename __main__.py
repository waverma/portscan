from argparse import ArgumentParser

from portscan import PortScanner

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-t', help='Сканировать tcp', action='store_true')
    parser.add_argument('-u', help='Сканировать udp', action='store_true')
    parser.add_argument('-p', '--ports', type=int, nargs=2, default=[1, 65535], help='Диапазон портов')
    parser.add_argument('--host', type=str, help='Удаленный хост')
    args = parser.parse_args()

    PortScanner(args.host, args.ports, args.u, args.t).run()