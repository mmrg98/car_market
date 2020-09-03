from .models import Car
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CarForm

def car_list(request):
	cars = Car.objects.all()
	context = {
		"cars": cars,
	}
	return render(request, 'car_list.html', context)


def car_detail(request, car_id):
	car = Car.objects.get(id=car_id)
	context = {
		"car": car,
	}
	return render(request, 'car_detail.html', context)


def car_create(request):
	form = CarForm()
	if request.method == "POST":
		form = CarForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'created.')
			return redirect('car-list')

	context = {
        "form": form,
    }
	return render(request, 'create.html', context)


def car_update(request, car_id):
	car_obj = Car.objects.get(id=car_id)
	form = CarForm(instance=car_obj)
	if request.method == "POST":
		form = CarForm(request.POST,request.FILES, instance=car_obj)
		if form.is_valid():
			form.save()
			messages.success(request, 'updated.')
			return redirect('car-list')


	context = {
        "car_obj": car_obj,
        "form": form,
    }
	return render(request, 'update.html', context)



def car_delete(request, car_id):
	car_obj = Car.objects.get(id=car_id)
	car_obj.delete()
	messages.success(request, 'deleted.')
	return redirect('car-list')
