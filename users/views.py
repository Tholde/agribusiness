from datetime import datetime, timezone

from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from association.models import Formation, Member, Association
from chat.models import Room, Message
from users.models import User, OneTimePassword
from users.utils import send_code_to_user_email, resend_code_to_user_email, send_notification_of_creation_to_user_email
from visitor.models import Visitor, UserProblem
from work.models import Event


# Create your views here.
def index(request):
    if request.session.get('user'):
        return redirect('dashboard')
    visitors = Visitor.objects.all()
    context = {'visitors': visitors}
    return render(request, 'home/index.html', context)


def contact_us(request):
    if request.session.get('user'):
        return redirect('dashboard')
    return render(request, 'home/contact.html')


def save_contact_us(request):
    if request.method == "POST":
        fullname = request.POST['fullname']
        email = request.POST['email']
        message = request.POST['message']
        if fullname or email or message:
            visitor = Visitor(fullname=fullname, email=email, message=message)
            visitor.save()
            return redirect('index')
        return redirect('contact_us')


def delete_contact_us(request, id):
    if request.session.get('user'):
        return redirect('login')
    else:
        visitor = Visitor.objects.get(pk=id)
        visitor.delete()
        return redirect('contact_list')


def send_answer_contact_us(request, id):
    if request.session.get('user'):
        return redirect('login')
    else:
        visitor = Visitor.objects.get(pk=id)
        send_answer_contact_us(visitor.fullname, visitor.email)
        return redirect('contact_list')


def about_show(request):
    if request.session.get('user'):
        return redirect('dashboard')
    else:
        visitor = Visitor.objects.all()
        technicien = User.objects.filter(role='technicien')
        partenaire = User.objects.filter(role='partenaire')
        user = User.objects.all()
        context = {'visitor': visitor, 'technicien': technicien, 'user': user, 'partenaire': partenaire}
        return render(request, 'home/about.html', context, status=200)


def formation_show(request):
    if request.session.get('user'):
        return redirect('dashboard')
    else:
        formation = Formation.objects.all().order_by('-id')[:4]
        frm = Formation.objects.all().order_by('-date')[:1]
        context = {'formation': formation, 'frm': frm}
        return render(request, 'home/formation.html', context, status=200)


def show_shop(request):
    if request.session.get('user'):
        return redirect('dashboard')
    else:
        return render(request, 'home/shop.html')


# ******************************** authentication activity ********************************
def registration(request):
    if request.session.get('user'):
        return redirect('dashboard')
    return render(request, 'auth/auth-register.html')


def login_panel(request):
    if request.session.get('user'):
        return redirect('dashboard')
    return render(request, 'auth/auth-login.html')


def confirmation_panel(request):
    if request.session.get('user'):
        return redirect('dashboard')
    return render(request, 'auth/auth-two-step-verification.html')


def mail_confirmation(request):
    if request.session.get('user'):
        return redirect('dashboard')
    return render(request, 'auth/auth-confirm-mail.html')


def reset_password(request):
    if request.session.get('user'):
        return redirect('dashboard')
    return render(request, 'auth/auth-recoverpw.html')


def mail_found(request):
    if request.session.get('user'):
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.get(email=email)
        context = {'user': user}
        return render(request, 'auth/auth-two-step-verification-reset-pass.html', context)
    else:
        return redirect('login')


def verify_email(request):
    if request.session.get('user'):
        return redirect('dashboard')
    if request.method == 'POST':
        code = request.POST['code']
        print('your code is: ' + code)
        try:
            user_code = OneTimePassword.objects.get(code=code)
            user = user_code.user
            context = {'user': user}
            return render(request, 'auth/auth-lock-screen.html', context, status=200)
        except OneTimePassword.DoesNotExist:
            messages = 'Sorry, you have not entered the code.'
            return render(request, 'auth/auth-two-step-verification.html', {'messages': messages}, status=500)


