# clinical-trial-matching-system
---

- Uses simulated datasets of patient information and actual clinical trials to match patients to trials.
- Uses ICTRP trials and EMRBots trial information with language processing to find which trials a patient would be eligible for.
- The user can sign in as a patient or a provider. For debugging purposes, the user can create a fake login in order to see what the provider would be able to see.

# Usage:
---
For patients, the user must put in a patient ID, as specified in the ./datasets/100-Patients/PatientCorePopulatedTable.txt file, in the "PatientID" column.

- The patients can view their information and all of their eligible trials. Any trial can be clicked on in order to view more information.

For providers, the debug login username is "testuser" and login password is "testpassword".

- The provider can then see all patients and clinical trials in the dataset. Any patient or trial can be clicked on in order to view more information.
- If a patient is clicked on, their information and eligible trials can be seen.

# Setup:
---
1. Run setup.py in order to install all required packages.
2. Run GUI.py to view the application. The application has buttons and text prompts to be inputted by the user, and will bring up error prompts when an inccorect input is put in.
