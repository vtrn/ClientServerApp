from socket import *
from func_param import *
from func_send_recv import *

context = [{'os'}, {'username'}, {'date'}]

def client_handler(addr):
    sockobj = socket(AF_INET, SOCK_STREAM)
    try:
        sockobj.connect(addr)
        return sockobj
    except:
        print('Нвозможно соединиться.')
        raise SystemExit

def file_hadler(file_name, sockobj):
    fragments = []
    try:
        file = open(file_name, 'r')
        lines = file.readlines()
        for line in lines:
            body = sender_handler(sockobj, line)
            fragments.append(body+'\n')
        file.close()
        return ''.join(fragments)
    except:
        print('Невозможно открыть файл.')
def dispather():
    host = ''
    port, *first = argv_client()
    if port:
        addr = (host, port)
        client = client_handler(addr)
        if first == '-show-context':
            msg = sender_handler(client, first)
            print('\n' + msg)
        elif first[0] == '-file':
            try:
                msg = file_hadler(client, first[1])
                print(msg)
            except:
                print('Не указан путь или не верен.')
        print('-' * 42, '\n' + 'Доступная команда [-show-context]')
        while True:
            msg = input('\nmsg> ')
            if not msg:
                sender_handler(client, 'STOP')
                break
            sender_handler(client, msg)
            answer = receiver_handler(client)
            print('\necho> ' + answer)
        client.close()
        print('Соединение закрыто.')

if __name__ == '__main__':
    dispather()