def update_password(request, id):
    if request.session.get('user'):
        return redirect('dashboard')
    if request.method == 'POST':
        user = User.objects.get(pk=id)
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if len(password) > 7:
            if password == confirm_password:
                user.password = password
                user.save()
                return redirect('login')
            else:
                messages = 'Mot de passe pas confirmer.'
                context = {'user': user, 'messages': messages}
                return render(request, 'auth/auth-lock-screen.html', context)
        else:
            messages = 'Mot de passe est trop court, essayer plus de 7 caracteres.'
            context = {'user': user, 'messages': messages}
            return render(request, 'auth/auth-lock-screen.html', context)


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        username = '@' + firstname.lower()
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role']
        if len(password) > 7:
            if password == confirm_password:
                if len(request.FILES) != 0:
                    pwd = make_password(password)
                    image = request.FILES['image']
                    cv = request.FILES['cv']
                    user = User(email=email, first_name=firstname, last_name=lastname, username=username, password=pwd,
                                role=role, image=image, cv=cv)
                    user.save()
                    send_code_to_user_email(email)
                    messages = 'Your account has been created.'
                    context = {'user': user, 'messages': messages}
                    return render(request, 'auth/auth-two-step-verification.html', context, status=200)
                else:
                    messages = 'Sorry, you have not entered the image.'
                    return render(request, 'auth/auth-register.html', {'messages': messages}, status=404)
            else:
                messages = 'Sorry, verify your password and confirm it again.'
                return render(request, 'auth/auth-register.html', {'messages': messages}, status=500)

        else:
            messages = 'Sorry, your password is very short. Try again and do it 8 character long.'
            return render(request, 'auth/auth-register.html', {'messages': messages}, status=400)


def resend_confirmation(request, email):
    if request.session.get('user'):
        return redirect('dashboard')
    user = User.objects.get(email=email)
    code = OneTimePassword.objects.get(user=user).code
    print('your code is: ' + code)
    resend_code_to_user_email(code, email)
    messages = 'Votre code a été envoyer avec succès.'
    return render(request, 'auth/auth-two-step-verification.html', {'messages': messages}, status=200)


def verification_email(request):
    if request.session.get('user'):
        return redirect('dashboard')
    if request.method == 'POST':
        code = request.POST['code']
        print('your code is: ' + code)
        try:
            user_code = OneTimePassword.objects.get(code=code)
            user = user_code.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                messages = 'Votre compte a été activer. Veillez retourner à la page de connexion, s\'il vous plaît.'
                return render(request, 'auth/auth-confirm-mail.html', {'messages': messages}, status=200)
            else:
                messages = 'Sorry, you have already verified your account.'
                return render(request, 'auth/auth-two-step-verification.html', {'messages': messages}, status=404)
        except OneTimePassword.DoesNotExist:
            messages = 'Sorry, you have not entered the code.'
            return render(request, 'auth/auth-two-step-verification.html', {'messages': messages}, status=500)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email).first()
        # user = authenticate(request, email=email, password=password)
        if user:
            pwd = check_password(password, user.password)
            if pwd:
                request.session['user'] = user.id
                print('user is authenticated : ' + str(user.first_name))
                # return render(request, 'auth/auth-login.html', context, status=200)
                return redirect('dashboard')
            else:
                messages = 'Password is incorrect.'
                context = {'messages': messages}
                return render(request, 'auth/auth-login.html', context, status=404)

        else:
            messages = 'E-mail is incorrect.'
            context = {'messages': messages}
            return render(request, 'auth/auth-login.html', context, status=404)


def user_counts_by_month(request):
    user_counts = User.objects.annotate(month=TruncMonth('date_joined')).values('month').annotate(
        count=Count('id')).order_by('month')
    visitor_counts = Visitor.objects.annotate(month=TruncMonth('date')).values('month').annotate(
        count=Count('id')).order_by('month')
    monthly_user_counts = [0] * 12
    monthly_visitor_counts = [0] * 12
    for entry in user_counts:
        month = entry['month'].month
        count = entry['count']
        monthly_user_counts[month - 1] = count

    for entry in visitor_counts:
        month = entry['month'].month
        count = entry['count']
        monthly_user_counts[month - 1] = count

    return JsonResponse({'monthly_user_counts': monthly_user_counts, 'monthly_visitor_counts': monthly_visitor_counts})


