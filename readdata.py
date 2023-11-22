# adding file dir to path to allow local imports
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

# imports
import time
import funcs as f
import debugs as d
 
# TODO make functions to get proportions/means, possibly t test
# TODO create findpatient() to get patient info given ID

# loop over patient core, b/c each unique patient, no multiples
# first checks: age range, gender, recruitment status
# if any one of those fail, immediate exclusion.
# if those all pass, THEN find all diagnoses for a single patient match based on conditions & criteria.
# return matches for condition & criteria,
# but only match exclusion. if any match, immediate exclusion.
# if patient is a match, append their number to a list specific to that trial.

# testing condition matching: patient 12 (i11), trial 11 (i10) both contain "diabetes"
# testing condition matching: patient 3 (i2) and trial 65 conditions (i64) both contain "leukemia"
# testing criteria matching: patient 3 (i2) and trial 57 exclusion criteria (i56) both contain "leukemia"
# conditions i29, inclusion i34, exclusion i35

def main():
    start = time.time()
    trials = f.readictrpcsv()
    patientdiagnoses = f.readpatientdiagnosistxt()
    patientinfo = f.readpatientinfotxt()

    #print(f.checkrecruitmentstatus(trials, 3))
    #print(f.convertICTRPyears(trials, 255))
    #print(f.convertpatientyears(patientinfo, 0))
    #print(f.checkage(patientinfo, 0, trials, 0))
    #print(f.matchgender(patientinfo, 0, trials, 1))
    #print(f.getalldiagnoses(patientdiagnoses, 0))
    #print(f.optimizedmatchgender(patientinfo, 0, trials, 21))
    #print(f.optimizedcheckcriteria(patientdiagnoses, 2, trials, 56), "\n")
    #print(f.readfilterlist('./datasets/100-patients/filteroutpatientdiagnosis.xlsx', 0))
    #print(f.matchdiagnosistrial(patientdiagnoses, 2, trials, 64))
    #print(f.checkcriteria(patientdiagnoses, 2, trials, 1897))
    
    #print(f.checkeligibility(patientinfo, 2, patientdiagnoses, trials, 0))

    #for i in range(len(trials)):
    #    if f.checkeligibility(patientinfo, 0, patientdiagnoses, trials, i) == 1:
    #        print(i)

    #print(d.getnumpatientdiagnosis(patientdiagnoses))

    print(f.createlogin("testuser2", "testpass2"))

    #print(f.findlogin("testuser", "testpassword"))

    print(time.time() - start)

if __name__ == "__main__":
    main()