from common import * 
import unittest 
import run4v
run4v.VERBOSE = False

class TestVaspFile(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_createFile(self):
        fileName = "TEST_VASPFILE"
        vaspFile = run4v.VASPFile(fileName = fileName, autogen = False, verbose=True)
        vaspFile.createFile()
        self.assertTrue(vaspFile.exists())
        self.assertTrue(vaspFile.rm())
    def test_raw_content(self):
        fileName = "TEST_VASPFILE_RAW_CONTENT"
        raw_content = "Hello folks"
        vaspFile = run4v.VASPFile(raw_content = raw_content, fileName = fileName, autogen = True, verbose=True)
        fd = open(fileName)
        self.assertTrue(vaspFile.exists())
        self.assertTrue(raw_content in fd.read())
        fd.close()
        self.assertTrue(vaspFile.rm())



class TestIncar(TestVaspFile):
    def setUp(self):
        pass
    def test_getContents(self):
        settings = {'ISPIN':'2', 'IBRION':2, 'ENCUT' : '400'}
        fileName = 'TEST_INCAR'
        vaspFile = run4v.INCAR(settings, fileName = fileName)
        vaspFile.createFile()
        contents = vaspFile.getContents()
        expectedContents = "ISPIN=2\nIBRION=2\nENCUT=400"
        self.assertTrue(expectedContents in contents)
        self.assertTrue(vaspFile.rm())
    def test_getContents_with_false_value(self):
        settings = {'ISPIN':'2', 'IBRION':2, 'ENCUT' :False}
        fileName = 'TEST_INCAR_WITHOUT_ENCUT'
        vaspFile = run4v.INCAR(settings, fileName = fileName)
        vaspFile.createFile()
        contents = vaspFile.getContents()
        self.assertTrue("ENCUT" not in contents)
        self.assertTrue(vaspFile.rm())
