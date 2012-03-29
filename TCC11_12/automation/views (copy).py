# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Max ,Q, Sum
from TCC.automation.convert_function import *
from TCC.automation.functions import *
from TCC.automation.models import *
from TCC.automation.forms import *
from TCC.automation.variable import *

def index(request):
    return render_to_response('index.html',context_instance=RequestContext(request))

   
def newclient(request):
	if request.method == 'POST':
		form = ClientForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			form.save()
		return render_to_response('automation/new_client_ok.html', {'form': form,}, context_instance=RequestContext(request))
	else:
		form = ClientForm()
	return render_to_response('automation/new_client.html', {'form': form}, context_instance=RequestContext(request))

def client(request):
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	maxid = maxid + 1
	if request.method == 'POST':
		form = ClientJobForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			report_type =cd['report_type']
			form.save()
			if report_type=="SUSPENCE":
				return HttpResponseRedirect(reverse('TCC.automation.views.suspence_calculation'))
			else :
				return HttpResponseRedirect(reverse('TCC.automation.views.report_calculation'))
	else:
		form = ClientJobForm()
		return render_to_response('automation/clientjob.html', {'form': form,'maxid':maxid}, context_instance=RequestContext(request))

def job_register(request):
	if request.method == 'POST':
		form = JobRegisterForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			name =cd['name_and_address']
			letter_date =cd['letter_date']
			letter_no = cd ['letter_no']
			material_type = cd['material_type']
			file_disposal = cd['file_disposal']
			phone_no = cd ['phone_no']
			form.save()
			template= {'form': form,'name':name,'letter_date':letter_date,'letter_no':letter_no, 'file_disposal': file_disposal,
			'phone_no' : phone_no , 'material_type':material_type }
		return render_to_response('automation/job_register_ok.html', template, context_instance=RequestContext(request))
	else:
		form = JobRegisterForm()
	return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))

def non_payment_job_register_report(request):
	jobregister = JobRegister.objects.all()
	template ={'jobregister':jobregister}
	return render_to_response('automation/nonpaymentjobregisterreport.html', template, context_instance=RequestContext(request))

def payment_job_register_report(request):
	client = ClientJob.objects.all()
	amount = Amount.objects.all()
	template ={'jobregister':client, 'amount' :amount}
	return render_to_response('automation/paymentjobregisterreport.html', template, context_instance=RequestContext(request))

def proforma_bill(request):
	from TCC.automation.variable import *
	if request.method == 'POST':
		form = ProformabillForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			amount =cd['amount']
			name =cd['name']
			address=cd['address']
			refrence_no =cd['ref_no']
			charges_for =cd['charges_for']
			sample =cd['sample']
			rate =cd['rate']
			transpotation =cd['transpotation']
			form.save()
			service_tax= servicetax * amount
			education_tax = educationtax * amount
			higher_education_tax = highereducationtax * amount
			net_total = amount + higher_education_tax + education_tax + service_tax
			id = Proformabill.objects.aggregate(Max('pro_no'))
			pro_no = id['pro_no__max'] 
			p = ProfromaTax(pro_no = pro_no, service_tax=service_tax, education_tax=education_tax, higher_education_tax=higher_education_tax, total=net_total)
			p.save()
			template ={'form': form,'refrence_no':refrence_no,'address':address,'name':name, 'pro_no':pro_no ,'rate' :rate, 
			'transpotation':transpotation,'amount':amount,'sample':sample,'charges_for':charges_for}
		return render_to_response('automation/proforma_bill_ok.html',template , context_instance=RequestContext(request))
	else:
		form = ProformabillForm()
	return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))
		
