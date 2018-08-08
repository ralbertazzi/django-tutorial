from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from .models import Album
from .forms import UserForm


class IndexView(generic.ListView):
    context_object_name = 'albums'  # default is object_list
    template_name = 'music/index.html'

    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class AlbumCreate(generic.CreateView):
    model = Album
    fields = ['artist', 'title', 'genre', 'logo']


class AlbumUpdate(generic.UpdateView):
    model = Album
    fields = ['artist', 'title', 'genre', 'logo']


class AlbumDelete(generic.DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class UserFormView(generic.View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    # user doesn't have an account
    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})


    # User types in information and hits submit
    # Create a new user
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            # Create an object from the form, but don't save it yet
            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            # returns User object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                return redirect('music:index')
                # from now on you can user request.user

        return render(request, self.template_name, {'form': form})