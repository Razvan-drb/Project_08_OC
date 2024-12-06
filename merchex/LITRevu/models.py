from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth.models import User

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, blank=True)
    book_title = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=255, blank=True)
    review_content = models.TextField(blank=True)
    review_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="", blank=True, null=True)   # save to MEDIA_ROOT
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book_title} - {self.author}"

class Inscription(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        # hash
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower} follows {self.followed}"

######### CRITIQUE PART #################

class Critique(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="")  # save to MEDIA_ROOT
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user who created it
    created_at = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class CritiqueFeedback(models.Model):
    critique = models.ForeignKey(Critique, on_delete=models.CASCADE, related_name='feedback')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(6)])
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user who gave feedback
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback on {self.critique.title} - Rating: {self.rating}/5"


class TicketFeedback(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="feedbacks")
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(6)])
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user who gave feedback
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.ticket.book_title} - Rating: {self.rating}/5"