def suspence_calculation(request):
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	if request.method == 'POST':
		form =AmountForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			#job_no = cd['job_no']
			total = cd['total']
			lab = cd['lab']
			tds= cd['tds']
			field = cd['field']
			other_field = cd['other_field']
			if field =="OTHER":
				field = other_field
			else :
				field= field
			from TCC.automation.variable import *
			college_income = collegeincome * total / 100
			admin_charge = admincharge * total / 100
			temp = total - college_income - admin_charge
			client = ClientJob.objects.get(job_no=maxid)
			con_type = client.type_of_consultancy
			ratio1 = ratio1(con_type)
			ratio2 = ratio2(con_type)
			consultancy_asst = ratio1 * temp / 100
			development_fund = ratio2 * temp / 100
			service_tax= round(servicetax * total)
			education_tax = round(educationtax * total)
			higher_education_tax = round(highereducationtax * total)
			net_total = total + higher_education_tax + education_tax + service_tax
			balance = net_total - tds
			id = ClientJob.objects.aggregate(Max('job_no'))
			job_no = id['job_no__max'] 
			p = Amount(job_no = job_no ,total=total,lab=lab,tds=tds, net_total=net_total, balance=balance, development_fund=development_fund, 
			service_tax=service_tax, higher_education_tax=higher_education_tax, education_tax=education_tax, field=field,
			college_income = college_income, admin_charge=admin_charge, consultancy_asst=consultancy_asst, other_field = other_field)
			p.save()
	if request.method == 'POST':
		form1 = SuspenceForm(request.POST)
		if form1.is_valid():
			cd = form1.cleaned_data
			type = cd['type']
			check_number = cd['check_number']
			check_dd_date = cd['check_dd_date']
			id = ClientJob.objects.aggregate(Max('job_no'))
			job_no = id['job_no__max']
			s = Suspence( job_no = job_no, type=type,check_number=check_number,check_dd_date=check_dd_date)
			s.save()
		return render_to_response('automation/suspence_ok.html', {'form': form,'maxid': maxid}, context_instance=RequestContext(request))
	else:
		form = AmountForm()
		form1 = SuspenceForm()
	return render_to_response('automation/suspence.html', {'form1': form1,'form': form ,'maxid': maxid}, context_instance=RequestContext(request))
				
def report_calculation(request):
	#from django.db import connection
	#cursor = connection.cursor()
	#cursor.execute('SELECT max(job_no) FROM automation_clientjob')
	#maxid = cursor.fetchone()
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	if request.method == 'POST':
		form =AmountForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			#job_no = cd['job_no']
			total = cd['total']
			lab = cd['lab']
			tds= cd['tds']
			field = cd['field']
			other_field = cd['other_field']
			if field =="OTHER":
				field = other_field
			else :
				field= field
			from TCC.automation.variable import *
			college_income = collegeincome * total / 100
			admin_charge = admincharge * total / 100
			temp = total - college_income - admin_charge
			client = ClientJob.objects.get(job_no=maxid)
			con_type = client.type_of_consultancy
			ratio1 = ratio1(con_type)
			ratio2 = ratio2(con_type)
			consultancy_asst = ratio1 * temp / 100
			development_fund = ratio2 * temp / 100
			service_tax= round(servicetax * total)
			education_tax = round(educationtax * total)
			higher_education_tax = round(highereducationtax * total)
			net_total = total + higher_education_tax + education_tax + service_tax
			balance = net_total - tds
			id = ClientJob.objects.aggregate(Max('job_no'))
			job_no = id['job_no__max'] 
			p = Amount(job_no = job_no ,total=total,lab=lab,tds=tds, net_total=net_total, balance=balance, development_fund=development_fund, 
			service_tax=service_tax, higher_education_tax=higher_education_tax, education_tax=education_tax, field=field, 
			college_income = college_income, admin_charge=admin_charge, consultancy_asst=consultancy_asst, other_field=other_field)
			p.save()
		return render_to_response('automation/job_ok.html', {'form': form, 'maxid':maxid}, context_instance=RequestContext(request))
	else:
		form = AmountForm()
	return render_to_response('automation/job_add.html', {'form': form, 'maxid': maxid}, context_instance=RequestContext(request))
	
