from common import * 


initDependencies = {"POSCAR":"POSCAR", "POTCAR":"POTCAR", "INCAR":"INCAR", "KPOINTS":"KPOINTS"}

A = abcd.Job("run", folder="A", prevDependencies=initDependencies)
B = abcd.Job("run", folder="B", prev=A, prevDependencies=initDependencies)
C = abcd.Job("run", folder="C", prev=B, prevDependencies=initDependencies)
D = abcd.Job("run", folder="D", prev=C, prevDependencies=initDependencies)

A.setNext(B)
B.setNext(C)
C.setNext(D)

runner = abcd.Runner()
#runner.addJobs([A,B,C,D])
runner.setFirstJob(A)

runner.run()

