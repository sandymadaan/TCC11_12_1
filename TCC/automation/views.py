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
from TCC.automation.choices import *
from django.db.models import F
from django.db.models import Q

def index(request):
    return render_to_response('index.html',context_instance=RequestContext(request))

def newclient(request):
	if request.method == 'POST':
		form = ClientForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			name = cd['name']
			address_1 = cd['address_1']
			address_2 = cd['address_2']
			city = cd['city']
			pin_code = cd['pin_code']
			state =cd['state']
			email = cd['email']
			website = cd['website']
			contact_no = cd['contact_no']
			type_of_organisation =cd['type_of_organisation']
			form.save()
		return render_to_response('automation/new_client_ok.html', {'form': form,}, context_instance=RequestContext(request))
	else:
		form = ClientForm()
	return render_to_response('automation/new_client.html', {'form': form}, context_instance=RequestContext(request))

def search(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(name__icontains=query) |
            Q(type_of_organisation__icontains=query)
        )
        results = Client.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response("automation/search.html", {
        "results": results,
        "query": query
    })
    #if "ADD JOB":
	#			return HttpResponseRedirect(reverse('TCC.automation.views.add_job'))
    #else:
    
def add_job(request):
	#results= Client.objects.get(id=request.GET['id'])
	#results = Client.objects.filter(qset).distinct()
	#id = ClientJob.objects.aggregate(Max('job_no'))
	#maxid =id['job_no__max']
	results = Client.objects.get(id=request.GET['id'])
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	if maxid== None :
		maxid = 1
	else:
		maxid = maxid + 1
	auto_receipt_no = Receipt_Auto_number.objects.aggregate(Max('receipt_no'))
	auto_receipt_no = auto_receipt_no['receipt_no__max']
	if auto_receipt_no == None :
		auto_receipt_no = 1
	else:
		auto_receipt_no = auto_receipt_no + 1
	if request.method == 'POST':
		form = ClientJobForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			report_type =cd['report_type']
			type_of_consultancy =cd['type_of_consultancy']
			form.save()
			ClientJob.objects.filter(job_no=maxid).update( receipt_no = auto_receipt_no)
			p = Auto_number(job_no = maxid)
			p.save()
			r = Receipt_Auto_number(job_no=maxid)
			r.save()
			if report_type=="SUSPENCE":
				return HttpResponseRedirect(reverse('TCC.automation.views.suspence_calculation'))
			elif report_type=="CDF" and type_of_consultancy=="CDF":
				return HttpResponseRedirect(reverse('TCC.automation.views.cdf_calculation'))
			else :
				return HttpResponseRedirect(reverse('TCC.automation.views.report_calculation'))
	
	else:
		form = ClientJobForm()
		#return render_to_response('automation/add_job.html', {'results': results,
		return render_to_response('automation/clientjob.html', {'results': results,
        'form': form,'auto_receipt_no':auto_receipt_no}, context_instance=RequestContext(request))
      
    
def client(request):
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	if maxid== None :
		maxid = 1
	else:
		maxid = maxid + 1
	auto_receipt_no = Receipt_Auto_number.objects.aggregate(Max('receipt_no'))
	auto_receipt_no = auto_receipt_no['receipt_no__max']
	if auto_receipt_no == None :
		auto_receipt_no = 1
	else:
		auto_receipt_no = auto_receipt_no + 1
	if request.method == 'POST':
		form = ClientJobForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			report_type =cd['report_type']
			type_of_consultancy =cd['type_of_consultancy']
			form.save()
			ClientJob.objects.filter(job_no=maxid).update( receipt_no = auto_receipt_no)
			p = Auto_number(job_no = maxid)
			p.save()
			r = Receipt_Auto_number(job_no=maxid)
			r.save()
			if report_type=="SUSPENCE":
				return HttpResponseRedirect(reverse('TCC.automation.views.suspence_calculation'))
			elif report_type=="CDF" and type_of_consultancy=="CDF":
				return HttpResponseRedirect(reverse('TCC.automation.views.cdf_calculation'))
			else :
				return HttpResponseRedirect(reverse('TCC.automation.views.report_calculation'))
	
	else:
		form = ClientJobForm()
		return render_to_response('automation/clientjob.html', {'form': form,'maxid':maxid,'auto_receipt_no':auto_receipt_no}, context_instance=RequestContext(request))

def job_register(request):
	id = JobRegister.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	if maxid== None :
		maxid = 1
	else:
		maxid = maxid + 1
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
			template= {'form': form,'name':name,'maxid':maxid,'letter_date':letter_date,'letter_no':letter_no, 'file_disposal': file_disposal,
			'phone_no' : phone_no , 'material_type':material_type }
			return render_to_response('automation/job_register_ok.html', template, context_instance=RequestContext(request))
	else:
		form = JobRegisterForm()
	return render_to_response('automation/clientjob.html', {'form': form,'maxid':maxid}, context_instance=RequestContext(request))

def non_payment_job_register_report(request):
	if request.method == 'POST':
		form = MonthlyReport(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			month = cd['month']
			year = cd['year']
			month_print = month
			month = months(month)
			jobregister = JobRegister.objects.filter(date__year=year).filter(date__month=month)
			template ={'jobregister':jobregister,'year':year,'month' :month_print}
			return render_to_response('automation/nonpaymentjobregisterreport.html', template, context_instance=RequestContext(request))
	else:
		form = MonthlyReport()
	return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))

