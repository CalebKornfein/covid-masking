kRawDataPath = "data/BOOSTVAX.csv"
kProcessedDataPath = "data/processed.csv"

kRaceOptions = {
    "Race_White",
    "Race_Hispanic",
    "Race_African_American",
    "Race_Asian",
    "Race_Middle_Eastern",
    "Race_Pacific_Islander",
    "Race_Native_American",
    "Race_Other",
    "Race_Prefer_No_Answer",
}

kInsuranceOptions = [
    "Insurance_Private_Insurance",
    "Insurance_Medicaid",
    "Insurance_Medicare",
    "Insurance_ACA",
    "Insurance_Kaiser",
    "Insurance_VA",
    "Insurance_Healthy_SF",
    "Insurance_Other",
]

kPoliticalOptions = [
    "Political_Independent",
    "Political_Democrat",
    "Political_Republican",
    "Political_Other",
    "Political_None",
    "Political_Do_Not_Know",
    "Political_Prefer_No_Answer",
]

kCovidInfoSourceOptions = [
    "Source_Internet",
    "Source_News",
    "Source_Family_Or_Friends",
    "Source_Pamphlets",
    "Source_Community_Organizations",
    "Source_Coworkers_Or_Classmates",
    "Source_Health_Care_Professionals",
    "Source_Gov_Health_Department",
    "Source_Other",
    "Source_No_Info",
]

kMaskFrequencyOptions = [
    "Mask_Indoors_Always",
    "Mask_Indoors_Majority",
    "Mask_Indoors_Half",
    "Mask_Indoors_Infrequent",
    "Mask_Indoors_Never",
    "Mask_Indoors_Do_Not_Go_Out",
    "Mask_Indoors_Unsure",
]

kReasonOptions = [
    "Reason_No_Mask_Access",
    "Reason_Do_Not_Believe_Efficacy",
    "Reason_Ran_Out_Of_Masks",
    "Reason_Pressured_Not_To_Wear_Mask",
    "Reason_Make_It_Hard_To_Work",
    "Reason_Uncomfortable",
    "Reason_Previously_Wore_But_Got_Tired",
    "Reason_Make_Breathing_Difficult",
    "Reason_Masks_No_Longer_Recommended",
    "Reason_Other",
]


kOptions = [
    kRaceOptions,
    kInsuranceOptions,
    kPoliticalOptions,
    kCovidInfoSourceOptions,
    kMaskFrequencyOptions,
    kReasonOptions,
]

kColNames = [
    "Age",
    "Condition",
    "Education",
    "Housing",
    "Insurance",
    "Gender",
    "Has_Doctor",
] + [option for option_type in kOptions for option in option_type]

