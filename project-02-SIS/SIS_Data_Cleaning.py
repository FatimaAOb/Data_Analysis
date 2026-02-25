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

#ONE. Data Loading & Profiling
print("\n" + "="*40)
print("1. Data Loading & Profiling")
print("="*40)

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

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
#TWO. Data Cleaning
print("\n" + "="*40)
print("2. DATA CLEANING")
print("="*40)

SISdfClean=SISdf.copy()
#1. Fix failing grades for students 1-6
grades_col=['math_grade', 'science_grade', 'english_grade', 'it_grade']

targeted_grades=SISdfClean['Grade']<=6
fixed_records=0

for col in grades_col:
    failing=targeted_grades & (SISdfClean[col]<50)
    fixed_records+=failing.sum()
    SISdfClean.loc[failing,col]=50

print(f"\nAdjusted {fixed_records} failing elementary grades to minimum 50")
print(f"Grades 7-12 failing grades kept as-is (realistic assessment)\n")

#2. Standrized name formatting
SISdfClean['first_name']=SISdfClean['first_name'].str.strip()
SISdfClean['last_name']=SISdfClean['last_name'].str.strip()

#THREE. FEATURE ENGINEERING
print("\n" + "="*40)
print("3. FEATURE ENGINEERING")
print("="*40)

#1 Individual subject pass/fail (50+ is passing)
SISdfClean['math_pass']=(SISdfClean['math_grade']>=50).astype(int)
SISdfClean['science_pass']=(SISdfClean['science_grade']>=50).astype(int)
SISdfClean['english_pass']=(SISdfClean['english_grade']>=50).astype(int)
SISdfClean['it_pass']=(SISdfClean['it_grade']>=50).astype(int)

#2 Average grade across all subjects
SISdfClean['avg_grade']=SISdfClean[grades_col].mean(axis=1)


#3 Attendance metrics
totalScdays=180
SISdfClean['attendance_rate']=((totalScdays-SISdfClean['absence_days'])/totalScdays*100).round(2)
SISdfClean['tardy_rate']=((SISdfClean['tardy_days']/totalScdays)*100).round(2)
SISdfClean['total_attendance_issues'] = SISdfClean['absence_days'] + SISdfClean['tardy_days']

#4 Attendance situation
def attendance_situation(row):
    if row['absence_days']>10:
        return 'Excessive Absence'
    elif row ['tardy_days']>20:
        return 'Excessive Tardiness'
    elif row['total_attendance_issues']>25:
        return 'Tardiness and absence issues'
    else:
        return 'Acceptable'

SISdfClean['attendance_situation']=SISdfClean.apply(attendance_situation, axis=1)

#5 Overall pass/fail status
SISdfClean['pass_status']=np.where(SISdfClean['avg_grade'] >= 50, 'Pass', 'Fail')

#6 Attendance flags
def categorize_attendance(total_issues):
    if total_issues == 0:
        return 'Perfect'
    elif total_issues <= 10:
        return 'Good'
    elif total_issues <= 20:
        return 'Moderate'
    elif total_issues <= 30:
        return 'Concerning'
    else:
        return 'Exessive'

SISdfClean['attendance_category'] = SISdfClean['total_attendance_issues'].apply(categorize_attendance)

#7 Grade Level Grouping
def group_grade_level(grade):
    if grade <= 5:
        return 'Elementary (1-5)'
    elif grade <= 8:
        return 'Middle (6-8)'
    else:
        return 'High (9-12)'

SISdfClean['grade_level_group'] = SISdfClean['Grade'].apply(group_grade_level)


#8 At-risk flag (low attendance + low grades)
SISdfClean['at_risk'] = ((SISdfClean['attendance_rate'] < 85) & (SISdfClean['avg_grade'] < 60)).astype(int)

#9 Intervention flag (attendance concerns)
SISdfClean['needs_intervention'] = (SISdfClean['attendance_situation'] != 'Acceptable').astype(int)

