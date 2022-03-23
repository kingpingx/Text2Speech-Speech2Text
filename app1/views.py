from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os


def home(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dire = BASE_DIR+'\media'
    for i in os.listdir(dire):
        print(i)
        os.remove(BASE_DIR+f'\media\{i}')

    return render(request, 'home.html')

def listen(request):
    if request.method == 'POST' and request.FILES['myfile']:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        fn = str(filename).split('.')[0]
        from gtts import gTTS

        mytext = ""
        with open(BASE_DIR+f"/media/{file.name}", 'r', encoding="UTF-8") as f:
           for i in f.read():
                mytext += i

        output = gTTS(text=mytext, lang='hi', slow=False)

        output.save(BASE_DIR+f"/media/{fn}.mp3")

        fp = f"/media/{fn}.mp3"

        print(fp)

        return render(request, 'l.html', {
            'source': fp, 'uploaded' : "File Uploaded",
        })
    else:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dire = BASE_DIR+"/media/"
        for f in os.listdir(dire):
            os.remove(os.path.join(dire, f))
        return render(request, 'l.html')




def speak(request):
    if request.method == 'POST' and request.FILES['myfile']:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = request.FILES['myfile']
        fs = FileSystemStorage()     
        filename = fs.save(file.name, file)
        fn = str(filename).split('.')[0]

        try:
            from os import path
            from pydub import AudioSegment
            # files.
            src =  BASE_DIR+f"/media/{fn}.mp3"

            dst =  BASE_DIR+f"/media/{fn}.wav"
            # convert wav to mp3.
            sound = AudioSegment.from_mp3(src)
            sound.export(dst, format="wav")
        except Exception as e:
                print(e)
                return render(request, 'error.html')

        

        import speech_recognition as sr
        
        r = sr.Recognizer()

        with sr.AudioFile(dst) as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            try:
                text = r.recognize_google(audio_data)
            except Exception as e:
                print(e)
                return render(request, 'error.html')
            else:
                print(text)
        
        completeName = BASE_DIR+f"/media/{fn}.txt"        
        with open(completeName, 'w') as file:
            file.write(text)

        fp2 = f"/media/{fn}.txt"

        return render(request, 's.html', {
            'source': fp2
        })
    else:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dire = BASE_DIR+'\media'
        for f in os.listdir(dire):
            os.remove(os.path.join(dire, f))
        return render(request, 's.html')
