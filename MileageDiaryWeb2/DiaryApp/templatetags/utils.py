'''
Created on 2020/07/16

@author: snowc
'''


from django import template
from DiaryApp.models import Log
import html
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
 
register = template.Library()
 
#自作フィルタの名称を定義
@register.simple_tag
def Vuser():
    u = get_user_model()
    return u

#自作フィルタで実行される処理内容を関数として定義
@register.filter
def mileage(value, args):
    return round(value / args, 2)

@register.filter
def cost(value, args):
    return round(value * args, 0)

@register.simple_tag
def totalKm(passedId, value):
    passId = passedId
    kmList = Log.objects.values_list("km", flat=True).filter(author_id=passId, id__range=(1, value))
    km = 0
    for itemKm in kmList:
        km += itemKm
    return km

@register.simple_tag
def totalLitter(passedId, value):
    passId = passedId
    litterList = Log.objects.values_list("litter", flat=True).filter(author_id=passId, id__range=(1, value))
    litter = 0
    for itemLitter in litterList:
        litter += itemLitter
    return litter

@register.simple_tag
def averageMileage(passedId, value):
    passId = passedId
    averageMileage = totalKm(passId, value) / totalLitter(passId, value)
    return round(averageMileage, 2)

@register.simple_tag
def totalCost(passedId, value):
    passId = passedId
    litterList = Log.objects.values_list("litter", flat=True).filter(author_id=passId, id__range=(1, value))
    priceList = Log.objects.values_list("price", flat=True).filter(author_id=passId, id__range=(1, value))
    cost = 0
    for itemLitter, itemPrice in zip(litterList, priceList):
        cost += itemLitter * itemPrice
    return round(cost,0)

@register.simple_tag
def chartKm():
    kmList = []
    for km in Log.objects.values_list("km", flat=True):
        kmList.append(km)
    return kmList

@register.simple_tag
def chartId():
    idList = []
    for i in range(len(Log.objects.values_list("id", flat=True))):
        i += 1
        idList.append(i)
    return idList

@register.simple_tag
def chartUtils(passId, value):
    passedId = passId
    if value in {'km', 'litter', 'price'}:
        yaxis = value
        ylist = Log.objects.filter(author_id=passedId).values_list(f'{yaxis}', flat=True)
    elif value in {'totalKm'}:
        ylist = []
        for ids in Log.objects.filter(author_id=passedId).values_list('id', flat=True):
            ylist.append(totalKm(passedId, ids))
    elif value in {'totalLitter'}:
        ylist = []
        for ids in Log.objects.filter(author_id=passedId).values_list('id', flat=True):
            ylist.append(totalLitter(passedId, ids))
    elif value in {'mileage'}:
        ylist = []
        for ids in Log.objects.filter(author_id=passedId).values_list('id', flat=True):
            km = Log.objects.filter(author_id=passedId).values_list('km', flat=True).get(pk=ids)
            litter = Log.objects.filter(author_id=passedId).values_list('litter', flat=True).get(pk=ids)
            ylist.append(mileage(km, litter))
    elif value in {'aveMileage'}:
        ylist = []
        for ids in Log.objects.filter(author_id=passedId).values_list('id', flat=True):
            ylist.append(averageMileage(passedId, ids))
    elif value in {'cost'}:
        ylist = []
        for ids in Log.objects.filter(author_id=passedId).values_list('id', flat=True):
            price = Log.objects.filter(author_id=passedId).values_list('price', flat=True).get(pk=ids)
            litter = Log.objects.filter(author_id=passedId).values_list('litter', flat=True).get(pk=ids)
            ylist.append(cost(price, litter))
    elif value in {'totalCost'}:
        ylist = []
        for ids in Log.objects.filter(author_id=passedId).values_list('id', flat=True):
            ylist.append(totalCost(passedId, ids))
    else:
        yaxis = 'km'
        ylist = Log.objects.filter(author_id=passedId).values_list(f'{yaxis}', flat=True)
    
    return ylist

@register.simple_tag
def chartLabel(value):
    if value in {'km'}:
        label = '走行距離(km)'
    elif value in {'totalKm'}:
        label = '累計走行距離(km)'
    elif value in {'litter'}:
        label = '給油量(L)'
    elif value in {'totalLitter'}:
        label = '累計給油量(L)'
    elif value in {'mileage'}:
        label = '燃費(km/L)'
    elif value in {'aveMileage'}:
        label = '平均燃費(km/L)'
    elif value in {'price'}:
        label = 'ガソリン単価(円)'
    elif value in {'cost'}:
        label = 'ガソリン代(円)'
    elif value in {'totalCost'}:
        label = '累計ガソリン代(円)'
    else :
        label = '未選択'
    return label
    