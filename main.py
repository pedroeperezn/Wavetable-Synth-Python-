# Pedro E. Perez Navarro - Recreating Daisy Bell with python
import numpy as np
import scipy.io.wavfile as wav

WAVETABLE_LENGTH = 64
SAMPLE_RATE = 44100

def apply_fades(signal, fade_length = 5000):
    """
    Apply fade in and fade out to a signal with a fixed length of 5000 samples.
    :param signal: Signal to apply fades to.
    :param fade_length: Length of the fade in samples.
    :return: Processed signal.
    """
    # Generate fade cosine wave that represents our fade
    fade_in = (1 - np.cos(np.linspace(0, np.pi, fade_length))) * 0.5
    # Flip fade in for fade out
    fade_out = np.flip(fade_in)
 
    # Apply fade-in by multiplying the fade waves to the first and last samples (according to length)
    signal[:fade_length] = np.multiply(fade_in, signal[:fade_length])
    signal[-fade_length:] = np.multiply(fade_out, signal[-fade_length:])

    # Return processed signal
    return signal
def interpolate(wavetable, index):
    """
    Generates an interpolated value between the fixed values of the wavetable to smooth the signal.
    :param wavetable: Wavetable from which we are getting the values to interpolate. 
    :param index: Index in which we are interpolating
    :return: Interpolated value
    """
    # Truncate the index to the neares integer and found the next rounded integer
    truncated_index = int(np.floor(index))
    next_index = (truncated_index + 1) % wavetable.shape[0]

    # Get the diference in value from the truncated indexes and the actual index value 
    next_index_weight = index - truncated_index
    truncated_index_weigth = 1 - next_index_weight

    # Returned a value that lies between the truncated index and the next index that is proportional in distance
    return truncated_index_weigth * wavetable[truncated_index] + next_index_weight * wavetable[next_index]

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
        output[n] = interpolate(wavetable, index)
        # Increment the index
        index += index_increment
        # Make sure the next index we will use is within our wavetable's bounds
        index %= len(wavetable)

    # Return teh populated numpy arrays with values that represent a sound wave. It can be translated to a wav file
    return output

def sawtooth(x):
    """
    We can use this function to use a sawtooth waveform instead of a sine wave
    :returns a sample of a sawtooth wave
    :param x: sample
    :return: processed sample
    """
    return (x + np.pi) / np.pi % 2 -1
def main():
    # Declare the final array in which the sound will be, the frequencies to reproduce and the duration of the frequencies
    complex_output = []
    # Daisy Bell's Chorus notes and duration of each note
    frequencies_and_duration = [
        (587.33,1.5), (493.88,1.5),
        (392,1.5), (293.66,1.5),
        (326.63,0.5),(369.99,0.5),(392,0.5),
        (326.63, 1),(392,0.5),(293.66,3),
        (440,1.5),(587.33,1.5),(493.88,1.5),(392,1.5),
        (329.63,0.5),(369.99,0.5),(392,0.5), (440, 1),
        (493.88,0.5),(440,3)
    ]

    # For each frequency, generate it's wavetable and their numpy array that represents the audio file. 
    # Then, concatenate each numpy array to generate a final audio file
    for frequency, duration in frequencies_and_duration:
        wavetable = generate_wavetable(frequency, duration)
        output = generate_output(wavetable, frequency, duration)
        output = apply_fades(output)
        complex_output = np.concatenate((complex_output, output))

    # Modify amplitude to avoid clipping
    gain = -20
    amplitude = 10 ** (gain / 20)
    complex_output *= amplitude
    # Apply fades to our sound file
    complex_output = apply_fades(complex_output)
    # Write sound file
    wav.write('test.wav', SAMPLE_RATE, complex_output.astype(np.float32))


if __name__ == '__main__': 
    main()