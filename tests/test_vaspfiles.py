from common import * 
import unittest 



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
        self.settings = {'IBRION':2, 'ISPIN':'2','ENCUT' : '400'}#,'NELECT':'046','NELM':'50','ISMEAR':'-2','FERWE':'256*1 128*0','FERDO':'254*1 130*0','NBANDS':'384'}
        self.fileName = 'TEST_INCAR'
        self.vaspFile = run4v.INCAR(self.settings, fileName = self.fileName)
        self.vaspFile.createFile()
    def test_getContents(self):
        contents = self.vaspFile.getContents()
        expectedContents = "IBRION=2\nISPIN=2\nENCUT=400"
        self.assertTrue(expectedContents in contents)

if __name__=="__main__":
    unittest.main()
