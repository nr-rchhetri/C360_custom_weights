def query():
    q = """
    with filtered_data as 
(
select *
from dev.gtm.customer_360_v5_hscores
where 
 LATEST_EFFECTIVE_ACR between 500000 and 1000000
and SALES_HIER_GEO in ('AMER')
),
min_accnt_date as 
(
select SUBSCRIPTION_ACCOUNT_ID, SFDC_ACCOUNT_NAME, min(subscription_term_start_date) as min_sub_date
from dev.gtm.customer_360_v5_hscores
group by SUBSCRIPTION_ACCOUNT_ID, SFDC_ACCOUNT_NAME
),
segments as (
select DATEDIFF(MONTH, m.min_sub_date, current_date()) as accnt_age_mths, f.*,
 CASE WHEN DATEDIFF(MONTH, m.min_sub_date, current_date()) <=6 AND latest_buying_program = 'Volume Plan' THEN 'Early Volume Plan'
     WHEN DATEDIFF(MONTH, m.min_sub_date, current_date()) > 6 AND latest_buying_program = 'Volume Plan' THEN 'Late Volume Plan'
     WHEN DATEDIFF(MONTH, m.min_sub_date, current_date()) <= 6 AND latest_buying_program = 'Savings Plan' THEN 'Early Savings Plan'
     WHEN DATEDIFF(MONTH, m.min_sub_date, current_date()) > 6 AND latest_buying_program = 'Savings Plan' THEN 'Late Savings Plan'
     WHEN latest_buying_program = 'PAYG' THEN 'PAYG' ELSE 'Others' END AS segment_name

from filtered_data f
left join min_accnt_date m
on f.SUBSCRIPTION_ACCOUNT_ID = m.SUBSCRIPTION_ACCOUNT_ID
and f.SFDC_ACCOUNT_NAME = m.SFDC_ACCOUNT_NAME
)

select *
from segments
where segment_name in ('Late Volume Plan','Late Savings Plan')
and SUBSCRIPTION_ACCOUNT_ID in ('478028') ;


--select * 
--from filtered_data 
--where SUBSCRIPTION_ACCOUNT_ID in ('1643184', '478028', '2716899', '331786', '975442', '1939509', '675452', '194925', '3407446', '2120507', '2021156', '4133080', '28811', '4233048','2295672','2705945','3109311');
    """
    return q









          