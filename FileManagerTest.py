import unittest
import logging

import os
from FileManager import FileLookUpManager
 
from beans import FileInfo
logging.basicConfig(filename='test.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level= logging.DEBUG) 

class FileManagerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.dbname = "testdb"
        self.manager = FileLookUpManager(self.dbname)
        return super().setUp()

    def assertCheck(self,expected, actual):
        assert expected == actual, f'Expected {expected} actual {actual}'

    def test_createInfo(self):
        info = FileInfo('cat1','img1', 'vect1');

        assert self.manager.save(info), "Should recive possitive resp"
        info = self.manager.getById(1, True);
        assert info, "Should return info"
        self.assertCheck(info['category'], 'cat1')
        self.assertCheck(info['imageFile'], 'img1')
        self.assertCheck(info['vectorFile'], 'vect1')

    def test_searchInfo(self):
        info = FileInfo('cat1','img1', 'vect1');

        assert self.manager.save(info), "Should recive possitive resp"
        info = self.manager.performSearch('cat');
        assert info, "Should return info"
        self.assertCheck(len(info),1) 

    def test_labelLink(self):
        info = FileInfo('cat1','img1', 'vect1');
        assert self.manager.save(info), "Should recive possitive resp"
        info = self.manager.getById(1, True)
        self.assertCheck(len(info['labels']),1)
        self.manager.linkLabel(1,"label1")
        info = self.manager.getById(1, True)
        self.assertCheck(len(info['labels']),2)
        #assert 
    def test_labelUnLink(self):
        info = FileInfo('cat1','img1', 'vect1');
        assert self.manager.save(info), "Should recive possitive resp"
        info = self.manager.getById(1, True)
        self.assertCheck(len(info['labels']),1)
        self.manager.linkLabel(1,"label1")
        info = self.manager.getById(1, True)
        self.assertCheck(len(info['labels']),2)
        self.manager.unlinkLabel(1,1) 
        info = self.manager.getById(1, True)
        self.assertCheck(len(info['labels']),1)



    def tearDown(self) -> None:
        self.manager.resetDB();
        return super().tearDown()

if __name__ == '__main__':
    unittest.main()