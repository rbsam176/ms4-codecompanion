from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from faq.models import FaqEntry, FaqQuestion
from .forms import AddUserFaq
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def admin_controls(request):
	faq_questions = FaqQuestion.objects.all()

	context = {
		'faq_questions': faq_questions,
	}

	if request.method == 'POST':
		if 'delete' in request.POST:
			faq_id = get_object_or_404(FaqQuestion, id=request.POST['delete'])
			faq_id.delete()
			messages.warning(request, 'Removed user-submitted question')
			return redirect('admin_controls')

	if request.user.is_superuser:
		return render(request, 'admin/admin_controls.html', context)
	else:
		return redirect('home')


def redirect_services(request):
	return redirect('/admin_controls')
	

@staff_member_required
def edit_question(request, question_id):
	faq_question = FaqQuestion.objects.get(id=question_id)
	faq_category = faq_question.category
	faq_form = AddUserFaq(request.POST or None, faq_question=faq_question, faq_category=faq_category)

	if request.method == 'POST':
		if faq_form.is_valid():
			faq_form.save()
			faq_question.delete()
			messages.success(request, 'Added FAQ entry')
			return redirect('faq')

	context = {
		'faq_form': faq_form,
		'question_id': question_id,
	}

	if request.user.is_superuser:
		return render(request, 'admin/edit_question.html', context)
	else:
		return redirect('home')