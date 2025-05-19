# https://www.informit.com/articles/article.aspx?p=169460

from machine import Pin, PWM
import time

BUZZER_PIN = 27
# define frequency for each tone
B1  = 31
C2  = 33
CS2 = 35
D2  = 37
DS2 = 39
E2  = 41
F2  = 44
FS2 = 46
G2  = 49
GS2 = 52
A2  = 55
AS2 = 58
B2  = 62
C3  = 65
CS3 = 69
D3  = 73
DS3 = 78
E3  = 82
F3  = 87
FS3 = 93
G3  = 98
GS3 = 104
A3  = 110
AS3 = 117
B3  = 123
C4  = 131
CS4 = 139
D4  = 147
DS4 = 156
E4  = 165
F4  = 175
FS4 = 185
G4  = 196
GS4 = 208
A4  = 220
AS4 = 233
B4  = 247
C5  = 262
CS5 = 277
D5  = 294
DS5 = 311
E5  = 330
F5  = 349
FS5 = 370
G5  = 392
GS5 = 415
A5  = 440
AS5 = 466
B5  = 494
C6  = 523
CS6 = 554
D6  = 587
DS6 = 622
E6  = 659
F6  = 698
FS6 = 740
G6  = 784
GS6 = 831
A6  = 880
AS6 = 932
B6  = 988
C7  = 1047
CS7 = 1109
D7  = 1175
DS7 = 1245
E7  = 1319
F7  = 1397
FS7 = 1480
G7  = 1568
GS7 = 1661
A7  = 1760
AS7 = 1865
B7  = 1976
C8  = 2093
CS8 = 2217
D8  = 2349
DS8 = 2489
E8  = 2637
F8  = 2794
FS8 = 2960
G8  = 3136
GS8 = 3322
A8  = 3520
AS8 = 3729
B8  = 3951
C9  = 4186
CS9 = 4435
D9  = 4699
DS9 = 4978
P = 0

# Super Mario - Main Theme:d=4,o=5,b=125:a,8f.,16c,16d,16f,16p,f,16d,16c,16p,16f,16p,16f,16p,8c6,8a.,g,16c,a,8f.,16c,16d,16f,16p,f,16d,16c,16p,16f,16p,16a#,16a,16g,2f,16p,8a.,8f.,8c,8a.,f,16g#,16f,16c,16p,8g#.,2g,8a.,8f.,8c,8a.,f,16g#,16f,8c,2c6

def RTTTL(text):
    try:
        title, defaults, song = text.split(':')
        d, o, b = defaults.split(',')
        d = int(d.split('=')[1])
        o = int(o.split('=')[1])
        b = int(b.split('=')[1])
        whole = (60000/b)*4
        noteList = song.split(',')
    except:
        return 'Please enter a valid RTTTL string.'
    notes = 'abcdefgp'
    outList = []
    for note in noteList:
        index = 0
        for i in note:
            if i in notes:
                index = note.find(i)
                break
        length = note[0:index]
        value = note[index:].replace('#','s').replace('.','')
        if not any(char.isdigit() for char in value):
            value += str(o)
        if 'p' in value:
            value = 'p'
        if length == '':
            length = d
        else:
            length = int(length)
        length = whole/length
        if '.' in note:
            length += length/2
        outList.append((eval(value.upper()), length))
    return outList

def play(tune):
    tune = RTTTL(tune)
    if type(tune) is not list:
        return tune
    for freqc, msec in tune:
        msec = msec * 0.001
        if freqc > 0:
            pwm0 = PWM(Pin(BUZZER_PIN), freq=freqc, duty=512)
        time.sleep(msec*0.9)
        if freqc > 0:
            pwm0.deinit()
        time.sleep(msec*0.1)
        
