from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import User


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

    first_name = models.CharField(max_length=100, default="lilichka")

    last_name = models.CharField(max_length=100, default="cool")

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
        ("arms", "Arms"),
        ("core", "Core"),
        ("legs", "Legs"),
        ("cardio", "Cardio")
    ]

    name = models.CharField(max_length=100, default="Exercise")
    image = CloudinaryField('image', blank=True, null=True)
    muscles_group = models.CharField(
        max_length=10,
        choices=MUSCLE_GROUP_CHOICES
    )
    description = models.TextField()

    def get_image(self):
        defaults = {
            "chest": "https://res.cloudinary.com/duwxznzwk/image/upload/v1756033108/pexels-olly-3837788_ipnvjr.jpg",
            "back": "https://res.cloudinary.com/duwxznzwk/image/upload/v1756032753/pexels-scottwebb-28061_ws1x5y.jpg",
            "arms": "https://res.cloudinary.com/duwxznzwk/image/upload/v1756032753/pexels-olly-3757376_laqqii.jpg",
            "core": "https://res.cloudinary.com/duwxznzwk/image/upload/v1756032754/pexels-roman-odintsov-8038625_fyl72q.jpg",
            "legs": "https://res.cloudinary.com/duwxznzwk/image/upload/v1756032755/pexels-victorfreitas-949129_ircj8c.jpg",
            "cardio": "https://res.cloudinary.com/duwxznzwk/image/upload/v1756032754/pexels-willpicturethis-1954524_g3brqm.jpg"
        }
        if self.image:
            return self.image.url
        return defaults.get(self.muscles_group, "https://res.cloudinary.com/duwxznzwk/image/upload/v1756032754/pexels-roman-odintsov-8038625_fyl72q.jpg")

    def __str__(self):
        return self.name


class Workout(models.Model):

    PROGRAM_TYPE_CHOICES = [
        ("Upper body", "Workout for upper body"),
        ("Legs day", "Workout for legs"),
        ("Core", "Workout for core muscles"),
        ("Yoga", "Yoga workout"),
        ("Pilates", "Pilates"),
        ("Stretching", "Stretching"),
        ("Cardio", "Cardio workout")
    ]


    name = models.CharField(max_length=255)
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="my_workouts"
    )
    description = models.TextField(default="author did not provide any "
                                           "description but maybe this "
                                           "workout name says everything...")
    saved_by = models.ManyToManyField(
        Profile,
        related_name="saved_workouts"
        ),
    type_of_program = models.CharField(
        max_length=25,
        choices=PROGRAM_TYPE_CHOICES
    )
    time = models.DurationField(null=True, blank=True)
    image = CloudinaryField(
        'image', blank=True, null=True
    )

    def __str__(self):
        return self.name

    def get_image(self):
        defaults = {
            "Upper body": "https://res.cloudinary.com/duwxznzwk/image/upload/v1756032753/pexels-scottwebb-28061_ws1x5y.jpg",
            "Legs day": "https://res.cloudinary.com/duwxznzwk/image/upload/v1756032755/pexels-victorfreitas-949129_ircj8c.jpg",
            "Core": "https://res.cloudinary.com/duwxznzwk/image/upload/v1756032754/pexels-roman-odintsov-8038625_fyl72q.jpg",
            "Yoga": "https://res.cloudinary.com/duwxznzwk/image/upload/v1756032753/pexels-cottonbro-4327033_yslk5h.jpg",
            "Pilates": "https://res.cloudinary.com/duwxznzwk/image/upload/v1756123124/pexels-olly-868483_mhx371.jpg",
            "Stretching": "https://res.cloudinary.com/duwxznzwk/image/upload/v1756032753/pexels-olly-868757_qqsds3.jpg",
            "Cardio": "https://res.cloudinary.com/duwxznzwk/image/upload/v1756032754/pexels-willpicturethis-1954524_g3brqm.jpg",
        }
        if self.image:
            return self.image.url
        return defaults.get(self.type_of_program, "https://res.cloudinary.com/duwxznzwk/image/upload/v1756032754/pexels-roman-odintsov-8038625_fyl72q.jpg")


class WorkoutRoutine(models.Model):
    profile = models.ManyToManyField(
        Profile,
        related_name="routines"
    )
    workout = models.ForeignKey(
        Workout,
        on_delete=models.SET_NULL,
        related_name="routine_workout",
        null=True
    )
    time = models.DurationField(null=True, blank=True)
    date = models.DateTimeField()
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.workout.name

class WorkoutExercise(models.Model):
    sets = models.IntegerField(default=3)
    reps = models.IntegerField(default=8)
    rest = models.DurationField(null=True, blank=True)
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        null=True,
        related_name="workout_exercises"
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return f"{self.workout.name}: {self.exercise.name}"

class WorkoutPlan(models.Model):
    name = models.CharField(max_length=100)
    profile = models.ForeignKey(
        Profile,
        related_name="workout_plans",
        on_delete=models.CASCADE
    )
    current = models.BooleanField(default=False)
    days_per_week = models.PositiveIntegerField(default=3)

    def save(
        self,
        force_insert = False,
        force_update = False,
        using = None,
        update_fields = None,
    ):
        if self.current:
            WorkoutPlan.objects.filter(
                profile=self.profile,
                current=True,
            ).exclude(id=self.id).update(current=False)
        if self.days_per_week > 7:
            self.days_per_week = 7
        super().save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
        )

    def __str__(self):
        workouts = [s.workout.name for s in self.schedules.all()]
        return f"Plan for {self.profile.user.username}: {', '.join(workouts)}"


class WorkoutSchedule(models.Model):
    WEEKDAYS_CHOICES = [
        ("1", "Monday"),
        ("2", "Tuesday"),
        ("3", "Wednesday"),
        ("4", "Thursday"),
        ("5", "Friday"),
        ("6", "Saturday"),
        ("7", "Sunday")
    ]
    workout_plan = models.ForeignKey(
        WorkoutPlan,
        on_delete=models.CASCADE,
        related_name="schedules"
    )
    workout = models.ForeignKey(
        Workout,
        related_name="schedules",
        on_delete=models.CASCADE
    )
    weekday = models.CharField(
        choices=WEEKDAYS_CHOICES,
        max_length=10
    )