def report(request):
	from TCC.automation.functions import *
	from TCC.automation.variable import *
	client = ClientJob.objects.get(job_no=request.GET['job_no'])
	amount = Amount.objects.get(job_no=request.GET['job_no'])
	title = get_object_or_404(Variable, pk='1')
	sub_title = get_object_or_404(Variable, pk='2')
	sign = get_object_or_404(Variable, pk='3')
	con_type = client.type_of_consultancy
	ratio1 = ratio1(con_type)
	ratio2 = ratio2(con_type)
	lab = amount.lab
	job_no = amount.job_no
	net_total1 = amount.net_total
	net_total_eng = num2eng(net_total1)
	teachers = Teachers.objects.all().filter(lab=lab)
	retrieve()
	template = {'job_no': job_no,'net_total_eng':net_total_eng,'sign':sign,'lab' : lab, 'teachers':teachers, 'servicetaxprint':servicetaxprint,
	'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,'client': client,'amount':amount,'title':title,
	'sub_title':sub_title ,'con_type':con_type, 'ratio1':ratio1 ,'ratio2':ratio2,'collegeincome':collegeincome,'admincharge' : admincharge }
	return render_to_response('automation/report.html', template , context_instance=RequestContext(request))

def suspence(request):
	from TCC.automation.variable import *
	client = ClientJob.objects.get(job_no=request.GET['job_no'])
	amount = Amount.objects.get(job_no=request.GET['job_no'])
	suspence = Suspence.objects.get(job_no=request.GET['job_no'])
	title = get_object_or_404(Variable, pk='1')
	sub_title = get_object_or_404(Variable, pk='2')
	sign = get_object_or_404(Variable, pk='3')
	con_type = client.type_of_consultancy
	#amount = get_object_or_404(Amount, pk=job_no_id)
	collegeincome = collegeincome
	admincharge = admincharge
	servicetaxprint = servicetaxprint
	educationtaxprint =educationtaxprint
	highereducationtaxprint = highereducationtaxprint
	lab = amount.lab
	job_no = amount.job_no
	net_total1 = amount.balance
	net_total_eng = num2eng(net_total1)
	template = {'job_no': job_no ,'sign':sign,'suspence':suspence ,'net_total_eng':net_total_eng,'servicetaxprint':servicetaxprint,
	'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,'client': client, 'amount':amount, 'title':title, 
	'sub_title':sub_title ,'collegeincome':collegeincome,'admincharge' : admincharge }
	return render_to_response('automation/suspence_report.html', template , context_instance=RequestContext(request))

def bill(request):
	from TCC.automation.variable import *
	client = ClientJob.objects.get(job_no=request.GET['job_no'])
	amount = Amount.objects.get(job_no=request.GET['job_no'])
	title = get_object_or_404(Variable, pk='1')
	sub_title = get_object_or_404(Variable, pk='2')
	sign = get_object_or_404(Variable, pk='3')
	servicetaxprint = servicetaxprint
	educationtaxprint = educationtaxprint
	highereducationtaxprint = highereducationtaxprint
	job_no = amount.job_no
	net_total1 = amount.net_total
	net_total_eng = num2eng(net_total1)
	template = {'job_no': job_no ,'net_total_eng':net_total_eng,'sign':sign,'servicetaxprint':servicetaxprint,
	'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,'client': client, 'amount':amount, 'title':title,
	'sub_title':sub_title,}
	return render_to_response('automation/bill.html', template , context_instance=RequestContext(request))

def  monthly_report(request):
	if request.method == 'POST':
		form = MonthlyReport(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			month = cd['month']
			year = cd['year']
			month = months(month)
			title = get_object_or_404(Variable, pk='1')
			client = ClientJob.objects.filter(date__year=year).filter(date__month=month)
			amount = Amount.objects.all()
			template ={'form':form, 'title':title,'month': month, 'year':year,'client':client,'amount':amount}
			return render_to_response('automation/monthlyreport.html', template, context_instance=RequestContext(request))
	else:
		form = MonthlyReport()
	return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))

def suspence_report(request):
	if request.method == 'POST':
		form = MonthlyReport(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			month = cd['month']
			year = cd['year']
			month =months(month)
			title = get_object_or_404(Variable, pk='1')
			sign = get_object_or_404(Variable, pk='3')
			client = ClientJob.objects.filter(date__year=year).filter(date__month=month)
			suspence = Suspence.objects.all()
			amount = Amount.objects.all()
			template ={'form':form, 'title':title ,'sign':sign,'month': month, 'year':year,'client':client,'amount':amount,'suspence':suspence}
			return render_to_response('automation/suspencereport.html', template, context_instance=RequestContext(request))
	else:
		form = MonthlyReport()
	return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))


