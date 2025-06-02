def query():
    q = """
select SUBSCRIPTION_ACCOUNT_ID, EFFECTIVE_SUBSCRIPTION_ACCOUNT_ID, sfdc_account_name,buying_program,DATE_TRUNC('month', report_as_of_dt) as bcm_month,
mthly_fcst_consumption_eff_amt as bcm, act_acr as contract_value
from reporting.consumption_metrics.consumption_daily_metrics
where report_as_of_dt = last_day(report_as_of_dt)
and report_as_of_dt >='2024-01-01'
    """
    return q









          