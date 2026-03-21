from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group

from .forms import RegisterForm, LoginForm
from .models import AppUser

def is_manager(user):
    return user.is_authenticated and user.role == "manager"


class RegisterView(CreateView):

    model = AppUser
    form_class = RegisterForm
    template_name = "accounts/register-page.html"
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save()

        #default role
        user.role = "user"
        user.save()

        messages.success(
            self.request,
            "Регистрацията е успешна. Моля влезте в профила си."
        )

        return redirect(self.success_url)


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login-page.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


#защитен view само заmanager
@method_decorator(user_passes_test(is_manager), name='dispatch')
class ManagerOnlyView(CreateView):
    template_name = "some_template.html"


from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {
        "user": request.user
    })