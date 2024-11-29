from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from LITRevu.models import Ticket, Follow, CritiqueFeedback
from .forms import InscriptionForm, TicketForm, FollowUserForm, LoginForm, CritiqueForm, CritiqueFeedbackForm
from .models import Inscription
from django.utils.http import url_has_allowed_host_and_scheme



def home(request):
    return render(request, 'LITRevu/home.html')


def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscription réussie!")
            return redirect('home')
    else:
        form = InscriptionForm()

    return render(request, 'LITRevu/inscription.html', {'form': form})


def flux(request):
    tickets = Ticket.objects.all().order_by('-review_time')
    return render(request, 'LITRevu/flux.html', {'tickets': tickets})


@login_required(login_url='/home/')
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ticket créé avec succès!")
            return redirect('flux')
    else:
        form = TicketForm()

    return render(request, 'LITRevu/create_ticket.html', {'form': form})

@login_required(login_url='/home/')
def create_critique(request):
    if request.method == 'POST':
        critique_form = CritiqueForm(request.POST, request.FILES)
        feedback_form = CritiqueFeedbackForm(request.POST)

        # Log the form validation status
        print("Critique Form Valid: ", critique_form.is_valid())
        print("Feedback Form Valid: ", feedback_form.is_valid())

        if critique_form.is_valid() and feedback_form.is_valid():
            # Save the critique first
            critique = critique_form.save(commit=False)
            critique.user = request.user
            critique.save()

            # Create the feedback manually since it's a regular form, not a ModelForm
            feedback = CritiqueFeedback(
                critique=critique,  # Link feedback to the critique
                rating=feedback_form.cleaned_data['rating'],  # Get cleaned data from form
                comment=feedback_form.cleaned_data['comment'],  # Get cleaned data from form
                user=request.user  # Assign the user who gave feedback
            )
            feedback.save()

            messages.success(request, "Critique et commentaire créés avec succès!")
            return redirect('flux')

        else:
            # Log errors if forms are not valid
            print("Critique Form Errors: ", critique_form.errors)
            print("Feedback Form Errors: ", feedback_form.errors)

    else:
        critique_form = CritiqueForm()
        feedback_form = CritiqueFeedbackForm()

    return render(
        request,
        'LITRevu/create_critique.html',
        {'critique_form': critique_form, 'feedback_form': feedback_form}
    )





def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Vous êtes maintenant connecté !')

                return redirect('flux')
            else:
                messages.error(request, 'Identifiants invalides')
        else:
            messages.error(request, 'Le formulaire est invalide')
    else:
        form = LoginForm()

    return render(request, 'LITRevu/home.html', {'form': form})



def custom_logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/home/')
def manage_followers(request):
    if request.method == 'POST':
        form = FollowUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user_to_follow = User.objects.get(username=username)

            # Check if already following
            if Follow.objects.filter(follower=request.user, followed=user_to_follow).exists():
                messages.info(request, "Vous suivez déjà cet utilisateur.")
            else:
                Follow.objects.create(follower=request.user, followed=user_to_follow)
                messages.success(request, f"Vous suivez maintenant {username}!")
            return redirect('manage_followers')
    else:
        form = FollowUserForm()

    following = Follow.objects.filter(follower=request.user)
    followers = Follow.objects.filter(followed=request.user)

    users_to_follow = User.objects.exclude(id=request.user.id)
    print(users_to_follow)

    return render(request, 'LITRevu/manage_followers.html', {
        'form': form,
        'following': following,
        'followers': followers,
        'users_to_follow': users_to_follow,
    })


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)

    # Check if already following
    if Follow.objects.filter(follower=request.user, followed=user_to_follow).exists():
        messages.info(request, "Vous suivez déjà cet utilisateur.")
    else:
        Follow.objects.create(follower=request.user, followed=user_to_follow)
        messages.success(request, f"Vous suivez maintenant {user_to_follow.username}!")

    return redirect('manage_followers')


@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)

    # Remove the follow relationship
    Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()

    messages.success(request, f"Vous ne suivez plus {user_to_unfollow.username}.")

    return redirect('manage_followers')

def home_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Vous êtes maintenant connecté !')
                return redirect('home')
            else:
                messages.error(request, 'Identifiants invalides')
        else:
            messages.error(request, 'Le formulaire est invalide')
    else:
        form = LoginForm()

    return render(request, 'LITRevu/home.html', {'form': form})
