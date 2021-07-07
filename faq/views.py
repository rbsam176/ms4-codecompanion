from django.shortcuts import render
from faq.models import FaqEntry, FaqCategory

def faq(request):

	faq_content = FaqEntry.objects.all()
	faq_categories = FaqEntry.objects.values_list('category', flat=True).distinct()
	faq_categories_names = []
	for x in faq_categories:
		faq_categories_names.append(FaqCategory.objects.get(pk=x))
	
	print(faq_categories_names)

	context = {
		'faq_categories_names': faq_categories_names,
		'faq_content': faq_content,
	}

	return render(request, 'faq/faq.html', context)