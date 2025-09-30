from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Petition
from .forms import PetitionForm

def index(request):
    # List all petitions
    petitions = Petition.objects.all()
    template_data = {}
    template_data['title'] = 'Petitions'
    template_data['petitions'] = petitions
    return render(request, 'petitions/index.html',
                  {'template_data': template_data})

def show(request, id):
    # Show a single petition
    petition = get_object_or_404(Petition, id=id)
    template_data = {}
    template_data['title'] = petition.title
    template_data['petition'] = petition
    return render(request, 'petitions/show.html',
                  {'template_data': template_data})

@login_required
def create_petition(request):
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            return redirect('petitions.show', id=petition.id)
    else:
        form = PetitionForm()

    template_data = {}
    template_data['title'] = 'Create Petition'
    template_data['form'] = form
    return render(request, 'petitions/create_petition.html',
                  {'template_data': template_data})

@login_required
def vote_yes(request, id):
    petition = get_object_or_404(Petition, id=id)
    if request.method == 'POST':
        petition.yes_votes += 1
        petition.save()
    return redirect('petitions.show', id=id)
