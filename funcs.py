import pandas as pd
import re
from datetime import date

# TRIALS & patient info
#trialfile = './datasets/ICTRP/ICTRPWeek25September2023.csv'
#trialfile = './datasets/ICTRP/test.csv' # DEBUG FOR TESTING
trialfile = './datasets/ICTRP/thousandtrials.csv'
patientdiagnosisfile = './datasets/100-patients/AdmissionsDiagnosesCorePopulatedTable.txt'
patientinfofile = './datasets/100-patients/PatientCorePopulatedTable.txt'

# FILTER FILES
diagnosisfilterfile = './datasets/100-patients/filteroutpatientdiagnosis.xlsx'
recruitmentfilterfile = './datasets/ICTRP/filterlists/filterinrecruitment.xlsx'
genderfilterfile = './datasets/ICTRP/filterlists/filteringender.xlsx'

# LOGIN csv file
loginfile = './datasets/logins/logins.csv'

# reads in ICTRP clinical trial data
def readictrpcsv():
    return pd.read_csv(trialfile, header=None)

# reads in EMRBots patient diagnosis data
def readpatientdiagnosistxt():
    return pd.read_csv(patientdiagnosisfile, sep='\t')

# reads in EMRBots patient info data
def readpatientinfotxt():
    return pd.read_csv(patientinfofile, sep='\t')

# reads in any filtering xlsx list
def readfilterlist(filename, columnnum):
    return list(pd.read_excel(filename, header=None).loc[:, columnnum])

# gets patient id from patientinfo 
def getid(patientinfo, patientnum):
    return patientinfo.loc[patientnum, 'PatientID']

# checks to see if patient ID exists, returns info from getpatientinfo if so, if not, returns False
def findpatient(patientinfo, patientID):
    patientnum = 0
    for i in patientinfo.loc[:, 'PatientID']:
        if i == patientID:
            info = getpatientinfo(patientinfo, patientnum)
            info.append(patientnum)

            return info
        
        patientnum += 1

    return False

# gets patient info to print out to screen in GUI
'''
PatientID: i0
PatientGender: i1
PatientDateOfBirth: i2
PatientRace: i3
PatientMaritalStatus: i4
PatientLanguage: i5
PatientPopulationPercentageBelowPoverty: i6
'''
def getpatientinfo(patientinfo, patientnum):
    patient = []

    patient.append(f"Patient ID: {patientinfo.loc[patientnum, 'PatientID']}")
    patient.append(f"Patient Gender: {patientinfo.loc[patientnum, 'PatientGender']}")
    patient.append(f"Patient Date of Birth: {patientinfo.loc[patientnum, 'PatientDateOfBirth']}")
    patient.append(f"Patient Race: {patientinfo.loc[patientnum, 'PatientRace']}")
    patient.append(f"Patient Marital Status: {patientinfo.loc[patientnum, 'PatientMaritalStatus']}")
    patient.append(f"Patient Language: {patientinfo.loc[patientnum, 'PatientLanguage']}")
    patient.append(f"Patient Population Percentage Below Poverty: {patientinfo.loc[patientnum, 'PatientPopulationPercentageBelowPoverty']}")

    return patient

# checks to see if trial ID exists, returns info from gettrialinfo if so, if not, returns False
def findtrial(trials, trialID):
    trialnum = 0
    for i in trials.loc[:, 0]:
        if i == trialID:
            trialinfo = gettrialinfo(trials, trialnum)
            trialinfo.append(trialnum)

            return trialinfo
        
        trialnum += 1
        
    return False

