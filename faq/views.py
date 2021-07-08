from django.shortcuts import render
from faq.models import FaqEntry, FaqCategory

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