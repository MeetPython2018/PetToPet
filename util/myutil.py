from django.shortcuts import redirect, render, reverse


def authuser(fn):
    def newfn(request):
        tel = request.session.get('tel', None)
        if tel:
            res = fn(request)
            return res
        else:
            return redirect(reverse("official:index"))
    return newfn
