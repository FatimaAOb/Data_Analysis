"""Students data cleaning

Data source: Mockaroo
Records: 1000 students, Grades 1-12

Data quality issues identifed
refer to: SIS_Data_Profiling.sql:
1. Failing grades for grade levels 1-6, from 0-49, all should be pushed to 50

Cleaning decisions:
1. Grade adjustment: Elementary (1-6) failing grades (0-49) bumped to 50 (minimum passing)
2. Middle/High (7-12) failing grades kept as-is (realistic consequences)
3. Attendance flags based on intervention thresholds
4. Individual subject pass/fail tracking"""

import pandas as pd
import numpy as np

#1. Data Loading & Profiling

SISdf=pd.read_csv("STUDENTS_DATA.csv")
print(f"\nIntial shape: {SISdf.shape}")
print(f"\nColumn names: {SISdf.columns.tolist()}")
print(f"\nData types:\n {SISdf.dtypes}")
print(f"\nMissing values:\n {SISdf.isnull().sum()}")
print(f"\nDuplicates: {SISdf.duplicated().sum()}")

print(f"\nGrade level range: {SISdf['Grade'].min()} - {SISdf['Grade'].max()}")
print(f"\nAbsence range: {SISdf['absence_days'].min()} - {SISdf['absence_days'].max()}")
print(f"\nTardy range: {SISdf['tardy_days'].min()} - {SISdf['tardy_days'].max()}")
print(f"\nGender distribution:\n {SISdf['gender'].value_counts()}")


#2. Data Cleaning