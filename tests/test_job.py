
from common import * 
import unittest 


def makeDummyScript(self, name="run", path=os.curdir):
    f = open(os.path.join(path,name),"w+")
    f.close()


class TestGeneralSingleJob(unittest.TestCase):
    def setUp(self):
        folder = "TestFolderA"
        makeDummyScript(name="run")
        prevDependencies={'INCAR_OLD':'INCAR_MOVED'}
        self.job = run4v.Job(script="run", folder=folder, prevDependencies=prevDependencies)
    def tearDown(self):
        pass