def payment_job_register_report(request):
	if request.method == 'POST':
		form = MonthlyReport(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			month = cd['month']
			year = cd['year']
			month_print = month
			month = months(month)
			client = ClientJob.objects.filter(date__year=year).filter(date__month=month)
			amount = Amount.objects.all()
			template ={'jobregister':client, 'amount' :amount,'year':year,'month' :month_print}
			return render_to_response('automation/paymentjobregisterreport.html', template, context_instance=RequestContext(request))
	else:
		form = MonthlyReport()
	return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))

def lab_report(request):                             #sandeep
       if request.method == 'POST':
                #form =AmountForm(request.POST)
                form = LabReport(request.POST)
		if form.is_valid():
                        cd = form.cleaned_data
                        start_date = cd['start_date']
                        end_date = cd['end_date']  
			#start_date = datetime.date(start_year,start_month,start_day)
			#end_date =datetime.date(2011,1,26)
			#end_date =datetime.date(end_year,end_month,end_day)
                        lab = cd['lab']
                        field = cd['field']
			title = get_object_or_404(Variable, pk='1')
			sign = get_object_or_404(Variable, pk='3')
                        from TCC.automation.choices import *
			amount = Amount.objects.all().filter(lab=lab).filter(field=field)
                        retrieve()
                        #client = ClientJob.objects.filter(lab='SOIL')
			client = ClientJob.objects.filter(date__range=(start_date,end_date))
                        total_temp = Amount.objects.all().filter(lab=lab).filter(field=field).filter(date__range=(start_date,end_date)).aggregate(Sum('total'))
			total= total_temp['total__sum']
                        net_total_temp = Amount.objects.all().filter(lab=lab).filter(field=field).filter(date__range=(start_date,end_date)).aggregate(Sum('net_total'))
			net_total= net_total_temp['net_total__sum']
			template ={'form':form, 'title':title ,'sign':sign, 'net_total':net_total,'total':total,'date':start_date, 'client':client,'amount':amount,}
                        #p = Amount(job_no = job_no ,total=total,lab=lab, net_total=net_total,lab_choices=lab_choices)
                        #p.save()
                return render_to_response('automation/lab.html', locals() , context_instance=RequestContext(request))
       else:
	        form = LabReportadd()           
       return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))

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
			amount = amount + transpotation
			service_tax= round(servicetax * amount) 
			education_tax = round(educationtax * amount)
			higher_education_tax = round(highereducationtax * amount)
			net_total = round(amount + higher_education_tax + education_tax + service_tax)
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
			job_no_id = id['job_no__max'] 
			client = ClientJob.objects.get(job_no=job_no)
			report_type = client.report_type
			form.save()
			receipt_no = Receipt_Auto_number.objects.aggregate(Max('receipt_no'))
			receipt_no = receipt_no['receipt_no__max'] 
			ClientJob.objects.filter(job_no = client.job_no).update( receipt_no = receipt_no)
			p = Amount(id ='', job_no_id = job_no_id ,date=datetime.date.today(),total=total,lab=lab,tds=tds, net_total=net_total, balance=balance, development_fund=development_fund, 
			service_tax=service_tax, higher_education_tax=higher_education_tax, education_tax=education_tax, field=field, 
			college_income = college_income, admin_charge=admin_charge, consultancy_asst=consultancy_asst, other_field=other_field,report_type=report_type)
			p.save()
	if request.method == 'POST':
		form1 = SuspenceForm(request.POST)
		if form1.is_valid():
			cd = form1.cleaned_data
			type = cd['type']
			check_number = cd['check_number']
			check_dd_date = cd['check_dd_date']
			id = ClientJob.objects.aggregate(Max('job_no'))
			job_no_id = id['job_no__max']
			s = Suspence( job_no_id = job_no_id, type=type,check_number=check_number,check_dd_date=check_dd_date)
			s.save()
			p = Amount(job_no_id = job_no_id ,type = type,date=datetime.date.today(),)
			p.save()
		return render_to_response('automation/suspence_ok.html', {'form': form,'maxid': maxid}, context_instance=RequestContext(request))
	else:
		form = AmountForm()
		form1 = SuspenceForm()
	return render_to_response('automation/suspence.html', {'form1': form1,'form': form ,'maxid': maxid}, context_instance=RequestContext(request))

def cdf_calculation(request):
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	if request.method == 'POST':
		form =CdfAmountForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			#job_no = cd['job_no']
			total = cd['total']
			lab = cd['lab']
			field = cd['field']
			other_field = cd['other_field']
			if field =="OTHER":
				field = other_field
			else :
				field= field
			from TCC.automation.variable import *
			id = ClientJob.objects.aggregate(Max('job_no'))
			job_no = id['job_no__max'] 
			client = ClientJob.objects.get(job_no=job_no)
			report_type = client.report_type
			receipt_no = Receipt_Auto_number.objects.aggregate(Max('receipt_no'))
			receipt_no = receipt_no['receipt_no__max'] 
			ClientJob.objects.filter(job_no = client.job_no).update( receipt_no = receipt_no)
			p = CdfAmount(job_no = job_no ,date=datetime.date.today(),total=total,lab=lab,other_field=other_field,report_type=report_type,field=field)
			p.save()
		return render_to_response('automation/cdf_ok.html', {'form': form, 'maxid':maxid}, context_instance=RequestContext(request))
	else:
		form = CdfAmountForm()
	return render_to_response('automation/cdf_add.html', {'form': form, 'maxid': maxid}, context_instance=RequestContext(request))