SONGS = [
    'MamboIta:d=4,o=5,b=140:8e6,8p,8b,8p,b,p,8a,8p,8a,8a,8a,8b,8c6,8a,8e6,88b,8p,b,8p,8b,8a,8p,8a,8a,8a,8b,8c6,8a,8e,8e,8e,8e,8e,8e,8e,8e,8e,8e,8e,8e,8g,8e,8e,16e',
    'ShellBeC:d=8,o=5,b=140:c,d,f.,16f,f,f,d,c,d,c,2f.,f,g,a.,16a,a,a,c6,a,g,f,2g.,c6,a#,a.,16a,a,a,g,f,f,f,c,d,16d,d,d,g,f,e,d,c.,16c,c,c,a,g,d,e,2f',
    'MortalKo:d=4,o=6,b=35:32a#5,32a#5,32c#6,32a#5,32d#6,32a#5,32f6,32d#6,32c#6,32c#6,32f6,32c#6,32g#6,32c#6,32f6,32c#6,32g#5,32g#5,32c6,32g#5,32c#6,32g#5,32d#6,32c#6,32f#5,32f#5,32a#5,32f#5,32c#6,32f#5,32c#6,32c6,32a#5,32a#5,32c#6,32a#5,32d#6,32a#5,32f6,32d#6,32c#6,32c#6,32f6,32c#6,32g#6,32c#6,32f6,32c#6,32g#5,32g#5,32c6,32g#5,32c#6,32g#5,32d#6,32c#6,32f#5,32f#5,32a#5,32f#5,32c#6,32f#5,32c#6,32c6',
    'Wannabe:d=4,o=5,b=125:16g,16g,16g,16g,8g,8a,8g,8e,8p,16c,16d,16c,8d,8d,8c,e,p,8g,8g,8g,8a,8g,8e,8p,c6,8c6,8b,8g,8a,16b,16a,g',
    'NaginThe:d=4,o=6,b=125:8d,8c,8d#,8c,8d,8a#5,c,8d,8c,8d#,8c,8d,8a#5,c,8d,8d#,g,g#,g,g#,g,8d,8d#,f,g,f,g,f,8d#,8d,c,8d,8c,8d#,8c,8d,8a#5,c,8d,8c,8d#,8c,8d,8a#5,c5',
    'MuppetSh:d=4,o=6,b=125:16d5,16p,16d5,16p,16d5,16p,16b5,16p,8c#,16c5,8c#.5,16a5,16p,16d5,16p,16d,16p,16d5,16p,16b5,16p,16c#5,16p,16d5,8a5,16p,8p,16d5,16p,16f#5,16p,16f#5,16p,16a5,16p,8g5,16f#5,16g5,16p,16d5,16d5,16e5,16f#5,16f#5,16p,16f#5,16p,16f#5,16a5,8p',
    'Mozart:d=4,o=6,b=120:16f#5,16e5,16d#5,16e5,g5,16a5,16g5,16f#5,16g5,b5,16c,16b5,16a#5,16b5,16f#,16e,16d#,16e,16f#,16e,16d#,16e,g,8e,8g,32d,32e,16f#,8e,8d,8e,32d,32e,16f#,8e,8d,8e,32d,32e,16f#,8e,8d,8c#,b5',
    'Bollywoo:d=4,o=6,b=112:8g.5,8g.5,32a5,32b5,16a5,8g5,8g5,8b5,8a5,8g.5,8g.5,32a5,32b5,16a5,8g5,8g5,8g5,8a5,16e5,8e5,16e5,16a5,8a5,16a5,16a5,8e5,16e5,16a5,8a5,16a5,16a5,2e5,8a.5,8c,16c.,2e.,c,8c,2b5',
    'Theme:d=4,o=5,b=112:16g6,8p,16g6,8p,16f6,16p,16f#6,16p,16g6,8p,16g6,8p,16a#6,16p,16c7,16p,16g6,8p,16g6,8p,16f6,16p,16f#6,16p,16g6,8p,16g6,8p,16a#6,16p,16c7,16p,16a#6,16g6,2d6,32p,16a#6,16g6,2c#6,32p,16a#6,16g6,2c6,16p,16a#,16c6',
    'Macarena:d=16,o=5,b=180:4f6,8f6,8f6,4f6,8f6,8f6,8f6,8f6,8f6,8f6,8f6,8a6,8c6,8c6,4f6,8f6,8f6,4f6,8f6,8f6,8f6,8f6,8f6,8f6,8d6,8c6,4p,4f6,8f6,8f6,4f6,8f6,8f6,8f6,8f6,8f6,8f6,8f6,8a6,4p,2c.7,4a6,8c7,8a6,8f6,4p,2p',
    'HakunaMa:d=32,o=6,b=35:p,e,f.,f.,d#,8c#.,a#.5,c#,c#.,a#5,c#.,8d#.,16p,f.,f.,d#,c#.,8c#.,f.,f.,d#,8d#.,d#,e.,d#,e,d#,16c#.',
    'TheGodfa:d=2,o=6,b=125:c#,8c,8c#,d,4c#,4c#,1a5,p,c#,8c,8c#,d,4c#,4c#,1g#5,p,c#,8c,8c#,e,4c#,c,4d#,1c#,8p,4a5,4g#5,4a5,c#,4c,g#5',
    'Terminat:d=4,o=6,b=40:32d#6,16f6,4f#6,16f.6,16c#6,4f#5,32d#6,16f6,4f#6,16f.6,16c#6,4a#6,4g#6,16d#6,16f6,4f#6,16f.6,16c#6,4g#5,4f#5,16d#5,4f#5,4f5,32d#6,16f6,4,f#6,2f#.5',
    'StarTrek:d=32,o=6,b=225:16c#,d,d#,4e.,d#,d,8c#',
    'StarTrek:d=8,o=6,b=125:f5.,16a#5,4d#.,d,16a#5.,16g5.,16c.,4f.,16f,4g#.,p,4f5.,a#5,d,4c.,g#5,g,2f.,a#5,d#,f,g,d#,4f.,4d#.,2d,a#5,2c.,4f5.,a#5,d,4c.,g#5,g,2f.,a#5,d#,f,g,d#,4f.,4d#.,4d.,d,a#5,d,2c.',
    'StarTrek:d=32,o=7,b=180:d#,e,g,d#,g,d#,f#,e,f,2p,d#,e,g,d#,g,d#,f#,e,f,2p,d#,e,g,d#,g,d#,f#,e,f',
    'PippiLon:d=4,o=6,b=250:g5,c,e,c,d,p,8f,8e,8d,8c,b5,d,g5,b5,2c,e,p,g5,c,e,c,d,p,8f,8e,8d,8c,b5,d,g5,b5,2c,2p,2e,e,e,2f,f,8f,8e,d,8d,8d,d,8c,8c,b5,c,d,p,2e,e,e,2f,f,e,d,d,c,b5,1c',
    'HarryPot:d=8,o=6,b=100:b5,e.,16g,f#,4e,b,4a.,4f#.,e.,16g,f#,4d,f,2b5,p,b5,e.,16g,f#,4e,b,4d7,c#7,4c7,g#,c.7,16b,a#,4a#5,g,2e',
    'Rocky2Th:d=4,o=6,b=112:8d5,8e5,8f5,8p,8f5,16f5,8f5,16p,8e5,8d5,8c5,8c5,8d5,8e5,8d5,8p,8d5,8e5,8f5,16p,32p,8e5,8f5,8g5,16p,32p,8f5,16p,32a5,8p,16p,2a5,p,8d5,16c5,8d5,16p,8c5',
    'DilToPaa:d=16,o=6,b=63:a5,b5,c,8a5,8e,8d.,c,4b5,p,a5,b5,c,8a5,8f,4e,8p,a5,b5,c,8a5,8e,8d.,c,8b.5,32p,c,d,e,b5,8c,8b5,8a.5',
    'WohChali:d=4,o=6,b=112:8c,8d,e,8e,8e,e,8e,8f,8d,8e,16f,16a,8g,g,8f,8e,8d,8e,8d,16d,d,8d,8g,g,8d,16e,16f,e,8c,8d,e,8e,8e,e,8e,8f,8d,8e,16f,16a,8g,g,8f,8e,8d,e,8d,16d,a',
    'Saathiya:d=4,o=6,b=70:8f#5,16c#,16b5,16c#,16b5,16c#,16b5,16c#,16d#,16e,16d#,c#,8f#5,16c#,16b5,16c#,16b5,16c#,16b5,16c#,16d#,16c#,16b5,g#5,8f#5,16c#,16b5,16c#,16b5,16c#,16b5,16c#,16d#,16e,16d#,c#,16b5,16c#,16b5,16g#5,16b5,16g#5,16f#5,16e5,f#5',
    'NaNaNaNa:d=4,o=6,b=200:8d,8d,8d,8d,8d,8d,8d,d,8d,8e,8f,e,c,8d,8d,8d,8d,8d,8d,8d,d,8d,8e,8f,e,c,8f,8f,8e,8f,g,e,f,d,e,c,8f,8f,8e,8f,g,e,f,d,2e',
    'DilChaht:d=4,o=6,b=125:8d,8e,8g,8b,a,8g,f#,d,e,f#,8d,8e,8g,8b,a,8g,f#,d,e.,8p,8d7,8e7,8g7,8b7,a7,8g7,f#7,d7,e7,f#7,8d7,8e7,8g7,8b7,a7,8g7,f#7,d7,e.7,p,8d,8e,8g,8a,2p,16p,8d,8e,8g,8a',
    '5thSymph:d=16,o=5,b=100:g,g,g,4d#,4p,f,f,f,4d,4p,g,g,g,d#,g#,g#,g#,g,d#6,d#6,d#6,4c6,8p,g,g,g,d,g#,g#,g#,g,f6,f6,f6,4d6,8p,g6,g6,f6,4d#6,8p,g6,g6,f6,4d#6',
    'OdeToJoy:d=4,o=6,b=160:a5,a5,a#5,c,c,a#5,a5,g5,f5,f5,g5,a5,a.5,8g5,2g5,a5,a5,a#5,c,c,a#5,a5,g5,f5,f5,g5,a5,g.5,8f5,2f5,g5,g5,a5,f5,g5,8a5,8a#5,a5,f5,g5,8a5,8a#5,a5,g5,f5,g5,c5,2a5,a5,a#5,c,c,a#5,a5,g5,f5,f5,g5,a5,g.5,8f5,2f5',
    'WhoLetsT:d=16,o=5,b=125:8g6,g6,p,8g6,4g6,8g.6,p,4c6,8p,8c6,8p,8c6,p,8c6,p,8c6,p,4g6,g6,p,8g6,4g6,8g.6,p,4c6,8p,8c6,8p,8c6,p,8c6,p,8c6',
    'Brandenb:d=4,o=6,b=125:16g,16f#,8g,16d,16c,8d,16g,16f#,8g,16b5,16a5,8b5,16g,16f#,8g,16g5,16a5,8b5,8c#,16d,16c#,16d,16e,16d,16f#,16d,16g,16d,16c#,16d,16e,16d,16a,16d,16b,16d,16c#,16d,16e,16d,16c7,16d,16d7,8b,16a,16g,8a,16g,16f#,g',
    'Bourree:d=8,o=6,b=140:e,f#,4g,32p,16g,32g,32f#,e,4d#,e,f#,4b5,c#,d#,4e,d,c,4b5,a5,g5,4f#5,g5,a5,b5,a5,g5,f#5,4e5,32p,e,f#,4g,32p,16g,32g,32f#,e,4d#,e,f#,4b5,c#,d#,4e,d,c,4b5,a5,g5,32f#5,32e5,32f#5,4f#5,32p,g5,2g.5',
    'Badineri:d=16,o=6,b=125:8b,d7,b,8f#,b,f#,8d,f#,d,4b5,f#5,b5,d,b5,c#,b5,c#,b5,a#5,c#,e,c#,8d,8b5,8b,d7,b,8f#,b,f#,8d,f#,d,4b5,8d,8d,8d,8d,8b,8d,32d,32c#,32d,32c#,8c#,8f#,8f#,8f#,8f#,8d7,8f#,32f#,32f,32f#,32f,8f,c#,f#,a,f#,g#,f#,g#,f#,f,g#,b,g#,a,g#,a,g#,f#,a,f#,f,f#,b,f#,f,f#,c#7,f#,f,f#,d7,f#,f,f#,d7,c#7,b,c#7,a,g#,f#,8a,8g#,4f#',
    'ArabianN:d=16,o=6,b=63:8a#5,a#.5,c.,c#,4f.,32e,32f,8e,c#,c,c#.,c.,a#5,4f.,c#,c#.,c.,a#5,8f.,f,g#.,f.,d#,8f.,32c#,32f,e.,c#.,e,2f',
    'MammaMia:d=16,o=5,b=40:f6,d#6,f6,4d#6,d#6,d#6,f6,g6,f6,8d#.6,p,8f6,4d#6,8g#6,g#6,g#6,g#6,8g6,8d#.6,p,4a#6,a#6,a#6,8a#6,8f6,8g6,4g#6,8g6,8g6,g6,8g6,8d6,8d#6,4f6,8f6,4d#6,8g#6,g#6,g#6,g#6,g6,d#6,f6,8d#6',
    'Beethoven - Violin Concerto no1 in D:d=4,o=5,b=160:8d6,a,8d6,8f#6,8a6,8d6,a,8d6,8f#6,8a6,8g6,e6,8f#6,d6,8e6,8c#6,8c#6,32d.6,32e.6,32c#.6,32d.6,8e6,8p,8d6,a,8d6,8f#6,8a6,8d6,a,8d6,8f#6,8a6,8g6,e6,8f#6,d6,8e6,8b,8e6,8c#6,8d6,8p,8a,e6,32f#.6,32g.6,32e.6,32f#.6,8g6',
    '5th:d=4,o=5,b=125:16g,16g,16g,16d#,16g#,16g#,16g#,16g,16d#6,16d#6,16d#6,c6,16g,16g,16g,16d,16g#,16g#,16g#,16g,16f6,16f6,16f6,d6,16g6,16g6,16f6,16d#6,16d#,16d#,16f,16g,16g6,16g6,16f6,16d#6,16d#,16d#,16f,16g,16g6,16g6,16f6,8d#6,p,8c6,p,2g6',
    'FurElise:d=4,o=5,b=160:8e7,8d#7,8e7,8d#7,8e7,8b6,8d7,8c7,8a6,8e,8a,8c6,8e6,8a6,8b6,8e,8g#,8e6,8g#6,8b6,8c7,8e,8a,8e6,8e7,8d#7,8e7,8d#7,8e7,8b6,8d7,8c7,8a6,8e,8a,8c6,8e6,8a6,8b6,8e,8g#,8e6,8c7,8b6,2a6',
    'Toccata:d=4,o=5,b=125:a,16d6,16a,16e6,16a,16f6,16a,16d6,16a,16e6,16a,16f6,16a,16g6,16a,16e6,16a,16f6,16a,16g6,16a,16a6,16a,16f6,16a,16g6,16a,16a6,16a,16a#6,16a,16g6,16a,16a6,16a,16f6,16a,16g6,16a,16e6,16a,16f6,16a,16d6,16a,16e6,16a,16c#6,16a,2d6',
    'Minuet:d=4,o=5,b=160:d6,8g,8a,8b,8c6,d6,g,g,e6,8c6,8d6,8e6,8f#6,g6,g,g,c6,8d6,8c6,8b,8a,b,8c6,8b,8a,8g,f#,8g,8a,8b,8g,32b,32c,16b,16c6,16b,2a.',
    'cn3:d=4,o=5,b=125:8e6,8f#6,16e6,16d6,8e6,16d6,16c#6,8d6,16c#6,16b,16a,16d6,16a,16d6,8b,16a,16g,16f#,16d6,16f#,16d6,8g,16f#,16e,16d,16d6,16e,16d6,16f#,16d6,16g#,16d6,16a,16c#6,16a,16d6,16a,16e6,16a,16f#6,16a,16g6,16a,16a6,8f#6,16e6,16d6,8a,8c#6,d6',
    'Superman:d=4,o=6,b=200:8d5,8d5,8d5,8g.5,16p,8g5,2d,8p,8d,8e,8d,8c,1d,8p,8d5,8d5,8d5,8g.5,16p,8g5,2d,8d,8d,8e,8c,8g5,8e,2d.,p,8g5,8g5,8g5,2f#.,d.,8g5,8g5,8g5,2f#.,d.,8g5,8g5,8g5,8f#,8e,8f#,2g.,8g5,8g5,8g5,2g.5',
    'mozart:d=4,o=6,b=140:32d#.5,32d.5,32d#.5,8f#.5,32g#.5,32f#.5,32f.5,32f#.5,8a#.5,16b5,16a#5,16a5,16a#5,16f6,16d#6,16d6,16d#6,16f6,16d#6,16d6,16d#6,8f#.6,8d#6,8f#6,32c#6,32d#6,16f6,8d#6,8c#6,8d#6,32c#6,32d#6,16f6,8d#6,8c#6,8d#6,32c#6,32d#6,16f6,8d#6,8c#6,8c6,4a#5,16f5,32d#5,16d5,16d#5,4f#5,16g#5,16f#5,16f5,16f#5,4a#5,16b5,16a#5,16a5,16a#5,16f6,16d#6,16d6,16d#6,16f6,16d#6,16d6,16d#6,4f#6,8d#6,8f#6,32c#6,32d#6,16f6,8d#6,8c#6,8d#6,32c#6,32d#6,16f6,8d#6,8c#6,8d#6,32c#6,32d#6,16f6,8d#6,8c#6,8c6,4a#5,8a#5,8b5,8c#6,8c#6,16d#6,16c#6,16b5',
    'Macarena:d=4,o=5,b=180:f,8f,8f,f,8f,8f,8f,8f,8f,8f,8f,8a,8c,8c,f,8f,8f,f,8f,8f,8f,8f,8f,8f,8d,8c,p,f,8f,8f,f,8f,8f,8f,8f,8f,8f,8f,8a,p,2c.6,a,8c6,8a,8f,p,2p',
    'Godfather:d=8,o=7,b=80:e5,a5,c6,b5,a5,c6,a5,b5,a5,f5,g5,2e5,e5,e5,a5,c6,b5,a5,c6,a5,b5,a5,e5,e5,2d5,d5,d5,f5,g#5,2b5,b5,d5,f5,g#5,2a5,a5,c5',
    'countdown:d=4,o=5,b=125:p,8p,16b,16a,b,e,p,8p,16c6,16b,8c6,8b,a,p,8p,16c6,16b,c6,e,p,8p,16a,16g,8a,8g,8f#,8a,g.,16f#,16g,a.,16g,16a,8b,8a,8g,8f#,e,c6,2b.,16b,16c6,16b,16a,1b',
    'rock:d=4,o=6,b=80:32f#6,32f#6,16f#6,16f#6,16e6,16e6,16d.6,16a.5,32a5,32a5,16a5,16a5,16e6,16e6,16d.6,16b.5,32d6,32d6,16d6,16d6,16d6,16e6,16f#.6,16d.6,16g5,16g5,16g5,16g5,16g5,16f#.5,16d.6,32f#6,32f#6,16f#6,16f#6,16e6,16e6,16d.6,16a.5,16a5,16a5,16a5,16e6,16e6,16d.6,16b.5,32d6,32d6,16d6,16d6,16d6,16e6,16f#.6,16d.6,16g5,16g5,16g5,16g5,16g5,16f#.5,32d6',
    'Beethoven:d=4,o=5,b=160:c,e,c,g,c,c6,8b,8a,8g,8a,8g,8f,8e,8f,8e,8d,c,e,g,e,c6,g',
    'BarbieGirl:d=4,o=5,b=125:32e,32f#,8g#,8e,8g#,8c#6,a,8p,16p,16g#,8f#,8d#,8f#,8b,g#,8f#,8e,p,8e,8c#,f#,c#,p,8f#,8e,g#,f#,16e,16p,16e,16p,8c#4,8b4,16e,16p,16e,16p,8c#4,8b4,b,g#,e,c#4,16e,16p,16e,16p,8c#4,8b4,16e,16p,16e,16p,8c#4,8b4,8p,8c#6,8b,8c#6,8p,8c#6,8b,8c#6',
    'Never:d=4,o=5,b=200:8g,8a,8c6,8a,e6,8p,e6,8p,d6.,p,8p,8g,8a,8c6,8a,d6,8p,d6,8p,c6,8b,a.,8g,8a,8c6,8a,2c6,d6,b,a,g.,8p,g,2d6,2c6.,p,8g,8a,8c6,8a,e6,8p,e6,8p,d6.,p,8p,8g,8a,8c6,8a,2g6,b,c6.,8b,a,8g,8a,8c6,8a,2c6,d6,b,a,g.,8p,g,2d6,2c6.',
    'WeWishYo:d=4,o=6,b=35:16a5,16d6,32d6,32e6,32d6,32c#6,16b5,16g5,16b5,16e6,32e6,32f#6,32e6,32d6,16c#6,16a5,16c#6,16f#6,32f#6,32g6,32f#6,32e6,16d6,16b5,16a5,16b5,16e6,16c#6,8d6',
    'Super Mario - Main Theme:d=4,o=5,b=125:a,8f.,16c,16d,16f,16p,f,16d,16c,16p,16f,16p,16f,16p,8c6,8a.,g,16c,a,8f.,16c,16d,16f,16p,f,16d,16c,16p,16f,16p,16a#,16a,16g,2f,16p,8a.,8f.,8c,8a.,f,16g#,16f,16c,16p,8g#.,2g,8a.,8f.,8c,8a.,f,16g#,16f,8c,2c6',
    'Super Mario - Title Music:d=4,o=5,b=125:8d7,8d7,8d7,8d6,8d7,8d7,8d7,8d6,2d#7,8d7,p,32p,8d6,8b6,8b6,8b6,8d6,8b6,8b6,8b6,8d6,8b6,8b6,8b6,16b6,16c7,b6,8a6,8d6,8a6,8a6,8a6,8d6,8a6,8a6,8a6,8d6,8a6,8a6,8a6,16a6,16b6,a6,8g6,8d6,8b6,8b6,8b6,8d6,8b6,8b6,8b6,8d6,8b6,8b6,8b6,16a6,16b6,c7,e7,8d7,8d7,8d7,8d6,8c7,8c7,8c7,8f#6,2g6',
    'SMBtheme:d=4,o=5,b=100:16e6,16e6,32p,8e6,16c6,8e6,8g6,8p,8g,8p,8c6,16p,8g,16p,8e,16p,8a,8b,16a#,8a,16g.,16e6,16g6,8a6,16f6,8g6,8e6,16c6,16d6,8b,16p,8c6,16p,8g,16p,8e,16p,8a,8b,16a#,8a,16g.,16e6,16g6,8a6,16f6,8g6,8e6,16c6,16d6,8b,8p,16g6,16f#6,16f6,16d#6,16p,16e6,16p,16g#,16a,16c6,16p,16a,16c6,16d6,8p,16g6,16f#6,16f6,16d#6,16p,16e6,16p,16c7,16p,16c7,16c7,p,16g6,16f#6,16f6,16d#6,16p,16e6,16p,16g#,16a,16c6,16p,16a,16c6,16d6,8p,16d#6,8p,16d6,8p,16c6',
    'SMBwater:d=8,o=6,b=225:4d5,4e5,4f#5,4g5,4a5,4a#5,b5,b5,b5,p,b5,p,2b5,p,g5,2e.,2d#.,2e.,p,g5,a5,b5,c,d,2e.,2d#,4f,2e.,2p,p,g5,2d.,2c#.,2d.,p,g5,a5,b5,c,c#,2d.,2g5,4f,2e.,2p,p,g5,2g.,2g.,2g.,4g,4a,p,g,2f.,2f.,2f.,4f,4g,p,f,2e.,4a5,4b5,4f,e,e,4e.,b5,2c.',
    'SMBunderground:d=16,o=6,b=100:c,c5,a5,a,a#5,a#,2p,8p,c,c5,a5,a,a#5,a#,2p,8p,f5,f,d5,d,d#5,d#,2p,8p,f5,f,d5,d,d#5,d#,2p,32d#,d,32c#,c,p,d#,p,d,p,g#5,p,g5,p,c#,p,32c,f#,32f,32e,a#,32a,g#,32p,d#,b5,32p,a#5,32p,a5,g#5',
    'Picaxe:d=4,o=6,b=101:g5,c,8c,c,e,d,8c,d,8e,8d,c,8c,e,g,2a,a,g,8e,e,c,d,8c,d,8e,8d,c,8a5,a5,g5,2c',
    'The#Simpsons:d=4,o=5,b=160:c.6,e6,f#6,8a6,g.6,e6,c6,8a,8f#,8f#,8f#,2g,8p,8p,8f#,8f#,8f#,8g,a#.,8c6,8c6,8c6,c6',
    'Indiana:d=4,o=5,b=250:e,8p,8f,8g,8p,1c6,8p.,d,8p,8e,1f,p.,g,8p,8a,8b,8p,1f6,p,a,8p,8b,2c6,2d6,2e6,e,8p,8f,8g,8p,1c6,p,d6,8p,8e6,1f.6,g,8p,8g,e.6,8p,d6,8p,8g,e.6,8p,d6,8p,8g,f.6,8p,e6,8p,8d6,2c6',
    'TakeOnMe:d=4,o=4,b=160:8f#5,8f#5,8f#5,8d5,8p,8b,8p,8e5,8p,8e5,8p,8e5,8g#5,8g#5,8a5,8b5,8a5,8a5,8a5,8e5,8p,8d5,8p,8f#5,8p,8f#5,8p,8f#5,8e5,8e5,8f#5,8e5,8f#5,8f#5,8f#5,8d5,8p,8b,8p,8e5,8p,8e5,8p,8e5,8g#5,8g#5,8a5,8b5,8a5,8a5,8a5,8e5,8p,8d5,8p,8f#5,8p,8f#5,8p,8f#5,8e5,8e5',
    'Entertainer:d=4,o=5,b=140:8d,8d#,8e,c6,8e,c6,8e,2c.6,8c6,8d6,8d#6,8e6,8c6,8d6,e6,8b,d6,2c6,p,8d,8d#,8e,c6,8e,c6,8e,2c.6,8p,8a,8g,8f#,8a,8c6,e6,8d6,8c6,8a,2d6',
    'Muppets:d=4,o=5,b=250:c6,c6,a,b,8a,b,g,p,c6,c6,a,8b,8a,8p,g.,p,e,e,g,f,8e,f,8c6,8c,8d,e,8e,8e,8p,8e,g,2p,c6,c6,a,b,8a,b,g,p,c6,c6,a,8b,a,g.,p,e,e,g,f,8e,f,8c6,8c,8d,e,8e,d,8d,c',
    'Xfiles:d=4,o=5,b=125:e,b,a,b,d6,2b.,1p,e,b,a,b,e6,2b.,1p,g6,f#6,e6,d6,e6,2b.,1p,g6,f#6,e6,d6,f#6,2b.,1p,e,b,a,b,d6,2b.,1p,e,b,a,b,e6,2b.,1p,e6,2b.',
    'Looney:d=4,o=5,b=140:32p,c6,8f6,8e6,8d6,8c6,a.,8c6,8f6,8e6,8d6,8d#6,e.6,8e6,8e6,8c6,8d6,8c6,8e6,8c6,8d6,8a,8c6,8g,8a#,8a,8f',
    '20thCenFox:d=16,o=5,b=140:b,8p,b,b,2b,p,c6,32p,b,32p,c6,32p,b,32p,c6,32p,b,8p,b,b,b,32p,b,32p,b,32p,b,32p,b,32p,b,32p,b,32p,g#,32p,a,32p,b,8p,b,b,2b,4p,8e,8g#,8b,1c#6,8f#,8a,8c#6,1e6,8a,8c#6,8e6,1e6,8b,8g#,8a,2b',
    'Bond:d=4,o=5,b=80:32p,16c#6,32d#6,32d#6,16d#6,8d#6,16c#6,16c#6,16c#6,16c#6,32e6,32e6,16e6,8e6,16d#6,16d#6,16d#6,16c#6,32d#6,32d#6,16d#6,8d#6,16c#6,16c#6,16c#6,16c#6,32e6,32e6,16e6,8e6,16d#6,16d6,16c#6,16c#7,c.7,16g#6,16f#6,g#.6',
    'MASH:d=8,o=5,b=140:4a,4g,f#,g,p,f#,p,g,p,f#,p,2e.,p,f#,e,4f#,e,f#,p,e,p,4d.,p,f#,4e,d,e,p,d,p,e,p,d,p,2c#.,p,d,c#,4d,c#,d,p,e,p,4f#,p,a,p,4b,a,b,p,a,p,b,p,2a.,4p,a,b,a,4b,a,b,p,2a.,a,4f#,a,b,p,d6,p,4e.6,d6,b,p,a,p,2b',
    'StarWars:d=4,o=5,b=45:32p,32f#,32f#,32f#,8b.,8f#.6,32e6,32d#6,32c#6,8b.6,16f#.6,32e6,32d#6,32c#6,8b.6,16f#.6,32e6,32d#6,32e6,8c#.6,32f#,32f#,32f#,8b.,8f#.6,32e6,32d#6,32c#6,8b.6,16f#.6,32e6,32d#6,32c#6,8b.6,16f#.6,32e6,32d#6,32e6,8c#6',
    'GoodBad:d=4,o=5,b=56:32p,32a#,32d#6,32a#,32d#6,8a#.,16f#.,16g#.,d#,32a#,32d#6,32a#,32d#6,8a#.,16f#.,16g#.,c#6,32a#,32d#6,32a#,32d#6,8a#.,16f#.,32f.,32d#.,c#,32a#,32d#6,32a#,32d#6,8a#.,16g#.,d#',
    'TopGun:d=4,o=4,b=31:32p,16c#,16g#,16g#,32f#,32f,32f#,32f,16d#,16d#,32c#,32d#,16f,32d#,32f,16f#,32f,32c#,16f,d#,16c#,16g#,16g#,32f#,32f,32f#,32f,16d#,16d#,32c#,32d#,16f,32d#,32f,16f#,32f,32c#,g#',
    'A-Team:d=8,o=5,b=125:4d#6,a#,2d#6,16p,g#,4a#,4d#.,p,16g,16a#,d#6,a#,f6,2d#6,16p,c#.6,16c6,16a#,g#.,2a#',
    'Flinstones:d=4,o=5,b=40:32p,16f6,16a#,16a#6,32g6,16f6,16a#.,16f6,32d#6,32d6,32d6,32d#6,32f6,16a#,16c6,d6,16f6,16a#.,16a#6,32g6,16f6,16a#.,32f6,32f6,32d#6,32d6,32d6,32d#6,32f6,16a#,16c6,a#,16a6,16d.6,16a#6,32a6,32a6,32g6,32f#6,32a6,8g6,16g6,16c.6,32a6,32a6,32g6,32g6,32f6,32e6,32g6,8f6,16f6,16a#.,16a#6,32g6,16f6,16a#.,16f6,32d#6,32d6,32d6,32d#6,32f6,16a#,16c.6,32d6,32d#6,32f6,16a#,16c.6,32d6,32d#6,32f6,16a#6,16c7,8a#.6',
    'Jeopardy:d=4,o=6,b=125:c,f,c,f5,c,f,2c,c,f,c,f,a.,8g,8f,8e,8d,8c#,c,f,c,f5,c,f,2c,f.,8d,c,a#5,a5,g5,f5,p,d#,g#,d#,g#5,d#,g#,2d#,d#,g#,d#,g#,c.7,8a#,8g#,8g,8f,8e,d#,g#,d#,g#5,d#,g#,2d#,g#.,8f,d#,c#,c,p,a#5,p,g#.5,d#,g#',
    'Gadget:d=16,o=5,b=50:32d#,32f,32f#,32g#,a#,f#,a,f,g#,f#,32d#,32f,32f#,32g#,a#,d#6,4d6,32d#,32f,32f#,32g#,a#,f#,a,f,g#,f#,8d#',
    'Smurfs:d=32,o=5,b=200:4c#6,16p,4f#6,p,16c#6,p,8d#6,p,8b,p,4g#,16p,4c#6,p,16a#,p,8f#,p,8a#,p,4g#,4p,g#,p,a#,p,b,p,c6,p,4c#6,16p,4f#6,p,16c#6,p,8d#6,p,8b,p,4g#,16p,4c#6,p,16a#,p,8b,p,8f,p,4f#',
    'MahnaMahna:d=16,o=6,b=125:c#,c.,b5,8a#.5,8f.,4g#,a#,g.,4d#,8p,c#,c.,b5,8a#.5,8f.,g#.,8a#.,4g,8p,c#,c.,b5,8a#.5,8f.,4g#,f,g.,8d#.,f,g.,8d#.,f,8g,8d#.,f,8g,d#,8c,a#5,8d#.,8d#.,4d#,8d#.',
    'LeisureSuit:d=16,o=6,b=56:f.5,f#.5,g.5,g#5,32a#5,f5,g#.5,a#.5,32f5,g#5,32a#5,g#5,8c#.,a#5,32c#,a5,a#.5,c#.,32a5,a#5,32c#,d#,8e,c#.,f.,f.,f.,f.,f,32e,d#,8d,a#.5,e,32f,e,32f,c#,d#.,c#',
    'MissionImp:d=16,o=6,b=95:32d,32d#,32d,32d#,32d,32d#,32d,32d#,32d,32d,32d#,32e,32f,32f#,32g,g,8p,g,8p,a#,p,c7,p,g,8p,g,8p,f,p,f#,p,g,8p,g,8p,a#,p,c7,p,g,8p,g,8p,f,p,f#,p,a#,g,2d,32p,a#,g,2c#,32p,a#,g,2c,a#5,8c,2p,32p,a#5,g5,2f#,32p,a#5,g5,2f,32p,a#5,g5,2e,d#,8d',
    'Wii_Fit_Ob:d=4,o=5,b=149:1p,g,512p,g6,512p,7f6,15e.6,256p,7d6,15c.6,256p,7d6,e6,512p,g.,256p,7a,15c.6,p,g.6,15g.6,256p,7a6,15g.6,256p,28a6,512p,10a#6,128p,a6,512p,g.6,p,a6,512p,c6,512p,7c6,15c.6,256p,7d6,d#6,512p,g#6,512p,d#6,512p,d6,512p,15c.6,256p,e6,512p,g6,512p,g6,512p,7a6,15g.6,256p,7a#6,a6,512p,15g.6,2p,7a6,15c.7,256p,7d7,15c.7,256p,7d#7,d7,512p,15c.7,256p,d7,512p,7f#6,g6,512p,15g.6,256p,7a6,15c.7',
    'Dryer_Song:d=4,o=5,b=70:8c#.6,16f#6,16f6,16d#6,8c#.6,8a#.,16b,16c#6,16d#6,16g#,16a#,16b,8a#.,8c#.6,8c#.6,16f#6,16f6,16d#6,8c#.6,8f#.6,16f#6,16g#6,16f#6,16f6,16d#6,16f6,8f#.6',
    'tetris:d=4,o=5,b=160:e6,8b,8c6,8d6,16e6,16d6,8c6,8b,a,8a,8c6,e6,8d6,8c6,b,8b,8c6,d6,e6,c6,a,2a,8p,d6,8f6,a6,8g6,8f6,e6,8e6,8c6,e6,8d6,8c6,b,8b,8c6,d6,e6,c6,a,a',
    'One:d=4,o=5,b=120:2f6,38p,g6,74p,8g#6,137p,g6,74p,8f6,137p,f6,74p,e6,74p,f6,74p,2f6,38p,g6,74p,8g#6,137p,a#6,74p,8f6,137p,f6,74p,e6,74p,f6,74p,2c7,38p,a#6,74p,8g#6,137p,g6,74p,17g#.6,192p,8g.6,101p,g6,77p,17g#.6,175p,8g.6,96p,17g6,240p,g6,74p,8f6,137p,2f6',
]

def playAll():
    for song in SONGS:
        print(song)
        play(song)

def play0(song):
    rtttl.play(find(song))

def ls():
    for song in SONGS:
        song_name = song.split(':')[0]
        print(song_name)

def find(name):
    for song in SONGS:
        song_name = song.split(':')[0]
        if song_name == name:
            return song

playAll()