kReplaceDict = {
    # MASKING
    "Mask_Indoors_Always": "Always",
    "Mask_Indoors_Majority": "Majority",
    "Mask_Indoors_Half": "Around Half",
    "Mask_Indoors_Infrequent": "Infrequently",
    "Mask_Indoors_Never": "Never",
    "Mask_Indoors_Do_Not_Go_Out": "Do Not Go Out",
    "Mask_Indoors_Unsure": "Missing",
    # RACE
    "Race_White": "White Non-Latinx",
    "Race_Hispanic": "Hispanic or Latinx",
    "Race_African_American": "African American / Black",
    "Race_Asian": "Asian",
    "Race_Middle_Eastern": "Middle Eastern",
    "Race_Pacific_Islander": "Native Hawaiian / Pacific Islander",
    "Race_Native_American": "Native American",
    "Race_Other": "Other",
    "Race_Prefer_No_Answer": "Missing",
    # POLITICS
    "Political_Independent": "Independent",
    "Political_Democrat": "Democrat",
    "Political_Republican": "Republican",
    "Political_Other": "Other",
    "Political_None": "No Affiliation",
    "Political_Do_Not_Know": "Missing",
    "Political_Prefer_No_Answer": "Missing",
    # SOURCES
    "Source_Internet": "Internet",
    "Source_News": "News",
    "Source_Family_Or_Friends": "Family or Friends",
    "Source_Pamphlets": "Pamphlets",
    "Source_Community_Organizations": "Community Organizations",
    "Source_Coworkers_Or_Classmates": "Coworkers or Classmates",
    "Source_Health_Care_Professionals": "Health Care Professionals",
    "Source_Gov_Health_Department": "Government Health Department",
    "Source_Other": "Other",
    "Source_No_Info": "No Information",
    # REASONS
    "Reason_No_Mask_Access": "Reason No Access to Masks",
    "Reason_Do_Not_Believe_Efficacy": "Reason Do Not Believe in Efficacy",
    "Reason_Ran_Out_Of_Masks": "Reason Ran Out of Masks",
    "Reason_Pressured_Not_To_Wear_Mask": "Reason Pressured Not to Wear Mask",
    "Reason_Make_It_Hard_To_Work": "Reason Makes it Hard to Work",
    "Reason_Uncomfortable": "Reason Uncomfortable",
    "Reason_Previously_Wore_But_Got_Tired": "Reason Previously Wore But Got Tired",
    "Reason_Make_Breathing_Difficult": "Reason Makes Breathing Difficult",
    "Reason_Masks_No_Longer_Recommended": "Reason Masks No Longer Recommended",
    "Reason_Other": "Reason Other",
    # HOUSING
    "housed": "Housed",
    "unhoused": "Unhoused",
    # EDUCATION
    "high school or less": "High School or Less",
    "college degree (i.e., bachelor's)": "College Degree",
    "some college": "Some College",
    "graduate or professional (i.e., jd, md, phd)": "Graduate or Professional Degree",
    # GENDER
    "male": "Male",
    "female": "Female",
    "trans man": "Trans Male",
    "genderqueer/gender nonbinary": "Nonbinary",
    # GENERAL
    "yes": "Yes",
    "no": "No",
    # MISSING SYNONYMS
    "prefer not to answer": "Missing",
    "unk": "Missing",
    "unsure": "Missing",
}

kOrderingDict = {
    "Masking": ["Always", "Majority", "Around Half", "Infrequently", "Never"],
    "Masking Categories": ["Frequent", "Infrequent"],
    "Age": ["18-24", "25-34", "35-44", "45-64", "65-84", "84-99", "Missing"],
    "Gender": ["Female", "Male", "Nonbinary", "Trans Male", "Missing"],
    "Race": [
        "African American / Black",
        "Asian",
        "Hispanic or Latinx",
        "Middle Eastern",
        "Native American",
        "Native Hawaiian / Pacific Islander",
        "White Non-Latinx",
        "Other",
        "Multiracial",
        "Missing",
    ],
    "Prior Condition": ["Yes", "No", "Missing"],
    "Political Affiliation": [
        "Democrat",
        "Independent",
        "Republican",
        "Other",
        "No Affiliation",
        "Multiparty",
        "Missing",
    ],
    "Has Primary Care Physician": ["Yes", "No", "Missing"],
    "Education": [
        "High School or Less",
        "Some College",
        "College Degree",
        "Graduate or Professional Degree",
        "Missing",
    ],
    "Housing Status": ["Housed", "Unhoused", "Missing"],
    "Insurance Status": ["Yes", "No", "Missing"],
    "Internet": ["Yes", "No"],
    "News": ["Yes", "No"],
    "Health Care Professionals": ["Yes", "No"],
    "Family or Friends": ["Yes", "No"],
    "Pamphlets": ["Yes", "No"],
    "Community Organizations": ["Yes", "No"],
    "Coworkers or Classmates": ["Yes", "No"],
    "Government Health Department": ["Yes", "No"],
    "Other": ["Yes", "No"],
    "No Information": ["Yes", "No"],
    "Reason No Access to Masks": ["Yes", "No"],
    "Reason Do Not Believe in Efficacy": ["Yes", "No"],
    "Reason Ran Out of Masks": ["Yes", "No"],
    "Reason Pressured Not to Wear Mask": ["Yes", "No"],
    "Reason Makes it Hard to Work": ["Yes", "No"],
    "Reason Uncomfortable": ["Yes", "No"],
    "Reason Previously Wore But Got Tired": ["Yes", "No"],
    "Reason Makes Breathing Difficult": ["Yes", "No"],
    "Reason Masks No Longer Recommended": ["Yes", "No"],
    "Reason Other": ["Yes", "No"],
}