def dashboard_redirect(request):
    if not request.session.get('user'):
        # return render(request, 'auth/auth-login.html')
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(id=id)
        users = User.objects.all().order_by('-id')
        techniciens = User.objects.filter(role='technicien').order_by('-id')
        paysans = User.objects.filter(role='paysan').order_by('-id')
        visitor = Visitor.objects.all().order_by('-id')
        problems = UserProblem.objects.filter(status=False).order_by('-id')
        if user.role == 'admin':
            context = {'admin': user, 'users': users, 'techniciens': techniciens, 'visitor': visitor,
                       'problem': problems}
            print("Hello Admin")
            return render(request, 'admin/dashboard-blog.html', context, status=201)
        elif user.role == 'technicien':
            context = {'admin': user, 'users': users, 'paysans': paysans}
            print("Hello Technician")
            return render(request, 'technicien/dashboard-blog.html', context, status=201)
        elif user.role == 'paysan':
            print("Hello Paysan")
            try:
                membre = Member.objects.get(user=user)
                if membre:
                    return redirect('read_all_projects')
                else:
                    association = Association.objects.all().order_by('-id')
                    context = {'association': association}
                    return render(request, 'paysan/member-confirm.html', context, status=201)
            except:
                association = Association.objects.all().order_by('-id')
                context = {'association': association}
                return render(request, 'paysan/member-confirm.html', context, status=201)
        elif user.role == 'partenaire':
            print("Hello Partenaire")
            return redirect('read_all_projects')
        else:
            print("Hello Fournisseur")
            return redirect('list_product')


def logout(request):
    request.session.pop('user', None)
    request.session.modified = True
    return redirect('login')


