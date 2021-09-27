from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os


def home(request):
    return render(request, 'home.html')

def listen(request):
    if request.method == 'POST' and request.FILES['myfile']:
        file = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        fn = str(filename).split('.')[0]
        from gtts import gTTS
        fp1 = f'C:\\Users\\Admin\\Desktop\\listener\\media\\{file.name}'

        mytext = ""
        with open(fp1, 'r', encoding="UTF-8") as f:
           for i in f.read():
                mytext += i

        output = gTTS(text=mytext, lang='hi', slow=False)

        output.save(f"C:\\Users\\Admin\\Desktop\\listener\\media\\{fn}.mp3")

        fp = f"/media/{fn}.mp3"

        return render(request, 'l.html', {
            'source': fp, 'uploaded' : "File Uploaded",
        })
    else:
        dire = 'C:\\Users\\Admin\\Desktop\\listener\\media'
        for f in os.listdir(dire):
            os.remove(os.path.join(dire, f))
        return render(request, 'l.html')




def speak(request):
    if request.method == 'POST' and request.FILES['myfile']:
        file = request.FILES['myfile']
        fs = FileSystemStorage()     
        filename = fs.save(file.name, file)
        fn = str(filename).split('.')[0]
        fp = f'C:\\Users\\Admin\\Desktop\\listener\\media\\{file.name}'

        try:
            from os import path
            from pydub import AudioSegment
            # files.
            src = fp
            dst =  f'C:\\Users\\Admin\\Desktop\\listener\\media\\{fn}.wav'
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
        
        completeName = f"C:\\Users\\Admin\\Desktop\\listener\\media\\{fn}.txt"        
        with open(completeName, 'w') as file:
            file.write(text)

        fp2 = f"/media/{fn}.txt"

        return render(request, 's.html', {
            'source': fp2
        })
    else:
        dire = 'C:\\Users\\Admin\\Desktop\\listener\\media'
        for f in os.listdir(dire):
            os.remove(os.path.join(dire, f))
        return render(request, 's.html')
