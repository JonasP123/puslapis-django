from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import requests
from datetime import datetime
from unidecode import unidecode

# Create your views here.
def homepage(request):
	return render(request=request,
				  template_name='pagrindas/home.html', 
				  context={})

def register(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()#sukuriamas useris
			username = form.cleaned_data.get('username')
			messages.success(request, f'Sukurtas naujas accountas: {username}')#sukuriamas pranesimas, taciau niekur nerodomas
			login(request, user)
			return redirect("pagrindas:homepage")#app_name ir path pavadinimu skliaustuose sujungimas
		else:
			for msg in form.error_messages:
				messages.error(request, f'{msg}: {form.error_messages[msg]}')

	form = UserCreationForm
	return render(request,
				  'pagrindas/register.html',
				  context={'form':form})

def logout_request(request):
	logout(request)
	messages.info(request, 'Sėkmignai atsijungta')
	return redirect("pagrindas:homepage")

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, f'Sėkmignai prisijungėte kaip: {username}')
				return redirect("pagrindas:homepage")
			else:
				messages.error(request, 'Neteisingas prisijungimo vardas arba slaptažodis')
		else:
			messages.error(request, 'Neteisingas prisijungimo vardas arba slaptažodis')
		

	form = AuthenticationForm()
	return render(request,
				  'pagrindas/login.html',
				  {'form':form})

def laipsniaiView(request):
    return render(request, 'pagrindas/laipsniai.html')

def temperaturaView(request):
<<<<<<< HEAD
    try:
        miestas = request.POST['content']
        miestas_mazas = miestas.lower()
        miestas_mazas = miestas_mazas.replace(' ','-')
        miestas_mazas = unidecode(miestas_mazas)#pakeicia lietuviskas raides angliskomis
        r = requests.get('https://api.meteo.lt/v1/places/'+miestas_mazas+'/forecasts/long-term')
        turinys = r.json()
        miestas = turinys['place']['name']
        prognozes = turinys['forecastTimestamps']
        for prognoze in prognozes:
            dabartinis_laikas = str(datetime.now())
            if dabartinis_laikas < prognoze['forecastTimeUtc']:
                laikas = prognoze['forecastTimeUtc']
                temperatura = prognoze['airTemperature']
                vejas = prognoze['windSpeed']#tikriname, verciame reiksme
                vejo_gusiai = prognoze['windGust']
                vejo_kryptis = prognoze['windDirection']
                debesuotumas = prognoze['cloudCover']
                slegis = prognoze['seaLevelPressure']
                krituliu_kiekis = prognoze['totalPrecipitation']
                oro_salygos = prognoze['conditionCode']#tikriname, verciame reiksme
                if 0 <= vejo_kryptis <= 11:
                    vejo_kryptis = 'šiaurės'
                elif 11 < vejo_kryptis <= 34:
                    vejo_kryptis = 'šiaurės, šiaurės rytų'
                elif 34 < vejo_kryptis <= 56:
                    vejo_kryptis = 'šiaurės rytų'
                elif 56 < vejo_kryptis <= 79:
                    vejo_kryptis = 'rytų, šiaurės rytų'
                elif 79 < vejo_kryptis <= 101:
                    vejo_kryptis = 'rytų'
                elif 101 < vejo_kryptis <= 124:
                    vejo_kryptis = 'rytų, pietryčių'
                elif 124 < vejo_kryptis <= 146:
                    vejo_kryptis = 'pietryčių'
                elif 146 < vejo_kryptis <= 169:
                    vejo_kryptis = 'pietų, pietryčių'
                elif 169 < vejo_kryptis <= 191:
                    vejo_kryptis = 'pietų'
                elif 191 < vejo_kryptis <= 214:
                    vejo_kryptis = 'pietų, pietvakarių'
                elif 214 < vejo_kryptis <= 236:
                    vejo_kryptis = 'pietvakarių'
                elif 236 < vejo_kryptis <= 259:
                    vejo_kryptis = 'vakarų, pietvakarių'
                elif 259 < vejo_kryptis <= 281:
                    vejo_kryptis = 'vakarų'
                elif 281 < vejo_kryptis <= 304:
                    vejo_kryptis = 'vakarų, šiaurės vakarų'
                elif 304 < vejo_kryptis <= 326:
                    vejo_kryptis = 'šiaurės vakarų'
                elif 326 < vejo_kryptis <= 349:
                    vejo_kryptis = 'šiaurės, šiaurės vakarų'
                elif 349 < vejo_kryptis <= 360:
                    vejo_kryptis = 'šiaurės'

                if oro_salygos == 'clear':
                    oro_salygos = 'giedra'
                if oro_salygos == 'isolated-clouds':
                    oro_salygos = 'mažai debesuota'
                if oro_salygos == 'scattered-clouds':
                    oro_salygos = 'debesuota su pragiedruliais'
                if oro_salygos == 'overcast':
                    oro_salygos = 'debesuota'
                if oro_salygos == 'light-rain':
                    oro_salygos = 'nedidelis lietus'
                if oro_salygos == 'moderate-rain':
                    oro_salygos = 'lietus'
                if oro_salygos == 'heavy-rain':
                    oro_salygos = 'smarkus lietus'
                if oro_salygos == 'sleet':
                    oro_salygos = 'šlapdriba'
                if oro_salygos == 'light-snow':
                    oro_salygos = 'nedidelis sniegas'
                if oro_salygos == 'moderate-snow':
                    oro_salygos = 'sniegas'
                if oro_salygos == 'heavy-snow':
                    oro_salygos = 'smarkus sniegas'
                if oro_salygos == 'fog':
                    oro_salygos = 'rūkas'
                oro_salygos = oro_salygos[0].upper()+oro_salygos[1:]
                return render(request,
                              'pagrindas/home.html',
                              {'miestas': miestas,
                               'laikas': laikas,
                               'temperatura': temperatura,
                               'vejas': vejas,
                               'vejo_gusiai': vejo_gusiai,
                               'vejo_kryptis': vejo_kryptis,
                               'debesuotumas': debesuotumas,
                               'slegis': slegis,
                               'krituliu_kiekis': krituliu_kiekis,
                               'oro_salygos': oro_salygos})
    except:
        messages.error(request, 'Neegzistuojantis miestas, bandyk dar kartą')
        return render(request=request,
                      template_name='pagrindas/home.html', 
                      context={})
