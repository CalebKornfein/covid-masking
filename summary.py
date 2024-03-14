import pandas as pd

# Constants
kDataPath = "BOOSTVAX.csv"

kRaceOptions = {
    'Race_White',
    'Race_Hispanic',
    'Race_Black',
    'Race_Asian',
    'Race_Middle_Eastern',
    'Race_Pacific_Islander',
    'Race_Other',
    'Race_Prefer_No_Answer'
}

kInsuranceOptions = {
    'Insurance',
    'Insurance_Private_Insurance',
    'Insurance_Medicaid',
    'Insurance_Medicare',
    'Insurance_ACA',
    'Insurance_Kaiser',
    'Insurance_VA',
    'Insurance_Healthy_SF',
    'Insurance_Other'
}

kPoliticalOptions = {
    'Political_Independent',
    'Political_Democrat',
    'Political_Republican',
    'Political_Other',
    'Political_None'
    'Political_Do_Not_Know',
    'Political_Prefer_No_Answer'
}

kCovidInfoSourceOptions = {
    'Source_Internet',
    'Source_News',
    'Source_Family_Or_Friends',
    'Source_Pamphlets',
    'Source_Community_Organizations',
    'Source_Coworkers_Or_Classmates',
    'Source_Health_Care_Professionals',
    'Source_Gov_Health_Department',
    'Source_Other',
    'Source_No_Info'
}

kMaskFrequencyOptions = {
    'Mask_Indoors_Always',
    'Mask_Indoors_Majority',
    'Mask_Indoors_Half',
    'Mask_Indoors_Infrequent',
    'Mask_Indoors_Never'
    'Mask_Indoors_Do_Not_Go_Out',
    'Mask_Indoors_Unsure'
}

kReasonOptions = {
    'Reason_No_Mask_Access',
    'Reason_Do_Not_Believe_Efficacy',
    'Reason_Ran_Out_Of_Masks',
    'Reason_Pressured_Not_To_Wear_Mask'
    'Reason_Make_It_Hard_To_Work',
    'Reason_Uncomfortable',
    'Reason_Previously_Wore_But_Got_Tired',
    'Reason_Make_Breathing_Difficult',
    'Reason_Masks_No_Longer_Recommended',
    'Reason_Other'
}






def main():
    df = pd.read_csv(kDataPath)
    df.describe()


if __name__ == "__main__":
    main()