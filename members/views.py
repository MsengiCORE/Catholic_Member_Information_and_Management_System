from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ChurchMemberForm


def register_member(request):
    if request.method == "POST":
        form = ChurchMemberForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Church member registered successfully."
            )

            return redirect("members:register")

    else:
        form = ChurchMemberForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "members/register.html",
        context
    )