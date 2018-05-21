import sys
import os
import platform
import time


def port_handler(port):
    if port.isdigit():
        return int(port)
    else:
        print('Недопустимое значение порта.')
        raise SystemExit


def argv_client():
    argv = sys.argv

    try:
        port = port_handler(sys.argv[1])
    except:
        raise SystemExit

    if len(argv) < 2:
        print('Введите номер порта. Доступные команды [-show-context]  [-file [путь к файлу]]')
        print('.... [номер порта] [команда]')
        raise SystemExit
    elif len(argv) == 2:
        return port, None
    elif len(argv) == 3:
        context = sys.argv[2]
        return port, context
    elif len(argv) == 4:
        context = sys.argv[2]
        path = sys.argv[3]
        if context == '-file':
            return port, context, path
        else:
            print('Неизвестная команда')


def argv_server():
    if len(sys.argv) == 2:
        port = sys.argv[1]
        if port.isdigit():
            return int(port)
        else:
            print('Недопустимое значение номера порта.')
    else:
        print('Укажите номер порта')


def param_handler(input_data, dict_pattern):
    '''Функция принимает на вход список, находит
    совпадения из контекста,
    и заменят их на необходимые параметры.'''
    if len(input_data) > 0:
        for pattern in dict_pattern:
            if pattern in input_data:
                id_pattern = input_data.index(pattern)
                input_data[id_pattern] = dict_pattern[pattern]
    else:
        input_data = 'НЕТ ВХОДНЫХ ПАРАМЕТРОВ'
    return ' '.join(input_data)


def create_dict_pattern():
    username = os.getlogin()
    sstm = platform.system()
    time_now = time.ctime()
    dict_pattern = {'{os}': sstm, '{username}': username, '{date}': time_now}
    return dict_pattern
