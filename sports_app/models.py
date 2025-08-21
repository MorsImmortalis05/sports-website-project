from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


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

    def __str__(self):
        return f"{self.user.username}"


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
        Profile,
        on_delete=models.CASCADE,
        related_name="my_workouts"
    )
    saved_by = models.ManyToManyField(
        Profile,
        related_name="saved_workouts"
        )
    exercises = models.ManyToManyField(
        Exercise,
        related_name="exercises"
    )
    type_of_program = models.CharField(
        max_length=25,
        choices=PROGRAM_TYPE_CHOICES
    )
    time = models.DurationField()


class WorkoutRoutine(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="routines"
    )
    workout = models.OneToOneField(
        Workout,
        on_delete=models.SET_NULL,
        related_name="routine_workout",
        null=True
    )
    time = models.DurationField(null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