def report_calculation(request):
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	if request.method == 'POST':
		form =AmountForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			#job_no = cd['job_no']
			total = cd['total']
			type = cd['type']             #sandeep
			lab = cd['lab']
			tds= cd['tds']
			field = cd['field']
			other_field = cd['other_field']
			if field =="OTHER":
				field = other_field
			else :
				field= field
			job_no_id = ClientJob.objects.aggregate(Max('job_no'))
			maxid =id['job_no__max']
			if maxid== None :
				maxid = 1
			else:
				maxid = maxid + 1
			from TCC.automation.variable import *
			college_income = round(collegeincome * total / 100.00)
			admin_charge = round(admincharge * total / 100.00)
			temp = total - college_income - admin_charge
			client = ClientJob.objects.get(job_no=maxid)
			con_type = client.type_of_consultancy
			ratio1 = ratio1(con_type)
			ratio2 = ratio2(con_type)
			consultancy_asst = round(ratio1 * temp / 100)
			development_fund = round(ratio2 * temp / 100)
			service_tax= round(servicetax * total)
			education_tax = round(educationtax * total)
			higher_education_tax = round(highereducationtax * total)
			net_total = total + higher_education_tax + education_tax + service_tax
			balance = net_total - tds
			id = ClientJob.objects.aggregate(Max('job_no'))
			#job_no_id = client.job_no 
			client = ClientJob.objects.get(job_no=job_no)
			report_type = client.report_type
			#form.save()
			#receipt_no = Receipt_Auto_number.objects.aggregate(Max('receipt_no'))
			#receipt_no = receipt_no['receipt_no__max'] 
			#ClientJob.objects.filter(job_no = job_no).update( receipt_no = receipt_no)
			p = Amount(job_no_id = id ,date=datetime.date.today(),total=total,type=type,lab=lab,tds=tds, net_total=net_total, balance=balance, development_fund=development_fund, 
			service_tax=service_tax, higher_education_tax=higher_education_tax, education_tax=education_tax, field=field, 
			college_income = college_income, admin_charge=admin_charge, consultancy_asst=consultancy_asst, other_field=other_field,report_type=report_type)
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
	if lab=="STRUCTURAL DESIGN":
		varaible = "DESIGNED BY"
	else:
		varaible= "LAB TESTING"
	job_no = amount.job_no_id
	net_total1 = amount.net_total
	net_total_eng = num2eng(net_total1)
	teachers = Teachers.objects.all().filter(lab=lab).order_by('id')
	retrieve()
	template = {'job_no': job_no,'varaible':varaible,'net_total_eng':net_total_eng,'sign':sign,'lab' : lab, 'teachers':teachers, 'servicetaxprint':servicetaxprint,
	'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,'client': client,'amount':amount,'title':title,
	'sub_title':sub_title ,'con_type':con_type, 'ratio1':ratio1 ,'ratio2':ratio2,'collegeincome':collegeincome,'admincharge' : admincharge }
	return render_to_response('automation/report.html', template , context_instance=RequestContext(request))

def suspence(request):
	from TCC.automation.variable import *
	client = ClientJob.objects.get(job_no=request.GET['job_no'])
	amount = Amount.objects.get(job_no=request.GET['job_no_id'])
	suspence = Suspence.objects.get(job_no=request.GET['job_no_id'])
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
	job_no = amount.job_no_id
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
	auto_number = Auto_number.objects.get(job_no=client.job_no)
	job_no = amount.job_no
	net_total1 = amount.net_total
	net_total_eng = num2eng(net_total1)
	template = {'job_no': job_no ,'bill_no':auto_number.id,'net_total_eng':net_total_eng,'sign':sign,'servicetaxprint':servicetaxprint,
	'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,'client': client, 'amount':amount, 'title':title,
	'sub_title':sub_title,}
	return render_to_response('automation/bill.html', template , context_instance=RequestContext(request))

