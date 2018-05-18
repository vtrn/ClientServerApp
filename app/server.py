from socket import *
from func_send_recv import *
from func_param import *


def create_server(addr):
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.bind(addr)
    sockobj.listen()
    print('Серевер запущен.')
    return sockobj


def server_handler(sockobj):
    while True:
        conn, address = sockobj.accept()
        print('Server connected by', address)
        while True:
            client_handler(conn)
            break
        break
    sockobj.close()


def client_handler(conn):
    while True:
        body = receiver_handler(conn)
        if body == '-show-context':
            show_context = ' '.join(create_dict_pattern())
            sender_handler(show_context)
        elif body == 'STOP':
            break
        else:
            context = create_dict_pattern()
            body = body.split()
            data = param_handler(body, context)
            print(data)
            sender_handler(conn, data)


def dispather():
    host = ''
    port = argv_server()
    print(port)
    if port:
        addr = (host, port)
        server = create_server(addr)
        server_handler(server)


if __name__ == '__main__':
    dispather()