def receipt_report(request):
	"""
	View the Receipt Data In Html format 
	"""
	from TCC.automation.variable import *
	client = ClientJob.objects.get(job_no=request.GET['job_no'])
	amount = Amount.objects.get(job_no=request.GET['job_no'])
	title = get_object_or_404(Variable, pk='1')
	sub_title = get_object_or_404(Variable, pk='2')
	sign = get_object_or_404(Variable, pk='3')
	job_no = amount.job_no
	net_total1 = amount.net_total
	net_total_eng = num2eng(net_total1)
	type = 'CASH'
	template = {'job_no': job_no ,'sign':sign, 'net_total_eng':net_total_eng,'type':type,'client': client, 'amount':amount, 
	'title':title, 'sub_title':sub_title,}
	return render_to_response('automation/receipt.html', template , context_instance=RequestContext(request))

def receipt_suspence(request):
	"""
	View of Receipt Data In Html format 
	"""
	from TCC.automation.variable import *
	client = ClientJob.objects.get(job_no=request.GET['job_no'])
	amount = Amount.objects.get(job_no=request.GET['job_no'])
	suspence = Suspence.objects.get(job_no=request.GET['job_no'])
	title = get_object_or_404(Variable, pk='1')
	sub_title = get_object_or_404(Variable, pk='2')
	sign = get_object_or_404(Variable, pk='3')
	job_no = amount.job_no
	net_total1 = amount.net_total
	net_total_eng = num2eng(net_total1)
	template = {'job_no': job_no ,'sign':sign, 'net_total_eng':net_total_eng,'suspence': suspence,'client': client, 'amount':amount,
	'title':title, 'sub_title':sub_title,}
	return render_to_response('automation/receipt.html', template , context_instance=RequestContext(request))

def proforma_bill_report(request):
	"""
	View of Profroma Bill Report In HTML Format
	"""
	from TCC.automation.variable import *
	proforma_bill =Proformabill.objects.get(pro_no=request.GET['pro_no'])
	proforma_tax = ProfromaTax.objects.get(pro_no=request.GET['pro_no'])
	title = get_object_or_404(Variable, pk='1')
	sub_title = get_object_or_404(Variable, pk='2')
	sign = get_object_or_404(Variable, pk='3')
	pro_no = proforma_bill.pro_no
	net_total1 = proforma_tax.total
	net_total_eng = num2eng(net_total1)
	template = {'pro_no': pro_no,'sign':sign, 'proforma_tax' : proforma_tax,'net_total_eng':net_total_eng,'title':title,'sub_title' :sub_title,
	'proforma_bill': proforma_bill,'servicetaxprint':servicetaxprint,'highereducationtaxprint':highereducationtaxprint,
	'educationtaxprint':educationtaxprint}
	return render_to_response('automation/proformabillreport.html', template , context_instance=RequestContext(request))

def pro_bill(request):
	"""
	View of Profroma Bill  In HTML Format
	"""
	from TCC.automation.variable import *
	proforma_bill = Proformabill.objects.get(pro_no=request.GET['pro_no'])
	proforma_tax = ProfromaTax.objects.get(pro_no=request.GET['pro_no'])
	title = get_object_or_404(Variable, pk='1')
	sub_title = get_object_or_404(Variable, pk='2')
	sign = get_object_or_404(Variable, pk='3')
	pro_no = proforma_bill.pro_no
	net_total1 = proforma_tax.total
	net_total_eng = num2eng(net_total1)
	template = {'pro_no': pro_no ,'proforma_tax' : proforma_tax, 'sign':sign, 'proforma_bill':proforma_bill, 'net_total_eng':net_total_eng,
	'servicetaxprint':servicetaxprint,'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint, 'title':title,
	'sub_title':sub_title,}
	return render_to_response('automation/pro_bill.html', template , context_instance=RequestContext(request))
	