def  monthly_report(request):
	if request.method == 'POST':
		form = MonthlyReportadd(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			month = cd['month']
			year = cd['year']
			month_print = month
			paid_education_tax= cd['paid_education_tax']
			paid_higher_education_tax= cd['paid_higher_education_tax']
			paid_service_tax= cd['paid_service_tax']
			month = months(month)
			title = get_object_or_404(Variable, pk='1')
                        client = ClientJob.objects.filter(date__year=year).filter(date__month=month)
                        count = ClientJob.objects.filter(date__year=year).filter(date__month=month).filter  (report_type='GENERAL REPORT').count()
			amount = Amount.objects.all()
			total_temp = Amount.objects.filter(date__year=year).filter(date__month=month).aggregate(Sum('total'))
                       
			total= int(total_temp['total__sum'])
			service_tax_temp = Amount.objects.filter(date__year=year).filter(date__month=month).aggregate(Sum('service_tax'))

			service_tax= int(service_tax_temp['service_tax__sum'])
			education_tax_temp = Amount.objects.filter(date__year=year).filter(date__month=month).aggregate(Sum('education_tax'))
			education_tax= int(education_tax_temp['education_tax__sum'])
			higher_education_tax_temp = Amount.objects.filter(date__year=year).filter(date__month=month).aggregate(Sum('higher_education_tax'))
			higher_education_tax= int(higher_education_tax_temp['higher_education_tax__sum'])
			net_total_temp = Amount.objects.filter(date__year=year).filter(date__month=month).aggregate(Sum('net_total'))
			net_total= int(net_total_temp['net_total__sum'])
			tax = service_tax+education_tax+higher_education_tax
		
			ser_tax = service_tax-int(paid_service_tax)
			edu_tax = education_tax-paid_education_tax
			high_tax = higher_education_tax-paid_higher_education_tax
			final = ser_tax + edu_tax +high_tax
			paid_tax = paid_education_tax+paid_higher_education_tax+ paid_service_tax
			template ={'form':form, 'title':title,'tax':tax,'month': month_print,'service_tax':service_tax,
			'education_tax':education_tax,'higher_education_tax':higher_education_tax, 'net_total':net_total,'total':total,
			'year':year,'client':client,'amount':amount,'paid_higher_education_tax':paid_higher_education_tax,'paid_tax':paid_tax,
			'paid_education_tax': paid_education_tax, 'paid_service_tax':paid_service_tax, 'final':final, 'ser_tax':ser_tax,
			'edu_tax':edu_tax, 'high_tax':high_tax,}
			return render_to_response('automation/monthlyreport.html', locals(), context_instance=RequestContext(request))
	else:
		form = MonthlyReportadd()
	return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))

def old_client(request):
        if request.method == 'POST':
		form = OldClientadd(request.POST)
		if form.is_valid():
                        from TCC.automation.functions import *
			cd = form.cleaned_data
                        name_and_address = cd['name_and_address']
                        
                        title = get_object_or_404(Variable, pk='1')
			sign = get_object_or_404(Variable, pk='3')
                        from TCC.automation.choices import *
                        client = ClientJob.objects.filter(name_and_address=name_and_address)
                        amount = Amount.objects.all()
                        suspence = Suspence.objects.all()
                        total_temp = Amount.objects.aggregate(Sum("total"))
                        total  = int(total_temp['total__sum'])
                        net_total_temp = Amount.objects.aggregate(Sum('net_total'))
			net_total= int(net_total_temp['net_total__sum'])
                        template ={'form':form, 'total':total,'title':title ,'sign':sign, 'net_total':net_total, 'client':client,'amount':amount,'suspence':suspence,'name_and_address':name_and_address ,}
			return render_to_response('automation/oldclient.html',locals(), context_instance=RequestContext(request))
        else:
		form = OldClientadd()
	return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))

def  daily_report(request):                                   #sandeep
	if request.method == 'POST':
		form = DailyReportadd(request.POST)
		if form.is_valid():
                        from TCC.automation.functions import *
			cd = form.cleaned_data
                        start_date = cd['start_date']
                        end_date = cd['end_date'] 
                        type = cd['type']
                        if type=="CASH":   
                                title = get_object_or_404(Variable, pk='1')
			        sign = get_object_or_404(Variable, pk='3')
                                from TCC.automation.choices import *
                                client = ClientJob.objects.filter(date__range=(start_date,end_date))
			        amount = Amount.objects.filter(date__range=(start_date,end_date)).filter(type='CASH')
                                retrieve()
                                suspence = Suspence.objects.all()
                                balance_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(type='CASH').aggregate(Sum('balance'))
			        balance= balance_temp['balance__sum']
			        tds_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(type='CASH').aggregate(Sum('tds'))
			        tds= tds_temp['tds__sum']
       			        template ={'form':form, 'tds':tds,'title':title ,'sign':sign, 'date': start_date, 'balance':balance, 'client':client,'amount':amount,'type':type,'suspence':suspence}
			        return render_to_response('automation/dailyreport.html',locals(), context_instance=RequestContext(request))
                         elif type=="CHEQUE":
                                title = get_object_or_404(Variable, pk='1')
			        sign = get_object_or_404(Variable, pk='3')
                                from TCC.automation.choices import *
			        client = ClientJob.objects.filter(date__range=(start_date,end_date))
			        amount = Amount.objects.filter(date__range=(start_date,end_date)).filter(type='CHEQUE')
			        retrieve()
                                suspence = Suspence.objects.all()
                                balance_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(type='CHEQUE').aggregate(Sum('balance'))
			        balance= balance_temp['balance__sum']
			        tds_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(type='CHEQUE').aggregate(Sum('tds'))
			        tds= tds_temp['tds__sum']
			        template ={'form':form,'tds':tds, 'title':title ,'sign':sign, 'date': start_date, 'balance':balance, 'client':client,'amount':amount,'type':type,'suspence':suspence}
			        return render_to_response('automation/dailyreport1.html', locals(), context_instance=RequestContext(request))
                        elif type=="ONLINE":
                                title = get_object_or_404(Variable, pk='1')
			        sign = get_object_or_404(Variable, pk='3')
                                from TCC.automation.choices import *
			        client = ClientJob.objects.filter(date__range=(start_date,end_date))
			        amount = Amount.objects.filter(date__range=(start_date,end_date)).filter(type='ONLINE')
			        retrieve()
                                suspence = Suspence.objects.all()
                                balance_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(type='ONLINE').aggregate(Sum('balance'))
			        balance= balance_temp['balance__sum']
			        tds_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(type='ONLINE').aggregate(Sum('tds'))
			        tds= tds_temp['tds__sum']
			        template ={'form':form,'tds':tds, 'title':title ,'sign':sign, 'date': start_date, 'balance':balance, 'client':client,'amount':amount,'type':type,'suspence':suspence,}
			        return render_to_response('automation/dailyreport1.html', locals(), context_instance=RequestContext(request))
                        elif type=="DD":
                                title = get_object_or_404(Variable, pk='1')
			        sign = get_object_or_404(Variable, pk='3')
                                from TCC.automation.choices import *
			        client = ClientJob.objects.filter(date__range=(start_date,end_date))
			        amount = Amount.objects.filter(date__range=(start_date,end_date)).filter(type='DD')
			        retrieve()
                                suspence = Suspence.objects.all()
                                balance_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(type='DD').aggregate(Sum('balance'))
			        balance= balance_temp['balance__sum']
			        tds_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(type='DD').aggregate(Sum('tds'))
			        tds= tds_temp['tds__sum']
			        template ={'form':form,'tds':tds, 'title':title ,'sign':sign, 'date': start_date, 'balance':balance, 'client':client,'amount':amount,'type':type,'suspence':suspence}
			        return render_to_response('automation/dailyreport1.html', locals(), context_instance=RequestContext(request))
	else:
		form = DailyReportadd()
	return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))
   

