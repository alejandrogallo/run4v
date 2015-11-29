#! /bin/usr/python2

import os, shutil, sys
import time

__version__="0.0.1"
VERBOSE=True



class Runner(object):
    """ 
    Class that manages all VASP jobs. It will run the jobs one after another. 
    """
    jobs=[]
    verbose=VERBOSE
    firstJob = None
    def vprint(self, something):
        if self.verbose:
            print("RUNNER:: ---> %s"%something)
    def setFirstJob(self, job):
        self.firstJob = job
    def getFirstJob(self):
        return self.firstJob
    def run(self):
        """ Run the runner """
        if self.getFirstJob():
            self.vprint("Starting to run the jobs")
            job = self.getFirstJob()
            while job:
                try:
                    self.vprint("Running  %s"%job)
                    job.run()
                except Exception, e:
                    self.vprint("Some problem happened running the job %s"%job)
                    raise Exception(e)
                    sys.exit(-1)
                else:
                    self.vprint("Running %s done!\t\033[42;93m[x]\033[0m"%job)
                    job = job.getNext()
        

class Job(object):
    def __init__(self, script="", folder=os.curdir, dependencies=[], prevDependencies={}, next=None, prev=None, verbose=VERBOSE, execute=True):
        self.script = script
        self.folder = folder
        self.dependencies = dependencies
        self.next=next
        self.prev=prev 
        self.verbose = verbose
	self.execute=execute
        self.prevDependencies = prevDependencies
        self.runCommand = "llsubmit"
        self.principalFolder=os.path.abspath(os.curdir)
    def __str__(self):
        return "Job %s"%self.folder
    def vprint(self, something):
        if self.verbose:
            print("\033[7;49;32m Job::\033[0m --> %s"%something)
    def setNext(self, obj):
        """ Set next job """
        self.next=obj
        return self.next
    def setPrev(self, obj):
        """ Set previous job """ 
        self.prev=obj
        return self.prev
    def getNext(self):
        """ Get next job """
        return self.next
    def getPrev(self):
        """ Get previous job """ 
        return self.prev
    def setPrevDependencies(self, dependencies = {}):
        """
            Set the dependencies we need from the prev VASPLoader object
                dependencies = {
                    "prevDependencyName":"newName", .. 
                }
        """
        self.prevDependencies = dependencies 
    def getPath(self, depName):
        if depName in self.dependencies:
            return os.path.join(self.ABS_PATH, self.folder, depName)
        else:
            raise Exception("ERROR: %s is not a valid dependency"%depName)
            sys.exit(-1)
    def controlPrevDependencies(self):
        # Controlling previous dependencies
        self.vprint("Preparing the previous job dependencies: %s"%self.prevDependencies)        
        if self.prev:
            # Self is not the first job of the chain
            prevFolder = self.prev.folder
        else:
            # Self is the first job of the chain
            prevFolder = os.curdir
        for depName in self.prevDependencies: 
            prevFilePath = os.path.join(prevFolder,depName)
            newName = self.prevDependencies[depName]
            filePath = os.path.join(self.folder, newName)
            self.vprint("Getting %s to destination %s for %s"%(prevFilePath, filePath, self ))
            if os.path.exists(prevFilePath):
                shutil.copy(prevFilePath, filePath)
            else:
                raise Exception("The file %s was not found!"%filePath)
                sys.exit(-1)

    def controlDirectory(self):
        self.vprint("Is there a folder called %s?"%self.folder)
        # Controlling directory 
        if os.path.exists(self.folder):
            self.vprint("Folder %s found"%self.folder)
        else:
            self.vprint("Folder %s not found\n\t Creating it..."%self.folder)
            try:
                os.mkdir(self.folder)
            except:
                raise Exception("Folder %s could not be created"%self.folder)
                sys.exit(-1)
    def controlDependencies(self):
        # Controlling dependencies
        dependenciesFailure = False
        for depName in self.dependencies:
            if type(depName) is str:   
                filePath = os.path.join(self.folder, depName)
                if not os.path.exists(filePath):
                    dependenciesFailure = depName 
                    break
            else:
                if not depName.exists():
                    depName.createFile(self.folder)
                    if not depName.exists():
                        dependenciesFailure = depName 
                        break
        if dependenciesFailure:
            raise Exception("The file %s was not found!"%filePath)
            sys.exit(-1)
    def prepare(self):
        """ 
            Prepare data for the running of the VASP program: 
               1.   Look at the prevDependencies to copy the needed files from the prev object into the folder 
               2.   Look at the dependencies names to see if we have all dependencies 
        """
        self.controlDirectory()
        self.controlPrevDependencies()
        self.controlDependencies()
    def controlRun(self):
        """ In the case that a run script was given, this function controls that the run script exists. """
        if not self.script:
            return True
        runFailure=False
        self.vprint("Preparing job for running...")
        self.vprint("Is there the run script '%s' in %s"%(self.script, self.folder))
        runPath = os.path.join(self.folder, self.script)
        if not os.path.exists(runPath):
            runFailure = True
        if not self.prev:
            # we are in the first job
            runPath = os.path.join(os.curdir, self.script)
            if os.path.exists(runPath):
                self.vprint("Run script found at %s, moving the script to the %s folder"%(os.curdir, self.folder))
                shutil.copy(runPath, self.folder)
                runFailure = False
        else:
            scriptPrevPath = os.path.join(self.prev.folder, self.script)
            if os.path.exists(scriptPrevPath):
                runFailure=False
                shutil.copy(scriptPrevPath, self.folder)
        if runFailure:
            raise Exception("No script '%s' to be run found in  '%s' !"%(self.script, self.folder))
            sys.exit(-1)
    def cd(self, folder="-"):
        if folder in [self.folder, "-"]:
            if folder!="-":
                destination=folder
            else:
                destination=self.principalFolder
        else:
            raise Exception("For the moment you can only change directory either to %s or to %s"%(self.folder, self.principalFolder))
            sys.exit(-1) 
        self.vprint("Changing directory to %s"%destination)
        os.chdir(destination)
    def runScript(self):
        command = self.runCommand+" "+self.script
        self.vprint("Running command '%s'"%command)
        os.system(command)
    def run(self):
        """ 
        This function runs the job. If 'execute=False' then the job will not be run, maybe because you have 
        already run it and you just want to run the next jobs
        """
        if not self.execute:
            self.vprint("The job %s will not be executed"%self)
            return 0
        self.prepare()
        self.controlRun()
        self.cd(self.folder)
        self.runScript()
        self.cd()