# gets important trial info to print out to screen in GUI
'''
i0: TrialID -> i0
I3: public_title -> i1
I5: url -> i2 
I18: study_type -> i3
I24: recruitment_status -> i4
I25: primary sponsor -> i5
I29: conditions -> i6
I30: interventions -> i7
I32: agemin -> i8
I33: agemax -> i9 
I34: inclusion_criteria -> i10
I35: excusion_criteria -> i11
I36: primary_outcome -> i12
'''
def gettrialinfo(trials, trialnum):
    trialinfo = []

    trialinfo.append(f"Trial ID: {trials.loc[trialnum, 0]}")
    trialinfo.append(f"Title: {trials.loc[trialnum, 3]}")
    trialinfo.append(f"URL: {trials.loc[trialnum, 5]}")
    trialinfo.append(f"Study Type: {trials.loc[trialnum, 18]}")
    trialinfo.append(f"Recruitment Status: {trials.loc[trialnum, 24]}")
    trialinfo.append(f"Primary Sponsor: {trials.loc[trialnum, 25]}")
    trialinfo.append(f"Conditions: {trials.loc[trialnum, 29]}")
    trialinfo.append(f"Interventions: {trials.loc[trialnum, 30]}")
    trialinfo.append(f"Age Minimum: {trials.loc[trialnum, 32]}")

    inclusioncriteria = str(trials.loc[trialnum, 34]).lower()
    exclusioncriteria = str(trials.loc[trialnum, 35]).lower()

    # exclusion criteria packaged with inclusion criteria
    if len(inclusioncriteria.split("exclusion criteria")) > len([inclusioncriteria]):
        newinclusioncriteria = inclusioncriteria.split("exclusion criteria")[0]
        newexclusioncriteria = inclusioncriteria.split("exclusion criteria")[-1]

        trialinfo.append(f"Inclusion Criteria: {newinclusioncriteria}")
        trialinfo.append(f"Exclusion Criteria: {newexclusioncriteria}")

    # seperate criteria
    else:
        trialinfo.append(f"Inclusion Criteria: {inclusioncriteria}")
        trialinfo.append(f"Exclusion Critieria: {exclusioncriteria}")

    trialinfo.append(trials.loc[trialnum, 36])

    return trialinfo

# searches to see if username and password are correct in order to login
def findlogin(username, password):

    usernames = list(pd.read_csv(loginfile, header=None).loc[:, 0])
    passwords = list(pd.read_csv(loginfile, header=None).loc[:, 1])

    if (username == None) or (password == None):
        return False

    for i in range(len(usernames)):
        if username == usernames[i] and password == passwords[i]:
            return True

    return False

# writes username and password to csv file containing all existing logins
def createlogin(username, password):
    usernames = list(pd.read_csv(loginfile, header=None).loc[:, 0])

    # make each username unique, and make an input required
    if (username in usernames) or (username == None) or (password == None):
        return False

    # else append new login to existing csv file
    else:
        newlogin = {'0': [username], '1': [password]}
        df = pd.DataFrame(newlogin)
        df.to_csv(loginfile, mode='a', index=False, header=False)

        return True

# returns True if ICTRP trial can accept patientdiagnoses, False if not
def checkrecruitmentstatus(trials, trialnum):
    if trials.loc[trialnum, 24].split("\"")[-2].lower() in readfilterlist(recruitmentfilterfile, 0):
        return True
    return False

# geta all diagnoses for a patient based on ID number
def getalldiagnoses(patientdiagnoses, patientID):
    diagnoseslist = []
    index = 0

    for i in patientdiagnoses.loc[:, 'PatientID']:
        if i == patientID:
            diagnoseslist.append(patientdiagnoses.loc[index, 'PrimaryDiagnosisDescription'].lower())
        index += 1
    
    return diagnoseslist

# gets all patient diagnoses, filters out all unneccessary words from EMRBots patient diagnosis description through filterlist.xlsx
# then cross checks the patient diagnosis description with a search term
def search(patientdiagnoses, patientID, searchterm):
    diagnosisfilterlist = readfilterlist(diagnosisfilterfile, 0)
    foundlist = []
    diagnosislist = getalldiagnoses(patientdiagnoses, patientID)

    for patientdiagnosis in diagnosislist:
        patientdiagnosis = re.sub('[^A-Za-z0-9\']+', ' ', patientdiagnosis).split()
        newpatientdiagnosis = [x for x in patientdiagnosis if not x in diagnosisfilterlist]
        
        for word in newpatientdiagnosis:
            search = re.search(word, searchterm)

            if search is not None: # add found match between diagnosis & trial
                foundlist.append(search)
    
    return foundlist

# First filters out all unneccessary words from EMRBots patient diagnosis description through filterlist.xlsx
# then cross checks the patient diagnosis description with ICTRP trial conditions
# returns results of search or 1 if trial accepts any/healthy patients.
def matchdiagnosistrial(patientdiagnoses, patientID, trials, trialnum):
    conditions = trials.iloc[trialnum, 29].lower()

    return search(patientdiagnoses, patientID, conditions)

