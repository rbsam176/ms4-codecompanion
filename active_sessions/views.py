from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from profiles.forms import UserProfile

@login_required
def active_sessions(request):
    account = get_object_or_404(User, username=request.user)
    profile = get_object_or_404(UserProfile, user=request.user)
    # orders = profile.orders.filter(active=True).order_by('-date')

    context = {
        'account': account,
        'profile': profile,
        # 'orders': orders,
    }

    return render(request, 'active_sessions/active_sessions.html', context)