class VASPFile(object):
    def __init__(self, fileName = "GenericVaspFile", path=os.curdir, autogen=False, verbose=VERBOSE):
        self.fileName = fileName
        self.path = path
        self.autogen = autogen 
        self.verbose = verbose
        self.filePath = os.path.join(self.path, self.fileName)
        if self.autogen:
            self.createFile()
    def vprint(self, something):
        if self.verbose:
            print("\033[7;49;91m%s::\033[0m >>>> %s"%(self.fileName, something))
    def getContents(self):
        return "This is a generic VaspFile"
    def createFile(self, path=""):
        if path:
            self.path = path
        self.vprint("Creating file...")
        try:
            f = open(os.path.join(self.path, self.fileName), "w+")
            f.write("# %s FILE AUTOMATICALLY GENERATED \n"%self.fileName)
            f.write(self.getContents())
        except Exception: 
            raise Exception("The file '%s' could not be created!"%(self.fileName))
            sys.exit(-1)
        else :
            f.close()
            self.vprint("File created succesfully")
    def exists(self):
        if os.path.exists(os.path.join(self.path, self.fileName)):
            return True
        else:
            return False
    def rm(self):
        self.vprint("Removing file")
        if self.exists():
            try:
                os.remove(self.filePath)
            except Exception, e:
                raise Exception("A problem removing file %s occourred"%self.filePath)
                return False 
            else:
                self.vprint("File removed succesfully")
                return True 
        else: 
            raise Exception("Trying to remove a non-existent file at %s"%self.filePath)
            return False 

class INCAR(VASPFile):
    def __init__(self, settings, fileName="INCAR", **kwargs ):
        # set settings before initializing before of autogen and createFile
        self.settings = settings
        super(INCAR, self).__init__(fileName, **kwargs)
    def getContents(self):
        settings = self.settings
        if not type(settings) is dict:
            raise Exception("Settings in INCAR FILE must be a dict!")
            sys.exit(-1)
        contents = ""
        for settingName in settings:
            contents += str(settingName)+"="+str(settings[settingName])+"\n"
        return contents 



class POSCAR(VASPFile):
    def __init__(self, basis_atoms, basis_vectors, replication_steps, cell_atoms, basis_positions=[(0,0,0)], fileName="POSCAR", **kwargs):
        super(POSCAR, self).__init__(fileName, **kwargs)
        self.basis_atoms=basis_atoms
        self.basis_vectors=basis_vectors
        self.replication_steps=replication_steps
        self.cell_atoms=cell_atoms
        self.basis_positions=basis_positions
    
    def getContents(self):
        pass 
        

















