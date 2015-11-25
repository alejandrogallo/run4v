from common import * 


initDependencies = {"POSCAR":"POSCAR", "POTCAR":"POTCAR", "INCAR":"INCAR", "KPOINTS":"KPOINTS"}

A = run4v.Job("run", folder="A", prevDependencies=initDependencies)
B = run4v.Job("run", folder="B", prev=A, prevDependencies=initDependencies)
C = run4v.Job("run", folder="C", prev=B, prevDependencies=initDependencies)
D = run4v.Job("run", folder="D", prev=C, prevDependencies=initDependencies)

A.setNext(B)
B.setNext(C)
C.setNext(D)

runner = run4v.Runner()
runner.setFirstJob(A)

runner.run()

