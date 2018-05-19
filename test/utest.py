import unittest
import os
import platform
from threading import Thread
import time

import sys

sys.path.append('..')

from app  import client
from app import server
from app import func_send_recv


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        addServer = ('', 0)
        cls.server = server.create_server(addServer)
        Thread(target=server.server_handler, args=(cls.server,)).start()
        addrClient = (cls.server.getsockname())
        time.sleep(.1)
        cls.client = client.client_handler(addrClient)

    @classmethod
    def tearDownClass(cls):
        cls.client.close()

    def testSimple(self):
        msg = 'Скрипт запущен на {os} от имени {username}'
        func_send_recv.sender_handler(self.client, msg)
        expectedMsg = 'Скрипт запущен на {} от имени {}'.format(platform.system(), os.getlogin())
        result = func_send_recv.receiver_handler(self.client)
        self.assertEqual(expectedMsg, result)

    def testShowContext(self):
        msg = '-show-context'
        func_send_recv.sender_handler(self.client, msg)
        expectedMsg = '{os} {username} {date}'
        result = func_send_recv.receiver_handler(self.client)
        self.assertEqual(expectedMsg, result)

    def testLongMessage(self):
        msg = 'hard message' * 1024
        func_send_recv.sender_handler(self.client, msg)
        expectedMsg = 'hard message' * 1024
        result = func_send_recv.receiver_handler(self.client)
        self.maxDiff = None
        self.assertEqual(expectedMsg, result)

    def testFile(self):
        self.maxDiff = None
        try:
            string = """Из ржавой ванны, как из гроба жестяного,"""
            name_file = 'test.txt'
            file = open(name_file, 'w')
            for line in range(5):
                file.write(string)
            file.close()
            expectedMsg = """Из ржавой ванны, как из гроба жестяного,""" * 5
            result = client.file_hadler(name_file, self.client)
            self.assertEqual(expectedMsg, result)
        finally:
            os.remove(name_file)





if __name__ == '__main__':
    unittest.main()
