import pandas as pd
from constants import *


def fetch_age_stats(df):
    ages = []
    for i, row in df.iterrows():
        if row["Age"] == "unk":
            continue
        ages.append(int(row["Age"]))

    print(pd.DataFrame({"Age": ages}).describe())


def validate(df):
    validate_option(df, kRaceOptions, "race")
    validate_options(df, kInsuranceOptions, "insurance")


def validate_option(df, options, option_type):
    subset = df[[option for option in options]]
    print(f"-----------------------------\nCleaning {option_type}:")
    unique = pd.unique(subset).values.ravel("K")
    print(f"Unique values: {unique}")
    print(f"Missing values: {subset.isnull().sum()}")
    print("")

    print("-----------------------------\n")


def add_masking_behaviors(df):
    behaviors = []
    subset = df[[option for option in kMaskFrequencyOptions]]
    for i, row in subset.iterrows():
        behavior = []
        for option in kMaskFrequencyOptions:
            if row[option] == "yes":
                behavior.append(option)

        if len(behavior) == 0:
            print(i, behavior, "NO RESPONSE")
            behaviors.append("No Responses")
        elif len(behavior) == 1:
            behaviors.append(behavior[0])
        else:
            print(i, behavior, "MULTIPLE RESPONSES")
            behaviors.append("Multiple Responses")
    return behaviors


def add_binary_masking_behaviors(vals):
    behaviors = []

    for val in vals:
        if (
            val == "Mask_Indoors_Always"
            or val == "Mask_Indoors_Majority"
            or val == "Mask_Indoors_Half"
        ):
            behaviors.append("Frequent")
        elif val == "Mask_Indoors_Infrequent" or val == "Mask_Indoors_Never":
            behaviors.append("Infrequent")
        else:
            behaviors.append("Other")
    return behaviors


def add_age(df):
    ages = []
    for i, row in df.iterrows():
        age = row["Age"]

        if age == "unk":
            ages.append("unk")
            continue
        age = int(age)

        if 18 <= age <= 24:
            ages.append("18-24")
        elif 25 <= age <= 34:
            ages.append("25-34")
        elif 35 <= age <= 44:
            ages.append("35-44")
        elif 45 <= age <= 64:
            ages.append("45-64")
        elif 65 <= age <= 84:
            ages.append("65-84")
        elif 85 <= age <= 99:
            ages.append("84-99")
        elif age >= 100:
            ages.append("100+")
    return ages


def add_race(df):
    races = []
    subset = df[[option for option in kRaceOptions]]
    for i, row in subset.iterrows():
        race = []
        for option in kRaceOptions:
            if row[option] == "yes":
                race.append(option)

        if len(race) == 0:
            print(row)
        elif len(race) == 1:
            races.append(race[0])
        else:
            print(race)
            races.append("Multiracial")
    return races


def add_politics(df):
    politics = []
    subset = df[[option for option in kPoliticalOptions]]
    for i, row in subset.iterrows():
        politic = []
        for option in kPoliticalOptions:
            if row[option] == "yes":
                politic.append(option)

        if len(politic) == 0:
            print(row)
            politics.append("Missing")
        elif len(politic) == 1:
            politics.append(politic[0])
        else:
            print(politic)
            politics.append("Multiparty")
    return politics


def add_condition(df):
    return list(df[["Condition"]].values.ravel())


def add_housing(df):
    return list(df[["Housing"]].values.ravel())


def add_education(df):
    return list(df[["Education"]].values.ravel())


def add_insurance(df):
    return list(df[["Insurance"]].values.ravel())


def add_gender(df):
    return list(df[["Gender"]].values.ravel())


def add_doctor(df):
    return list(df[["Has_Doctor"]].values.ravel())


def no_response(row, options):
    for option in options:
        if row[option] == "yes":
            return False
    return True


def multiple_responses(row, options):
    response_counter = 0
    for option in options:
        if row[option] == "yes":
            response_counter += 1
    return response_counter >= 2


def valid(df):
    return df.apply(
        lambda row: not (
            no_response(row, kMaskFrequencyOptions)
            or multiple_responses(row, kMaskFrequencyOptions)
        ),
        axis=1,
    )


def answered_masking(df):
    return df.apply(
        lambda row: not (
            row["Mask_Indoors_Unsure"] == "yes"
            or row["Mask_Indoors_Do_Not_Go_Out"] == "yes"
        ),
        axis=1,
    )


def process(df, output_path, summary_path):
    # Add all variables for analysis to a cleaned dataframe
    d = {}

    d["Masking"] = add_masking_behaviors(df)
    d["Masking Categories"] = add_binary_masking_behaviors(d["Masking"])
    d["Age"] = add_age(df)
    d["Gender"] = add_gender(df)
    d["Race"] = add_race(df)
    d["Prior Condition"] = add_condition(df)
    d["Political Affiliation"] = add_politics(df)
    d["Has Primary Care Physician"] = add_doctor(df)
    d["Education"] = add_education(df)
    d["Housing Status"] = add_housing(df)
    d["Insurance Status"] = add_insurance(df)

    for source in kCovidInfoSourceOptions:
        d[kReplaceDict[source]] = list(df[[source]].values.ravel())

    for reason in kReasonOptions:
        d[kReplaceDict[reason]] = list(df[[reason]].values.ravel())

    processed = pd.DataFrame(d)

    # Make all the nice swaps so that the values print nicely :)
    for value, replacement in kReplaceDict.items():
        processed = processed.replace(value, replacement)

    processed.to_csv(output_path, index=False)

    # Print out some information
    print(fetch_age_stats(df))
    return processed


def main():
    df = pd.read_csv(kRawDataPath)

    # Only look at relevant columns
    df = df[kColNames]

    # Strip all strings and make all letters lower case
    df = df.map(lambda x: x.strip().lower() if isinstance(x, str) else x)

    # Flag invalid observations missing the mask frequency response variable or containing multiple responses
    valid_index = valid(df)
    df = df[valid_index]

    # Also exclude observations for people who did not go out or were unsure
    answered = answered_masking(df)
    df = df[answered]

    process(
        df,
        output_path="data/processed_full.csv",
        summary_path="results/summary_full.csv",
    )

    # Also look at only infrequent mask users
    infrequent = df[
        df.apply(
            lambda row: row["Mask_Indoors_Infrequent"] == "yes"
            or row["Mask_Indoors_Never"] == "yes",
            axis=1,
        )
    ]
    process(
        infrequent,
        output_path="data/processed_infrequent.csv",
        summary_path="results/summary_infrequent.csv",
    )

    # And frequent mask users
    frequent = df[
        df.apply(
            lambda row: row["Mask_Indoors_Always"] == "yes"
            or row["Mask_Indoors_Majority"] == "yes"
            or row["Mask_Indoors_Half"] == "yes",
            axis=1,
        )
    ]
    process(
        frequent,
        output_path="data/processed_frequent.csv",
        summary_path="results/summary_frequent.csv",
    )


if __name__ == "__main__":
    main()