def  gov_pri_report(request):
	if request.method == 'POST':
		form = GovPriReport(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			type_of_organisation =cd['type_of_organisation']
			month = cd['month']
			year = cd['year']
			month = months(month)
			title = get_object_or_404(Variable, pk='1')
			client = ClientJob.objects.filter(date__year=year).filter(date__month=month).filter(type_of_work=type_of_organisation)
			amount = Amount.objects.all()
			template ={'form':form, 'title':title,'month': month, 'year':year, 'client':client,'amount':amount,'servicetaxprint':servicetaxprint,
			'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,'type_of_organisation' : type_of_organisation,
			'collegeincome' : collegeincome , 'admincharge':admincharge }
			return render_to_response('automation/gov_pri_report.html', template, context_instance=RequestContext(request))
	else:
		form = MonthlyReport()
	return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))

def  main_register(request):
	if request.method == 'POST':
		form = MonthlyReport(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			month = cd['month']
			year = cd['year']
			month = months(month)
			title = get_object_or_404(Variable, pk='1')
			client = ClientJob.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT')
			amount = Amount.objects.all()
			template ={'form':form, 'title':title,'month': month, 'year':year, 'client':client,'amount':amount,'servicetaxprint':servicetaxprint,
			'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,'collegeincome' : collegeincome ,
			'admincharge':admincharge }
			return render_to_response('automation/main_register.html', template, context_instance=RequestContext(request))
	else:
		form = MonthlyReport()
	return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))


def transport(request):
	"""
	View of Transport Bill
	"""
	if request.method == 'POST':
		form = TransportForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			job_no =cd['job_no']
			test_date =cd['test_date']
			kilometer =cd['kilometer']
			date =cd ['date']
			bill_no = cd['bill_no']
			rate = cd ['rate']
			form.save()
			data = {'job_no':job_no,'rate':rate, 'kilometer': kilometer,'bill_no':bill_no,'test_date':test_date}
			return render_to_response('automation/transport_ok.html', data,  context_instance=RequestContext(request))
	else:
		form = TransportForm()
	return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))

def ta_da(request):
	"""
	View of TA/DA Bill
	"""
	if request.method == 'POST':
		form = Ta_DaForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			job_no =cd['job_no']
			test_date =cd['test_date']
                        end_date =cd['end_date']
			reach_site =cd['reach_site']
			form.save()
			data = {'job_no':job_no, 'reach_site': reach_site, 'test_date':test_date, 'end_date':end_date}
			return render_to_response('automation/tada_ok.html', data,  context_instance=RequestContext(request))
	else:
		form = Ta_DaForm()
	return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))
	
def ta_da_bill(request):
	"""
	Report of TA/DA Bill For Particular Date
	"""
	tada = Ta_Da.objects.get(job_no=request.GET['job_no'],test_date=request.GET['test_date'])
	client = ClientJob.objects.get(job_no=request.GET['job_no'])
	teachers =Teachers.objects.all().filter(Q(code=tada.testing_staff_code_1)| Q(code=tada.testing_staff_code_2) | Q(code=tada.testing_staff_code_3) 
	| Q(code=tada.testing_staff_code_4) | Q(code=tada.testing_staff_code_5) | Q(code=tada.testing_staff_code_6) | Q(code=tada.testing_staff_code_7) 
	| Q(code=tada.testing_staff_code_8) | Q(code=tada.testing_staff_code_9) | Q(code=tada.testing_staff_code_10) ) 
	daily_income = Teachers.objects.filter(Q(code=tada.testing_staff_code_1)| Q(code=tada.testing_staff_code_2) | Q(code=tada.testing_staff_code_3) 
	| Q(code=tada.testing_staff_code_4) | Q(code=tada.testing_staff_code_5) | Q(code=tada.testing_staff_code_6) | Q(code=tada.testing_staff_code_7) 
	| Q(code=tada.testing_staff_code_8) | Q(code=tada.testing_staff_code_9) | Q(code=tada.testing_staff_code_10) ).aggregate(Sum('daily_income'))
	daily = int(daily_income['daily_income__sum']) 
	Ta_Da.objects.filter(job_no = tada.job_no).update( tada_amount = daily )
	data = {'tada':tada,'client':client,'teachers':teachers, 'daily':daily}
	return render_to_response('automation/ta_da_bill.html', data , context_instance=RequestContext(request))
	
