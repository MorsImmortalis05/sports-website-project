from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Exercise(models.Model):
    MUSCLE_GROUP_CHOICES = [
        ("chest", "Chest"),
        ("back", "Back"),
        ("shoulders", "Shoulders"),
        ("arms", "Arms"),
        ("core", "Core"),
        ("legs", "Legs"),
    ]

    image = models.ImageField()
    muscles_group = models.CharField(
        max_length=10,
        choices=MUSCLE_GROUP_CHOICES
    )
    description = models.TextField()


class Workout(models.Model):

    PROGRAM_TYPE_CHOICES = [
        ("Upper body", "Workout for upper body"),
        ("Legs day", "Workout for legs"),
        ("Core", "Workout for core muscles"),
        ("Yoga", "Yoga workout"),
        ("Pilates", "Pilates"),
        ("Stretching", "Stretching")
    ]


    name = models.CharField(max_length=255)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="my_workouts"
    )
    saved_by = models.ManyToManyField(
        User,
        related_name="saved_workouts"
        )
    exercises = models.ManyToManyField(
        Exercise,
        related_name="+"
    )
    type_of_program = models.CharField(
        max_length=25,
        choices=PROGRAM_TYPE_CHOICES
    )
    time = models.DurationField()


class Profile(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("N", "I don't want to share"),
    ]

    ACTIVITY_LEVEL_CHOICES = [
        ("sedentary", "Sedentary"),
        ("light", "Lightly active"),
        ("moderate", "Moderately active"),
        ("very", "Very active"),
        ("extra", "Extra active"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    weight = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True
    )
    weight_goal = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True
    )
    height = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    age = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    sex = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default="N"
    )
    activity_level = models.CharField(
        max_length=10,
        choices=ACTIVITY_LEVEL_CHOICES,
        default="sedentary"
    )
    saved_workouts = models.ManyToManyField(
        Workout,
        related_name="saved_by")

    def __str__(self):
        return f"{self.user.username}"
