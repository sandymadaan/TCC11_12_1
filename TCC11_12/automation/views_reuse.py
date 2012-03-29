"""
Regenrate reports for reteive data from Data Base for particular job
"""
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Max ,Q, Sum
from TCC11_12.automation.convert_function import *
from TCC11_12.automation.functions import *
from TCC11_12.automation.models import *
from TCC11_12.automation.forms import *
from TCC11_12.automation.variable import *


def client_report(request):
	"""
	View of All Clients Report Form.
	"""
	if request.method == 'POST':
		form = ClientReportForm(request.POST)
		if form.is_valid():
			from TCC11_12.automation.functions import *
			from TCC11_12.automation.variable import *
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
			teachers = Teachers.objects.all().filter(lab=lab).order_by('id')
			retrieve()
			if type_of_report =="GENERAL REPORT":
				if lab=="STRUCTURAL DESIGN":
					varaible = "DESIGNED BY"
				else:
					varaible= "LAB TESTING"
				template = {'form': form,'job_no': job_no,'varaible':varaible,'net_total_eng':net_total_eng,'lab' : lab,'sign':sign, 'teachers':teachers,
				'servicetaxprint':servicetaxprint,'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,
				'client': client, 'amount':amount, 'title':title, 'sub_title':sub_title ,'con_type':con_type, 'ratio1':ratio1 ,'ratio2':ratio2,
				'collegeincome':collegeincome,'admincharge' : admincharge }
				return render_to_response('automation/report.html', template, context_instance=RequestContext(request))
			elif type_of_report =="BILL":
				auto_number = Auto_number.objects.get(job_no=job_no)
				template = {'job_no': job_no ,'bill_no': auto_number.id ,'net_total_eng':net_total_eng,'sign':sign,'servicetaxprint':servicetaxprint,
				'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,'client': client, 'amount':amount,
				'title':title, 'sub_title':sub_title,}
				return render_to_response('automation/bill.html', template , context_instance=RequestContext(request))
			
			elif type_of_report =="SUSPENCE":
				suspence = Suspence.objects.get(job_no=job_no)
				template = {'job_no': job_no ,'net_total_eng':net_total_eng,'sign':sign,'servicetaxprint':servicetaxprint,
				'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,'client': client, 'amount':amount,
				'title':title, 'sub_title':sub_title,'suspence':suspence ,'collegeincome':collegeincome,'admincharge' : admincharge }
				return render_to_response('automation/suspence_report.html', template , context_instance=RequestContext(request))
			elif type_of_report =="SUSPENCE BILL":
				suspence = Suspence.objects.get(job_no=job_no)
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
			elif type_of_report=="SUSPENCE CLERENCE REPEORT":
				suspence = Suspence.objects.get(job_no=job_no)
				transport = Transport.objects.get(job_no=job_no)
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
				tada_temp = Ta_Da.objects.filter(job_no=client.job_no).aggregate(Sum('tada_amount'))
				tada_sum= int(tada_temp['tada_amount__sum']) 
				field_testing_staff = Ta_Da.objects.filter(job_no=client.job_no)
				temp = suspence.labour_charge+transport.total+suspence.boring_charge_external+suspence.car_taxi_charge
				balance= amount.total - (tada_sum + temp + suspence.boring_charge_internal)
				college_income = round(collegeincome * balance / 100)
				admin_charge = round(admincharge * balance / 100)
				work_charge = round(workcharge * balance / 100)
				balance_temp = balance - college_income - admin_charge -work_charge
				from TCC11_12.automation.functions import *
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
			elif type_of_report=="SUSPENCE CLERENCE REPEORT(without Charge)":
				suspence = Suspence.objects.get(job_no=job_no)
				#transport = Transport.objects.get(job_no=job_no)
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
				#tada_temp = Ta_Da.objects.filter(job_no=client.job_no).aggregate(Sum('tada_amount'))
				#tada_sum= int(tada_temp['tada_amount__sum'])
				#field_testing_staff = Ta_Da.objects.filter(job_no=client.job_no)
				#temp = suspence.labour_charge+transport.total+suspence.boring_charge_external+suspence.car_taxi_charge
				balance= amount.total# - (tada_sum + temp + suspence.boring_charge_internal)
				college_income = round(collegeincome * balance / 100)
				admin_charge = round(admincharge * balance / 100)
				balance_temp = balance - college_income - admin_charge 
				from TCC11_12.automation.functions import *
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
				data = {'net_balance_eng':net_balance_eng,'teachers':teachers,'servicetaxprint':servicetaxprint,
				'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,'ratio1':ratio1,
				'job_no':client.job_no,'ratio2':ratio2,'collegeincome':collegeincome,'admincharge' : admincharge ,'client' :client, 'amount': amount,
				'suspence':suspence,'sign':sign,'title':title,'sub_title':sub_title,}
				return render_to_response('automation/suspence_clearence_report_no_charge.html', data , context_instance=RequestContext(request))
			elif type_of_report=="OTHER CHARGE BILL":
				suspence = Suspence.objects.get(job_no=job_no)
				transport = Transport.objects.get(job_no=job_no)
				tada_temp = Ta_Da.objects.filter(job_no=client.job_no).aggregate(Sum('tada_amount'))
				tada_sum= int(tada_temp['tada_amount__sum']) 
				total = tada_sum + suspence.labour_charge + suspence.car_taxi_charge + suspence.boring_charge_external + transport.total
				total_temp =tada_sum+suspence.labour_charge+suspence.car_taxi_charge+suspence.boring_charge_external
				other =suspence.labour_charge+suspence.car_taxi_charge+suspence.boring_charge_external + transport.total
				data = {'transport' : transport, 'client' :client, 'amount': amount, 'suspence':suspence,'tada_sum':tada_sum,'sign':sign,'title':title,
				'sub_title':sub_title,'total_temp': total_temp, 'total' :total, 'other':other,}
				return render_to_response('automation/other_charge_report.html', data , context_instance=RequestContext(request))
			elif type_of_report=="TRANSPORT BILL":
				transport_old = Transport.objects.get(job_no=job_no)
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
				vehical_no = get_object_or_404(Variable, pk='4')
				template ={'transport':transport,'title':title,'sub_title':sub_title, 'vehical_no':vehical_no ,'client':client,'sign':sign}
				return render_to_response('automation/transport_bill.html', template , context_instance=RequestContext(request))
			
	else:
		form = ClientReportForm()
	return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))