#10 Subject failure count
SISdfClean['failed_subjects'] = (
    (SISdfClean['math_grade'] < 50).astype(int) +
    (SISdfClean['science_grade'] < 50).astype(int) +
    (SISdfClean['english_grade'] < 50).astype(int) +
    (SISdfClean['it_grade'] < 50).astype(int)
)

#11 Best and worst subject per student
SISdfClean['best_subject'] = SISdfClean[grades_col].idxmax(axis=1).str.replace('_grade', '').str.title()
SISdfClean['worst_subject'] = SISdfClean[grades_col].idxmin(axis=1).str.replace('_grade', '').str.title()

#12 Grade variance (consistency indicator)
SISdfClean['grade_variance'] = SISdfClean[grades_col].std(axis=1).round(2)

#13 Performance tier
def performance_tier(avg):
    if avg >= 90:
        return 'Excellent'
    elif avg >= 80:
        return 'Good'
    elif avg >= 70:
        return 'Satisfactory'
    elif avg >= 60:
        return 'Needs Improvement'
    elif avg >=50:
        return 'Passing'
    else:
        return 'Failing'

SISdfClean['performance_tier']=SISdfClean['avg_grade'].apply(performance_tier)

#14 Honor roll flag (avg >= 85 AND all subjects >= 80)
SISdfClean['honor_roll'] = (
    (SISdfClean['avg_grade'] >= 85) &
    (SISdfClean['math_grade'] >= 80) &
    (SISdfClean['science_grade'] >= 80) &
    (SISdfClean['english_grade'] >= 80) &
    (SISdfClean['it_grade'] >= 80)
).astype(int)

#FOUR. VALIDATION & SAVE
print("\n" + "="*40)
print("4. VALIDATION")
print("="*40)

print(f"\nFinal shape: {SISdfClean.shape}")
print(f"Final columns: {len(SISdfClean.columns)} ({len(SISdfClean.columns) - len(SISdf.columns)} new features)")
print(f"Missing values: {SISdfClean.isnull().sum().sum()}")

print(f"\n--- KEY METRICS ---")
print(f"Overall pass rate: {(SISdfClean['pass_status'] == 'Pass').sum() / len(SISdfClean) * 100:.1f}%")
print(f"At-risk students: {SISdfClean['at_risk'].sum()} ({SISdfClean['at_risk'].sum()/len(SISdfClean)*100:.1f}%)")
print(f"Students needing intervention: {SISdfClean['needs_intervention'].sum()} ({SISdfClean['needs_intervention'].sum()/len(SISdfClean)*100:.1f}%)")
print(f"Honor roll students: {SISdfClean['honor_roll'].sum()} ({SISdfClean['honor_roll'].sum()/len(SISdfClean)*100:.1f}%)")

print(f"\n--- SUBJECT PASS RATES ---")
print(f"Math: {SISdfClean['math_pass'].sum() / len(SISdfClean) * 100:.1f}%")
print(f"Science: {SISdfClean['science_pass'].sum() / len(SISdfClean) * 100:.1f}%")
print(f"English: {SISdfClean['english_pass'].sum() / len(SISdfClean) * 100:.1f}%")
print(f"IT: {SISdfClean['it_pass'].sum() / len(SISdfClean) * 100:.1f}%")

print(f"\n--- ATTENDANCE SITUATIONS ---")
print(SISdfClean['attendance_situation'].value_counts())

print(f"\n--- PERFORMANCE TIER DISTRIBUTION ---")
print(SISdfClean['performance_tier'].value_counts())

print(f"\n--- SUBJECT AVERAGES (after adjustment) ---")
print(f"Math: {SISdfClean['math_grade'].mean():.2f}")
print(f"Science: {SISdfClean['science_grade'].mean():.2f}")
print(f"English: {SISdfClean['english_grade'].mean():.2f}")
print(f"IT: {SISdfClean['it_grade'].mean():.2f}")

# Save cleaned data
#SISdfClean.to_csv('STUDENTS_DATA_CLEANED.csv', index=False)
print("\n✓ Cleaned data saved to 'student_data_cleaned.csv'")

print(pd.read_csv("STUDENTS_DATA_CLEANED.csv"))
