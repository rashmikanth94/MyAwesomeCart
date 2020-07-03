from django.shortcuts import render
from django.http import HttpResponse
from .models import product, Contact, Orders, Orderupdate
from math import ceil
import json
# Create your views here.

def index(request):
	catprods=product.objects.values('category')
	'''
	print(catprods)
	[{'category': 'camera'}, {'category': 'camera'}, {'category': 'g'}, {'category': 'headphones'}, {'category': 'watches'}, {'category': 'glasses'}, {'category': 'phones'}, {'category': 'alltabs'}]

	'''
	cats={item['category'] for item in catprods }
	'''
	print(cats)
	{'watches', 'glasses', 'alltabs', 'phones', 'camera', 'headphones', 'g'}
	'''
	allprods=[]
	for cat in cats:
		prod=product.objects.filter(category=cat)
		n=len(prod)
		nslides=n//4+ceil((n/4)-n//4)
		allprods.append([prod,range(1,nslides),nslides])
	'''
	print(allprods)
	[[<QuerySet [<product: rayban>]>, range(1, 1), 1], [<QuerySet [<product: tablet>]>, range(1, 1), 1], [<QuerySet [<product: headphone>]>, range(1, 1), 1], [<QuerySet [<product: boat headphone>]>, range(1, 1), 1], [<QuerySet [<product: canon>, <product: gopro>]>, range(1, 1), 1], [<QuerySet [<product: Titan>]>, range(1, 1), 1], [<QuerySet [<product: iphone8>]>, range(1, 1), 1]]
	'''
	params={'allprods':allprods}
	return render(request,'shop/index.html',params)
def about(request):
	return render(request,'shop/about.html')
def contact(request):
	if request.method =="POST":
		name=request.POST.get('qname','')
		email=request.POST.get('qemail','')
		phone=request.POST.get('qphone','')
		desc=request.POST.get('qquery','')
		cont = Contact(name=name,email=email,phone=phone,desc=desc)
		cont.save()
		return render(request,'shop/contact.html',{'submitted':True})


	return render(request,'shop/contact.html')
def status(request):
	if request.method =="POST":
		Orderid=request.POST.get('orderid','')
		email=request.POST.get('email','')

		try:
			order=Orders.objects.filter(order_id=Orderid,email=email)
			if len(order)>0:
				update=Orderupdate.objects.filter(order_id=Orderid)
				updates=[]
				for i in update:
					updates.append({'text':i.update_desc,  'time':i.timestamp})
					response=json.dumps([updates,order[0].items_json],default=str)
				return HttpResponse(response)
			else:
				return HttpResponse('{}')

		except Exception as a:
				return HttpResponse('{}')

	return render(request,'shop/status.html')
def search(request):
	proname=request.POST.get('proname','nothing')
	actualprod=[]
	searchedprods=product.objects.values('product_name')
	for item in searchedprods:
		actualprod=product.objects.filter(product_name=proname)
	print(actualprod)

	return render(request,'shop/search.html',{'product':actualprod[0]})
def productview(request,myid):
	products=product.objects.filter(id=myid)
	print(products)
	return render(request,'shop/productview.html',{'product':products[0]})
def checkout(request):
	if request.method =="POST":
		items_json=request.POST.get('itemsJson','')
		name=request.POST.get('name','')
		email=request.POST.get('email','')
		address=request.POST.get('address1','')+" "+request.POST.get('address2','')
		city=request.POST.get('city','')
		state=request.POST.get('state','')
		zip_code=request.POST.get('zip_code','')
		phone=request.POST.get('phone','')

		order = Orders(items_json=items_json,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone)
		order.save()
		update=Orderupdate(order_id=order.order_id,update_desc="The order has been placed")
		update.save()
		thank=True
		id=order.order_id
		return render(request,'shop/checkout.html',{'thank':thank,'id':id})

	return render(request,'shop/checkout.html')