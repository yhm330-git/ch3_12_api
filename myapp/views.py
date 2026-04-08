from urllib import request

from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import *
from django.forms.models import model_to_dict

def search_list(request):
    if 'cname' in request.GET:
        cname = request.GET['cname']
        print("cname=", cname)
        # resultList = students.objects.filter(cname=cname)
        resultList = students.objects.filter(cname__contains=cname) # 模糊查詢，包含cname的資料都會被查出來
    else:
        resultList = students.objects.all().order_by('cid')


    for item in resultList:
        print(model_to_dict(item))
    # return HttpResponse("Hello, world. You're at the search_list index.")
    errormessage=""
    # resultList=[] # 模擬查無資料的情況
    if not resultList:
        errormessage="No data found."
    # return render(request, 'search_list.html', locals())
    return render(request, 'search_list.html', {'resultList': resultList, 'errormessage': errormessage})

def search_name(request):
    return render(request, 'search_name.html')

from django.db.models import Q
from django.core.paginator import Paginator
def index(request):
    if 'site_search' in request.GET:
        site_search = request.GET['site_search']
        site_search = site_search.strip()  # 去除前後空白
        keywords = site_search.split()  # 將關鍵字分割成列表
        # print(f"site_search={site_search}")
        print(f"keywords={keywords}")
        # 一個關鍵字+搜尋一個欄位
        # resultList = students.objects.filter(cname__contains=site_search).order_by('cid') # 模糊查詢，包含site_search的資料都會被查出來
        # 一個關鍵字+搜尋多個欄位
        # resultList = students.objects.filter(
        #     Q(cid__contains=site_search) |
        #     Q(cname__contains=site_search) | 
        #     Q(cbirthday__contains=site_search) |
        #     Q(cemail__contains=site_search) | 
        #     Q(cphone__contains=site_search) |
        #     Q(caddr__contains=site_search)
        # )
        # 多個關鍵字+搜尋多個欄位
        query = Q() 
        for keyword in keywords:
            query |= Q(cid__contains=keyword) | Q(cname__contains=keyword) | Q(cbirthday__contains=keyword) | Q(cemail__contains=keyword) | Q(cphone__contains=keyword) | Q(caddr__contains=keyword)
        resultList = students.objects.filter(query).order_by('cid')
    else:
        resultList = students.objects.all().order_by('cid')

    for item in resultList:
        print(model_to_dict(item))
    data_count = len(resultList)
    print(f"Total data count: {data_count}")
    status = True
    errormessage = ""
    if not resultList:
        status = False
        errormessage = "No data found."
    # return HttpResponse("Hello, world. You're at the index page.")

    # 分頁設定，每頁顯示兩筆資料
    paginator = Paginator(resultList, 2)
    page_number = request.GET.get('page')  # 從URL參數獲取當前頁碼
    page_obj = paginator.get_page(page_number)  # 獲取當前頁的資料
    print(f"Current page number: {page_number}")
    for item in page_obj:
        print(model_to_dict(item))


    return render(request, 'index.html', 
                  {'resultList': resultList, 
                   'status': status, 
                   'errormessage': errormessage, 
                   'data_count': data_count,
                   'page_obj': page_obj
                   }
                  )
from django.shortcuts import redirect
def post(request): 
    if request.method == 'POST':
        cname = request.POST.get('cname')
        csex = request.POST.get('csex')
        cbirthday = request.POST.get('cbirthday')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        caddr = request.POST.get('caddr')
        print(f"Received POST data: cname={cname}, csex={csex}, cbirthday={cbirthday}, cemail={cemail}, cphone={cphone}, caddr={caddr}")
        add = students(cname=cname, csex=csex, cbirthday=cbirthday, cemail=cemail, cphone=cphone, caddr=caddr)
        add.save()

        # return HttpResponse("已送出 POST 请求。")
        return redirect('index')  # 重定向到 index 页面，显示更新后的数据列表
    else:
        return render(request, 'post.html')
    # return HttpResponse("Hello, this is the post page.")

def edit(request, id):
    print(id)
    if request.method == 'POST':
        cname = request.POST.get('cname')
        csex = request.POST.get('csex')
        cbirthday = request.POST.get('cbirthday')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        caddr = request.POST.get('caddr')
        print(f"Received POST data: cname={cname}, csex={csex}, cbirthday={cbirthday}, cemail={cemail}, cphone={cphone}, caddr={caddr}")
        #orm
        update = students.objects.get(cid=id)
        update.cname = cname
        update.csex = csex
        update.cbirthday = cbirthday
        update.cemail = cemail  
        update.cphone = cphone
        update.caddr = caddr
        update.save()
        return redirect('index')  # 重定向到 index 页面，显示更新后的数据列表

        # return HttpResponse("已送出 POST 请求。")
    else:
        obj_data = students.objects.get(cid=id)
        print(model_to_dict(obj_data))
        # return HttpResponse("Hello")
        return render(request, 'edit.html', {'obj_data': obj_data})
    
