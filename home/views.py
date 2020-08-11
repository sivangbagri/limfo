from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Feedback


# Create your views here.
def home(request):
    return render(request, 'home/index.html')


def short(request):
    import pyshorteners
    if request.method == 'POST':
        url = request.POST.get('link')
        shorted = pyshorteners.Shortener()
        # new3 = shorted.chilpit.short(url)
        new2 = shorted.osdb.short(url)
        # new3 = shorted.post.short(url)
        new = shorted.tinyurl.short(url)
    else:
        return HttpResponse('ERROR')

    return render(request, 'home/short.html', {'new': new, 'old': url, 'new2': new2})


def info(request):
    import phonenumbers
    from phonenumbers import geocoder
    from phonenumbers import carrier
    if request.method == 'POST':
        num = request.POST['number']

        phone_obj = phonenumbers.parse(num, 'CH')
        country = geocoder.description_for_number(phone_obj, 'en')

        service = phonenumbers.parse(num, 'RO')
        isp = carrier.name_for_number(service, 'en')
    else:
        return render(request, 'home/info.html')

    return render(request, 'home/info.html', {'country': country, 'isp': isp, 'num': num})


n = 0


def qrCode(request):
    global n
    n += 1
    import qrcode
    from PIL import Image
    img = None

    if request.GET.get('data'):
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5
        )
        mystr = request.GET.get('data')
        color = request.GET.get('color', 'black')

        qr.add_data(mystr)
        qr.make(fit=True)  # still working after removing it
        img = qr.make_image(fill_color=str(color.lower()), back_color="white")
        img.save(f'media/limfo{n}.png')
    else:
        return render(request, 'home/qrcode.html')

    return render(request, 'home/qrcode.html', {'n': n})


def translate(request):
    from googletrans import Translator
    if request.POST.get('trans'):
        txt = request.POST.get('trans')
        trans = Translator()
        lang = request.POST.get('lang')
        to = 'hi'
        if lang.lower() == 'spanish':
            to = 'es'
        elif lang.lower() == 'french':
            to = 'fr'
        elif lang.lower() == 'german':
            to = 'de'

        translated = trans.translate(txt, src='en', dest=to)
    else:
        return render(request, 'home/translate.html')
    return render(request, 'home/translate.html', {'new_text': translated.text, 'txt': txt})


x = 0


def captcha(request):
    global x
    x += 1

    from captcha.image import ImageCaptcha
    from captcha.audio import AudioCaptcha

    if request.GET.get('text'):
        image = ImageCaptcha()
        text = request.GET.get('text')
        data = image.generate(str(text))
        image.write(str(text), f'media/cap{x}.png')

        # audio = AudioCaptcha()
        # new_data = audio.generate(str(text))
        # audio.write(str(text), f'media/audio{x}.wav')
    return render(request, 'home/captcha.html', {'x': x})


def spell(request):
    from textblob import TextBlob

    if request.POST.get('incorrect'):
        incorrect = request.POST.get('incorrect')

        b = TextBlob(incorrect)
        new = str(b.correct())
    else:
        return render(request, 'home/spell.html')

    return render(request, 'home/spell.html', {'new': new})


b = 0


def bar_code(request):
    global b
    b += 1
    import barcode
    from barcode.writer import ImageWriter
    if request.POST.get('txt'):
        txt = request.POST.get('txt')
        hr = barcode.get_barcode_class('code39')
        HR = hr(txt, writer=ImageWriter())
        qr = HR.save(f'media/bar{b}')
    else:
        return render(request, 'home/bar.html')

    return render(request, 'home/bar.html', {'b': b})


def filter(request):
    if request.POST.get('curse'):
        from better_profanity import profanity

        profanity.load_censor_words()
        cursed = request.POST.get('curse')

        output = profanity.censor(cursed)
    else:
        return render(request, 'home/profanity.html')
    return render(request, 'home/profanity.html', {'output': output})


def covid_19(request):
    if request.POST.get('country'):
        country = request.POST.get('country').capitalize()
        from covid import Covid

        covid = Covid()
        try:
            data = covid.get_status_by_country_name(str(country))
            deaths = data['deaths']
            recover = data['recovered']
            active = data['active']
            confirmed = data['confirmed']
        except Exception:
            deaths = recover = active = confirmed = None

    else:
        return render(request, 'home/covid.html')
    return render(request, 'home/covid.html',
                  {'deaths': deaths, 'recover': recover, 'active': active, 'confirmed': confirmed})


def joke(request):
    import pyjokes

    Joke = pyjokes.get_joke()
    Joke1 = pyjokes.get_joke()
    Joke2 = pyjokes.get_joke()
    return render(request, 'home/joke.html', {'joke': Joke, 'joke1': Joke1, 'joke2': Joke2})


def handleSignup(request):
    if request.method == 'POST':
        # getting post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for error  input
        if len(username) > 15:
            messages.error(request, 'Username must be under 15 characters.')
            return redirect('home')
        if not username.isalnum():
            messages.error(request, 'Username must be Alphanumeric.')
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match. Try again.')
            return redirect('home')

        # create user
        myuser = User.objects.create_user(username, email, pass1)
        myuser_first_name = fname
        mysuer_last_name = lname
        myuser.save()
        messages.success(request, "limfo Account created successfully.")
        return redirect('home')
    else:
        return HttpResponse('404 Not Found')


def handleLogin(request):
    if request.method == 'POST':
        # getting post parameters
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user = authenticate(username=loginusername, password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in to your limfo account successfully.")
            return redirect('home')
        else:
            messages.error(request, 'Invalid Username or Password. Try again later.')
            return redirect('home')

    return HttpResponse('404 Not Found')


def handleLogout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')


def feedback(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        text = request.POST['text']
        if len(name) < 2 or len(email) < 3 or len(text) < 5:
            messages.error(request, "Form Submission failed!")
        else:
            messages.success(request, "Form submitted successfully!")
            feed = Feedback(name=name, email=email, text=text)
            feed.save()
    return render(request, 'home/feedback.html')


def about(request):
    return render(request, 'home/about.html')
