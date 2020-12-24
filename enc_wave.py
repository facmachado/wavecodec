#!/usr/bin/python3

#
#  Copyright (c) 2020 Flavio Augusto (@facmachado)
#
#  This software may be modified and distributed under the terms
#  of the MIT license. See the LICENSE file for details.
#

import sys, wave, numpy

MAX = 32767
DUR = 0.5
RATE = 8000
FREQS = [
    880.0, 2093.004, 987.7666, 1864.655,       # A5, C7, B5, A#6/Bb6
    1108.7306, 1661.2188, 1244.508, 1479.9776, # C#6/Db6, G#6/Ab6, D#6/Eb6, F#6/Gb6
    1396.913, 1318.5102, 1567.9818, 1174.659,  # F6, E6, G6, D6
    1760.0, 1046.5022, 1975.5332, 932.3276     # A6, C6, B6, A#5/Bb5
]

def input_data(input):
    with open(input, 'rb') as f:
        r = []
        while True:
            byte = f.read(1)
            if not byte:
                break
            else:
                l = ['{:02x}'.format(b) for b in byte]
                for h in l:
                    m = [int(d, 16) for d in h]
                    r.extend(m)
    return r

def sine_wave(rate, freq, dur):
    t = numpy.linspace(0, dur, int(dur * rate), False)
    w = numpy.int16(numpy.sin(2 * numpy.pi * freq * t) * MAX)
    return w

def prepare_audio(input):
    r = input_data(input)
    s = numpy.empty(0, 'b')
    for i in r:
        w = sine_wave(RATE, FREQS[i], DUR)
        s = numpy.append(s, w)
    s = numpy.int16(s)
    return s

    # l = len(w)
    # n = [str(b) for b in '{:04b}'.format(i)]
    # for j in n:
    # d = numpy.append(numpy.empty(0, 'b'), numpy.full(int(l / 4), (1 if int(j) == 1 else -1) * MAX))
    # s = numpy.resize(s, int(RATE * len(r)))

def output_audio(input, output):
    s = prepare_audio(input)
    g = wave.open(output, 'wb')
    g.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
    g.writeframes(s)
    g.close()

output_audio(sys.argv[1], sys.argv[2])