def transport_bill(request):
	"""
	Final Report of Transport Bill
	"""
	transport_old = Transport.objects.get(job_no=request.GET['job_no'])
	client = ClientJob.objects.get(job_no=request.GET['job_no'])
	kilometer = transport_old.kilometer
	temp = [0,0,0,0,0,0,0,0,0,0]
	range = kilometer.split(',')
	i=0
	while i < len(range):
		temp[i] = range[i]
		i+=1
	rate = transport_old.rate
	amount1 = int(temp[0])*rate
	amount2 = int(temp[1])*rate
	amount3 = int(temp[2])*rate
	amount4 = int(temp[3])*rate
	amount5 = int(temp[4])*rate
	amount6 = int(temp[5])*rate
	amount7 = int(temp[6])*rate
	amount8 = int(temp[7])*rate
	amount9 = int(temp[8])*rate
	amount10 = int(temp[9])*rate
	total = amount1 + amount2 + amount3 + amount4 + amount5 + amount6 + amount7 + amount8 + amount9 + amount10
	all_amounts = amount1,amount2,amount3,amount4,amount5,amount6,amount7,amount8,amount9,amount10
	Transport.objects.filter(job_no = transport_old.job_no).update( total = total, amounts = all_amounts )
	transport = Transport.objects.get(job_no=transport_old.job_no)
	title = get_object_or_404(Variable, pk='1')
	sub_title = get_object_or_404(Variable, pk='2')
	sign = get_object_or_404(Variable, pk='3')
	vehical_no = get_object_or_404(Variable, pk='4')
	template ={'transport':transport,'title':title,'sub_title':sub_title, 'vehical_no':vehical_no ,'client':client,'sign':sign}
	return render_to_response('automation/transport_bill.html', template , context_instance=RequestContext(request))

def suspence_clearence(request):
	if request.method == 'POST':
		form = SuspenceClearence(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			job_no =cd['job_no']
			labour_charge =cd['labour_charge']
			car_taxi_charge =cd['car_taxi_charge']
			boring_charge_external=cd['boring_charge_external']
			boring_charge_internal=cd['boring_charge_internal']
			lab_testing_staff=cd['lab_testing_staff']
			suspence_bill_no =cd['suspence_bill_no']
			Suspence.objects.filter(job_no = job_no).update(labour_charge=labour_charge,boring_charge_external=boring_charge_external,suspence_bill_no=suspence_bill_no, 
			boring_charge_internal= boring_charge_internal,car_taxi_charge=car_taxi_charge,lab_testing_staff=lab_testing_staff)
			data = {'job_no' :job_no, 'labour_charge':labour_charge,'boring_charge_external':boring_charge_external,
			'boring_charge_internal': boring_charge_internal,'car_taxi_charge':car_taxi_charge,'lab_testing_staff':lab_testing_staff,
			'suspence_bill_no':suspence_bill_no }
		return render_to_response('automation/suspence_clearence_ok.html', data, context_instance=RequestContext(request))
	else:
		form = SuspenceClearence()
		return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))

def other_charge(request):
	transport = Transport.objects.get(job_no=request.GET['job_no'])
	client = ClientJob.objects.get(job_no=request.GET['job_no'])
	amount = Amount.objects.get(job_no=request.GET['job_no'])
	suspence = Suspence.objects.get(job_no=request.GET['job_no'])
	title = get_object_or_404(Variable, pk='1')
	sub_title = get_object_or_404(Variable, pk='2')
	sign = get_object_or_404(Variable, pk='3')
	tada_temp = Ta_Da.objects.filter(job_no=client.job_no).aggregate(Sum('tada_amount'))
	tada_sum= int(tada_temp['tada_amount__sum']) 
	total = tada_sum + suspence.labour_charge + suspence.car_taxi_charge + suspence.boring_charge_external + transport.total
	total_temp =tada_sum+suspence.labour_charge+suspence.car_taxi_charge+suspence.boring_charge_external
	other =suspence.labour_charge+suspence.car_taxi_charge+suspence.boring_charge_external + transport.total
	data = {'transport' : transport, 'client' :client, 'amount': amount, 'suspence':suspence,'tada_sum':tada_sum,'sign':sign,'title':title,
	'sub_title':sub_title,'total_temp': total_temp, 'total' :total, 'other':other,}
	return render_to_response('automation/other_charge_report.html', data , context_instance=RequestContext(request))