# ********************************** administration activity  *************************************
def admin_profile(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(id=id)
        context = {'admin': user}
        if user.role == 'admin':
            return render(request, 'admin/profile.html', context, status=200)
        elif user.role == 'technicien':
            return render(request, 'technicien/profile.html', context, status=200)
        elif user.role == 'paysan':
            return render(request, 'paysan/profile.html', context, status=200)
        elif user.role == 'partenaire':
            return render(request, 'partenaire/profile.html',context, status=404)
        else:
            return render(request, 'fournisseur/profile.html', context, status=404)


def admin_update_profile(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(id=id)
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            contact = request.POST['contact']
            address = request.POST['address']
            if len(request.FILES) != 0:
                cv = request.FILES['cv']
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.contact = contact
                user.address = address
                user.cv = cv
                user.save()
                return redirect('dashboard')
            else:
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.contact = contact
                user.address = address
                user.save()
                return redirect('dashboard')


def update_image(request):
    if not request.session.get('user'):
        return redirect('login')
    if request.method == "POST":
        id = request.session.get('user')
        user = User.objects.get(id=id)
        if len(request.FILES) != 0:
            image = request.FILES['image']
            user.image = image
            user.save()
            return redirect('dashboard')
        else:
            messages = 'Something went wrong.'
            context = {'admin': user, 'messages': messages}
            if user.role == 'admin':
                return render(request, 'admin/profile.html', context, status=200)
            if user.role == 'technicien':
                return render(request, 'technicien/profile.html', context, status=200)
            else:
                return redirect('dashboard')


def calendar_admin(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(id=id)
        event = Event.objects.all()
        context = {'admin': user, 'event': event}
        if user.role == 'admin':
            return render(request, 'admin/calendar-full.html', context, status=200)
        if user.role == 'technicien':
            return render(request, 'technicien/calendar-full.html', context, status=200)
        else:
            return redirect('dashboard')


def problem(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.get(id=id)
        problems = UserProblem.objects.filter(status=False).order_by('-id')
        context = {'admin': user, 'problems': problems}
        if user.role == 'admin':
            return render(request, 'admin/problem-list.html', context, status=200)
        else:
            return redirect('dashboard')


# ********************** chat activity *****************************
def admin_message(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        admin = User.objects.get(id=id)
        room_all = Room.objects.all().order_by('-id')
        context = {'admin': admin, 'room_all': room_all}
        if admin.role == 'admin':
            return render(request, 'admin/chat.html', context, status=200)
        if admin.role == 'technicien':
            return render(request, 'technicien/chat.html', context, status=200)
        else:
            return redirect('dashboard')


def room(request, room):
    if not request.session.get('user'):
        return redirect('login')
    else:
        if room:
            id = request.session.get('user')
            admin = User.objects.get(id=id)
            try:
                username = request.GET.get('username')
                room_name = request.GET.get('room')
                room_details = Room.objects.get(name=room)
                room_all = Room.objects.all().order_by('-id')
                if room_name:
                    if admin.role == 'admin':
                        try:
                            return render(request, 'admin/chat.html', {
                                'username': username,
                                'room': room,
                                'room_details': room_details,
                                'admin': admin,
                                'room_all': room_all
                            })
                        except Room.DoesNotExist:
                            return redirect('admin_message')
                    else:
                        try:
                            return render(request, 'technicien/chat.html', {
                                'username': username,
                                'room': room,
                                'room_details': room_details,
                                'admin': admin,
                                'room_all': room_all
                            })
                        except Room.DoesNotExist:
                            return redirect('admin_message')
                else:
                    if admin.role == 'admin':
                        return render(request, 'admin/chat.html', {
                            'username': username,
                            'room': room,
                            'room_details': room_details,
                            'admin': admin,
                            'room_all': room_all
                        })
                    else:
                        return render(request, 'technicien/chat.html', {
                            'username': username,
                            'room': room,
                            'room_details': room_details,
                            'admin': admin,
                            'room_all': room_all
                        })
            except Room.DoesNotExist:
                search_query = request.GET.get('search', '')
                user = User.objects.filter(role='technicien').order_by('-id')
                member = User.objects.exclude(role__in=['admin', 'technicien'])
                # member = User.objects.all().order_by('-id')
                if admin.role == 'admin':
                    if search_query:
                        user = user.filter(first_name__icontains=str(search_query).lower()) | user.filter(
                            last_name__icontains=str(search_query).lower()) | user.filter(
                            address__icontains=str(search_query).lower()) | user.filter(
                            email__icontains=str(search_query).lower()) | user.filter(
                            contact__icontains=str(search_query).lower())
                        context = {'admin': admin, 'users': user}
                        return render(request, 'admin/technicien-list.html', context)
                elif admin.role == 'technicien':
                    if search_query:
                        user = member.filter(first_name__icontains=str(search_query).lower()) | member.filter(
                            last_name__icontains=str(search_query).lower()) | member.filter(
                            address__icontains=str(search_query).lower()) | member.filter(
                            email__icontains=str(search_query).lower()) | member.filter(
                            contact__icontains=str(search_query).lower())
                        context = {'admin': admin, 'users': user}
                        return render(request, 'technicien/users-list.html', context)
                else:
                    return redirect('dashboard')


def checkview(request, id):
    try:
        if id != 0:
            room = Room.objects.get(pk=id).name
            user_id = request.session.get('user')
            user = User.objects.get(id=user_id)
            username = user.username
            if Room.objects.filter(name=room).exists():
                return redirect('/' + room + '/?username=' + username)
            else:
                new_room = Room.objects.create(name=room)
                new_room.save()
                return redirect('/' + room + '/?username=' + username)
        else:
            room = request.POST['room_name']
            user_id = request.session.get('user')
            user = User.objects.get(id=user_id)
            username = user.username
            if Room.objects.filter(name=room).exists():
                return redirect('/' + room + '/?username=' + username)
            else:
                new_room = Room.objects.create(name=room)
                new_room.save()
                return redirect('/' + room + '/?username=' + username)
    except Room.DoesNotExist:
        return redirect('admin_message')


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message envoyé avec succès')


def getMessages(request, room):
    user_id = request.session.get('user')
    user = User.objects.get(id=user_id)
    username = user.username
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id).order_by('date')
    return JsonResponse({"messages": list(messages.values()), "username": username})


def contacts_list(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        id = request.session.get('user')
        user = User.objects.filter(id=id).first()
        visitor = Visitor.objects.all().order_by('-id')
        context = {'admin': user, 'visitor': visitor}
        if user.role == 'admin':
            return render(request, 'admin/contacts-list.html', context, status=200)
        else:
            return redirect('dashboard')


def technicien_list(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        try:
            id = request.session.get('user')
            admin = User.objects.get(id=id)
            user = User.objects.filter(role='technicien').order_by('-id')
            search_query = request.GET.get('search', '')
            if search_query:
                user = user.filter(first_name__icontains=str(search_query).lower()) | user.filter(
                    last_name__icontains=str(search_query).lower()) | user.filter(
                    address__icontains=str(search_query).lower()) | user.filter(
                    email__icontains=str(search_query).lower()) | user.filter(
                    contact__icontains=str(search_query).lower())
                context = {'admin': admin, 'users': user}
                if user.role == 'admin':
                    return render(request, 'admin/technicien-list.html', context, status=200)
                else:
                    return redirect('dashboard')
            context = {'admin': admin, 'users': user}
            if admin.role == 'admin':
                return render(request, 'admin/technicien-list.html', context, status=200)
            elif admin.role == 'technicien':
                return render(request, 'technicien/users-list.html', context, status=200)
            else:
                return redirect('dashboard')
        except User.DoesNotExist:
            return render(request, 'admin/technicien-list.html')


# ********************* CRUD Technicien ***************************
def addTechnicien(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        try:
            if request.method == "POST":
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                username = '@' + first_name.lower()
                email = request.POST['email']
                contact = request.POST['contact']
                address = request.POST['address']
                password = request.POST['password']
                confirm_password = request.POST['confirm_password']
                role = 'technicien'
                id = request.session.get('user')
                admin = User.objects.get(id=id)
                user = User.objects.filter(role='technicien').order_by('-id')
                if len(password) > 7:
                    if password == confirm_password:
                        if len(request.FILES) != 0:
                            pwd = make_password(password)
                            image = request.FILES['image']
                            cv = request.FILES['cv']
                            fullname = first_name + ' ' + last_name
                            user = User(email=email, first_name=first_name, last_name=last_name,
                                        username=username, image=image, cv=cv, contact=contact, address=address,
                                        password=pwd, role=role)
                            user.save()
                            send_notification_of_creation_to_user_email(fullname, email)
                            print('user created' + str(user))
                            return redirect('list_of_technicien')
                        else:
                            messages = 'Sorry, you have not entered the image.'
                            context = {'admin': admin, 'users': user, 'messages': messages}
                            return render(request, 'admin/technicien-list.html', context, status=500)
                    else:
                        messages = 'Sorry, verify password and confirm it again.'
                        context = {'admin': admin, 'users': user, 'messages': messages}
                        return render(request, 'admin/technicien-list.html', context, status=500)

                else:
                    messages = 'Sorry, password is very short. Try again and do it 8 character long.'
                    context = {'admin': admin, 'users': user, 'messages': messages}
                    return render(request, 'admin/technicien-list.html', context, status=400)
        except User.DoesNotExist:
            return render(request, 'admin/technicien-list.html')


def technicien_show(request, id):
    if not request.session.get('user'):
        return redirect('login')
    try:
        admin_id = request.session.get('user')
        user = User.objects.get(id=admin_id)
        if id:
            if user.role == 'admin':
                users = User.objects.get(id=id)
                context = {'admin': user, 'user': users}
                return render(request, 'admin/edit_user.html', context, status=200)
            elif user.role == 'technicien':
                users = User.objects.get(id=id)
                context = {'admin': user, 'user': users}
                return render(request, 'technicien/edit_user.html', context, status=200)
            else:
                return redirect('dashboard')
        else:
            if user.role == 'admin':
                return redirect('list')
            elif user.role == 'technicien':
                return redirect('list_user')
            else:
                return redirect('dashboard')
    except User.DoesNotExist:
        return render(request, 'admin/technicien-list.html')


def update_technicien(request, id):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        contact = request.POST['contact']
        address = request.POST['address']
        email = request.POST['email']
        admin_id = request.session.get('user')
        admin = User.objects.get(id=admin_id)
        user = User.objects.get(id=id)
        if user:
            if first_name and last_name and contact and address and email:
                user.first_name = first_name
                user.last_name = last_name
                user.contact = contact
                user.address = address
                user.email = email
                user.save()
                if admin.role == 'admin':
                    return redirect('list_of_technicien')
                elif user.role == 'technicien':
                    return redirect('list_user')
                else:
                    return redirect('dashboard')
            else:
                messages = 'Something went wrong. Please try again.'
                context = {'admin': admin, 'user': user, 'messages': messages}
                return render(request, 'admin/edit_user.html', context, status=500)
        else:
            messages = 'Something went wrong. Please try again.'
            context = {'admin': admin, 'user': user, 'messages': messages}
            return render(request, 'admin/edit_user.html', context, status=500)


def delete_technicien(request, id):
    if not request.session.get('user'):
        return redirect('login')
    else:
        user = User.objects.get(id=id)
        user.delete()
        user_id = request.session.get('user')
        admin = User.objects.get(id=user_id)
        if admin.role == 'admin':
            return redirect('list_of_technicien')
        elif admin.role == 'technicien':
            return redirect('list_user')
        else:
            return redirect('dashboard')


# ********************* Technician Activity ******************************
# ********* CRUD Member ***********
def addMember(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        if request.method == "POST":
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            username = '@' + firstname.lower()
            email = request.POST['email']
            contact = request.POST['contact']
            address = request.POST['address']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            role = request.POST['role']
            id = request.session.get('user')
            admin = User.objects.get(id=id)
            user = User.objects.exclude(role__in=['admin', 'technicien']).order_by('-id')
            if len(password) > 7:
                if password == confirm_password:
                    if len(request.FILES) != 0:
                        pwd = make_password(password)
                        image = request.FILES['image']
                        cv = request.FILES['cv']
                        fullname = firstname + ' ' + lastname
                        user = User(email=email, first_name=firstname, last_name=lastname,
                                    username=username, image=image, cv=cv, contact=contact, address=address,
                                    password=pwd, role=role)
                        user.save()
                        send_notification_of_creation_to_user_email(fullname, email)
                        print('user created' + str(user))
                        return redirect('list_user')
                    else:
                        messages = 'Sorry, you have not entered the image.'
                        context = {'admin': admin, 'users': user, 'messages': messages}
                        return render(request, 'admin/technicien-list.html', context, status=500)
                else:
                    messages = 'Sorry, verify password and confirm it again.'
                    context = {'admin': admin, 'users': user, 'messages': messages}
                    return render(request, 'admin/technicien-list.html', context, status=500)

            else:
                messages = 'Sorry, password is very short. Try again and do it 8 character long.'
                context = {'admin': admin, 'users': user, 'messages': messages}
                return render(request, 'admin/technicien-list.html', context, status=400)


def users_list(request):
    if not request.session.get('user'):
        return redirect('login')
    else:
        try:
            id = request.session.get('user')
            admin = User.objects.get(id=id)
            # user = User.objects.exclude(role__in=['admin', 'technicien']).order_by('-id')
            user = User.objects.filter(role__in=['paysan','fournisseur', 'partenaire']).order_by('-id')
            search_query = request.GET.get('search', '')
            if search_query:
                user = user.filter(first_name__icontains=str(search_query).lower()) | user.filter(
                    last_name__icontains=str(search_query).lower()) | user.filter(
                    address__icontains=str(search_query).lower()) | user.filter(
                    email__icontains=str(search_query).lower()) | user.filter(
                    contact__icontains=str(search_query).lower())
                context = {'admin': admin, 'users': user}
                if admin.role == 'technicien':
                    return render(request, 'technicien/users-list.html', context, status=200)
                else:
                    return redirect('dashboard')
            context = {'admin': admin, 'users': user}
            if admin.role == 'technicien':
                return render(request, 'technicien/users-list.html', context, status=200)
            else:
                return redirect('dashboard')
        except User.DoesNotExist:
            return render(request, 'technicien/users-list.html')
