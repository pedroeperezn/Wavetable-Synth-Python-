# Pedro E. Perez Navarro - Recreating Daisy Bell with python
import numpy as np
import scipy.io.wavfile as wav
import utilities
import synthesizer

WAVETABLE_LENGTH = 64
SAMPLE_RATE = 44100

def main():
    # Declare the final array in which the sound will be, the frequencies to reproduce and the duration of the frequencies
    all_samples = []
    # Daisy Bell's Chorus notes and duration of each note
    frequencies_and_duration = utilities.DAISY_BELL_FREQ_AND_DURATIONS
    
    # For each frequency, generate it's wavetable and their numpy array that represents the audio file. 
    # Then, concatenate each numpy array to generate a final audio file
    for frequency, duration in frequencies_and_duration:
        wavetable = synthesizer.generate_wavetable(frequency, duration)
        output = synthesizer.generate_output(wavetable, frequency, duration)
        output = utilities.apply_fades(output)
        all_samples = np.concatenate((all_samples, output))

    # Modify amplitude to avoid clipping
    all_samples = utilities.normalize_gain(all_samples)
    # Apply fades to our sound file
    all_samples = utilities.apply_fades(all_samples)
    # Write sound file
    wav.write('daisy_bell.wav', SAMPLE_RATE, all_samples.astype(np.float32))


if __name__ == '__main__': 
    main()