# returns [[inclusion matches], [exclusion matches]] 
# either can be matches (or lack of) or 1 if no criteria given
def checkcriteria(patientdiagnoses, patientID, trials, trialnum):
    inclusioncriteria = str(trials.loc[trialnum, 34]).lower()
    exclusioncriteria = str(trials.loc[trialnum, 35]).lower()

    # no inclusion criteria given
    if inclusioncriteria == "nan":
        inclusionlist = 1

    # exclusion criteria packaged with inclusion criteria
    elif len(inclusioncriteria.split("exclusion criteria")) > len([inclusioncriteria]):
        newinclusioncriteria = inclusioncriteria.split("exclusion criteria")[0]
        newexclusioncriteria = inclusioncriteria.split("exclusion criteria")[-1]

        inclusionlist = search(patientdiagnoses, patientID, newinclusioncriteria)
        exclusionlist = search(patientdiagnoses, patientID, newexclusioncriteria)

        return [inclusionlist, exclusionlist]

    # only inclusion criteria given
    else:
        inclusionlist = search(patientdiagnoses, patientID, inclusioncriteria)

    # no exclusion criteria given
    if exclusioncriteria == "nan":
        exclusionlist = 1

    # exclusion criteria given
    else:
        exclusionlist = search(patientdiagnoses, patientID, exclusioncriteria)

    return [inclusionlist, exclusionlist]

# converts agemin and agemax from ICTRP trials to years or arbitraily large/small if not specified
def convertICTRPyears(trials, trialnum):
    ages = [trials.loc[trialnum, 31].split("\"")[1].split(" "), trials.loc[trialnum, 32].split("\"")[1].split(" ")]

    for i in range(2):
        # if units are given
        if (len(ages[i]) > 1) and (ages[i][0].isdigit()):
            checkunit = ages[i][-1].lower().split("s")[0]

            if checkunit == "minute":
                ages[i] = int(ages[i][0])/525600
            elif checkunit == "hour":
                ages[i] = int(ages[i][0])/8760
            elif checkunit == "day":
                ages[i] = int(ages[i][0])/365
            elif checkunit == "week":
                ages[i] = int(ages[i][0])/52
            elif checkunit == "month":
                ages[i] = int(ages[i][0])/12
            elif checkunit == "year":
                ages[i] = int(ages[i][0])

        # if number is given, but units are not 
        elif (ages[i][0].isdigit()):
            ages[i] = int(ages[i][0])

        # for the SINGULAR TRIAL #5338 that has ">18"
        elif (len(ages[i][0].split(">")) > len(ages[i])):
            ages[i] = int(ages[i][0].split(">")[1])+1

        # if a number is not given (i.e. "days" or "N/A")
        # set age min to 0, age max to 200
        else:
            ages[i] = 200 * i

    return ages

# converts EMRBots' PatientDateOfBirth to age in years
def convertpatientyears(patientinfo, patientnum):
    dateofbirth = patientinfo.loc[patientnum, 'PatientDateOfBirth'].split()[0].split("-")
    return date.today().year - int(dateofbirth[0]) - ((date.today().month, date.today().day) < (int(dateofbirth[1]), int(dateofbirth[2])))

# checks if patient age fits within ICTRP trial age requirements. Returns True if so, False if not
def checkage(patientinfo, patientnum, trials, trialnum):
    agereqs = convertICTRPyears(trials, trialnum)
    patientage = convertpatientyears(patientinfo, patientnum)

    return (patientage>=int(agereqs[0])) and (patientage<=int(agereqs[1]))

# checks if patient gender fits within ICTRP trial gender reguirements. Returns True if so, False if not
def matchgender(patientinfo, patientnum, trials, trialnum):
    genderreqs = trials.loc[trialnum, 33].lower()
    allgenderfilterlist = readfilterlist(genderfilterfile, 0)

    # if trial allows men and women
    if genderreqs in allgenderfilterlist:
        return True
    
    patientgender = patientinfo.loc[patientnum, 'PatientGender'].lower()

    # read filter list depending on patient gender, check if reqs in that list
    if genderreqs in readfilterlist(genderfilterfile, int(patientgender == "male")+1):
        return True
    
    return False

# "wrapper" function that makes all checks, returns True if patient is eligible, False if not
# TODO may become more stringent depending on testing results-
def checkeligibility(patientinfo, patientnum, patientdiagnoses, trials, trialnum):

    # check age, gender, recruitment status. patient has to match all of these
    if not (checkage(patientinfo, patientnum, trials, trialnum) 
            and matchgender(patientinfo, patientnum, trials, trialnum) 
            and checkrecruitmentstatus(trials, trialnum)):
        return False
    
    patientID = getid(patientinfo, patientnum)

    criterion = checkcriteria(patientdiagnoses, patientID, trials, trialnum)

    # check criteria, patient must match inclusion criteria and no exclusion criteria.
    # exclusion not blank or not == 1
    # or
    # inclusion blank or not == 1
    if (not (criterion[1] == []) or not (criterion[1] == 1)):
        return False
    
    if (criterion[0] == [] or not (criterion[0] == 1)):
        return False

    trialinfo = gettrialinfo(trials, trialnum)
    
    return trialinfo