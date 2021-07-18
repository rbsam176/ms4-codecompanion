from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from faq.models import FaqEntry, FaqCategory
from .forms import FaqForm, NewFaq

from django.http import JsonResponse

def faq(request):

	faq_content = FaqEntry.objects.all()
	faq_categories = FaqEntry.objects.values_list('category', flat=True).distinct()
	faq_categories_names = []
	for x in faq_categories:
		faq_categories_names.append(FaqCategory.objects.get(pk=x))
	
	context = {
		'faq_categories_names': faq_categories_names,
		'faq_content': faq_content,
	}

	return render(request, 'faq/faq.html', context)

def faq_counter(request):
	if request.method == 'GET':
		clickId = request.GET['clickId']
		currentCount = FaqEntry.objects.filter(pk=clickId).values('clickCount')[0]['clickCount']
		newCount = currentCount + 1
		faq_entry_counter = FaqEntry.objects.filter(pk=clickId).update(clickCount=newCount)
		print(faq_entry_counter)
		data = None
		
	return JsonResponse(data, safe=False)


def add_faq(request, header_id=None):
	if request.user.is_superuser:
		faq_form = FaqForm(request.POST or None, header_id=header_id)
	else:
		faq_form = NewFaq(request.POST or None)

	if request.method == 'POST':
		if faq_form.is_valid():
			faq_form.save()
			messages.success(request, 'Added FAQ entry')

	context = {
		'faq_form': faq_form
	}

	# next steps: remove superuser requirements, handle user adding differently to superuser
	# normal user adds will go to admin profile page queue for approval

	# next app: messaging system for companions and users

	return render(request, 'faq/add.html', context)


def redirect_services(request):
	return redirect('/faq')


def edit_faq(request, faq_id):
	faq_entry = get_object_or_404(FaqEntry, id=faq_id)
	faq_edit_form = FaqForm(request.POST or None, instance=faq_entry)

	if request.method == 'POST':
		if 'edit' in request.POST:
			if faq_edit_form.is_valid():
				faq_edit_form.save()
				messages.success(request, 'Edited FAQ entry') # not showing 
				return redirect('faq')

		if 'delete' in request.POST:
			faq_entry.delete()
			messages.warning(request, 'Deleted FAQ entry') # not showing 
			return redirect('faq')

	context = {
		'faq_edit_form': faq_edit_form,
		'faq_id': faq_id,
	}

	if request.user.is_superuser:
		return render(request, 'faq/edit.html', context)
	else:
		return redirect('faq')