=======
    miestas = request.POST['content']
    miestas_mazas = miestas.lower()
    miestas_mazas = miestas_mazas.replace(' ','-')
    miestas_mazas = unidecode(miestas_mazas)#pakeicia lietuviskas raides angliskomis
    r = requests.get('https://api.meteo.lt/v1/places/'+miestas_mazas+'/forecasts/long-term')
    turinys = r.json()
    miestas = turinys['place']['name']
    prognozes = turinys['forecastTimestamps']
    for prognoze in prognozes:
        dabartinis_laikas = str(datetime.now())
        if dabartinis_laikas < prognoze['forecastTimeUtc']:
            laikas = prognoze['forecastTimeUtc']
            temperatura = prognoze['airTemperature']
            vejas = prognoze['windSpeed']#tikriname, verciame reiksme
            vejo_gusiai = prognoze['windGust']
            vejo_kryptis = prognoze['windDirection']
            debesuotumas = prognoze['cloudCover']
            slegis = prognoze['seaLevelPressure']
            krituliu_kiekis = prognoze['totalPrecipitation']
            oro_salygos = prognoze['conditionCode']#tikriname, verciame reiksme
            if 0 <= vejo_kryptis <= 11:
                vejo_kryptis = 'šiaurės'
            elif 11 < vejo_kryptis <= 34:
                vejo_kryptis = 'šiaurės, šiaurės rytų'
            elif 34 < vejo_kryptis <= 56:
                vejo_kryptis = 'šiaurės rytų'
            elif 56 < vejo_kryptis <= 79:
                vejo_kryptis = 'rytų, šiaurės rytų'
            elif 79 < vejo_kryptis <= 101:
                vejo_kryptis = 'rytų'
            elif 101 < vejo_kryptis <= 124:
                vejo_kryptis = 'rytų, pietryčių'
            elif 124 < vejo_kryptis <= 146:
                vejo_kryptis = 'pietryčių'
            elif 146 < vejo_kryptis <= 169:
                vejo_kryptis = 'pietų, pietryčių'
            elif 169 < vejo_kryptis <= 191:
                vejo_kryptis = 'pietų'
            elif 191 < vejo_kryptis <= 214:
                vejo_kryptis = 'pietų, pietvakarių'
            elif 214 < vejo_kryptis <= 236:
                vejo_kryptis = 'pietvakarių'
            elif 236 < vejo_kryptis <= 259:
                vejo_kryptis = 'vakarų, pietvakarių'
            elif 259 < vejo_kryptis <= 281:
                vejo_kryptis = 'vakarų'
            elif 281 < vejo_kryptis <= 304:
                vejo_kryptis = 'vakarų, šiaurės vakarų'
            elif 304 < vejo_kryptis <= 326:
                vejo_kryptis = 'šiaurės vakarų'
            elif 326 < vejo_kryptis <= 349:
                vejo_kryptis = 'šiaurės, šiaurės vakarų'
            elif 349 < vejo_kryptis <= 360:
                vejo_kryptis = 'šiaurės'

            if oro_salygos == 'clear':
                oro_salygos = 'giedra'
            if oro_salygos == 'isolated-clouds':
                oro_salygos = 'mažai debesuota'
            if oro_salygos == 'scattered-clouds':
                oro_salygos = 'debesuota su pragiedruliais'
            if oro_salygos == 'overcast':
                oro_salygos = 'debesuota'
            if oro_salygos == 'light-rain':
                oro_salygos = 'nedidelis lietus'
            if oro_salygos == 'moderate-rain':
                oro_salygos = 'lietus'
            if oro_salygos == 'heavy-rain':
                oro_salygos = 'smarkus lietus'
            if oro_salygos == 'sleet':
                oro_salygos = 'šlapdriba'
            if oro_salygos == 'light-snow':
                oro_salygos = 'nedidelis sniegas'
            if oro_salygos == 'moderate-snow':
                oro_salygos = 'sniegas'
            if oro_salygos == 'heavy-snow':
                oro_salygos = 'smarkus sniegas'
            if oro_salygos == 'fog':
                oro_salygos = 'rūkas'
            oro_salygos = oro_salygos[0].upper()+oro_salygos[1:]
            return render(request,
                          'pagrindas/home.html',
                          {'miestas': miestas,
                           'laikas': laikas,
                           'temperatura': temperatura,
                           'vejas': vejas,
                           'vejo_gusiai': vejo_gusiai,
                           'vejo_kryptis': vejo_kryptis,
                           'debesuotumas': debesuotumas,
                           'slegis': slegis,
                           'krituliu_kiekis': krituliu_kiekis,
                           'oro_salygos': oro_salygos})
>>>>>>> fc304c77fd876257c54625d3d3c43c0600ace91e
