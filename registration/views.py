from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth import logout
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from registration.tokens import account_activation_token
from .forms import RegisterForm
from .models import User


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)

            if User.objects.filter(username=user.username).exists():
                messages.error(request, "That username already exists")

            if User.objects.filter(email=user.email).exists():
                messages.error(request, "An account already exists with that email")

            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Planda Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(subject, message, "plandasoftware@gmail.com", [user.email])
            messages.success(request, "Check your email for activation link")
            return redirect(reverse("planner:landing_page"))
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


def logout_view(request):
    logout(request)

# def account_activation_sent(request):
#     return render(request, 'registration/confirmation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account successfully activated!")
        return redirect('planner:landing_page')
        # return reverse("/")
    else:
        return render(request, 'registration/account_activation_invalid.html')
