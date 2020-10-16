from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from .models import News, Company, Query
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
    return render(request,"TPO/analytics.html",{"bar":url,"pie":url1,"bar1":url2})

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
        Grid.append(Companies[i-1:])
    return render(request,'TPO/dashboard.html',{'Grid':Grid})

class CompanyDetailView(DetailView):
    model = Company

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