def suspence_clearence_report(request):
	transport = Transport.objects.get(job_no=request.GET['job_no'])
	client = ClientJob.objects.get(job_no=request.GET['job_no'])
	amount = Amount.objects.get(job_no=request.GET['job_no'])
	suspence = Suspence.objects.get(job_no=request.GET['job_no'])
	teachers = Teachers.objects.all()
	title = get_object_or_404(Variable, pk='1')
	sub_title = get_object_or_404(Variable, pk='2')
	sign = get_object_or_404(Variable, pk='3')
	tada_temp = Ta_Da.objects.filter(job_no=client.job_no).aggregate(Sum('tada_amount'))
	tada_sum= int(tada_temp['tada_amount__sum']) 
	field_testing_staff = Ta_Da.objects.filter(job_no=client.job_no)
	temp = suspence.labour_charge+transport.total+suspence.boring_charge_external+suspence.car_taxi_charge
	balance= amount.total - (tada_sum + temp + suspence.boring_charge_internal)
	college_income = round(collegeincome * balance / 100)
	admin_charge = round(admincharge * balance / 100)
	work_charge = round(workcharge * balance / 100)
	balance_temp = balance - college_income - admin_charge -work_charge
	from TCC.automation.functions import *
	con_type = client.type_of_consultancy
	ratio1 = ratio1(con_type)
	ratio2 = ratio2(con_type)
	consultancy_asst = round(ratio1 * balance_temp / 100)
	development_fund = round(ratio2 * balance_temp / 100)
	net_total1 = amount.balance
	net_balance_eng = num2eng(net_total1)
	retrieve()
	Amount.objects.filter(job_no = client.job_no).update( college_income = college_income, admin_charge=admin_charge,
	consultancy_asst=consultancy_asst, development_fund=development_fund )
	data = {'transport' : transport, 'net_balance_eng':net_balance_eng,'teachers':teachers,'servicetaxprint':servicetaxprint,
	'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,'ratio1':ratio1 ,'field_testing_staff':field_testing_staff,
	'job_no':client.job_no,'ratio2':ratio2,'other':temp,'collegeincome':collegeincome,'admincharge' : admincharge ,'client' :client, 'amount': amount,
	'suspence':suspence,'tada_sum':tada_sum,'sign':sign,'title':title,'sub_title':sub_title,}
	return render_to_response('automation/suspence_clearence_report.html', data , context_instance=RequestContext(request))

def suspence_clearence_report_no_charge(request):
	transport = Transport.objects.get(job_no=request.GET['job_no'])
	client = ClientJob.objects.get(job_no=request.GET['job_no'])
	amount = Amount.objects.get(job_no=request.GET['job_no'])
	suspence = Suspence.objects.get(job_no=request.GET['job_no'])
	teachers = Teachers.objects.all()
	title = get_object_or_404(Variable, pk='1')
	sub_title = get_object_or_404(Variable, pk='2')
	sign = get_object_or_404(Variable, pk='3')
	tada_temp = Ta_Da.objects.filter(job_no=client.job_no).aggregate(Sum('tada_amount'))
	tada_sum= int(tada_temp['tada_amount__sum'])
	field_testing_staff = Ta_Da.objects.filter(job_no=client.job_no)
	temp = suspence.labour_charge+transport.total+suspence.boring_charge_external+suspence.car_taxi_charge
	balance= amount.total - (tada_sum + temp + suspence.boring_charge_internal)
	college_income = round(collegeincome * balance / 100)
	admin_charge = round(admincharge * balance / 100)
	balance_temp = balance - college_income - admin_charge 
	from TCC.automation.functions import *
	con_type = client.type_of_consultancy
	ratio1 = ratio1(con_type)
	ratio2 = ratio2(con_type)
	consultancy_asst = round(ratio1 * balance_temp / 100)
	development_fund = round(ratio2 * balance_temp / 100)
	net_total1 = amount.balance
	net_balance_eng = num2eng(net_total1)
	retrieve()
	data = {'transport' : transport, 'net_balance_eng':net_balance_eng,'teachers':teachers,'servicetaxprint':servicetaxprint,
	'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,'ratio1':ratio1 ,'field_testing_staff':field_testing_staff,
	'job_no':client.job_no,'ratio2':ratio2,'other':temp,'collegeincome':collegeincome,'admincharge' : admincharge ,'client' :client, 'amount': amount,
	'suspence':suspence,'tada_sum':tada_sum,'sign':sign,'title':title,'sub_title':sub_title,}
	return render_to_response('automation/suspence_clearence_report_no_charge.html', data , context_instance=RequestContext(request))

