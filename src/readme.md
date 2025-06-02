---
applyTo: '/Users/rchhetri/Downloads/CSAT_NPS/src/health_score.ipynb'
title: 'Project guidelines to create health scores from raw data'
description: 'use the list cols to convert
perform the following steps.
for each of the columns create a new normalized score column based on the raw values in the actual column.
name the new column as oldcolumn_hscore
use the following logic:
calculate the 5th pctile and the 95th percentile for each column. ( consider non null values only)
for all scores above 95th percentile in each column, cap it to 100.
for all other raw scores try to map each raw score to an appropriate monotonic number from 0-100.
for below 5pctile cap it to 0.

for certain columns like
['PCT_P1_CASES','PCT_P1P2_CASES','MTHLY_FTTR_50', 'churn_risk_score', 'MAXIMUM_DAYS_PAST_DUE',
'SUM_TOTAL_AMOUNT_DUE',
'NUMBER_OF_OPEN_INVOICES_DUE_BEFORE_MONTH_END'] the health scores should be mapped in descending order. a high churn risk should correspond to lower health score '
keywords: 'AI, guidelines, coding standards, domain knowledge'  

---
Coding standards, domain knowledge, and preferences that AI should follow.