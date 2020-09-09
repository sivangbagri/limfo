from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Feedback, Scan
import requests
import json
from django.core.files.storage import FileSystemStorage


# ----Core Features----
def home(request):
    return render(request, 'home/index.html')


def short(request):
    import pyshorteners
    if request.method == 'POST':
        url = request.POST.get('link')
        shorted = pyshorteners.Shortener()
        # new3 = shorted.chilpit.short(url)
        # new2 = shorted.osdb.short(url)
        new2 = shorted.isgd.short(url)
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

    return render(request, 'home/info.html',
                  {'country': country, 'isp': isp, 'num': num})


n = 0
b = 0


def generate(request):
    bar_choice = False
    qr_choice = False
    global n
    global b
    import qrcode
    img = None
    choice = request.GET.get('Radios')
    if request.GET.get('data'):

        mystr = request.GET.get('data')
        if choice == 'qrcode':
            n += 1
            qr_choice = True
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5
            )
            color = request.GET.get('color', 'black')
            qr.add_data(mystr)
            qr.make(fit=True)  # still working after removing it
            img = qr.make_image(fill_color=str(color.lower()), back_color="white")
            img.save(f'media/limfo{n}.png')
        else:
            bar_choice = True
            b += 1
            # BAR code function goes brrrrr
            import barcode
            from barcode.writer import ImageWriter
            hr = barcode.get_barcode_class('code39')
            HR = hr(mystr, writer=ImageWriter())
            qr = HR.save(f'media/bar{b}')

    else:
        return render(request, 'home/qrcode.html')

    return render(request, 'home/qrcode.html', {'n': n, 'b': b, 'bar_choice': bar_choice, 'qr_choice': qr_choice})


x = 0


def captcha(request):
    global x
    x += 1
    audio = down = False
    from captcha.image import ImageCaptcha
    from captcha.audio import AudioCaptcha
    text = request.GET.get('text')
    choice = request.GET.get('choice_cap')

    if request.GET.get('text'):
        # ReCaptcha code goes brrr
        client_key = request.GET.get('g-recaptcha-response')
        secret_key = '6LfYRsUZAAAAABbkZ7b1AlAv10Nml3CwensXtJc2'
        capData = {
            'secret': secret_key,
            'response': client_key,
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=capData)
        response = json.loads(r.text)
        verify = response['success']
        if choice == 'text_cap' and verify:
            down = True
            image = ImageCaptcha()
            data = image.generate(str(text))
            image.write(str(text), f'media/cap{x}.png')
        elif choice == 'audio_cap' and verify:
            audio = True
            audio = AudioCaptcha()
            try:
                new_data = audio.generate(str(text))
                audio.write(str(text), f'media/audio{x}.wav')
            except Exception:
                messages.error(request, 'Only numbers are allowed while creating a Audio captcha.')
        else:
            audio = False
            messages.error(request, 'Please fill the required fields correctly.')
            return render(request, 'home/captcha.html')

    else:
        return render(request, 'home/captcha.html')

    return render(request, 'home/captcha.html', {'x': x, 'audio': audio, 'down': down})


p = 0
a = 0


def text_transform(request):
    global p
    global a
    choice = request.POST.get('Radios')
    if request.POST.get('text'):
        # Profanity Code goes brrrr

        if choice == 'profanity':
            from better_profanity import profanity

            profanity.load_censor_words()
            txt = request.POST.get('text')

            output = profanity.censor(txt)
            return render(request, 'home/text.html', {'output': output})

        # Translation Code goes brrrrr
        elif choice == 'translate':
            from googletrans import Translator

            txt = request.POST.get('text')

            trans = Translator()
            lang = request.POST.get('lang')
            to = 'hi'
            if lang.lower() == 'spanish':
                to = 'es'
            elif lang.lower() == 'french':
                to = 'fr'
            elif lang.lower() == 'german':
                to = 'de'
            elif lang.lower() == 'arabic':
                to = 'ar'
            elif lang.lower() == 'urdu':
                to = 'ur'

            output = trans.translate(txt, src='en', dest=to)
            return render(request, 'home/text.html', {'output': output.text})
        # Mistake Remover Code goes brrrr
        elif choice == 'mistake':
            from textblob import TextBlob
            txt = request.POST.get('text')
            b = TextBlob(txt)
            output = str(b.correct())
            return render(request, 'home/text.html', {'output': output})
        # Text to PDF Code goes brrrr
        elif choice == 'pdf':
            thank = True
            p += 1
            txt = request.POST.get('text')

            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 15, txt=str(txt)[0:120], ln=1, align="L")
            pdf.cell(200, 15, txt=str(txt)[120:250], ln=1, align="L")
            pdf.cell(200, 15, txt=str(txt)[250:510], ln=1, align="L")
            pdf.cell(200, 15, txt=str(txt)[510:640], ln=1, align="L")
            pdf.cell(200, 15, txt=str(txt)[640:770], ln=1, align="L")
            pdf.cell(200, 15, txt=str(txt)[770:900], ln=1, align="L")
            pdf.output(f"media/limfoPDF{p}.pdf")
            return render(request, 'home/text.html', {'p': p, 'thank': thank})
        # Audio Book Code goes brrrr
        elif choice == 'audio':
            audio_b = True
            a += 1
            from gtts import gTTS
            import os
            txt = request.POST.get('text')
            language = 'en'
            audio = gTTS(text=txt, lang=language, slow=False)
            audio.save(f"media/audio_b{a}.wav")
            os.system(f"media/audio_b{a}.wav")
            return render(request, 'home/text.html', {'p': p, 'audio': audio_b, 'a': a})
    else:
        return render(request, 'home/text.html')


