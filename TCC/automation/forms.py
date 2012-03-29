from django import forms
from TCC.automation.choices import *
from TCC.automation.models import *
class MonthlyReport(forms.Form):
	"""
	Montly Report Form to reterive Montly Tax Information.
	"""
	month = forms.ChoiceField(choices=MONTH_CHOICES)
	year = forms.ChoiceField(choices=YEAR_CHOICES)
class Preformaform(forms.Form):
	job_no = forms.IntegerField()
	type_of_report = forms.ChoiceField( choices=PREFORMA_CHOICES)
	
class MonthlyReportadd(forms.Form):
	month = forms.ChoiceField(choices=MONTH_CHOICES)
	year = forms.ChoiceField(choices=YEAR_CHOICES)
	paid_service_tax =forms.IntegerField(initial= '0')
	paid_education_tax =forms.IntegerField(initial= '0')
	paid_higher_education_tax =forms.IntegerField(initial= '0')
	
class GovPriReport(forms.Form):
	"""
	Montly Report for different Jobs like: Government/Semi_government/Private. 
	"""
	month = forms.ChoiceField(choices=MONTH_CHOICES)
	year = forms.ChoiceField(choices=YEAR_CHOICES)
	type_of_organisation =forms.ChoiceField(choices=ORGANISATION_CHOICES)

class SuspenceClearence(forms.Form):
	"""
	Suspence Clearence Form for adding extra Charges. 
	"""
	job_no = forms.IntegerField()
	labour_charge = forms.IntegerField(initial= '0')
	car_taxi_charge = forms.IntegerField(initial= '0')
	boring_charge_external = forms.IntegerField(initial= '0')
	boring_charge_internal = forms.IntegerField(initial= 0)
	lab_testing_staff = forms.CharField(max_length = 20)
	field_testing_staff = forms.CharField(max_length = 20,required=False)
	#suspence_bill_no = forms.CharField(max_length = 15)

class DateReport(forms.Form):
	"""
	Date Report Form to reterive Montly Tax Information.
	"""
	start_day= forms.ChoiceField(choices=DAY_CHOICES)
	start_month = forms.ChoiceField(choices=MONTH_CHOICES)
	start_year = forms.ChoiceField(choices=YEAR_CHOICES)
	end_day= forms.ChoiceField(choices=DAY_CHOICES)
	end_month = forms.ChoiceField(choices=MONTH_CHOICES)
	end_year = forms.ChoiceField(choices=YEAR_CHOICES)

class DailyReport(forms.Form):
	"""
	Daily Report Form to reterive Daily income Information.
	"""
        start_date= forms.DateField()
        end_date= forms.DateField()
        type = forms.ChoiceField( choices=PAYMENT_CHOICES)

class DailyReportadd(forms.Form):
        start_date= forms.DateField()
        end_date= forms.DateField()
        type = forms.ChoiceField( choices=PAYMENT_CHOICES)
        
class LabReport(forms.Form):
	    start_date= forms.DateField()
	    end_date= forms.DateField()
	    lab = forms.ChoiceField(choices=LAB_CHOICES)
            field = forms.ChoiceField(choices=FIELD_CHOICES)

class LabReportadd(forms.Form):
	    start_date= forms.DateField()
	    end_date= forms.DateField()
	    lab = forms.ChoiceField(choices=LAB_CHOICES)
            field = forms.ChoiceField(choices=FIELD_CHOICES)

class OldClient(forms.Form):
            name_and_address = forms.CharField(max_length=3000)

class OldClientadd(forms.Form):
            name_and_address = forms.CharField(max_length=3000)

class PerformaReg(forms.Form):
            start_date= forms.DateField()
	    end_date= forms.DateField()

class PerformaRegadd(forms.Form):
            start_date= forms.DateField()
	    end_date= forms.DateField()
            
