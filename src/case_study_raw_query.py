def query():
    q = """
    with filtered_data as 
(
select *
from dev.gtm.customer_360_v5_hscores
where 
--segment_name in ('Late Volume Plan','Late Savings Plan')
LATEST_EFFECTIVE_ACR between 500000 and 1000000
and SALES_HIER_GEO in ('AMER')
)

-- select distinct SUBSCRIPTION_ACCOUNT_ID, SFDC_ACCOUNT_NAME,segment_name,industry,LATEST_EFFECTIVE_ACR, count(*)
-- from filtered_data
-- group by all;


select * 
from filtered_data 
where SUBSCRIPTION_ACCOUNT_ID in ('1643184', '478028', '2716899', '331786', '975442', '1939509', '675452', '194925', '3407446', '2120507', '2021156', '4133080', '28811', '4233048','2295672','2705945','3109311');
    """
    return q









          