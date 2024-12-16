from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from LITRevu.models import Ticket, Follow, CritiqueFeedback, Critique, TicketFeedback
from .forms import InscriptionForm, TicketForm, FollowUserForm, LoginForm, CritiqueForm, CritiqueFeedbackForm, \
    TicketFeedbackForm, FeedbackForm
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
    tickets = Ticket.objects.filter(hidden=False).prefetch_related('feedbacks')
    critiques = Critique.objects.filter(hidden=False).order_by('-created_at')
    critique_feedbacks = CritiqueFeedback.objects.all().order_by('-critique__created_at')

    return render(
        request,
        'LITRevu/flux.html',
        {'tickets': tickets,'critiques': critiques, 'critique_feedbacks': critique_feedbacks}
    )



# View to create a ticket
@login_required(login_url='/home/')
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)  # for file uploads
        if form.is_valid():
            # Set the user field to the logged-in user before saving
            ticket = form.save(commit=False)
            ticket.user = request.user  # Assign the logged-in user to the ticket
            ticket.save()
            messages.success(request, "Ticket créé avec succès!")
            return redirect('flux')
    else:
        form = TicketForm()

    return render(request, 'LITRevu/create_ticket.html', {'form': form})


# View to hide a ticket
@login_required
def hide_ticket(request, ticket_id):
    # Get the ticket object, only allowing the owner to hide their ticket
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    ticket.hidden = True  # Set the ticket to be hidden
    ticket.save()
    messages.success(request, "Ticket caché avec succès!")
    return redirect('flux')


############## CRITIQUE VIEW ################
@login_required(login_url='/home/')
def create_critique(request):
    if request.method == 'POST':
        critique_form = CritiqueForm(request.POST, request.FILES)
        feedback_form = CritiqueFeedbackForm(request.POST)

        print("Critique Form Valid: ", critique_form.is_valid())
        print("Feedback Form Valid: ", feedback_form.is_valid())

        if critique_form.is_valid() and feedback_form.is_valid():

            critique = critique_form.save(commit=False)
            critique.user = request.user
            critique.save()

            feedback = CritiqueFeedback(
                critique=critique,  # Link feedback to the critique
                rating=feedback_form.cleaned_data['rating'],
                comment=feedback_form.cleaned_data['comment'],
                user=request.user  # user who gave feedback
            )
            feedback.save()

            messages.success(request, "Critique et commentaire créés avec succès!")
            return redirect('flux')

        else:

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


@login_required(login_url='/home/')
def hide_critique(request, critique_id):
    if request.method == 'POST':
        critique = get_object_or_404(Critique, id=critique_id)

        if critique.user != request.user:
            return HttpResponseForbidden("You are not allowed to hide this critique.")

        critique.hidden = True
        critique.save()

        return HttpResponseRedirect(reverse('flux'))


############### LOGIN ###########################""
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

#################### FOLLOWERS #######################""""
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


################## TICKET FEDDBACK ###########

@login_required(login_url='/home/')
def ticket_feedback(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        feedback_form = TicketFeedbackForm(request.POST)

        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.user = request.user
            feedback.ticket = ticket  # Link feedback to the ticket
            feedback.save()

            messages.success(request, "Commentaire et note ajoutés avec succès!")
            return redirect('flux')  # Redirect to the flux page after submission
        else:
            messages.error(request, "Veuillez vérifier les erreurs du formulaire.")

    else:
        feedback_form = TicketFeedbackForm()

    return render(
        request,
        'LITRevu/ticket_feedback.html',
        {'ticket': ticket, 'feedback_form': feedback_form}
    )

############ MY POSTS  #########################


@login_required(login_url='/home/')
def my_posts(request):

    tickets = Ticket.objects.filter(user=request.user).order_by('-review_time')

    feedbacks = CritiqueFeedback.objects.filter(user=request.user).order_by('-created_at')

    return render(
        request,
        'LITRevu/my_posts.html',
        {'tickets': tickets, 'feedbacks': feedbacks}
    )



def update_feedback(request, feedback_id):

    try:
        feedback = TicketFeedback.objects.get(id=feedback_id)
    except TicketFeedback.DoesNotExist:
        return redirect('flux')

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect('flux')
    else:
        form = FeedbackForm(instance=feedback)

    return render(request, 'LITRevu/update_feedback.html', {'form': form, 'feedback': feedback})