def delete(request, id):
    print(id)
    if request.method == 'POST':
        delete_data = students.objects.get(cid=id)
        delete_data.delete()
        return redirect('index')
        # return HttpResponse("已送出 POST 請求")
    else:
        obj_data = students.objects.get(cid=id)
        print(model_to_dict(obj_data))
        return render(request, 'delete.html', {'obj_data': obj_data})

from django.http import JsonResponse    
def getAllItems(request):
    resultObject = students.objects.all().order_by('cid')
    # print(type(resultList))
    # for item in resultList:
    #     # print(model_to_dict(item))
    #     print(type(item))
    resultList = list(resultObject.values()) # 將 "querySet(元素為object)" 轉成 "list(元素為dict)" 的型態
    # print(type(resultList))
    # for item in resultList:
    #     # print(model_to_dict(item))
    #     print(type(item))

    # return HttpResponse("Hello")
    return JsonResponse(resultList, safe=False)
    # safe=True: 只允許傳入dict
    # safe=False: 只允許傳入非dict

def getItem(request, id):
    try:
        obj = students.objects.get(cid=id)
        # print(model_to_dict(obj))
        resultDict = model_to_dict(obj) # 將object轉成dict
        # return HttpResponse("Hello")
        return JsonResponse(resultDict, safe=False)
    except:
        # return HttpResponse("False")
        return JsonResponse({"error": "Item not found"}, status=404)

from django.views.decorators.csrf import csrf_exempt
# 停止csrf驗證，讓前端可以直接呼叫api，不需要csrf token
@csrf_exempt    
def createItem(request):
    try:
        if request.method == "GET":
            cname = request.GET['cname']
            csex = request.GET['csex']
            cbirthday = request.GET['cbirthday']
            cemail = request.GET['cemail']
            cphone = request.GET['cphone']
            caddr = request.GET['caddr']
            print(f"GET data: cname={cname}, csex={csex}, cbirthday={cbirthday}, cemail={cemail}, cphone={cphone}, caddr={caddr}")
            # return HttpResponse("GET...")
        elif request.method == "POST":
            cname = request.POST['cname']
            csex = request.POST['csex']
            cbirthday = request.POST['cbirthday']
            cemail = request.POST['cemail']
            cphone = request.POST['cphone']
            caddr = request.POST['caddr']
            print(f"POST data: cname={cname}, csex={csex}, cbirthday={cbirthday}, cemail={cemail}, cphone={cphone}, caddr={caddr}")
            # return HttpResponse("POST...")
        try:
            add = students(cname=cname, csex=csex, cbirthday=cbirthday, cemail=cemail, cphone=cphone, caddr=caddr)
            add.save()
            return JsonResponse({"message": "Item created successfully"}, status=201)
        except:
            return JsonResponse({"error": "Failed to create item"}, status=500)
    except:
        return JsonResponse({"error": "Invalid data"}, status=400)

@csrf_exempt     
def updateItem(request, id):
    print(f"Updating item with ID: {id}")
    try:
        if request.method == "GET":
            cname = request.GET['cname']
            csex = request.GET['csex']
            cbirthday = request.GET['cbirthday']
            cemail = request.GET['cemail']
            cphone = request.GET['cphone']
            caddr = request.GET['caddr']
            print(f"GET data: cname={cname}, csex={csex}, cbirthday={cbirthday}, cemail={cemail}, cphone={cphone}, caddr={caddr}")
            # return HttpResponse("GET...")
        elif request.method == "POST":
            cname = request.POST['cname']
            csex = request.POST['csex']
            cbirthday = request.POST['cbirthday']
            cemail = request.POST['cemail']
            cphone = request.POST['cphone']
            caddr = request.POST['caddr']
            print(f"POST data: cname={cname}, csex={csex}, cbirthday={cbirthday}, cemail={cemail}, cphone={cphone}, caddr={caddr}")
            # return HttpResponse("POST...")
        try:
            # orm
            update = students.objects.get(cid=id)
            update.cname = cname
            update.csex = csex
            update.cbirthday = cbirthday
            update.cemail = cemail  
            update.cphone = cphone
            update.caddr = caddr
            update.save()
            return JsonResponse({"message": "Item updated successfully"}, status=200)
        except:
            return JsonResponse({"error": "Failed to update item"}, status=500)
    except:
        return JsonResponse({"error": "Invalid data"}, status=400)