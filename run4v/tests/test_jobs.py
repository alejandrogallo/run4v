
from common import * 
import unittest 

import run4v

THIS_FOLDER = os.path.split(__file__)[0]


class TestGeneralSingleJob(unittest.TestCase):
    def makeDummyFile(self, name, path=os.curdir):
        filePath = os.path.join(path,name)
        f = open(filePath,"w+")
        f.close()
        self.dummyFiles.append(filePath)
    def rmDummy(self):
        for fileName in self.dummyFiles:
            os.remove(fileName)
    def setUp(self):
        self.dummyFiles = []
        folder = "TestFolderA"
        self.makeDummyFile(name="run")
        self.makeDummyFile(name="POTCAR_N")
        self.makeDummyFile(name="POSCAR.6")
        dependencies = [run4v.INCAR({'IBRION':'2'})]
        prevDependencies={'POSCAR.6':'POSCAR', 'POTCAR_N':'POTCAR'}
        path = os.path.join(THIS_FOLDER, folder)
        self.job = run4v.Job(script="run", folder=path, prevDependencies=prevDependencies, dependencies = dependencies)
    def tearDown(self):
        self.rmDummy() 
        shutil.rmtree(self.job.folder)
        
    #TESTS
    def test_run(self):
        self.job.run()
        self.assertTrue(os.path.exists(self.job.folder))




