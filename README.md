# clinical-trial-matching-system
---
Uses ICTRP trials and EMRBots patient information with language processing to match patients to trials they would be eligible for.
-
  
- Patient IDs are specified in ./datasets/100-Patients/PatientCorePopulatedTable.txt, in the "PatientID" column. Ex. "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F"
- Trial IDs are specified in ./datasets/ICTRP/ICTRPWeek25September2023.csv, in the 1st column. Ex. "NCT06032923"

# Usage:
---
The user can sign in as a patient or a provider. For debugging purposes, the user can create a fake login in order to see what the provider would be able to see.
-

For patients, the user must put in a patient ID.
- The patients can view their information and all of their eligible trials. Any trial can be clicked on in order to view more information.

For providers, they must put in their login username and password. The debug login username is "testuser" and login password is "testpassword".
- The provider can then search all patients by patient ID or clinical trials by trial ID. Searching a patient brings up their information and eligible trials. Searching a trial brings up the trial information.

# Setup and Running:
---
1. Run setup.py in order to install all required packages.
2. Run CTMS.py to view the application. The application has buttons and text prompts to be inputted by the user, and will bring up error prompts when an inccorect input is put in.