m = f = c = 0


def pdf_manipulate(request):
    from PyPDF2 import PdfFileMerger
    txt = merge = protect = False
    global m
    global c
    global f
    m += 1
    choice = request.POST.get('Radios')
    if request.method == 'POST' and request.FILES['pdf_file']:
        mypdf = request.FILES['pdf_file']
        fs = FileSystemStorage()
        filename = fs.save(mypdf.name, mypdf)
        uploaded_file_url = fs.url(filename)
        if choice == 'merge' and request.FILES['pdf2']:
            merge = True
            pdf2 = request.FILES['pdf2']
            fs = FileSystemStorage()
            filename = fs.save(pdf2.name, pdf2)
            uploaded_pdf2 = fs.url(filename)

            merger = PdfFileMerger()
            merger.append(f'media/{uploaded_file_url[7:]}')
            merger.append(f'media/{uploaded_pdf2[7:]}')
            merger.write(f"media/merge{m}.pdf")
            merger.close()
            return render(request, 'home/pdfs.html', {'m': m, 'merge': merge})
        if choice == 'convert':
            txt = True
            c += 1
            import PyPDF2
            file = open(f'media/{uploaded_file_url[7:]}', 'rb')
            reader = PyPDF2.PdfFileReader(file)
            pages = reader.numPages
            pageobj = reader.getPage(pages - 1)
            text = pageobj.extractText()

            with open(f'media/convertPDF{c}.txt', "a") as file2:
                file2.writelines(text)
            return render(request, 'home/pdfs.html', {'c': c, 'text': txt})
        if choice == 'protect':
            password = request.POST.get('password')
            f += 1
            protect = True
            from PyPDF2 import PdfFileWriter, PdfFileReader
            pdfWriter = PdfFileWriter()
            pdf = PdfFileReader(f'media/{uploaded_file_url[7:]}')
            for page in range(pdf.numPages):
                pdfWriter.addPage(pdf.getPage(page))
            if password:
                pwd = str(password)
            else:
                pwd = 'limfo'
            print(pwd)
            pdfWriter.encrypt(pwd)

            with open(f'media/new{f}.pdf', 'wb') as file:
                pdfWriter.write(file)
            return render(request, 'home/pdfs.html', {'f': f, 'protect': protect})
    else:
        return render(request, 'home/pdfs.html')


g = e = d = 0


def image_transform(request):
    toPDF = enhance = difference = False
    global g
    global e
    global d
    choice = request.POST.get('Radios')
    if request.method == 'POST' and request.FILES['img_file']:
        myfile = request.FILES['img_file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        # print(uploaded_file_url[7:])
        if choice == 'toPDF':
            toPDF = True
            g += 1
            from PIL import Image
            image = Image.open(f'media/{uploaded_file_url[7:]}')
            im = image.convert('RGB')
            im.save(f'media/gain{g}.pdf')
            return render(request, 'home/image.html', {'g': g, 'toPDF': toPDF})
        if choice == 'enh':
            e += 1
            enhance = True
            from PIL import Image, ImageFilter

            im = Image.open(f'media/{uploaded_file_url[7:]}')
            from PIL import ImageEnhance
            enh = ImageEnhance.Contrast(im)
            enhanced = enh.enhance(1.8)
            enhanced.save(f'media/enhanced{e}.jpg')
            messages.success(request, 'Image enhanced.')
            return render(request, 'home/image.html', {'enhance': enhance, 'e': e})
        if choice == 'diff' and request.FILES['img2']:
            myfile = request.FILES['img2']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            img_2 = fs.url(filename)
            from PIL import Image, ImageChops

            img1 = Image.open(f'media/{uploaded_file_url[7:]}')
            img2 = Image.open(f'media/{img_2[7:]}')
            try:
                diff = ImageChops.difference(img1, img2)
                if diff.getbbox():
                    difference = True
                    d += 1
                    diff.save(f'media/difference{d}.jpg')
                else:
                    messages.error(request, 'No difference found.')
            except Exception:
                messages.error(request, 'Images are not comparable.')

            return render(request, 'home/image.html', {'d': d, 'difference': difference})
    else:
        return render(request, 'home/image.html')


def scan(request):
    if request.method == 'POST' and request.FILES['qrfile']:
        myfile = request.FILES['qrfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        # print(uploaded_file_url[1:])
        from pyzbar.pyzbar import decode
        from PIL import Image
        try:
            d = decode(Image.open(uploaded_file_url[1:]))
            return render(request, 'home/scan.html', {'data': d[0].data.decode()})

        except Exception:
            exception = True
            return render(request, 'home/scan.html',
                          {'data': 'Only QR Code files are allowed!', 'exception': exception})

    return render(request, 'home/scan.html')


# -----Website mex features----
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
        try:
            myuser = User.objects.create_user(username, email, pass1)
            myuser_first_name = fname
            mysuer_last_name = lname
            myuser.save()
            messages.success(request, "limfo Account created successfully.")
        except Exception as e:
            messages.error(request, "Username already exist. Try again with a unique one.")

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
