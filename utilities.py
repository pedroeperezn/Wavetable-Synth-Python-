import numpy as np

DAISY_BELL_FREQ_AND_DURATIONS = [
    (587.33,1.5), (493.88,1.5),
    (392,1.5), (293.66,1.5),
    (326.63,0.5),(369.99,0.5),(392,0.5),
    (326.63, 1),(392,0.5),(293.66,3),
    (440,1.5),(587.33,1.5),(493.88,1.5),(392,1.5),
    (329.63,0.5),(369.99,0.5),(392,0.5), (440, 1),
    (493.88,0.5),(440,3)
]

def normalize_gain(signal):
    # Modify amplitude to avoid clipping
    gain = -20
    amplitude = 10 ** (gain / 20)
    return (signal * amplitude)

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
def sawtooth(x):
    """
    We can use this function to use a sawtooth waveform instead of a sine wave
    :returns a sample of a sawtooth wave
    :param x: sample
    :return: processed sample
    """
    return (x + np.pi) / np.pi % 2 -1

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