def preforma(request):
	if request.method == 'POST':
		form = Preformaform(request.POST)
		if form.is_valid():
			from TCC11_12.automation.functions import *
			from TCC11_12.automation.variable import *
			cd = form.cleaned_data
			job_no = cd['job_no']
			type_of_report = cd['type_of_report']
			if type_of_report=="PROFORMA BILL":
				proforma_bill = Proformabill.objects.get(pro_no=job_no)
				proforma_tax = ProfromaTax.objects.get(pro_no=job_no)
				pro_no = proforma_bill.pro_no
				net_total1 = proforma_tax.total
				net_total_eng = num2eng(net_total1)
				title = get_object_or_404(Variable, pk='1')
				sub_title = get_object_or_404(Variable, pk='2')
				sign = get_object_or_404(Variable, pk='3')
				template = {'pro_no': pro_no ,'proforma_tax' : proforma_tax, 'sign':sign, 'proforma_bill':proforma_bill, 'net_total_eng':net_total_eng,
				'servicetaxprint':servicetaxprint,'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint, 'title':title,
				'sub_title':sub_title,}
				return render_to_response('automation/pro_bill.html', template , context_instance=RequestContext(request))
			elif type_of_report=="PROFORMA Report":
				proforma_bill = Proformabill.objects.get(pro_no=job_no)
				proforma_tax = ProfromaTax.objects.get(pro_no=job_no)
				pro_no = proforma_bill.pro_no
				net_total1 = proforma_tax.total
				net_total_eng = num2eng(net_total1)
				title = get_object_or_404(Variable, pk='1')
				sub_title = get_object_or_404(Variable, pk='2')
				sign = get_object_or_404(Variable, pk='3')
				template = {'pro_no': pro_no ,'proforma_tax' : proforma_tax, 'sign':sign, 'proforma_bill':proforma_bill, 'net_total_eng':net_total_eng,
				'servicetaxprint':servicetaxprint,'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint, 'title':title,
				'sub_title':sub_title,}
				return render_to_response('automation/proformabillreport.html', template , context_instance=RequestContext(request))
			elif type_of_report =="RECEIPT CDF":
				#amount = CdfAmount.objects.get(job_no=request.GET['job_no'])
				amount = CdfAmount.objects.get(job_no=job_no)
				job_no = amount.job_no
				client = ClientJob.objects.get(job_no=job_no)
				net_total1 = amount.total
				net_total_eng = num2eng(net_total1)
				title = get_object_or_404(Variable, pk='1')
				sub_title = get_object_or_404(Variable, pk='2')
				sign = get_object_or_404(Variable, pk='3')
				type = 'CASH'
				template = {'job_no': job_no ,'sign':sign, 'net_total_eng':net_total_eng,'type':type,
				'client': client, 'amount':amount, 'cdftotal':net_total1, 'title':title, 'sub_title':sub_title,}
				return render_to_response('automation/cdf_receipt.html', template , context_instance=RequestContext(request))

	else:
		form = Preformaform()
	return render_to_response('automation/client.html', {'form': form}, context_instance=RequestContext(request))
	
