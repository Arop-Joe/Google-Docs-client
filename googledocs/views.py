from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views import View
from . import api
from .models import Document

class IndexView(LoginRequiredMixin, TemplateView):
	template_name = "googledocs/addnew.html"
	login_url = '/login/'

class DocumentListView(LoginRequiredMixin, ListView):
	model = Document
	login_url = '/login/'
	
class DocumentCreatorView(View):
	DOCTYPE_SHEET = "sheet"
	doctype = ""

	def create(self, type, name, user):
		if self.doctype == self.DOCTYPE_SHEET:
			link = api.create_sheet(name)
		else:
			link = api.create_doc(name)
		sheet = Document(name=name, user=user, link=link)
		sheet.save()
		return link

	def get(self, request):
		if request.GET['name']:
			link = self.create(self.doctype, request.GET['name'], request.user)
			return JsonResponse({
				'data': link
			})
		else:
			return JsonResponse({
				'error': 'Brak nazwy.'
			})

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('index')
	else:
		form = UserCreationForm()
		context = {
			'form': form
		}
		return render(request, 'registration/register.html', context)