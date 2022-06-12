from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from .forms import CustomCreationForm, UserForm
from django.views import generic
from django.contrib.auth import login
from .models import User
from base.models import Room, Topic, Message
from django.db.models import Q, Count

# Create your views 
class SignUpView(generic.FormView):
    template_name = 'accounts/login_register.html'
    form_class = CustomCreationForm


    def get_context_data(self, **kwargs):
        page = 'signup'

        context = super().get_context_data(**kwargs)
        context.update({
            "page": page,
            'title':'SignUp',
        })

        return context
    

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        
        return super(SignUpView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('base:home')
        return super(SignUpView, self).dispatch(request, *args, **kwargs)



    def get_success_url(self):
        return reverse('base:home')

class CustomLoginView(LoginView):
    template_name = 'accounts/login_register.html'
    fields = '__all__'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('base:home')

    def get_context_data(self, **kwargs):
        page = 'login'

        context = super().get_context_data(**kwargs)
        context.update({
            "page": page,
            'title':'Login'
        })
        return context



def user_profile(request, slug):
    user = User.objects.get(slug=slug)
    print(user)
    q = request.GET.get('q') if request.GET.get('q') != None else ''
 
    topics = Room.objects.values('topic__name').annotate(Count('topic__name')).order_by('-topic__name__count')
    total_topics = Room.objects.aggregate(Count('topic'))

    rooms = user.room_set.all()
    messages = user.message_set.all()
        
    context = {
        
        'topics':topics,
        'user':user,
        'total_topics':total_topics,
        'messages':messages,
        'rooms':rooms,
        
    }

    # context = {
    # }


    return render(request, 'accounts/profile.html', context)


def user_settings(request):
    user = request.user
    
    form = UserForm(request.POST or None, request.FILES or None, instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST or None, request.FILES or None, instance=user)

        if form.is_valid():
            form.save()

            return redirect('accounts:user-profile')


    context ={
        'form':form
    }

    return render(request, 'accounts/user_settings.html', context=context)

