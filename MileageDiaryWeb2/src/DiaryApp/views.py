
# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.views.generic import ListView
from django.views.generic import UpdateView, CreateView, DeleteView, TemplateView
from django.urls import reverse
from .models import Log
from django.db.models import Q
from django.urls.base import reverse_lazy
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from DiaryApp.templatetags import utils
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('DiaryApp:index')
    else:
        form = UserCreationForm()
    return render(request, 'DiaryApp/signup.html', {'form': form})

def index(request):
    return render(request, 'DiaryApp/index.html')

@login_required
def home(request):
    
    log = Log.objects.filter(author_id = request.user.id).order_by('-updated_at')
    return render(request, 'DiaryApp/home.html', {'log': log})

def detail(request, log_id):
    logKm = get_object_or_404(Log, pk=log_id)
    return render(request, 'DiaryApp/detail.html', {'logKm': logKm})

def results(request, log_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % log_id)

def addLog(request, log_id):
    response = "You're looking at the addLog of question %s."
    return HttpResponse(response % log_id)

#一覧表示用のDjango標準ビュー(ListView)を承継して一覧表示用のクラスを定義
class LogListView(LoginRequiredMixin, ListView):
    #利用するモデルを指定
#    model = Log
    #データを渡すテンプレートファイルを指定
    template_name = 'DiaryApp/DiaryApp_list.html'
    #pagination
    paginate_by = 10
    #家計簿テーブルの全データを取得するメソッドを定義
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
        context["user"] = self.request.user
        return context
    def get_queryset(self):
        q_word = self.request.GET.get('query')
 
        if q_word:
            object_list = Log.objects.filter(
                Q(trip_memo__icontains=q_word), author_id = self.request.user.id)
        else:
            object_list = Log.objects.filter(author_id = self.request.user.id)
        return object_list
    
@login_required
@csrf_exempt
def ChartView(request, *args, **kwargs):
    passId = request.user
    if Log.objects.filter(author_id = request.user.id).values_list('km', flat=True):
        if request.POST.get('y1axis') in {'km', 'totalKm', 'litter', 'totalLitter', 'mileage', 'aveMileage', 'price', 'cost', 'totalCost'}:
            y1_list = utils.chartUtils(passId, request.POST.get('y1axis'))
            y1_label = utils.chartLabel(request.POST.get('y1axis'))
        else:
            y1_list = Log.objects.filter(author_id = request.user.id).values_list('km', flat=True)
            y1_label = '距離'
        
        if request.POST.get('y2axis') in {'km', 'totalKm', 'litter', 'totalLitter', 'mileage', 'aveMileage', 'price', 'cost', 'totalCost'}:
            y2_list = utils.chartUtils(passId, request.POST.get('y2axis'))
            y2_label = utils.chartLabel(request.POST.get('y2axis'))
        else:
            y2_list = Log.objects.values_list('litter', flat=True)
            y2_label = '給油量'
        x_list = Log.objects.filter(author_id = request.user.id).values_list('updated_at', flat=True)
    else:
        y1_list = [0]
        y2_list =[0]
        y1_label = 'No Data'
        y2_label = 'No Data'
        x_list = [0]
    
    y1max = max(y1_list)
    y1min = min(y1_list)
    y2max = max(y2_list)
    y2min = min(y2_list)
    return render(request, 'DiaryApp/log_chart.html', {'x_list' : x_list, 'y1_list' : y1_list, 'y2_list' : y2_list, 'y1_label' : y1_label, 'y2_label' : y2_label, 'y1max' : y1max, 'y2max' : y2max, 'y1min' : y1min, 'y2min' : y2min})

@login_required
def log_delete(request, log_id):
    logId = get_object_or_404(Log, pk=log_id)
    return render(request, 'DiaryApp/log_delete.html', {'logId': logId})


class LogUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'DiaryApp/log_update_form.html'
    model = Log
    fields = ['km', 'litter', 'price', 'trip_memo']
 
    def get_success_url(self):
        return reverse('DiaryApp:DiaryApp_list')
 
    def get_form(self):
        form = super(LogUpdateView, self).get_form()
        form.fields['km'].label = '走行距離'
        form.fields['litter'].label = '給油量'
        form.fields['price'].label = 'ガソリン単価'
        form.fields['trip_memo'].label = 'メモ'
        return form
    
class LogCreateView(LoginRequiredMixin, CreateView):
    template_name = 'DiaryApp/log_create_form.html'
    model = Log
    fields = ['km', 'litter', 'price', 'trip_memo']
 
    def form_valid(self, form):
        post = form.save(commit=False)
        # employeeフィールドはログインしているユーザ名とする
        post.author_id = self.request.user.id
        post.save()
        return redirect('DiaryApp:DiaryApp_list')

class LogDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'DiaryApp/log_delete.html'
    model = Log
 
    success_url = reverse_lazy('DiaryApp:DiaryApp_list')
    
def userId(request):
    userId = request.user.id
    return userId

def mileage(value, args):
    return round(value / args, 2)

def cost(value, args):
    return round(value * args, 0)

def totalKm(request, value):
    kmList = Log.objects.filter(author_id = request.user.id).values_list("km", flat=True).filter(id__range=(1, value))
    km = 0
    for itemKm in kmList:
        km += itemKm
    return km

def totalLitter(request, value):
    litterList = Log.objects.filter(author_id = request.user.id).values_list("litter", flat=True).filter(id__range=(1, value))
    litter = 0
    for itemLitter in litterList:
        litter += itemLitter
    return litter

def averageMileage(value):
    averageMileage = totalKm(value) / totalLitter(value)
    return round(averageMileage, 2)

def totalCost(value):
    litterList = Log.objects.values_list("litter", flat=True).filter(id__range=(1, value))
    priceList = Log.objects.values_list("price", flat=True).filter(id__range=(1, value))
    cost = 0
    for itemLitter, itemPrice in zip(litterList, priceList):
        cost += itemLitter * itemPrice
    return round(cost,0)

def chartKm():
    kmList = []
    for km in Log.objects.values_list("km", flat=True):
        kmList.append(km)
    return kmList

def chartId():
    idList = []
    for i in range(len(Log.objects.values_list("id", flat=True))):
        i += 1
        idList.append(i)
    return idList

def chartUtils(request, value):
    if value in {'km', 'litter', 'price'}:
        yaxis = value
        ylist = Log.objects.filter(author_id = request.user.id).values_list(f'{yaxis}', flat=True)
    elif value in {'totalKm'}:
        ylist = []
        for ids in Log.objects.values_list('id', flat=True):
            ylist.append(totalKm(ids))
    elif value in {'totalLitter'}:
        ylist = []
        for ids in Log.objects.values_list('id', flat=True):
            ylist.append(totalLitter(ids))
    elif value in {'mileage'}:
        ylist = []
        for ids in Log.objects.values_list('id', flat=True):
            km = Log.objects.values_list('km', flat=True).get(pk=ids)
            litter = Log.objects.values_list('litter', flat=True).get(pk=ids)
            ylist.append(mileage(km, litter))
    elif value in {'aveMileage'}:
        ylist = []
        for ids in Log.objects.values_list('id', flat=True):
            ylist.append(averageMileage(ids))
    elif value in {'cost'}:
        ylist = []
        for ids in Log.objects.values_list('id', flat=True):
            price = Log.objects.values_list('price', flat=True).get(pk=ids)
            litter = Log.objects.values_list('litter', flat=True).get(pk=ids)
            ylist.append(cost(price, litter))
    elif value in {'totalCost'}:
        ylist = []
        for ids in Log.objects.values_list('id', flat=True):
            ylist.append(totalCost(ids))
    else:
        yaxis = 'km'
        ylist = Log.objects.values_list(f'{yaxis}', flat=True)
    
    return ylist