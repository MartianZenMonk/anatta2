#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""
import argparse
import math
import time
import numpy as np

usage_line = ' press <enter> to quit '


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-l', '--list-devices', action='store_true',
                    help='list audio devices and exit')
parser.add_argument('-b', '--block-duration', type=float,
                    metavar='DURATION', default=50,
                    help='block size (default %(default)s milliseconds)')
parser.add_argument('-c', '--columns', type=int, default=80,
                    help='width of spectrogram')
parser.add_argument('-d', '--device', type=int_or_str,
                    help='input device (numeric ID or substring)')
parser.add_argument('-g', '--gain', type=float, default=10,
                    help='initial gain factor (default %(default)s)')
parser.add_argument('-r', '--range', type=float, nargs=2,
                    metavar=('LOW', 'HIGH'), default=[100, 2000],
                    help='frequency range (default %(default)s Hz)')

args = parser.parse_args()

global clap
clap = False
args.columns = 80

low, high = args.range
if high <= low:
    parser.error('HIGH must be greater than LOW')


try:
    import sounddevice as sd

    sd._terminate()
    time.sleep(10)
    sd._initialize()
    sd.default.latency = 'low'

    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)

    samplerate = sd.query_devices(args.device, 'input')['default_samplerate']

    delta_f = (high - low) / (args.columns - 1)
    fftsize = math.ceil(samplerate / delta_f)
    low_bin = math.floor(low / delta_f)

    def callback(indata, frames, time, status):
        global clap
        if any(indata):
            magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
            magnitude *= args.gain / fftsize
            print(sum(magnitude[low_bin:low_bin + args.columns]))
            if sum(magnitude[low_bin:low_bin + args.columns])>20:
                clap = True
                print("clap detect")
            else:
                pass
                
        else:
            print('no input')

    args.device = 0
    # print(samplerate)
    args.block_duration = 50

    with sd.InputStream(device=args.device, channels=1, callback=callback,
                        blocksize=int(samplerate * args.block_duration / 1000),
                        samplerate=samplerate):

        while True:
            if clap:
                sd._terminate()
                time.sleep(5)
                break
            
except KeyboardInterrupt:
    parser.exit('Interrupted by user')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))