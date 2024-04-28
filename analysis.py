import pandas as pd
from constants import *
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from scipy import stats
from statistics import stdev
from math import sqrt

def create_confints(df, frequent, infrequent, path):
    def stat(col):
        full_counter = Counter(df[col].values)
        frequent_counter = Counter(frequent[col].values)
        infrequent_counter = Counter(infrequent[col].values)

        total = df.shape[0]
        ordering = kOrderingDict[col]
        
        rows = []
        for c in ordering:
            if full_counter[c] <= 1:
                rows.append([col, # column name
                            c,   # value
                            full_counter[c], # value count
                            full_counter[c] / total * 100, # value as a percentage
                            frequent_counter[c], # frequent_count
                            frequent_counter[c] * 100, # frequent percentage
                            'NA', # frequent upper bound 95% CI
                            'NA', # frequent lower bound 95% CI
                            infrequent_counter[c], # infrequent count
                            infrequent_counter[c] * 100, # infrequent percentage
                            'NA', # infrequent percentage upper
                            'NA', # infrequent percentage lower
                ])
                continue

            frequent_percent = frequent_counter[c] / full_counter[c] * 100
            infrequent_percent = infrequent_counter[c] / full_counter[c] * 100

            fake = [100] * frequent_counter[c] + [0] * infrequent_counter[c]
            print(c, len(fake))
            std = stdev(fake)

            length =  1.95996 * std / sqrt(full_counter[c])
            rows.append([col, # column name
                        c,   # value
                        full_counter[c], # value count
                        round(full_counter[c] / total * 100, 2), # value as a percentage
                        frequent_counter[c], # frequent_count
                        round(frequent_percent, 2), # frequent percentage
                        min(round(frequent_percent + length, 2), 100), # frequent upper bound 95% CI
                        max(round(frequent_percent - length, 2), 0), # frequent lower bound 95% CI
                        infrequent_counter[c], # infrequent count
                        round(infrequent_percent, 2),# infrequent percentage
                        min(round(infrequent_percent + length, 2), 100), # infrequent percentage upper
                        max(round(infrequent_percent - length, 2), 0), # infrequent percentage lower
            ])
        return rows

    cumulative_rows = []
    for column in [c for c in df.columns]:
        rows = stat(column)
        for row in rows:
            cumulative_rows.append(row)

    final = pd.DataFrame(cumulative_rows)
    cols = ["Column", "Value", "Count", "Percent", "Frequent Count", "Frequent Percentage", "Frequent Upper Bound", "Frequent Lower Bound", "Infrequent Count", "Infrequent Percentage", "Infrequent Upper Bound", "Infrequent Lower Bound"]
    final.columns = cols
    
    final.to_csv(path, index=False)

    return final

def create_summary(df, path):

    frequent = df[df['Masking Categories'] == 'Frequent']
    n_frequent = frequent.shape[0]
    print("Frequent", frequent.shape)

    infrequent = df[df['Masking Categories'] == 'Infrequent']
    n_infrequent = infrequent.shape[0]
    print("Infrequent", infrequent.shape)

    def stat(col):
        full_counter = Counter(df[col].values)
        frequent_counter = Counter(frequent[col].values)
        infrequent_counter = Counter(infrequent[col].values)

        total = df.shape[0]
        ordering = kOrderingDict[col]
        
        rows = []
        for c in ordering:
            frequent_percent = frequent_counter[c] / n_frequent * 100
            infrequent_percent = infrequent_counter[c] / n_infrequent * 100
            rows.append([col, # column name
                        c,   # value
                        full_counter[c], # value count
                        round(full_counter[c] / total * 100, 2), # value as a percentage
                        frequent_counter[c], # frequent_count
                        round(frequent_percent, 2), # frequent percentage
                        infrequent_counter[c], # infrequent count
                        round(infrequent_percent, 2),# infrequent percentage
            ])
        return rows

    cumulative_rows = []
    for column in [c for c in df.columns]:
        rows = stat(column)
        for row in rows:
            cumulative_rows.append(row)

    final = pd.DataFrame(cumulative_rows)
    cols = ["Column", "Value", "Count", "Percent", "Frequent Count", "Frequent Percentage", "Infrequent Count", "Infrequent Percentage"]
    final.columns = cols
    
    final.to_csv(path, index=False)

    return final



def prettify(df, path, include_confints=False, r=2):

    def format_na(f):
        if f == 'NA':
            return f
        else:
            return round(f, r)

    def format(row):
        value = str(" ".join(row['Value'].split("_")))
        count = row['Count']
        percent = round(row['Percent'], r)
        frequent_count = round(row['Frequent Count'], r)
        frequent_percentage =  format_na(row['Frequent Percentage'])
        infrequent_count = round(row['Infrequent Count'], r)
        infrequent_percentage =  format_na(row['Infrequent Percentage'])
        
        if (include_confints):
            frequent_upper = format_na(row['Frequent Upper Bound'])
            frequent_lower = format_na(row['Frequent Lower Bound'])
            infrequent_upper = format_na(row['Infrequent Upper Bound'])
            infrequent_lower = format_na(row['Infrequent Lower Bound'])

            return [value, # Value
                f'{count} ({percent}%)',
                f'{frequent_count} ({frequent_percentage}%, {frequent_lower}%-{frequent_upper}%)',
                f'{infrequent_count} ({infrequent_percentage}%, {infrequent_lower}%-{infrequent_upper}%)']
        else:
            return [value, # Value
                f'{count} ({percent}%)',
                f'{frequent_count} ({frequent_percentage}%)',
                f'{infrequent_count} ({infrequent_percentage}%)']

    
    rows = []
    current_column = ''
    for i, row in df.iterrows():
        if row['Column'] != current_column:
            current_column = row['Column']
            rows.append([row['Column']])
        rows.append(format(row))

    data = pd.DataFrame(rows)
    data.columns = ["Category", "Total", "Frequent", "Infrequent"]
    data.to_csv(path,index=False)

