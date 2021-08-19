# PACKAGE IMPORT
import pandas as pd
import matplotlib.pyplot as plt

# Exploring the Stanford Open Policing Project dataset and analyze the impact of gender on police behavior using Pandas.
# Dataset from: https://openpolicing.stanford.edu/data/
# Analysis based on DataCamp course
# City Analyzed: New Orleans

# READ DATASET
dataset = pd.read_csv('la_new_orleans_2020_04_01.csv')

# DATAFRAME INSPECTION
#print(dataset.head())
# COUNTING THE NUMBER OF MISSING VALUES
#dataset.isnull().sum()
# EXAMINING THE SHAPE OF THE DATAFRAME
#print(dataset.shape)

# SELECT RELEVANT COLUMNS
columns = ['date','time','location','subject_race','subject_sex','arrest_made', 'outcome',
           'frisk_performed', 'search_conducted', 'reason_for_stop',
           'contraband_drugs']

# DATAFRAME COLUMNS UPDATE
dataset = dataset[columns]

# CHECK THE MISSING VALUES AGAIN
#print(dataset.isnull().sum())

# DROP ALL ROWS THAT ARE MISSING SUBJECT_SEX
dataset.dropna(subset=['subject_sex'], inplace=True)
# FILL MISSING VALUES WITH FALSE
dataset.contraband_drugs.fillna(False, inplace=True)

# CONCATENATE A STOP DATE AND TIME
combined = dataset.date.str.cat(dataset.time, sep=' ')
dataset['stop_datetime'] = pd.to_datetime(combined)


# CHANGE THE DATA TYPE TO CORRECT ONES
dataset['arrest_made'] = dataset.arrest_made.astype('bool')
dataset['frisk_performed'] = dataset.frisk_performed.astype('bool')
dataset['contraband_drugs'] = dataset.contraband_drugs.astype('bool')

# SET STOP_DATETIME AS THE DATAFRAME INDEX
dataset.set_index('stop_datetime', inplace=True)

# COMPARING THE VIOLATIONS BY GENDER
# COUNT THE UNIQUE VALUES IN VIOLATION
print(dataset.reason_for_stop.value_counts(normalize=True))

# CREATE DATASETS BY GENDER
female = dataset[dataset.subject_sex == 'female']
male = dataset[dataset.subject_sex == 'male']
# PRINT THE RESULTS
print(female.reason_for_stop.value_counts(normalize=True))
print(male.reason_for_stop.value_counts(normalize=True))

# DOES GENDER AFFECT WHO GETS A TICKET FOR SPEEDING?
female_and_speeding = dataset[(dataset.subject_sex == 'female') & (dataset.reason_for_stop == 'Speeding')]
male_and_speeding = dataset[(dataset.subject_sex == 'male') & (dataset.reason_for_stop == 'Speeding')]
# PRINT THE RESULTS
print(female.outcome.value_counts(normalize=True))
print(male.outcome.value_counts(normalize=True))

# DOES GENDER AFFECT WHOSE VEHICLE IS SEARCHED?
# CALCULATE THE SEARCH RATE BY COUNTING THE VALUES
print(dataset.search_conducted.value_counts(normalize=True))
# CALCULATE THE SEARCH RATE BY TAKING THE MEAN
print(dataset.search_conducted.mean())
# CALCULATE THE SEARCH RATE FOR FEMALE DRIVERS
print(dataset[dataset.subject_sex == 'female'].search_conducted.mean())
# CALCULATE THE SEARCH RATE FOR EACH COMBINATION OF GENDER AND VIOLATION
print(dataset.groupby(['subject_sex', 'reason_for_stop']).search_conducted.mean())

# DOES GENDER AFFECT WHO IS FRISKED DURING A SEARCH?
# TAKE THE SUM OF FRISK
dataset.frisk_performed.sum()

# CREATE A DATAFRAME OF STOPS IN WHICH A SEARCH WAS CONDUCTED
searched = dataset[dataset.search_conducted == True]
# CALCULATE THE OVERAL FRISK RATE BY TAKING THE MEAN OF FRISK
print(searched.frisk_performed.mean())
# CALCULATE THE FRISK RATE FOR EACH GENDER
print(searched.groupby('subject_sex').frisk_performed.mean())

# DOES TIME OF DAY AFFECT ARREST RATE?
# CALCULATE OVERAL ARREST RATE
print(dataset.arrest_made.mean())
# CALCULATE HOURLY ARREST RATE
print(dataset.groupby(dataset.index.hour).arrest_made.mean())
# SAVE THE RESULT HOURLY ARREST RATE
hourly_arrest_rate = dataset.groupby(dataset.index.hour).arrest_made.mean()

# CREATE A LINE PLOT OF HOURLY ARREST RATE
hourly_arrest_rate.plot()
# ADD THE XLABEL, YLABEL, AND TITLE
plt.xlabel('Hour')
plt.ylabel('Arrest Rate')
plt.title('Arrest Rate by Time of Day')
# DISPLAY THE PLOT
plt.show()

# ARE DRUG-RELATED STOPS ON THE RISE?
# CALCULATE THE ANNUAL RATE OF DRUG-RELATED STOPS
print(dataset.contraband_drugs.resample('A').mean())
# SAVE THE ANNUAL RATE OF DRUG-RELATED STOPS
annual_drug_rate = dataset.contraband_drugs.resample('A').mean()
# CREATE A LINE PLOT OF ANNUAL DRUG RATE
annual_drug_rate.plot()
# DISPLAY THE PLOT
plt.show()

# DOES THE DRUG RATE INCREASES BECAUSE OF THE SEARCH INCREASING?
# CALCULATE AND SAVE THE ANNUAL SEARCH RATE
annual_search_rate = dataset.search_conducted.resample('A').mean()
# CONCATENATE ANNUAL_DRUG_RATE AND ANNUAL SEARCH RATE
annual = pd.concat([annual_drug_rate, annual_search_rate], axis='columns')
# CREATE SUBPLOTS FROM ANNUAL
annual.plot(subplots=True)
# DISPLAY THE SUBPLOTS
plt.show()

# WHAT VIOLATIONS ARE CAUGHT BY GENDER?
# CREATE A FREQUENCY TABLE OF GENDER AND VIOLATIONS
#print(pd.crosstab(dataset.subject_sex, dataset.reason_for_stop))
# SAVE THE FREQUENCY TABLE AS VIOLATION BY GENDER
violation_by_gender = pd.crosstab(dataset.reason_for_stop, dataset.subject_sex)
# CREATE A BAR PLOT OF VIOLATION BY GENDER
violation_by_gender.plot(kind='barh')
plt.xlabel('Amount')
plt.ylabel('Reason for Stop')
plt.title('Violation Rate by Gender')
# DISPLAY THE PLOT
plt.plot()