from django.http import HttpResponse
from django.shortcuts import render, redirect
from playground.models import User_info
from playground.retrieval import getOutput
def form(request):
    return render(request,'diet.html')
def process_userform(request):
    if(request.method=='POST'):
        cuisine_name=request.POST.get("cuisine_name")
        allergies=request.POST.get("allergies")
        height=request.POST.get("height")
        weight=request.POST.get("weight")
        food_type=request.POST.getlist("food_type")
        age=request.POST.get("age")
        goals=request.POST.get("goals")
        issues=request.POST.get("issues")
        gender=request.POST.get("gender")
        user=User_info(cuisine_name=cuisine_name,food_type=food_type,allergies=allergies,height=height,weight=weight,age=age,goals=goals,issues=issues,gender=gender)
        user.save()
        return render(request,'response.html',getOutput())




