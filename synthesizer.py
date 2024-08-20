import numpy as np
import utilities

WAVETABLE_LENGTH = 64
SAMPLE_RATE = 44100
def generate_wavetable(frequency, duration):
    """
    Generates the wavetable given a frequency and duration.
    :param frequency: In Hz
    :param duration: In seconds
    :return: Wavetable for the requested frequency.
    """
    # Specify waveform (it can be either sin wave or sawtooth
    waveform = np.sin
    # Generate a numpy array with 0s with a length of our constant wavetable length
    wave_table = np.zeros(WAVETABLE_LENGTH)

    # Populate the wavetable with values according to one cycle of the sine wave of the requested frequency
    for n in range(WAVETABLE_LENGTH):
        wave_table[n] = waveform(2 * np.pi * n / WAVETABLE_LENGTH)

    # Return the wavetable
    return wave_table

def generate_output(wavetable, frequency, duration):
    """
    Generates a numpy array with numerical values that will reproduce the requested frequency given the wavetable and
    duration of the sound
    :param wavetable: wavetable of the frequency to generate
    :param frequency: frequency to generate
    :param duration: duration of the sound
    :return: Numpy array that represents the audio output of the requested frequency.
    """
    # Generate a numpy array with 0s depending on the duration of the audio in seconds and a constant sample rate
    output = np.zeros(int(duration * SAMPLE_RATE))

    # Keeps track of the index and index increment we will use to compute the values of each sample
    index = 0
    index_increment = frequency * len(wavetable)/SAMPLE_RATE

    # Assign one value of the wave for each sample of our empty audio file
    for n in range(output.shape[0]):
        # Assign an interpolated value to each sample
        output[n] = utilities.interpolate(wavetable, index)
        # Increment the index
        index += index_increment
        # Make sure the next index we will use is within our wavetable's bounds
        index %= len(wavetable)

    # Return teh populated numpy arrays with values that represent a sound wave. It can be translated to a wav file
    return output