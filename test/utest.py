import unittest
import os
import platform
from threading import Thread

import config
import app.client
import app.server
import app.func_send_recv


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        addServer = ('', 0)
        cls.server = app.server.create_server(addServer)
        print(cls.server)
        Thread(target=app.server.server_handler, args=(cls.server)).start()
        addrClient = (cls.server.getsockname())
        cls.client = app.client.client_handler(addrClient)

    @classmethod
    def tearDownClass(cls):
        cls.client.close()

    def test(self):
        msg = 'Скрипт запущен на {os} от имени {username}'
        app.func_send_recv.sender_handler(self.client, msg)
        expectedMsg = 'Скрипт запущен на {} от имени {}'.format(platform.system(), os.getlogin())
        result = app.func_send_recv.receiver_handler(self.client)
        self.assertEqual(expectedMsg, result)


if __name__ == '__main__':
    unittest.main()
