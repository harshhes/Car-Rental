from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from login_otp.settings import AUTH_KEY
from .models import Profile, Vehicle
import random, requests
from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated

def send_otp(mobile, otp):
        try: 
            url = f"https://2factor.in/API/V1/{AUTH_KEY}/SMS/+91{mobile}/{otp}/opt1"
            response = requests.get(url)
            return otp
        except Exception as e:
            return "Something went wrong!!"

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')

        check_mobile = Profile.objects.filter(mobile=mobile).first()
        check_username = User.objects.filter(username=username).first()

        if check_mobile:
            context = {"message": "Mobile already registered!!", "class":"danger"}
            return render(request, 'register.html', context=context)

        if check_username:
            context = {"message": "Username already registered!!", "class":"danger"}
            return render(request, 'register.html', context=context)

        user = User(username=username, first_name=name)
        user.save()

        otp = str(random.randint(1000,9999))
        profile = Profile(user=user, mobile=mobile, otp=otp)
        profile.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('otp')

        # context = {"message": "User Registered Successfully!!"}
        # return render(request, 'register.html', context=context)
    
    return render(request, 'register.html')

login_required(login_url='/')
def otp(request):
    try:
        mobile = request.session['mobile']
    except Exception:
        return HttpResponse("<h1>Please Register first!!</h1>")
    context = {'mobile': mobile}
    if request.method == "POST":
        otp = request.POST.get('otp')
        profile = Profile.objects.get(mobile=mobile)
        if otp == profile.otp:
            context['message'] = "User Registered Successfully!!"
            context['class'] = 'success'
            return render(request, 'otp.html', context=context)
        else:
            context['message'] = "Invalid OTP!!!"
            context['class'] = 'danger'
            return render(request, 'otp.html', context=context)
    return render(request, 'otp.html', context=context)


def login_user(request):
    if request.method == "POST":
        mobile = request.POST.get('mobile')

        user = Profile.objects.get(mobile=mobile)
        if not user:
            context = {"message": "User not found!!", "class":"danger"}
            return render(request, 'login.html', context=context)

        otp = str(random.randint(1000,9999))
        user.otp = otp
        user.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('login_otp')

    return render(request, 'login.html')

@login_required(login_url='/login')
def login_otp(request):
    mobile = request.session['mobile']
    context = {'mobile': mobile}
    if request.method == "POST":
        user_profile = Profile.objects.get(mobile=mobile)
        otp = request.POST.get('otp')

        if otp == user_profile.otp:
            user = User.objects.get(id=user_profile.user.id)
            login(request,user)
            return redirect('main')

        else:
            context['message'] = "Invalid OTP!!!"
            context['class'] = 'danger'
            return render(request, 'login_otp.html', context=context) 

    return render(request, 'login_otp.html', context=context) 

@login_required(login_url='/login')
def main(request):
    return HttpResponse("<h1>Logged In Successfully!!!!</h1>")



# add a vehicle(only for admins)
class AddVehicleView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = AddVehicleSerializer
    permission_classes = [IsAdminUser]

# add vehicle to inventory an assign it to a station
class DetailVehicleView(generics.RetrieveUpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = AddVehicleSerializer
    permission_classes = [IsAdminUser]

# admin can create a station
class VehicleStationView(generics.ListCreateAPIView):
    queryset = VehicleStation.objects.all()
    serializer_class = VehicleStationSerializer
    permission_classes = [IsAdminUser]


# User can see available vehicles at a particular station
class GetVehicles(generics.GenericAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def get(self, request, *args, **kwargs):
        station = request.query_params.get('station')
        # import ipdb; ipdb.set_trace()
        vehicles = Vehicle.objects.filter(station=station, is_available=True)
        print(vehicles)
        serializer = VehicleSerializer(vehicles,many=True)
        return Response(serializer.data,200)


# Pick a vehicle
class PickVehicle(generics.GenericAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        vehicle_id = request.query_params.get('vehicle_id')
        user = request.user
        print(user, user.id)
        # import ipdb; ipdb.set_trace()
        vehicle = Vehicle.objects.filter(id=vehicle_id).first()
        vehicle_history = VehicleHistory.objects.create(vehicle=vehicle, user=user, vehicle_station=vehicle.station)
        return Response("success!!", 200)

    
# drop vehicle post-usage
class VehicleHistoryView(generics.GenericAPIView):
    queryset = VehicleHistory.objects.all()
    serializer_class = VehicleHistorySerializer
    permission_classes = [IsAuthenticated]

    
    #drop vehicle post-usage
    def patch(self, request, pk=None):
        instance = self.get_object()
        print(instance)

        serializer = VehicleHistorySerializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,200)