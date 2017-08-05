import sys
import locale
from datetime import datetime
from subprocess import call
from num2words import num2words

def extractEvents( raw_agenda ):
    result = []
    for event in raw_agenda:
        splitted_line = event.strip().split('\t')
        hour = splitted_line[1]
        single_event = splitted_line[4]
        result.append((hour,single_event))
    return result

def extractDate( raw_agenda ):
    if( len(raw_agenda)==0):
        return ((0,0),0,0)
    dt = datetime.strptime(raw_agenda[0].strip().split()[0],'%Y-%m-%d')
    locale.setlocale(locale.LC_ALL, "es_CO.utf8")
    day_number = dt.strftime('%d')
    day_name = dt.strftime('%A')
    month = dt.strftime('%B')
    year =  dt.strftime('%Y')
    return ((day_number,day_name),month,year)

def readAgenda():
    s = sys.stdin.readlines()
    return s

def buildVoiceScript( date, events, name, language):
    if(len(events)==0):
        return "Noo tienes eventos"
    result = ""
    plural = ""
    for i in range(len(events)):
        if len(events) > 1:
            result += "El " + num2words(int(i)+1,ordinal=True,lang=language) + " es a las, "
        else:
            result += "El evento es a las, "
        result += events[i][0] + ", y se llama: " + events[i][1] +"."
    if len(events) > 1:
        plural = "s"
    res = "Hola {0}, hoy es {1},{2} de {3}. Hoy tienes {4} evento{5}.{6}".format(name, date[0][1],date[0][0],date[1],len(events),plural,result)
    return res

def str2MP3( filename, voice_script, language ):
    try:
        from gtts import gTTS
        tts = gTTS(text=voice_script,lang=language)
        tts.save(filename)
    except ValueError:
        print( ValueError ) 

def playMP3( filename ):
    try:
        from mpg123 import Mpg123, Out123
        mp3 = Mpg123( filename )
        out = Out123()
        for frame in mp3.iter_frames(out.start):
            out.play( frame )
    except ValueError:
        print( ValueError )

def buildNarration(language='es', name='Andres'):
    raw_agenda = readAgenda()
    date = extractDate( raw_agenda )
    events = extractEvents( raw_agenda ) 
    return buildVoiceScript( date, events, name, language )

def buildVoice( voice_script, filename="/tmp/agenda.mp3", language='es' ):
    str2MP3( filename, voice_script, language )
    playMP3( filename )


def voiceAgenda():
    voice_script = buildNarration()
    buildVoice( voice_script )

voiceAgenda()


#call(["espeak","-ves-la+f4 -s 150 -p 75","Hola Andrés, hoy es {0} de {1}.\n Hoy tienes {2} eventos.{3}".format(fecha[2],fecha[1],len(eventos),s_e)])