def suspence_report(request):
	if request.method == 'POST':
		form = DateReport(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			start_month = cd['start_month']
			month_print = start_month
			start_month =months(start_month)
			start_day = int(cd['start_day'])
			start_year = int(cd['start_year'])
			end_month = cd['end_month']
			end_month = months(end_month)
			end_day = int(cd['end_day'])
			end_year = int(cd['end_year'])
			start_date = datetime.date(start_year,start_month,start_day)
			#end_date =datetime.date(2011,1,26)
			end_date =datetime.date(end_year,end_month,end_day)
			from TCC.automation.variable import *
			title = get_object_or_404(Variable, pk='1')
			sign = get_object_or_404(Variable, pk='3')
			client = ClientJob.objects.filter(date__range=(start_date,end_date))
			suspence = Suspence.objects.all()
			amount = Amount.objects.filter(date__range=(start_date,end_date))
			service_tax_temp = Amount.objects.filter(report_type='SUSPENCE').filter(date__range=(start_date,end_date)).aggregate(Sum('service_tax'))
			service_tax= service_tax_temp['service_tax__sum']
			education_tax_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(report_type='SUSPENCE').aggregate(Sum('education_tax'))
			education_tax= education_tax_temp['education_tax__sum']
			higher_education_tax_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(report_type='SUSPENCE').aggregate(Sum('higher_education_tax'))
			higher_education_tax= higher_education_tax_temp['higher_education_tax__sum']
			balance_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(report_type='SUSPENCE').aggregate(Sum('balance'))
			balance= balance_temp['balance__sum']
			tds_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(report_type='SUSPENCE').aggregate(Sum('tds'))
			tds= tds_temp['tds__sum']
			net_total_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(report_type='SUSPENCE').aggregate(Sum('net_total'))
			net_total= net_total_temp['net_total__sum']
			total_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(report_type='SUSPENCE').aggregate(Sum('total'))
			total= total_temp['total__sum']	
			template ={'form':form, 'title':title ,'sign':sign,'month': month_print, 'year': start_year, 'client':client,'amount':amount,'suspence':suspence}
			return render_to_response('automation/suspencereport.html', locals(), context_instance=RequestContext(request))
	else:
		form = DateReport()
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

def proforma_register(request):
        if request.method == 'POST':
		form = PerformaRegadd(request.POST)
		if form.is_valid():
                        from TCC.automation.functions import *
			cd = form.cleaned_data
                        start_date = cd['start_date']
                        end_date = cd['end_date'] 
                        from TCC.automation.variable import *
                        from TCC.automation.choices import *
	                proformabill =Proformabill.objects.all().filter(date__range=(start_date,end_date))
	                proformatax = ProfromaTax.objects.all()
	                title = get_object_or_404(Variable, pk='1')
	                sub_title = get_object_or_404(Variable, pk='2')
	                sign = get_object_or_404(Variable, pk='3')
                        amount_temp = Proformabill.objects.filter(date__range=(start_date,end_date)).aggregate(Sum('amount'))
                        amount=amount_temp['amount__sum']
                        service_tax_temp = ProfromaTax.objects.aggregate(Sum('service_tax'))
			service_tax= service_tax_temp['service_tax__sum']
			education_tax_temp = ProfromaTax.objects.aggregate(Sum('education_tax'))
			education_tax= education_tax_temp['education_tax__sum']
			higher_education_tax_temp = ProfromaTax.objects.aggregate(Sum('higher_education_tax'))
			higher_education_tax= higher_education_tax_temp['higher_education_tax__sum']
                        total_temp = ProfromaTax.objects.aggregate(Sum('total'))
			total= total_temp['total__sum']
	                template = {'sign':sign, 'proformatax' : proformatax,'title':title,'sub_title' :sub_title,
	'proformabill': proformabill,'date': start_date,'service_tax': service_tax,'education_tax': education_tax,'higher_education_tax': higher_education_tax,'total':total}
	                return render_to_response('automation/proformabillreg.html', locals() , context_instance=RequestContext(request))
        else:
		form = PerformaRegadd()
	return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))
         

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
			admin_charge_temp = Amount.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT').aggregate(Sum('admin_charge'))
			admin_charge= admin_charge_temp['admin_charge__sum']
			college_income_temp = Amount.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT').aggregate(Sum('college_income'))
			college_income= college_income_temp['college_income__sum']
			consultancy_asst_temp = Amount.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT').aggregate(Sum('consultancy_asst'))
			consultancy_asst= consultancy_asst_temp['consultancy_asst__sum']
			development_fund_temp = Amount.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT').aggregate(Sum('development_fund'))
			development_fund= development_fund_temp['development_fund__sum']
			service_tax_temp = Amount.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT').aggregate(Sum('service_tax'))
			service_tax= service_tax_temp['service_tax__sum']
			education_tax_temp = Amount.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT').aggregate(Sum('education_tax'))
			education_tax= education_tax_temp['education_tax__sum']
			higher_education_tax_temp = Amount.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT').aggregate(Sum('higher_education_tax'))
			higher_education_tax= higher_education_tax_temp['higher_education_tax__sum']
			balance_temp = Amount.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT').aggregate(Sum('balance'))
			balance= balance_temp['balance__sum']
			tds_temp = Amount.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT').aggregate(Sum('tds'))
			tds= tds_temp['tds__sum']
			return render_to_response('automation/gov_pri_report.html', locals(), context_instance=RequestContext(request))
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
			month_print = month
			month = months(month)
			from TCC.automation.variable import *
			title = get_object_or_404(Variable, pk='1')
			client = ClientJob.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT')
			amount = Amount.objects.all()
			admin_charge_temp = Amount.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT').aggregate(Sum('admin_charge'))
			admin_charge= admin_charge_temp['admin_charge__sum']
			college_income_temp = Amount.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT').aggregate(Sum('college_income'))
			college_income= college_income_temp['college_income__sum']
			consultancy_asst_temp = Amount.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT').aggregate(Sum('consultancy_asst'))
			consultancy_asst= consultancy_asst_temp['consultancy_asst__sum']
			development_fund_temp = Amount.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT').aggregate(Sum('development_fund'))
			development_fund= development_fund_temp['development_fund__sum']
			service_tax_temp = Amount.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT').aggregate(Sum('service_tax'))
			service_tax= service_tax_temp['service_tax__sum']
			education_tax_temp = Amount.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT').aggregate(Sum('education_tax'))
			education_tax= education_tax_temp['education_tax__sum']
			higher_education_tax_temp = Amount.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT').aggregate(Sum('higher_education_tax'))
			higher_education_tax= higher_education_tax_temp['higher_education_tax__sum']
			balance_temp = Amount.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT').aggregate(Sum('balance'))
			balance= balance_temp['balance__sum']
			tds_temp = Amount.objects.filter(date__year=year).filter(date__month=month).filter(report_type='GENERAL REPORT').aggregate(Sum('tds'))
			tds= tds_temp['tds__sum']
			return render_to_response('automation/main_register.html', locals(), context_instance=RequestContext(request))
	else:
		form = MonthlyReport()
	return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))