def client_report(request):
	"""
	View of All Clients Report Form.
	"""
	if request.method == 'POST':
		form = ClientReportForm(request.POST)
		if form.is_valid():
			from TCC.automation.functions import *
			from TCC.automation.variable import *
			cd = form.cleaned_data
			job_no = cd['job_no']
			type_of_report = cd['type_of_report']
			client = ClientJob.objects.get(job_no=job_no)
			amount = Amount.objects.get(job_no=job_no)
			title = get_object_or_404(Variable, pk='1')
			sub_title = get_object_or_404(Variable, pk='2')
			sign = get_object_or_404(Variable, pk='3')
			con_type = client.type_of_consultancy
			ratio1 = ratio1(con_type)
			ratio2 = ratio2(con_type)
			lab = amount.lab
			net_total1 = amount.balance
			net_total_eng = num2eng(net_total1)
			teachers = Teachers.objects.all().filter(lab=lab)
			retrieve()
			if type_of_report =="GENERAL REPORT":
				template = {'form': form,'job_no': job_no,'net_total_eng':net_total_eng,'lab' : lab,'sign':sign, 'teachers':teachers,
				'servicetaxprint':servicetaxprint,'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,
				'client': client, 'amount':amount, 'title':title, 'sub_title':sub_title ,'con_type':con_type, 'ratio1':ratio1 ,'ratio2':ratio2,
				'collegeincome':collegeincome,'admincharge' : admincharge }
				return render_to_response('automation/report.html', template, context_instance=RequestContext(request))
			elif type_of_report =="SUSPENCE":
				template = {'job_no': job_no ,'net_total_eng':net_total_eng,'sign':sign,'servicetaxprint':servicetaxprint,
				'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,'client': client, 'amount':amount,
				'title':title, 'sub_title':sub_title ,'collegeincome':collegeincome,'admincharge' : admincharge }
				return render_to_response('automation/suspence_report.html', template , context_instance=RequestContext(request))
			elif type_of_report =="BILL":
				template = {'job_no': job_no ,'net_total_eng':net_total_eng,'sign':sign,'servicetaxprint':servicetaxprint,
				'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,'client': client, 'amount':amount,
				'title':title, 'sub_title':sub_title,}
				return render_to_response('automation/bill.html', template , context_instance=RequestContext(request))
			elif type_of_report =="RECEIPT SUSPENCE":
				suspence = Suspence.objects.get(job_no=job_no)
				template = {'job_no': job_no ,'net_total_eng':net_total_eng,'suspence':suspence,'client': client, 'amount':amount, 'title':title,
				'sub_title':sub_title,}
				return render_to_response('automation/receipt.html', template , context_instance=RequestContext(request))				
			elif type_of_report =="RECEIPT GENERAL":
				type = 'CASH'
				template = {'job_no': job_no ,'type':type,'net_total_eng':net_total_eng,'sign':sign,'client': client, 'amount':amount, 'title':title,
				'sub_title':sub_title,}
				return render_to_response('automation/receipt.html', template , context_instance=RequestContext(request))				
	else:
		form = ClientReportForm()
	return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))



