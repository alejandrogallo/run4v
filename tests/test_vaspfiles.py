from common import * 
import unittest 

run4v.VERBATIM = False

class TestVaspFile(unittest.TestCase):
    def setUp(self):
        self.fileName = "TEST_VASPFILE"
        self.autogen = False
        self.vaspFile = run4v.VASPFile(fileName = self.fileName, autogen = self.autogen, verbatim=True)
    def tearDown(self):
        self.assertTrue(self.vaspFile.rm()) 
    def test_createFile(self):
        self.vaspFile.createFile()
        self.assertTrue(self.vaspFile.exists())



class TestIncar(TestVaspFile):
    def setUp(self):
        self.settings = {'ISPIN':'2', 'IBRION':2, 'ENCUT' : '400'}
        self.fileName = 'TEST_INCAR'
        self.vaspFile = run4v.INCAR(self.settings, fileName = self.fileName)
        self.vaspFile.createFile()
    def test_getContents(self):
        contents = self.vaspFile.getContents()
        expectedContents = "ISPIN=2\nIBRION=2\nENCUT=400"
        self.assertTrue(expectedContents in contents)

