from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()
from TCC11_12.automation.models import *

urlpatterns = patterns('TCC11_12.automation.views',
    (r'^client/$', 'client'),
    (r'^cdf_calculation/$', 'cdf_calculation'),
    (r'^report_calculation/$', 'report_calculation'),
    (r'^suspence_calculation/$', 'suspence_calculation'),
    (r'^report/$', 'report'),
    (r'^nonpaymentjobregister/$', 'job_register'),
    (r'^paymentjobregisterreport/$', 'payment_job_register_report'),
    (r'^nonpaymentjobregisterreport/$', 'non_payment_job_register_report'),
    (r'^suspenceclearencereportnocharge/$', 'suspence_clearence_report_no_charge'),
    (r'^suspenceclearencereport/$', 'suspence_clearence_report'),
    (r'^othercharge/$', 'other_charge'),
    (r'^mainregister/$', 'main_register'),
    (r'^suspenceclearenceregister/$', 'suspence_clearence_register'),
    (r'^transport/$', 'transport'),
    (r'^transportbill/$', 'transport_bill'),
    (r'^tada/$', 'ta_da'),
    (r'^tadabill/$', 'ta_da_bill'),
    (r'^suspenceclearence/$', 'suspence_clearence'),
    (r'^proformabill/$', 'proforma_bill'),
    (r'^probill/$', 'pro_bill'),
    (r'^proformabillreport/$', 'proforma_bill_report'),
    (r'^suspence/$', 'suspence'),
    (r'^govprireport/$', 'gov_pri_report'),
    (r'^suspencereport/$', 'suspence_report'),
    (r'^newclient/$', 'newclient'),
    (r'^monthlyreport/$', 'monthly_report'),
    (r'^receipt_report/$', 'receipt_report'),
    (r'^cdfreceipt/$', 'cdf_receipt'),
    (r'^receipt_suspence/$', 'receipt_suspence'),
    (r'^bill/$', 'bill'),
    (r'^cdfbill/$', 'cdf_bill'),
    (r'^dailyreport/$', 'daily_report'),
    (r'^labs', 'lab_report'),
    (r'^oldclient', 'old_client'),
    (r'^proformaregister', 'proforma_register'),
)


urlpatterns += patterns('TCC11_12.automation.views_reuse',
	(r'^clientreport/$', 'client_report'),
	(r'^clientreport/preforma/$', 'preforma'),
)	
