from django.shortcuts import render, redirect

from association.models import MiniProject, Association, Temoignage, Formation, Member, Activity
from users.models import User


# Create your views here.
def read_four_projects(request):
    projects = MiniProject.objects.all().order_by('-id')[:4]
    project = MiniProject.objects.all().order_by('-id')[:1]
    context = {'projects': projects, 'project': project}
    return render(request, 'home/project.html', context, status=200)


def read_one_projects(request, id):
    if not request.session.get('user'):
        if id:
            projects = MiniProject.objects.all().order_by('-id')[:4]
            project = MiniProject.objects.get(id=id)
            context = {'project': project, 'projects': projects}
            return render(request, 'home/project.html', context, status=200)
        else:
            project = MiniProject.objects.all().order_by('-id')[:1]
            projects = MiniProject.objects.all().order_by('-id')[:4]
            context = {'project': project, 'projects': projects}
            return render(request, 'home/project.html', context, status=200)
    else:
        user_id = request.session.get('user')
        technicien = User.objects.get(id=user_id)
        project = MiniProject.objects.get(id=id)
        context = {'admin': technicien, 'project': project}
        return render(request, '', context, status=200)


def read_all_projects(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        technicien = User.objects.get(id=id)
        if technicien.role == 'admin':
            return redirect('dashboard')
        elif technicien.role == 'technicien':
            try:
                association = Association.objects.get(technicien=technicien)
                projects = MiniProject.objects.filter(association=association)
                context = {'admin': technicien, 'projects': projects}
                return render(request, 'technicien/project-list.html', context, status=200)
            except Association.DoesNotExist:
                return render(request, 'technicien/project-list.html')
        elif technicien.role == 'paysan':
            projects = MiniProject.objects.all()
            context = {'admin': technicien, 'projects': projects}
            return render(request, 'paysan/project-list.html', context, status=200)
        elif technicien.role == 'partenaire':
            projects = MiniProject.objects.all()
            context = {'admin': technicien, 'projects': projects}
            return render(request, 'partenaire/project-list.html', context, status=200)
        else:
            return redirect('list_product')


def read_four_temoignage(request):
    temoignages = Temoignage.objects.all().order_by('-id')[:4]
    temoignage = Temoignage.objects.all().order_by('-id')[:1]
    context = {'temoignage': temoignage, 'temoignages': temoignages}
    return render(request, 'home/temoignage.html', context, status=200)


def read_one_temoignage(request, id):
    if not request.session.get('user'):
        if id:
            temoignages = Temoignage.objects.all().order_by('-id')[:4]
            temoignage = Temoignage.objects.get(id=id)
            context = {'temoignage': temoignage, 'temoignages': temoignages}
            return render(request, 'home/temoignage.html', context, status=200)
        else:
            temoignage = Temoignage.objects.all().order_by('-id')[:1]
            temoignages = Temoignage.objects.all().order_by('-id')[:4]
            context = {'temoignage': temoignage, 'temoignages': temoignages}
            return render(request, 'home/temoignage.html', context, status=200)
    else:
        user_id = request.session.get('user')
        technicien = User.objects.get(id=user_id)
        temoignage = Temoignage.objects.get(id=id)
        context = {'admin': technicien, 'temoignage': temoignage}
        return render(request, '', context, status=200)


def accept_project(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id_user = request.session.get('user')
        technicien = User.objects.get(id=id_user)
        if technicien.role == 'technicien':
            project = MiniProject.objects.get(id=id)
            project.is_accepted = True
            project.save()
            return redirect('dashboard')
        return redirect('dashboard')


def read_all_temoignage(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        technicien = User.objects.get(id=id)
        if technicien.role == 'paysan':
            try:
                temoignage = Temoignage.objects.all()
                context = {'admin': technicien, 'temoignage': temoignage}
                return render(request, 'paysan/temoignage-list.html', context, status=200)
            except Association.DoesNotExist:
                return redirect('dashboard')
        else:
            return redirect('dashboard')


def list_of_associations(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        technicien = User.objects.get(id=id)
        if technicien.role == 'technicien':
            try:
                associations = Association.objects.filter(technicien=technicien).order_by('-id')
                context = {'admin': technicien, 'associations': associations}
                return render(request, 'technicien/association_manager.html', context, status=200)
            except Association.DoesNotExist:
                return render(request, 'technicien/association_manager.html')
        else:
            return redirect('dashboard')


def read_one_association(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        userid = request.session.get('user')
        technicien = User.objects.get(id=userid)
        if technicien.role == 'technicien':
            try:
                associations = Association.objects.filter(technicien=technicien).order_by('-id')
                one_association = Association.objects.get(id=id)
                member = Member.objects.filter(association=one_association)
                context = {'admin': technicien, 'associations': associations, 'one_association': one_association, 'member': member}
                return render(request, 'technicien/association_manager.html', context, status=200)
            except Association.DoesNotExist:
                return render(request, 'technicien/association_manager.html')


def create_associations(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        technicien = User.objects.get(id=id)
        if technicien.role == 'technicien':
            if request.method == "POST":
                nom = request.POST.get('nom')
                logo = request.FILES.get('logo')
                association = Association(name=nom, logo=logo, technicien=technicien)
                association.save()
                return redirect('association_manager')
        else:
            return redirect('dashboard')


def create_member_associations(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        technicien = User.objects.get(id=id)
        if technicien.role == 'paysan':
            if request.method == "POST":
                id_ass = request.POST.get('id_ass')
                role = request.POST.get('role')
                association = Association.objects.get(id=id_ass)
                member = Member(user=technicien, role=role, association=association)
                member.save()
                return redirect('readAllFormation')
            else:
                return redirect('dashboard')
        return redirect('dashboard')


def read_one_formation(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        user_id = request.session.get('user')
        technicien = User.objects.get(id=user_id)
        formation = Formation.objects.get(id=id)
        if technicien.role == 'technicien':
            context = {'admin': technicien, 'formation': formation}
            return render(request, 'technicien/edit_formation.html', context, status=200)
        else:
            return redirect('dashboard')


def read_all_formations(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        technicien = User.objects.get(id=id)
        if technicien.role == 'admin':
            return redirect('dashboard')
        elif technicien.role == 'technicien':
            try:
                # formation = Formation.objects.all()
                print(str(technicien))
                formation = Formation.objects.filter(technicien=technicien).order_by('-id')
                print(str(formation))
                context = {'admin': technicien, 'formation': formation}
                return render(request, 'technicien/formation-list.html', context, status=200)
            except Formation.DoesNotExist:
                return render(request, 'technicien/formation-list.html')
        else:
            try:
                formation = Formation.objects.all()
                context = {'admin': technicien, 'formation': formation}
                return render(request, 'paysan/formation-list.html', context, status=200)
            except Formation.DoesNotExist:
                return render(request, 'paysan/formation-list.html')


def read_all_activities(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        technicien = User.objects.get(id=id)
        if technicien.role == 'paysan':
            activities = Activity.objects.all().order_by('-id')
            context = {'admin': technicien, 'activities': activities}
            return render(request, 'paysan/activity-list.html', context, status=200)
        else:
            return redirect('dashboard')


def createFormation(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(id=id)
        if user.role == 'technicien':
            if request.method == "POST":
                title = request.POST.get('title')
                description = request.POST.get('description')
                if len(request.FILES) != 0:
                    image = request.FILES.get('image')
                    file = request.FILES.get('file')
                    formation = Formation(title=title, description=description, image=image, technicien=user, file=file)
                    formation.save()
                    return redirect('readAllFormation')
                else:
                    return redirect('dashboard')
        else:
            return redirect('dashboard')


def createProject(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(id=id)
        if user.role == 'paysan':
            member = Member.objects.get(user=user)
            if member:
                if member.role == 'admin':
                    if request.method == "POST":
                        name = request.POST.get('name')
                        description = request.POST.get('description')
                        budget = request.POST.get('budget')
                        if len(request.FILES) != 0:
                            file = request.FILES.get('file')
                            projet = MiniProject(name=name, description=description, budget=budget,
                                                 association=member.association, file=file)
                            projet.save()
                            return redirect('read_all_projects')
                        else:
                            return redirect('dashboard')
                    else:
                        return redirect('dashboard')
            else:
                return redirect('dashboard')
        else:
            return redirect('dashboard')


def create_activity(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(id=id)
        if user.role == 'paysan':
            member = Member.objects.get(user=user)
            if member:
                if member.role == 'admin':
                    if request.method == "POST":
                        name = request.POST.get('title')
                        description = request.POST.get('description')
                        budget = request.POST.get('budget')
                        if len(request.FILES) != 0:
                            image = request.FILES.get('image')
                            projet = Activity(title=name, description=description, budget=budget, image=image,
                                              association=member.association)
                            projet.save()
                            return redirect('read_all_projects')
                        else:
                            return redirect('dashboard')
                    else:
                        return redirect('dashboard')
            else:
                return redirect('dashboard')
        else:
            return redirect('dashboard')


def createTemoignage(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(id=id)
        if user.role == 'paysan':
            member = Member.objects.get(user=user)
            try:
                # if member:
                    if request.method == "POST":
                        title = request.POST.get('title')
                        description = request.POST.get('description')
                        if len(request.FILES) != 0:
                            image = request.FILES.get('image')
                            temoignage = Temoignage(title=title, description=description, image=image, member=member)
                            temoignage.save()
                            return redirect('read_temoignage')
                        else:
                            return redirect('dashboard')
                    else:
                        return redirect('dashboard')
            except member.DoesNotExist:
                return redirect('dashboard')
            # else:
            #     return redirect('dashboard')
        else:
            return redirect('dashboard')


def editFormation(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        formation = Formation.objects.get(pk=id)
        if request.method == "POST":
            title = request.POST.get('title')
            description = request.POST.get('description')
            if len(request.FILES) != 0:
                image = request.FILES.get('image')
                file = request.FILES.get('file')
                formation.title = title
                formation.description = description
                formation.image = image
                formation.file = file
                formation.save()
                return redirect('readAllFormation')
            else:
                formation.title = title
                formation.description = description
                formation.save()
                return redirect('readAllFormation')


def deleteFormation(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        product = Formation.objects.get(pk=id)
        product.delete()
        return redirect('readAllFormation')


def delete_activity(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id_user = request.session.get('user')
        user = User.objects.get(id=id_user)
        member = Member.objects.get(user=user)
        if member:
            if member.role == 'admin':
                activity = Activity.objects.get(pk=id)
                activity.delete()
                return redirect('read_all_activities')
            return redirect('dashboard')
        return redirect('dashboard')


def delete_temoignage(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id_user = request.session.get('user')
        user = User.objects.get(id=id_user)
        member = Member.objects.get(user=user)
        if member:
            temoignage = Temoignage.objects.get(member=member)
            if temoignage:
                tem = Temoignage.objects.get(pk=id)
                tem.delete()
                return redirect('read_temoignage')
            return redirect('dashboard')
        return redirect('dashboard')
