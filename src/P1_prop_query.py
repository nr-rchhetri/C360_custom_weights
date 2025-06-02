def query():
    q = """
WITH
-- Base table with all monthly BCM data using proper last day handling
monthly_data AS (
    SELECT
        --SUBSCRIPTION_ACCOUNT_ID,
        sfdc_account_name,
        sfdc_account_id,
        buying_program,
        contract_start_date,
        DATE_TRUNC('month', report_as_of_dt) AS month_start,
        LAST_DAY(DATE_TRUNC('month', report_as_of_dt)) AS month_end,
        adj_mthly_fcst_consumption_eff_amt AS bcm,
        -- Calculate months elapsed since contract start
        DATEDIFF('month', contract_start_date, report_as_of_dt) AS months_since_contract_start
    FROM reporting.consumption_metrics.consumption_daily_metrics
    WHERE report_as_of_dt = LAST_DAY(DATE_TRUNC('month', report_as_of_dt))  -- Ensuring we take month-end data
    AND report_as_of_dt >='2023-01-01'
),
-- For each month and account, find future months (m+3, m+6, m+12) if they exist
bcm_changes AS (
    SELECT
        --base.SUBSCRIPTION_ACCOUNT_ID,
        base.sfdc_account_name,
        base.sfdc_account_id,
        base.buying_program,
        base.contract_start_date,
        base.months_since_contract_start,
        base.month_start AS base_month_start,
        base.month_end AS base_month_end,
        base.bcm AS base_bcm,
        -- M+3 data
        future_m3.month_start AS month_plus_3_start,
        future_m3.month_end AS month_plus_3_end,
        future_m3.bcm AS bcm_plus_3,
        future_m3.months_since_contract_start AS months_since_contract_start_m3,
        COALESCE(future_m3.bcm, 0) - base.bcm AS absolute_change_m3,
        CASE
            WHEN base.bcm = 0 OR base.bcm IS NULL THEN NULL
            ELSE ROUND(((COALESCE(future_m3.bcm, 0) - base.bcm) / NULLIF(base.bcm, 0)) * 100, 2)
        END AS percentage_change_m3,
        -- M+6 data
        future_m6.month_start AS month_plus_6_start,
        future_m6.month_end AS month_plus_6_end,
        future_m6.bcm AS bcm_plus_6,
        future_m6.months_since_contract_start AS months_since_contract_start_m6,
        COALESCE(future_m6.bcm, 0) - base.bcm AS absolute_change_m6,
        CASE
            WHEN base.bcm = 0 OR base.bcm IS NULL THEN NULL
            ELSE ROUND(((COALESCE(future_m6.bcm, 0) - base.bcm) / NULLIF(base.bcm, 0)) * 100, 2)
        END AS percentage_change_m6,
        -- M+12 data
        future_m12.month_start AS month_plus_12_start,
        future_m12.month_end AS month_plus_12_end,
        future_m12.bcm AS bcm_plus_12,
        future_m12.months_since_contract_start AS months_since_contract_start_m12,
        COALESCE(future_m12.bcm, 0) - base.bcm AS absolute_change_m12,
        CASE
            WHEN base.bcm = 0 OR base.bcm IS NULL THEN NULL
            ELSE ROUND(((COALESCE(future_m12.bcm, 0) - base.bcm) / NULLIF(base.bcm, 0)) * 100, 2)
        END AS percentage_change_m12
    FROM monthly_data base
    LEFT JOIN monthly_data future_m3
        ON base.sfdc_account_id = future_m3.sfdc_account_id 
        AND base.sfdc_account_name = future_m3.sfdc_account_name
        AND future_m3.month_start = DATEADD('month', 3, base.month_start)
    LEFT JOIN monthly_data future_m6
        ON base.sfdc_account_id = future_m6.sfdc_account_id
        AND base.sfdc_account_name = future_m6.sfdc_account_name
        AND future_m6.month_start = DATEADD('month', 6, base.month_start)
    LEFT JOIN monthly_data future_m12
        ON base.sfdc_account_id = future_m12.sfdc_account_id
        AND base.sfdc_account_name = future_m12.sfdc_account_name
        AND future_m12.month_start = DATEADD('month', 12, base.month_start)
),
-- Enhanced bucketed analysis with contract duration insights
bucketed_analysis AS (
    SELECT
        sfdc_account_id,
        sfdc_account_name,
        buying_program,
        contract_start_date,
        months_since_contract_start,
        base_month_start,
        base_month_end,
        base_bcm,
        -- Contract phase categorization
        CASE
            WHEN months_since_contract_start < 3 THEN 'Initial Phase (0-3 months)'
            WHEN months_since_contract_start < 6 THEN 'Early Phase (3-6 months)'
            WHEN months_since_contract_start < 12 THEN 'Mid Phase (6-12 months)'
            WHEN months_since_contract_start < 24 THEN 'Mature Phase (1-2 years)'
            ELSE 'Long-term (>2 years)'
        END AS contract_phase,
        -- M+3 data and enhanced buckets
        month_plus_3_end,
        bcm_plus_3,
        -- months_since_contract_start_m3,
        absolute_change_m3,
        percentage_change_m3,
        CASE
            WHEN month_plus_3_start IS NULL THEN 'No Future Data'
            WHEN percentage_change_m3 IS NULL THEN 'No Initial BCM'
            WHEN percentage_change_m3 <= -50 THEN 'Severe Decline (>50% loss)'
            WHEN percentage_change_m3 <= -20 THEN 'Significant Decline (20-50% loss)'
            WHEN percentage_change_m3 < 0 THEN 'Moderate Decline (<20% loss)'
            WHEN percentage_change_m3 = 0 THEN 'No Change'
            WHEN percentage_change_m3 <= 20 THEN 'Moderate Growth (<20% gain)'
            WHEN percentage_change_m3 <= 50 THEN 'Significant Growth (20-50% gain)'
            ELSE 'Exceptional Growth (>50% gain)'
        END AS m3_change_bucket,
        -- M+6 data and enhanced buckets
        month_plus_6_end,
        bcm_plus_6,
        -- months_since_contract_start_m6,
        absolute_change_m6,
        percentage_change_m6,
        CASE
            WHEN month_plus_6_start IS NULL THEN 'No Future Data'
            WHEN percentage_change_m6 IS NULL THEN 'No Initial BCM'
            WHEN percentage_change_m6 <= -50 THEN 'Severe Decline (>50% loss)'
            WHEN percentage_change_m6 <= -20 THEN 'Significant Decline (20-50% loss)'
            WHEN percentage_change_m6 < 0 THEN 'Moderate Decline (<20% loss)'
            WHEN percentage_change_m6 = 0 THEN 'No Change'
            WHEN percentage_change_m6 <= 20 THEN 'Moderate Growth (<20% gain)'
            WHEN percentage_change_m6 <= 50 THEN 'Significant Growth (20-50% gain)'
            ELSE 'Exceptional Growth (>50% gain)'
        END AS m6_change_bucket,
        -- M+12 data and enhanced buckets
        month_plus_12_end,
        bcm_plus_12,
        -- months_since_contract_start_m12,
        absolute_change_m12,
        percentage_change_m12,
        CASE
            WHEN month_plus_12_start IS NULL THEN 'No Future Data'
            WHEN percentage_change_m12 IS NULL THEN 'No Initial BCM'
            WHEN percentage_change_m12 <= -50 THEN 'Severe Decline (>50% loss)'
            WHEN percentage_change_m12 <= -20 THEN 'Significant Decline (20-50% loss)'
            WHEN percentage_change_m12 < 0 THEN 'Moderate Decline (<20% loss)'
            WHEN percentage_change_m12 = 0 THEN 'No Change'
            WHEN percentage_change_m12 <= 20 THEN 'Moderate Growth (<20% gain)'
            WHEN percentage_change_m12 <= 50 THEN 'Significant Growth (20-50% gain)'
            ELSE 'Exceptional Growth (>50% gain)'
        END AS m12_change_bucket,
        -- Enhanced account status with pattern detection
        CASE
            WHEN percentage_change_m3 < -20 AND percentage_change_m6 < -20 AND percentage_change_m12 < -20 THEN 'Consistent Decline'
            WHEN percentage_change_m3 < -20 OR percentage_change_m6 < -30 OR percentage_change_m12 < -40 THEN 'At-risk Account'
            WHEN percentage_change_m3 > 20 AND percentage_change_m6 > 20 AND percentage_change_m12 > 20 THEN 'Consistent Growth'
            WHEN percentage_change_m3 > 20 AND percentage_change_m6 > 15 AND percentage_change_m12 > 10 THEN 'Growing Account'
            WHEN ABS(COALESCE(percentage_change_m3, 0)) < 5 AND ABS(COALESCE(percentage_change_m6, 0)) < 10 THEN 'Stable Account'
            WHEN percentage_change_m3 < 0 AND percentage_change_m6 > 0 AND percentage_change_m12 > 0 THEN 'Recent Decline After Growth'
            WHEN percentage_change_m3 > 0 AND percentage_change_m6 < 0 AND percentage_change_m12 < 0 THEN 'Recent Recovery After Decline'
            ELSE 'Normal Fluctuation'
        END AS account_status,
        -- Adding quarter and year info for easier grouping
        EXTRACT(YEAR FROM base_month_end) AS base_year,
        EXTRACT(QUARTER FROM base_month_end) AS base_quarter,
        -- Data completeness indicator (enhanced)
        CASE
            WHEN month_plus_3_start IS NOT NULL AND month_plus_6_start IS NOT NULL AND month_plus_12_start IS NOT NULL THEN 'Complete'
            WHEN month_plus_3_start IS NOT NULL AND month_plus_6_start IS NOT NULL THEN 'Partial (m+3, m+6)'
            WHEN month_plus_3_start IS NOT NULL THEN 'Minimal (m+3 only)'
            ELSE 'No Future Data'
        END AS data_completeness,
        -- Trend indicator (direction of change across time horizons)
        CASE
            WHEN month_plus_3_start IS NULL OR month_plus_6_start IS NULL OR month_plus_12_start IS NULL THEN 'Incomplete Data'
            WHEN percentage_change_m3 > percentage_change_m6 AND percentage_change_m6 > percentage_change_m12 THEN 'Accelerating Growth'
            WHEN percentage_change_m3 < percentage_change_m6 AND percentage_change_m6 < percentage_change_m12 THEN 'Decelerating Growth'
            WHEN percentage_change_m3 < 0 AND percentage_change_m6 < 0 AND percentage_change_m12 < 0
                 AND percentage_change_m3 < percentage_change_m6 AND percentage_change_m6 < percentage_change_m12 THEN 'Accelerating Decline'
            WHEN percentage_change_m3 < 0 AND percentage_change_m6 < 0 AND percentage_change_m12 < 0
                 AND percentage_change_m3 > percentage_change_m6 AND percentage_change_m6 > percentage_change_m12 THEN 'Decelerating Decline'
            WHEN percentage_change_m3 > 0 AND percentage_change_m6 < 0 THEN 'Recent Recovery'
            WHEN percentage_change_m3 < 0 AND percentage_change_m6 > 0 THEN 'Recent Decline'
            ELSE 'Mixed Pattern'
        END AS trend_pattern
    FROM bcm_changes
),
-- Final result with contract insights and buying program analysis
insights as (
SELECT
    bucketed_analysis.*,
    -- Growth rate normalization (annualized rate for easier comparison)
    CASE
        WHEN percentage_change_m12 IS NOT NULL THEN percentage_change_m12
        WHEN percentage_change_m6 IS NOT NULL THEN percentage_change_m6 * 2
        WHEN percentage_change_m3 IS NOT NULL THEN percentage_change_m3 * 4
        ELSE NULL
    END AS annualized_growth_rate,
    -- Contract lifecycle flag
    CASE
        WHEN months_since_contract_start < 3 AND percentage_change_m3 > 50 THEN 'Early Adopter (High Growth)'
        WHEN months_since_contract_start < 3 AND percentage_change_m3 < 0 THEN 'Early Struggler (Negative Growth)'
        WHEN months_since_contract_start >= 12 AND ABS(COALESCE(percentage_change_m3, 0)) < 10
             AND ABS(COALESCE(percentage_change_m6, 0)) < 10 THEN 'Stable Mature Contract'
        WHEN months_since_contract_start >= 24 AND percentage_change_m12 > 20 THEN 'Long-term High Performer'
        WHEN months_since_contract_start >= 24 AND percentage_change_m12 < -20 THEN 'Long-term Declining Contract'
        ELSE 'Normal Contract Progression'
    END AS contract_lifecycle_indicator
FROM bucketed_analysis
where buying_program in ('Savings Plan','Volume Plan')),
-- AND sfdc_account_name IN ('Tesco PLC', 'McDonald''s Corporation (Account/User Management Tool)', 'DAYTONA INTERNATIONAL', 'Adobe Systems Incorporated - Master')),

latest_priority as (
select c.case_id, DATE_TRUNC('month', created_date) as case_creation_month,
        coalesce(priority_at_case_creation.first_priority,c.priority) as first_priority
from ea_reporting.gtm_analytics.fct_all_support_cases c
 
    left join (select distinct case_id,   
                      first_value(old_value) over (partition by case_id order by created_date desc) as first_priority 
                from conformed.sfdc.stg_sfdc_case_history
                where field = 'Priority'
                ) priority_at_case_creation on c.case_id = priority_at_case_creation.case_id
    where c.created_date >= '2023-01-01'
   ),

accnt_level_tickets as 
( select DATE_TRUNC('month', c.created_date) as case_creation_month,c.sf_account_id,c.sf_account_name,
c.case_id, 
p.first_priority 
from ea_reporting.gtm_analytics.fct_all_support_cases c
    left join latest_priority as p on c.case_id = p.case_id
    where c.created_date >= '2023-01-01'
),

prop_P1_tickets as (
select a.sf_account_id,a.sf_account_name, 
a.case_creation_month,
sum(case when a.first_priority = 'P1' then 1 else 0 end) as cnt_P1,
sum(case when a.first_priority is not null then 1 else 0 end) as total_cases,
(cnt_P1*100.00/total_cases) as pct_P1_cases
from accnt_level_tickets a
group by all
having total_cases > 1
)


select i.*,
p.cnt_P1,
p.total_cases,
p.pct_P1_cases

from insights i
join prop_P1_tickets p
on p.sf_account_id = i.sfdc_account_id
and p.sf_account_name = i.sfdc_account_name
and p.case_creation_month = i.base_month_start;
"""
    return q









          