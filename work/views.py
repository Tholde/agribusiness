import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from users.models import User
from work.forms import EventForm
from work.models import Work, Event


# Create your views here.
def work(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(pk=id)
        works = Work.objects.filter(technicien=user).order_by('-date')
        context = {'admin': user, 'works': works}
        if user.role == 'admin':
            return render(request, 'admin/work-list.html', context, status=200)
        elif user.role == 'technicien':
            return render(request, 'technicien/rapport-travail-list.html', context, status=200)
        else:
            return redirect('dashboard')


def createWork(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        if request.session.get('user'):
            id = request.session.get('user')
            user = User.objects.get(id=id)
            if user.role == 'technicien':
                if request.method == "POST":
                    title = request.POST.get('title')
                    description = request.POST.get('description')
                    if len(request.FILES['file']) != 0:
                        file = request.FILES.get('file')
                        work = Work(title=title, description=description, technicien=user, file=file)
                        work.save()
                        return redirect('work')
                    else:
                        return redirect('dashboard')
            else:
                return redirect('dashboard')


def editWork(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        if request.session.get('user'):
            user_id = request.session.get('user')
            user = User.objects.get(pk=user_id)
            if user.role == 'technicien':
                work = Work.objects.get(pk=id)
                context = {'work': work}
                return render(request, 'technicien/rapport-travail-list.html', context, status=200)
            else:
                return redirect('dashboard')


def updateWork(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        if request.session.get('user'):
            user_id = request.session.get('user')
            user = User.objects.get(pk=user_id)
            if user.role == 'technicien':
                work = Work.objects.get(pk=id)
                if request.method == "POST":
                    title = request.POST.get('title')
                    description = request.POST.get('description')
                    if len(request.FILES['file']) != 0:
                        file = request.FILES.get('file')
                        work.title = title
                        work.description = description
                        work.file = file
                        work.save()
                        return redirect('work')
                    else:
                        work.title = title
                        work.description = description
                        work.save()
                        return redirect('work')
            else:
                return redirect('dashboard')


def deleteWork(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        if request.session.get('user'):
            user_id = request.session.get('user')
            user = User.objects.get(pk=user_id)
            if user.role == 'technicien':
                work = Work.objects.get(pk=id)
                work.delete()
                return redirect('work')
            else:
                return redirect('dashboard')


def calendar_view(request):
    events = Event.objects.all()
    return JsonResponse({"event": list(events.values())})


def save_data(request):
    if request.method == 'POST':
        key1 = request.POST.get('key1')
        key2 = request.POST.get('key2')
        key3 = request.POST.get('key3')
        key4 = request.POST.get('key4')
        my_model_instance = Event(title=key1, start=key2, end=key3,class_name=key4)
        my_model_instance.save()
        return redirect('calendar_admin')
        # return JsonResponse({'status': 'success'})
    return redirect('calendar_admin')
