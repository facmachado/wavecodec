#!/usr/bin/python3

#
#  Copyright (c) 2020 Flavio Augusto (@facmachado)
#
#  This software may be modified and distributed under the terms
#  of the MIT license. See the LICENSE file for details.
#

import sys, wave, numpy

MAX = 32767
DUR = 0.05
RATE = 8000
FREQS = [
    440.0, 1046.502, 493.8833, 932.3275,    # A4, C6, B4, A#5/Bb5
    554.3653, 830.6094, 622.254, 739.9888,  # C#5/Db5, G#5/Ab5, D#5/Eb5, F#5/Gb5
    698.4565, 659.2551, 783.9909, 587.3295, # F5, E5, G5, D5
    880.0, 523.2511, 987.7666, 466.1638     # A5, C5, B5, A#4/Bb4
]

def input_data(input):
    with open(input, 'rb') as f:
        r = []
        while True:
            d = f.read(1)
            if not d:
                break
            else:
                r.append(d)
    return r

def sine_wave(rate, freq, dur):
    t = numpy.linspace(0, dur, int(dur * rate), False)
    w = numpy.int16(numpy.sin(2 * numpy.pi * freq * t) * MAX)
    return w

def prepare_audio(input):
    r = input_data(input)
    s = numpy.empty(0, 'b')
    for i in r:
        w = sine_wave(RATE, FREQS[int(i, 16)], DUR)
        s = numpy.append(s, w)
    s = numpy.int16(s)
    return s

def output_audio(input, output):
    s = prepare_audio(input)
    g = wave.open(output, 'wb')
    g.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
    g.writeframes(s)
    g.close()

output_audio(sys.argv[1], sys.argv[2])