def diff_in_prop(x1, n1, x2, n2, alpha_confidence = 0.05, bonferroni=1):
    p1 = x1 / n1
    p2 = x2 / n2

    if min([n1 * p1, n1 * (1 - p1), n2 * p2, n2 * (1 - p2)]) < 5:
        return "Insufficient samples to conduct a difference in proportion test."

    variance_p1 = (p1 * (1 - p1)) / n1
    variance_p2 = (p2 * (1 - p2)) / n2
    pooled_variance = variance_p1 + variance_p2

    mean_estimate = p1 - p2
    cdf_percentile = (1 + (1 - (alpha_confidence / bonferroni))) / 2
    critical_value = stats.norm.ppf(cdf_percentile)

    p_pooled = (x1 + x2) / (n1 + n2)

    r = {}
    r["Conf_Lower"] = mean_estimate - critical_value * sqrt(pooled_variance)
    r["Conf_Middle"] = mean_estimate
    r["Conf_Upper"] = mean_estimate + critical_value * sqrt(pooled_variance)
    return r


def calculate_chi_squared_test_of_independence(df, categories):
    n_tests = len(categories)

    cols = ['Category', 'P-val', 'Adj. P-val','P-val (No Missing)', 'Adj. P-val (No Missing)']
    data = []

    for c in categories:
        full = df[df['Column'] == c]
        # With all values
        full_res = stats.chi2_contingency(
            full[['Frequent Count', 'Infrequent Count']].values, correction=False
        )
        # Without missing values
        no_missing = full[full['Value'] != 'Missing']
        no_missing_res = stats.chi2_contingency(
            no_missing[['Frequent Count', 'Infrequent Count']].values, correction=False
        )

        data.append([
            c,
            full_res.pvalue,
            full_res.pvalue * n_tests,
            no_missing_res.pvalue,
            no_missing_res.pvalue * n_tests])

    chi = pd.DataFrame(data)
    chi.columns = cols
    return chi

def prettify_chi(chi, path, r=3):
    def format(val):
        if val < 0.001:
            return "<.001"
        elif val > 1:
            return "1.000"
        else:
            return str(round(val, r))

    pretty = []
    for i, row in chi.iterrows():
        pretty.append([
            row['Category'],
            format(row['P-val']),
            format(row['Adj. P-val']),
            format(row['P-val (No Missing)']),
            format(row['Adj. P-val (No Missing)'])
        ])
    pretty_df = pd.DataFrame(pretty)
    pretty_df.columns = chi.columns
    pretty_df.to_csv(path, index=False)





def main():
    df = pd.read_csv('data/processed_full.csv')

    # Write summary tables to
    kSummaryPath = "results_v2/summary.csv"
    summary = create_summary(df, kSummaryPath)

    kPrettySummaryPath = "results_v2/pretty_summary.csv"
    prettify(summary, kPrettySummaryPath, include_confints=False, r=2)


    # Conduct Chi-Square Tests of Independence
    of_interest = [
        'Age', 'Gender', 'Race', 'Prior Condition', 'Political Affiliation',
        'Has Primary Care Physician', 'Education', 'Housing Status',
        'Insurance Status', 'Internet', 'News', 'Health Care Professionals',
        'Family or Friends', 'Pamphlets', 'Community Organizations',
        'Coworkers or Classmates', 'Government Health Department', 'Other',
        'No Information',
    ]
    chi = calculate_chi_squared_test_of_independence(summary, of_interest)
    kChiPath = "results_v2/chi.csv"
    prettify_chi(chi, kChiPath, r=3)
    
    





    # final = create_confints(df, frequent, infrequent, path)
    
    # prettify(final, 1)

    # # Test, x1, n1, x2, n2
    # diff_in_prop_test = [
    #     ('Female - Male', 318, 367, 327, 410),
    #     ('Democrat - Republican', 221, 251, 35, 64),
    #     ('Physician - No Physician', 494, 587, 148, 178),
    #     ('Housed - Unhoused', 591, 714, 57, 68),
    #     ('All Single Races - White',
    #         178 + 34 + 145 + 6 + 10 + 5 + 25,
    #         201 + 36 + 159 + 6 + 12 + 5 + 29,
    #         226, 311),
    #     ('Prior Condition - No Prior Condition', 338, 402, 284, 351),
    #     ('High School - Graduate', 262, 303, 78, 102),
    # ]

    # for name, x1, n1, x2, n2 in diff_in_prop_test:
    #     print("-"*30)
    #     print("Difference in proportion test for:", name)
    #     print(diff_in_prop(x1, n1, x2, n2, alpha_confidence=0.05, bonferroni=7))


if __name__ == "__main__":
    main()