import pyaudio
import wave
import struct
import sys
import random
from numpy.random import Generator, MT19937, SeedSequence
import simpleaudio as sa

#----------------------------------------------------------------------------------
CHUNK = 1024
FORMAT = pyaudio.paInt16 
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = ""
RANDOM_OUTPUT_FILENAME = ""
RANDOM_2_OUTPUT_FILENAME = ""
GAUSSE = ""
GAUSSE_v2 = ""
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("*** recording ***")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
#----------------------------------------------------------------------------------
wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
binary_data = wf.readframes(wf.getnframes())    #
gaus = open(GAUSSE, "a+")
a = []
masks=255
print(binary_data[0:50])
for i in range (100000):
    a.append(int.from_bytes(binary_data[15000+i:15002+i], byteorder="big") & masks)
    b=(int.from_bytes(binary_data[15000+i:15002+i], byteorder="big") & masks)
    gaus.write(str(i) + ". " + str(int(b)) + "\n")
wf.close()
gaus.close()
counter = []
gaus_v2 = open(GAUSSE_v2, "a+")
for i in range (256):
    c = a.count(i)
    gaus_v2.write(str(i) + ". " + str(int(c)) + "\n")
    counter.append(c)
#counter.sort()
print(counter)
#----------------------------------------------------------------------------------
wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
binary_data = wf.readframes(wf.getnframes())
bity = open("bity.txt","a+")
bity.write(str(binary_data))
bity.close()

#----------------------------------------------------------------------------------

wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
binary_data = wf.readframes(wf.getnframes())

#print(binary_data[15000:15001])
a = int.from_bytes(binary_data[15000:15025], byteorder="big")
mask = 255
seed = int(a) & mask
print("seed= "+ str(seed))
wf.close()
random.seed(seed)


#print (random.randint(0,255))       #'''build in MT function'''

'''

rand_1=open(RANDOM_OUTPUT_FILENAME, "a+")
for i in range(100000):
    number =random.randint(0,255)
    rand_1.write(str(i)+". "+ str(number)+"\n")
rand_1.close()
'''
#----------------------------------------------------------------------------------

#''' generator '''------------------------------------------------------------------------------------

r = 31
m = 397
n = 624
w = 32
a = 0x9908B0DF
u = 11
d = 0xFFFFFFFF
s = 7
b = 0x9D2C5680
t = 15
c = 0xEFC60000
l = 18
f = 1812433253

my_number = [0 for i in range(n)]
index = n+1
lower_mask = 0x7FFFFFFF
upper_mask = 0x80000000


def seed(seed):

    my_number[0] = seed
    for i in range(1, n):
        temp = f * (my_number[i-1] ^ (my_number[i-1] >> (w-2))) + i
        my_number[i] = temp & 0xffffffff       #zmiana z 8 bitów na 32 w zależności od długości maski



def get_number():
    global index
    if index >= n:
        mix()
        index = 0

    y = my_number[index]
    y = y ^ (y >> u)
    y = y ^ ((y << t) & c)
    y = y ^ ((y << s) & b)
    y = y ^ (y >> l)

    index += 1
    return y & 0xffffffff       #zmiana z 8 bitów na 32 w zależności od długości maski


def mix():
    for i in range(0, n):
        x = (my_number[i] & upper_mask) + (my_number[(i+1) % n] & lower_mask)
        x_bit = x >> 1
        if (x % 2) != 0:
            x_bit = x_bit ^ a
        my_number[i] = my_number[(i + m) % n] ^ x_bit


#''' generator '''------------------------------------------------------------------------------------
seed(seed)
number = []
number_2 = 0

rand_1 = open(RANDOM_2_OUTPUT_FILENAME, "a+")
for i in range(100000):
    number.append(get_number())
    number_2 = get_number()
    rand_1.write(str(i) + ". " + str(number_2)+"\n")
rand_1.close()
print("done")