def suspence_clearence_register(request):
	if request.method == 'POST':
		form = DateReport(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			start_month = cd['start_month']
			month_print = start_month
			start_month =months(start_month)
			start_day = int(cd['start_day'])
			start_year = int(cd['start_year'])
			end_month = cd['end_month']
			end_month = months(end_month)
			end_day = int(cd['end_day'])
			end_year = int(cd['end_year'])
			start_date = datetime.date(start_year,start_month,start_day)
			#end_date =datetime.date(2011,1,26)
			end_date =datetime.date(end_year,end_month,end_day)
			from TCC.automation.variable import *
			title = get_object_or_404(Variable, pk='1')
			sign = get_object_or_404(Variable, pk='3')
			client = ClientJob.objects.filter(date__range=(start_date,end_date))
			suspence = Suspence.objects.all()
			amount = Amount.objects.filter(date__range=(start_date,end_date))
                        admin_charge_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(report_type='SUSPENCE').aggregate(Sum('admin_charge'))
			admin_charge= admin_charge_temp['admin_charge__sum']
			college_income_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(report_type='SUSPENCE').aggregate(Sum('college_income'))
			college_income= college_income_temp['college_income__sum']
			consultancy_asst_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(report_type='SUSPENCE').aggregate(Sum('consultancy_asst'))
			consultancy_asst= consultancy_asst_temp['consultancy_asst__sum']
			development_fund_temp = Amount.objects.filter(date__range=(start_date,end_date)) .filter(report_type='SUSPENCE').aggregate(Sum('development_fund'))
			development_fund= development_fund_temp['development_fund__sum']
			service_tax_temp = Amount.objects.filter(report_type='SUSPENCE').filter(date__range=(start_date,end_date)).aggregate(Sum('service_tax'))
			service_tax= service_tax_temp['service_tax__sum']
			education_tax_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(report_type='SUSPENCE').aggregate(Sum('education_tax'))
			education_tax= education_tax_temp['education_tax__sum']
			higher_education_tax_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(report_type='SUSPENCE').aggregate(Sum('higher_education_tax'))
			higher_education_tax= higher_education_tax_temp['higher_education_tax__sum']
			balance_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(report_type='SUSPENCE').aggregate(Sum('balance'))
			balance= balance_temp['balance__sum']
			tds_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(report_type='SUSPENCE').aggregate(Sum('tds'))
			tds= tds_temp['tds__sum']
			net_total_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(report_type='SUSPENCE').aggregate(Sum('net_total'))
			net_total= net_total_temp['net_total__sum']
			total_temp = Amount.objects.filter(date__range=(start_date,end_date)).filter(report_type='SUSPENCE').aggregate(Sum('total'))
			total= total_temp['total__sum']	
			template ={'form':form, 'title':title ,'sign':sign,'month': month_print, 'year': start_year, 'client':client,'amount':amount,'suspence':suspence}
			return render_to_response('automation/suspence_clearence_register.html', locals(), context_instance=RequestContext(request))
	else:
		form = DateReport()
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
			id = Transport.objects.aggregate(Max('id'))
			maxid =id['id__max']
			if maxid== None :
				maxid = 1
			else:
				maxid = maxid + 1
			bill_no = maxid
			rate = cd ['rate']
			form.save()
			Transport.objects.filter(job_no = job_no).update( bill_no = maxid )
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
			field_testing_staff =cd ['field_testing_staff']
			#suspence_bill_no =cd['suspence_bill_no']
			Suspence.objects.filter(job_no = job_no).update(labour_charge=labour_charge,boring_charge_external=boring_charge_external, 
			boring_charge_internal= boring_charge_internal,field_testing_staff=field_testing_staff,car_taxi_charge=car_taxi_charge,lab_testing_staff=lab_testing_staff)
			data = {'job_no' :job_no, 'labour_charge':labour_charge,'boring_charge_external':boring_charge_external,
			'boring_charge_internal': boring_charge_internal,'car_taxi_charge':car_taxi_charge,'lab_testing_staff':lab_testing_staff}
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
	lab_staff = suspence.lab_testing_staff
	temp = [0,0,0,0,0,0,0,0,0,0]
	range = lab_staff.split(',')
	i=0
	while i < len(range):
		temp[i] = range[i]
		i+=1
	amount1 = temp[0]
	amount2 = temp[1]
	amount3 = temp[2]
	amount4 = temp[3]
	amount5 = temp[4]
	amount6 = temp[5]
	amount7 = temp[6]
	amount8 = temp[7]
	amount9 = temp[8]
	amount10 = temp[9]
	
	field_staff = suspence.field_testing_staff
	temp = [0,0,0,0,0,0,0,0,0,0]
	range = field_staff.split(',')
	i=0
	while i < len(range):
		temp[i] = range[i]
		i+=1
	amounts1 = temp[0]
	amounts2 = temp[1]
	amounts3 = temp[2]
	amounts4 = temp[3]
	amounts5 = temp[4]
	amounts6 = temp[5]
	amounts7 = temp[6]
	amounts8 = temp[7]
	amounts9 = temp[8]
	amounts10 = temp[9]
	teachers =Teachers.objects.all().filter(Q(code=amount1)| Q(code=amount2) | Q(code=amount3) 
	| Q(code=amount4) | Q(code=amount5) | Q(code=amount6) | Q(code=amount7)| Q(code=amount8)
	| Q(code=amount9) | Q(code=amount10)| Q(code=amounts1)| Q(code=amounts2) | Q(code=amounts3) 
	| Q(code=amounts4) | Q(code=amounts5) | Q(code=amounts6) | Q(code=amounts7)| Q(code=amounts8)
	| Q(code=amounts9) | Q(code=amounts10)).order_by('id')
	title = get_object_or_404(Variable, pk='1')
	sub_title = get_object_or_404(Variable, pk='2')
	sign = get_object_or_404(Variable, pk='3')
	tada_temp = Ta_Da.objects.filter(job_no=client.job_no).aggregate(Sum('tada_amount'))
	tada_sum= int(tada_temp['tada_amount__sum']) 
	field_testing_staff = Ta_Da.objects.filter(job_no=client.job_no)
	temp = suspence.labour_charge+transport.total+suspence.boring_charge_external+suspence.car_taxi_charge
	balance= amount.total - (tada_sum + temp + suspence.boring_charge_internal)
	college_income = round(collegeincome * balance / 100.00)
	admin_charge = round(admincharge * balance / 100.00)
	work_charge = round(workcharge * balance / 100.00)
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
	Suspence.objects.filter(job_no = client.job_no).update( work_charge = work_charge)
	Amount.objects.filter(job_no = client.job_no).update( college_income = college_income, admin_charge=admin_charge,
	consultancy_asst=consultancy_asst, development_fund=development_fund )
	data = {'transport' : transport, 'net_balance_eng':net_balance_eng,'teachers':teachers,'servicetaxprint':servicetaxprint,
	'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,'ratio1':ratio1 ,'field_testing_staff':field_testing_staff,
	'job_no':client.job_no,'ratio2':ratio2,'other':temp,'collegeincome':collegeincome,'admincharge' : admincharge ,'client' :client, 'amount': amount,
	'suspence':suspence,'tada_sum':tada_sum,'sign':sign,'title':title,'sub_title':sub_title,}
	return render_to_response('automation/suspence_clearence_report.html', data , context_instance=RequestContext(request))

def suspence_clearence_report_no_charge(request):
	#transport = Transport.objects.get(job_no=request.GET['job_no'])
	client = ClientJob.objects.get(job_no=request.GET['job_no'])
	amount = Amount.objects.get(job_no=request.GET['job_no'])
	suspence = Suspence.objects.get(job_no=request.GET['job_no'])
	lab_staff = suspence.lab_testing_staff
	temp = [0,0,0,0,0,0,0,0,0,0]
	range = lab_staff.split(',')
	i=0
	while i < len(range):
		temp[i] = range[i]
		i+=1
	amount1 = temp[0]
	amount2 = temp[1]
	amount3 = temp[2]
	amount4 = temp[3]
	amount5 = temp[4]
	amount6 = temp[5]
	amount7 = temp[6]
	amount8 = temp[7]
	amount9 = temp[8]
	amount10 = temp[9]
	
	field_staff = suspence.field_testing_staff
	temp = [0,0,0,0,0,0,0,0,0,0]
	range = field_staff.split(',')
	i=0
	while i < len(range):
		temp[i] = range[i]
		i+=1
	amounts1 = temp[0]
	amounts2 = temp[1]
	amounts3 = temp[2]
	amounts4 = temp[3]
	amounts5 = temp[4]
	amounts6 = temp[5]
	amounts7 = temp[6]
	amounts8 = temp[7]
	amounts9 = temp[8]
	amounts10 = temp[9]
	teachers =Teachers.objects.all().filter(Q(code=amount1)| Q(code=amount2) | Q(code=amount3) 
	| Q(code=amount4) | Q(code=amount5) | Q(code=amount6) | Q(code=amount7)| Q(code=amount8)
	| Q(code=amount9) | Q(code=amount10)| Q(code=amounts1)| Q(code=amounts2) | Q(code=amounts3) 
	| Q(code=amounts4) | Q(code=amounts5) | Q(code=amounts6) | Q(code=amounts7)| Q(code=amounts8)
	| Q(code=amounts9) | Q(code=amounts10)).order_by('id')
	title = get_object_or_404(Variable, pk='1')
	sub_title = get_object_or_404(Variable, pk='2')
	sign = get_object_or_404(Variable, pk='3')
	#tada_temp = Ta_Da.objects.filter(job_no=client.job_no).aggregate(Sum('tada_amount'))
	#tada_sum= int(tada_temp['tada_amount__sum'])
	#field_testing_staff = Ta_Da.objects.filter(job_no=client.job_no)
	#temp = suspence.labour_charge+transport.total+suspence.boring_charge_external+suspence.car_taxi_charge
	balance= amount.total #- (tada_sum + temp + suspence.boring_charge_internal)
	college_income = round(collegeincome * balance / 100.00)
	admin_charge = round(admincharge * balance / 100.00)
	balance_temp = balance - college_income - admin_charge 
	from TCC.automation.functions import *
	con_type = client.type_of_consultancy
	ratio1 = ratio1(con_type)
	ratio2 = ratio2(con_type)
	consultancy_asst = round(ratio1 * balance_temp / 100.00)
	development_fund = round(ratio2 * balance_temp / 100.00)
	net_total1 = amount.balance
	net_balance_eng = num2eng(net_total1)
	retrieve()
	Amount.objects.filter(job_no = client.job_no).update( college_income = college_income, admin_charge=admin_charge,
	consultancy_asst=consultancy_asst, development_fund=development_fund )
	data = {'net_balance_eng':net_balance_eng,'teachers':teachers,'servicetaxprint':servicetaxprint,
	'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,'ratio1':ratio1 ,
	'job_no':client.job_no,'ratio2':ratio2,'collegeincome':collegeincome,'admincharge' : admincharge ,'client' :client, 'amount': amount,
	'suspence':suspence,'sign':sign,'title':title,'sub_title':sub_title,}
	return render_to_response('automation/suspence_clearence_report_no_charge.html', data , context_instance=RequestContext(request))

def cdf_bill(request):
	from TCC.automation.variable import *
	client = ClientJob.objects.get(job_no=request.GET['job_no'])
	amount = CdfAmount.objects.get(job_no=request.GET['job_no'])
	title = get_object_or_404(Variable, pk='1')
	sub_title = get_object_or_404(Variable, pk='2')
	sign = get_object_or_404(Variable, pk='3')
	auto_number = Auto_number.objects.get(job_no=client.job_no)
	job_no = amount.job_no
	net_total1 = amount.total
	net_total_eng = num2eng(net_total1)
	template = {'job_no': job_no ,'bill_no':auto_number.id,'net_total_eng':net_total_eng,'sign':sign,'client': client, 'amount':amount, 'title':title,
	'sub_title':sub_title,'cdftotal':net_total1}
	return render_to_response('automation/bill.html', template , context_instance=RequestContext(request))

def cdf_receipt(request):
	"""
	View the Receipt Data In Html format 
	"""
	from TCC.automation.variable import *
	client = ClientJob.objects.get(job_no=request.GET['job_no'])
	amount = CdfAmount.objects.get(job_no=request.GET['job_no'])
	title = get_object_or_404(Variable, pk='1')
	sub_title = get_object_or_404(Variable, pk='2')
	sign = get_object_or_404(Variable, pk='3')
	job_no = amount.job_no
	net_total1 = amount.total
	net_total_eng = num2eng(net_total1)
	type = 'CASH'
	template = {'job_no': job_no ,'sign':sign, 'net_total_eng':net_total_eng,'type':type,'client': client, 'amount':amount, 'cdftotal':net_total1,
	'title':title, 'sub_title':sub_title,}
	return render_to_response('automation/cdf_receipt.html', template , context_instance=RequestContext(request))
