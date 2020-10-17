from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from .models import News, Company, Query, Enrolled
import numpy as np
from django.core.mail import send_mail

# Create your views here.
import matplotlib.pyplot as plt
import io
import urllib,base64
def home(request):
    context = {
    'news' : News.objects.all()
    }
    return render(request,'TPO/home.html',context)

def analytics(request):
    company_names = ['Consultancy','Core','Finance','FinTech','Product','Tech']
    no_of_student_placed = [8,3,5,7,15,35]
    plt.bar(company_names,no_of_student_placed,color=('r','b','k','g','m','y'))
    fig=plt.gcf()
    buf=io.BytesIO()
    fig.savefig(buf,format="png")
    buf.seek(0)
    s=base64.b64encode(buf.read())
    url=urllib.parse.quote(s)

    plt.clf()
    plt.pie(no_of_student_placed, explode=[0,0,0,0,0.1,0],startangle=90,shadow=True ,labels=company_names, colors=('r','b','k','g','m','y'))
    fig1=plt.gcf()
    buf1=io.BytesIO()
    fig1.savefig(buf1,format="png")
    buf1.seek(0)
    st=base64.b64encode(buf1.read())
    url1=urllib.parse.quote(st)

    plt.clf()
    year = ['2016-17','2017-18','2018-19','2019-20']
    salary_per_yr = [6.40,6.50,8.02,10.50]
    plt.bar(year,salary_per_yr,width=0.5)
    for index,data in enumerate(salary_per_yr):
        plt.text(x=index-0.1 , y =data//2 , s=f"{data}" , fontdict=dict(fontsize=10))
    plt.tight_layout()
    fig2=plt.gcf()
    buf2=io.BytesIO()
    fig2.savefig(buf2,format="png")
    buf2.seek(0)
    st=base64.b64encode(buf2.read())
    url2=urllib.parse.quote(st)

    plt.clf()
    data = [[30, 25, 50, 20],
    [40, 23, 51, 17],
    [30, 18, 40, 19],
    [32, 21, 43, 14],
    [38, 16, 52, 20]]
    # [32, 20, 48, 24]]

    legend = ['ETRX','EXTC','IT','COMPS','MCA']
    labels = ['2016-17','2017-18','2018-19','2019-20']
    X = np.arange(4)
    fig = plt.figure()
    ax = fig.add_axes([0.05,0.05,0.95,0.95])
    ax.set_xticks(X)
    ax.bar(X + 0.00, data[0], width = 0.10)
    ax.bar(X + 0.12, data[1], width = 0.10)
    ax.bar(X + 0.24, data[2], width = 0.10)
    ax.bar(X + 0.36, data[3], width = 0.10)
    ax.bar(X + 0.48, data[4], width = 0.10)
    # ax.bar(X + 0.6, data[5], width = 0.10)
    ax.set_xticks(X)
    ax.set_xticklabels(labels)
    ax.legend(legend)
    fig2=plt.gcf()
    buf2=io.BytesIO()
    fig2.savefig(buf2,format="png")
    buf2.seek(0)
    st=base64.b64encode(buf2.read())
    url3=urllib.parse.quote(st)

    plt.clf()

    return render(request,"TPO/analytics.html",{"bar":url,"pie":url1,"bar1":url2 , "bar2": url3})

class NewsListView(ListView):
    model = News
    template_name = 'TPO/home.html' #<app><model>_<viewtype>.html
    context_object_name = 'newss'
    ordering = ['-date_posted']
    paginate_by = 4

class NewsDetailView(DetailView):
    model = News

def about(request):
    return render(request,'TPO/about.html',{'title' : 'About'})

# def analytics(request):
#     return render(request,'TPO/about.html',{'title' : 'Analytics'})

def dashboard(request):
    Companies = Company.objects.all()
    L =  Company.objects.count()
    Grid = []
    i = 0
    while i<=L-3:
        Grid.append(Companies[i:i+3])
        i+=3
    if i<L:
        Grid.append(Companies[i:])
    return render(request,'TPO/dashboard.html',{'Grid':Grid})

class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = get_object_or_404(Company, id = self.kwargs.get('pk'))
        user = self.request.user
        en = Enrolled.objects.filter(student = user, company = company)
        if len(en)==0:
            context['check'] = True
        else:
            context['check'] = False
        return context

class CompanyQueryListView(ListView):
    model = Query
    template_name = 'TPO/company_queries.html' #<app><model>_<viewtype>.html
    context_object_name = 'queries'
    #ordering = ['-date_posted']
    paginate_by = 5
    
    def get_queryset(self):
        company = get_object_or_404(Company, title = self.kwargs.get('title'))
        return Query.objects.filter(company=company).order_by('-date_posted')    

class QueryCreateView(LoginRequiredMixin, CreateView):
    model = Query
    success_url = '/'
    fields = ['content']
    def form_valid(self,form):
        form.instance.student = self.request.user
        form.instance.company = Company.objects.get(title=self.kwargs.get('title'))
        return super().form_valid(form)

class CompanyCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Company
    success_url = '/'
    fields = ['title', 'description','background','Eligibility','Status']
    
    def form_valid(self,form):
        return super().form_valid(form)
    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

class QueryUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Query
    success_url = '/'
    fields = ['content']
    
    def form_valid(self,form):
        form.instance.student = self.request.user
        #form.instance.company = Company.objects.filter(title=self.kwargs.get('title'))
        return super().form_valid(form)
    
    def test_func(self):
        query = self.get_object()
        if self.request.user == query.student:
            return True
        return False

class CompanyUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Company
    success_url = '/'
    fields = ['title', 'description','background','Eligibility','Status']
    def form_valid(self,form):
        return super().form_valid(form)
    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

class QueryDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Query
    success_url = '/'

    def form_valid(self,form):
        form.instance.student = self.request.user
        #form.instance.company = Company.objects.filter(title=self.kwargs.get('title'))
        return super().form_valid(form)

    def test_func(self):
        query = self.get_object()
        if self.request.user == query.student:
            return True
        return False

class CompanyDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Company
    success_url = '/'

    def form_valid(self,form):
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False
'''
class EnrolledCreateView(LoginRequiredMixin, CreateView):
    
    model = Enrolled
    template_name = 'TPO/enrolled_form.html' #<app><model>_<viewtype>.html
    context_object_name = 'enrolled'
    success_url = '/'
    fields = ['date_applied']
    def form_valid(self,form):
        form.instance.student = self.request.user
        form.instance.company = Company.objects.get(title=self.kwargs.get('title'))
        return super().form_valid(form)
'''

def enrolled(request,title):
    send_mail('Application', 'Hello ' + request.user.username + ',' + '\nYou have successfully applied for ' + title + '.', 'avdeveloper00@gmail.com', [request.user.email])
    enrolled = Enrolled.objects.create(student = request.user, company = Company.objects.get(title = title) )
    return redirect('TPO-home')
