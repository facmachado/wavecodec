#!/usr/bin/python3

#
#  Copyright (c) 2020 Flavio Augusto (@facmachado)
#
#  This software may be modified and distributed under the terms
#  of the MIT license. See the LICENSE file for details.
#

import sys, wave, numpy

MAX = 32767
DUR = 0.0125
RATE = 8000
FREQ = 523.2511 # C5

def input_data(input):
    with open(input, 'rb') as f:
        r = []
        while True:
            b = f.read(1)
            if not b:
                break
            else:
                r.append(1 if int(b) == 1 else -1)
    return r

def sine_wave(rate, freq, dur):
    t = numpy.linspace(0, dur, int(dur * rate), False)
    w = numpy.int16(numpy.sin(2 * numpy.pi * freq * t) * MAX)
    return w

def prepare_audio(input):
    r = input_data(input)
    w = sine_wave(RATE, FREQ, DUR)
    s = numpy.empty(0, 'b')
    l = len(w)
    for i in r:
        # s = numpy.append(s, w if i == 1 else numpy.full(l, 0))
        s = numpy.append(s, numpy.full(l, i * MAX))
    s = numpy.int16(s)
    return s

def output_audio(input, output):
    s = prepare_audio(input)
    g = wave.open(output, 'wb')
    g.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
    g.writeframes(s)
    g.close()

output_audio(sys.argv[1], sys.argv[2])
