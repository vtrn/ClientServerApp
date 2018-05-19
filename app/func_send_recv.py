import sys


def create_package(message):
    '''создаю кортеж для отправки'''
    size_message = str(sys.getsizeof(message)) + ':'
    package = message.encode()
    return size_message.encode(), package


def send_header(sockobj, header):
    ''' отправить заголовок'''
    sockobj.sendall(header)


def send_body(sockobj, body):
    '''отправить тело'''
    sockobj.sendall(body)


def receive_header(sockobj):
    '''принять заголовок'''
    size = 1
    size_body = ''
    while True:
        header = sockobj.recv(size)
        if ':' in header.decode():
            break
        size_body += header.decode()
    return int(size_body)


def receive_body(sockobj, size_body):
    '''прининять тело'''
    body = sockobj.recv(size_body)
    return body


def sender_handler(sockobj, message):
    ''' Создаю заголовок и тело, отправляю заголовок,
    если ответ получен, отправляю тело'''
    header, body = create_package(message)
    send_header(sockobj, header)
    send_body(sockobj, body)


def receiver_handler(sockobj):
    ''' принять заголовок, принять тело, вернуть тело '''
    header = receive_header(sockobj)
    if not header:
        sockobj.close()
    body = receive_body(sockobj, header)
    return body.decode()
