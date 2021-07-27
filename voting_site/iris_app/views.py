from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import *
from .forms import *
from .models import Voter, Votes
from django.db.models import Count
from .functions import handle_uploaded_files
from django.contrib.auth.decorators import login_required
from datetime import datetime
from datetime import date, time
from django.utils import timezone
import os
import cv2
import tensorflow as tf
import numpy as np


# Create your views here.
def index(request):
    return render(request, "index.html")


def login(request):
    last_login.objects.all().delete()
    if request.method == 'POST':
        voterid = request.POST['voterid']
        phone = request.POST['mobile']
        if Voter.objects.filter(Voter_id=voterid, Phone_Number=phone).exists():
            g = last_login(voter_id=voterid)
            g.save()
            return redirect('detect_person')
        else:
            return render(request, "login.html", {'msg': 'Invalid Credentials..!'})
    else:
        return render(request, "login.html")


def home(request):
    return render(request, 'home.html')

@login_required(login_url="/login")
def iris(request):
    return render(request, 'iris_upload.html')

@login_required(login_url="/login")
def profile(request):
    var = prediction.objects.all().last()
    voterid = var.predicted_label
    if Voter.objects.filter(Voter_id=voterid).exists():
        profile_view = Voter.objects.get(Voter_id=voterid)
        return render(request, 'voter_profile.html',
                      {
                          'profile_view': profile_view
                      })
    else:
        return render(request, "iris_upload.html", {'msg': 'Not exist..!'})

@login_required(login_url="/login")
def poll(request):
    voter = last_login.objects.all().last()
    voterid = voter.voter_id
    voterdet = Voter.objects.get(Voter_id=voterid)
    status = voterdet.Poling_Status
    electiontime = CreateElection.objects.all().last()
    start = electiontime.Election_Start_Date.date()
    end = electiontime.Election_End_Date.date()
    start_time = electiontime.Election_Start_Date.time()
    end_time = electiontime.Election_End_Date.time()
    now = timezone.now()
    print(str(datetime.now()))
    print(str(start))
    print(str(start_time))
    if date.today() == start and date.today() == end:
        if datetime.now().time() >= start_time:
            print(datetime.now().time())
            if datetime.now().time() <= end_time:
                if status==False:
                    print(voterid)
                    voter = Voter.objects.get(Voter_id=voterid)
                    print(voter)
                    nominee_view = Add_Nominee.objects.all()
                    return render(request, 'polling.html', {
                    'nominee_view': nominee_view,
                    'voter': voterid,
                    'electiontime': electiontime
                    })
                else:
                    return render(request, 'success.html', {'votedmsg': 'Already voted'})
            else:
                return render(request, 'datetime.html', {'msg': 'Sorry...! , Election time exceeded.'})
        else:
            return render(request, 'datetime.html', {'msg': 'Sorry...! , Election not started.'})
    else:
        return render(request, 'datetime.html', {'msg': 'Sorry....! , No election found.'})


def votes(request, voterid=0, nomid=0):
    nominee = Add_Nominee.objects.get(id=nomid)
    voter = Voter.objects.get(Voter_id=voterid)
    '''vote = Votes(Nominee_Id=nominee,Voter=voter,Date =datetime.datetime.now())
    vote.save()'''
    print(voter)
    Voter_Image = voter.Voter_Image
    Voter_id = voter.Voter_id
    Name = voter.Name
    Age = voter.Age
    Date_of_Birth = voter.Date_of_Birth
    Gender = voter.Gender
    Phone_Number = voter.Phone_Number
    Address = voter.Address
    Address_Proof = voter.Address_Proof
    Iris_Image = voter.Iris_Image
    Poling_Status = True
    # voter.delete()
    v12 = Votes(Nominee_Id=nominee, Voter=voter, Date=datetime.today().date())
    v12.save()
    v = Voter(Voter_Image=Voter_Image, Voter_id=Voter_id, Name=Name, Age=Age, Date_of_Birth=Date_of_Birth,
              Gender=Gender, Phone_Number=Phone_Number, Address=Address, Address_Proof=Address_Proof,
              Iris_Image=Iris_Image, Poling_Status=Poling_Status)
    v.save()
    return render(request, 'success.html', {'msg': 'Voted Successfully'})


def result(request):
    nominee = Votes.objects.values(
        'Nominee_Id'
    ).annotate(id_count=Count('Nominee_Id')).filter(id_count__gt=0).order_by('Nominee_Id')
    print(nominee)
    return render(request, 'result.html', {'nominee': nominee})

def election_result_calculation(request):
    vote = Votes.objects.all()
    nom = Add_Nominee.objects.all()
    for n in nom:
        count = 0
        for v in vote:
            print(v.Nominee_Id.Nominee_Id)
            print(v.Nominee_Id.Nominee_Name)
            if n.Nominee_Id == v.Nominee_Id.Nominee_Id:
                count += 1
        v = voting_count(Nominee_Id=n, count=count)
        v.save()
    return render(request, 'index.html', {'msg': 'The votes were counted'})


def election_result_view(request):
    electiontime = CreateElection.objects.all().last()
    resultdate = electiontime.Election_Result_Date.date()
    resulttime = electiontime.Election_Result_Date.time()
    if date.today() >= resultdate and datetime.now().time() >= resulttime:
        votes = voting_count.objects.all()
        for i in votes:
            print(i)
        return render(request, 'election_result_view.html',  {'votes': votes, 'electiontime':electiontime})
    else:
        return render(request, 'election_result_view.html', {'msg': ' not published..!'})

def detect_person(request):
    if request.method == 'POST':
        form = photo_forms(request.POST, request.FILES)
        print(os.getcwd() + 'media\media\Images')
        dir = 'C:/Users/user/PycharmProjects/ivote/voting_site/media/media/Images'
        for root, dirs, files in os.walk(dir):
            for file in files:
                path = os.path.join(dir, file)
                print(path)
                os.remove(path)
        if form.is_valid():
            form.save()
            new_model = tf.keras.models.load_model('data/iris_model2.h5')
            for root, dirs, files in os.walk(dir):
                for file in files:
                    path = os.path.join(dir, file)
                    print(path)
            print(path)
            img = cv2.imread(path)
            im1 = cv2.resize(img, (224, 224))
            out = np.expand_dims(im1, axis=0)
            final_img = out / 255.0

            pred = new_model.predict(final_img)

            max_index = np.argmax(pred[0])
            print(max_index)
            values = (1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 2, 20, 21, 22, 23, 24, 25, 26, 27, 28
                      , 29, 3, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 5, 6, 7, 8, 9)
            predicted = values[max_index]
            print(pred[0])
            print(predicted)
            form = photo_forms()
            pvar = prediction(predicted_label=predicted)
            pvar.save()
            return redirect('voter_profile')
    else:
        form = photo_forms()
    return render(request, 'iris_upload.html', {'form': form})

@login_required(login_url="/login")
def success(request):
    return render(request, 'success.html')

@login_required(login_url="/login")
def oops(request):
    return render(request, 'datetime.html')

def voter_list(request):
    electiontime = CreateElection.objects.all().last()
    voter_list = Voter.objects.order_by('Voter_id').values('Voter_id', 'Name')
    return render(request, 'voters_list.html', {
        'voter_list': voter_list,
        'electiontime': electiontime
    })

