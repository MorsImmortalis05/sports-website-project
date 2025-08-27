from django import forms
from django.contrib.auth.forms import UserCreationForm

from sports_app.models import User, Profile, Exercise, Workout, WorkoutRoutine, \
    WorkoutExercise, WorkoutPlan, WorkoutSchedule

from django.forms import inlineformset_factory


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = "__all__"


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = "__all__"


class WorkoutRoutineForm(forms.ModelForm):
    class Meta:
        model = WorkoutRoutine
        fields = "__all__"

class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = "__all__"

WorkoutExerciseFormSet = inlineformset_factory(
    model=WorkoutExercise,
    parent_model=Workout,
    form=WorkoutExerciseForm,
    extra=1,
    max_num=10,
    can_delete=True,
)


class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = "__all__"


class WorkoutScheduleForm(forms.ModelForm):
    class Meta:
        model = WorkoutSchedule
        fields = "__all__"

WorkoutPlanScheduleFormset = inlineformset_factory(
    model=WorkoutSchedule,
    parent_model=WorkoutPlan,
    form=WorkoutScheduleForm,
    max_num=7,
    extra=0,
    can_delete=True
)


class ExerciseSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by exercise name"
            }
        )
    )


class WorkoutSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by workout name"
            }
        )
    )
