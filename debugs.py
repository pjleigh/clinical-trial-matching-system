from collections import Counter

# gets diagnosis code in correct format from EMRBots patient data
def getdiagnosiscode(patientdiagnoses, patientnum):
    if "." in patientdiagnoses.loc[patientnum, 'PrimaryDiagnosisCode']: # patient code
        return "".join(patientdiagnoses.loc[patientnum, 'PrimaryDiagnosisCode'].split("."))
    else:
        return patientdiagnoses.loc[patientnum, 'PrimaryDiagnosisCode']

# gets all unique recruitment statuses from ICTRP data
def getuniquerecruitmentstatus(trials):
    recruitmentstatuslist = list(trials.loc[:, 24])
    uniquelist = []

    for i in recruitmentstatuslist:
        uniquelist.append(i.lower())

    return Counter(uniquelist)

# gets all unique words in all of the patientdiagnoses diagnosis descriptions, and their counts
# used to create a list of words to filter out in matchpatienttrial()
def getuniquepatientdiagnosis(patientdiagnoses):
    patientdiagnosesdiagnosislist = list(patientdiagnoses.loc[:, 'PrimaryDiagnosisDescription'])
    uniquelist = []

    for i in patientdiagnosesdiagnosislist:
        for j in i.lower().split():
            uniquelist.append(j)

    return Counter(uniquelist)

# debug function to get unique values of age reqs in trials
def getuniqueage(trials):
    agelist = list(trials.loc[:, 32]) # 31 min, # 32 max
    uniquelist = []

    for i in agelist:
        uniquelist.append(i.lower())

    return Counter(uniquelist)

# debug function to get unique values of gender reqs in trials
def getuniquegender(trials):
    agelist = list(trials.loc[:, 33])
    uniquelist = []

    for i in agelist:
        uniquelist.append(i.lower())

    return Counter(uniquelist)

# debug function to get unique values of gender reqs in trials
def getuniquecriteria(trials):
    criterialist = list(trials.loc[:, 34]) # 34 inclusion, 35 exclusion
    uniquelist = []

    for i in criterialist:
        uniquelist.append(i.lower())

    return Counter(uniquelist)

def getuniqueconditions(trials):
    conditionlist = list(trials.loc[:, 29])
    uniquelist = []

    for i in conditionlist:
        uniquelist.append(str(i).lower())

    return Counter(uniquelist)

# returns number of males/females in patientinfo
def getnumgender(patientinfo):
    patientgenderlist = list(patientinfo.loc[:, 'PatientGender'])

    return Counter(patientgenderlist)

# returns number of each race in patientinfo
def getnumrace(patientinfo):
    patientracelist = list(patientinfo.loc[:, 'PatientRace'])

    return Counter(patientracelist)

# returns number of each age in patientinfo
def getnumage(patientinfo):

    # adding file dir to path to allow local imports
    from pathlib import Path
    import sys
    path_root = Path(__file__).parents[2]
    sys.path.append(str(path_root))

    # imports
    import funcs as f

    ages = []

    for i in range(len(patientinfo)):
        age = f.convertpatientyears(patientinfo, i)
        ages.append(age)

    return Counter(ages)

# returns number of each diagnoses in patientdiagnoses
def getnumpatientdiagnosis(patientdiagnoses):
    patientdiagnosislist = list(patientdiagnoses.loc[:, 'PrimaryDiagnosisDescription'])

    return Counter(patientdiagnosislist)