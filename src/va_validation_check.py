"""
Virginia early-vote source columns:

county       - locality name
cd           - congressional district of locality
sdl          - Virginia House of Delegates district of locality
sdu          - Virginia Senate district of locality
request_all  - number of mail-in ballots requested
accept_all   - number of accepted mail-in ballots
inperson_all - number of in-person ballots cast
voted_all    - total early votes cast | accept_all + inperson_all
return_rate  - portion of mail-in ballots returned | accept_all / request_all
"""

import pandas as pd

csv_url = 'https://election.lab.ufl.edu/data-downloads/earlyvote/2026/VA_county.csv'

df = pd.read_csv(csv_url)

# the following code conducts validation testing on the new csv file to ensure
# data quality and accuracy

# initalizes validation_results dictionary
validation_results = {}

# checks that all expected columns are inside dataframe

expected_columns = [
    'county', 'cd', 'sdl', 'sdu', 'request_all', 'accept_all', 'inperson_all', 'voted_all', 'return_rate'
]

columns_result = all(
    column in df.columns for column in expected_columns
)

validation_results['expected_columns_test'] = columns_result

# checks that all counties only have one row

unique_localities_test = df['county'].duplicated().any()

unique_localities_result = not unique_localities_test

validation_results['unique_localities_test'] = unique_localities_result

# checks that length of csv to confirm all localities are present
# Virginia contains 133 counties and county-level equivalents

complete_localities_result = (len(df) == 133)

validation_results['complete_localities_test'] = complete_localities_result

# checks that there are no missing values

no_missing_values_result = not df.isna().any().any()

validation_results['no_missing_values_test'] = no_missing_values_result

# checks that all numeric values are nonnegative

numerical_columns = df.select_dtypes(include='number').columns.tolist()

nonnegative_result = (df[numerical_columns] >= 0).all().all()

validation_results['nonnegative_test'] = nonnegative_result

# checks that voted_all = accept_all + inperson_all
voted_all_test = (df['voted_all'] == df['accept_all'] + df['inperson_all'])

voted_all_result = voted_all_test.all()

validation_results['voted_all_test'] = voted_all_result

# checks that return_rate reflects the true returned ratio

# removes extra spaces and symbols from the strings and converts to float type
numeric_return_rate = (df['return_rate'].str.replace(
    r"[%, ]", "", regex=True
).astype(float) / 100).round(4)

return_rate_test = (
    numeric_return_rate 
    == (df['accept_all'] / df['request_all']).round(4)
)

return_rate_result = return_rate_test.all()

validation_results['return_rate_test'] = return_rate_result

# checks whether all validation tests passed
final_validation_check = all(validation_results.values())

# selects the names of any tests that failed
failed_tests = [test_name for test_name, result in validation_results.items()
                if not result]

if final_validation_check == True:
    print(True)
else:
    print("Validation Test Failed.")
    print("The following tests failed:")
    print(failed_tests)