# practical_project_2020
The code was created as part of a Practical Project at the University of Oldenburg in 2020 under supervision of Moritz Boos and Dr. Arkan Al-Zubaidi. 

This function extracts the Modulation Power Spectrum from an auditory stimulus in a BIDS compliant format.
The function is based on the MEL spectrogram and the 2D Fourier Transform. 

Use with 

# Usage
<pre> 
usage: mps_extract.py 

positional arguments:
-------
  filename :      str, path to wav files to be converted. Can be used with wildcard * .wav. 

keyword arguments:
------
  sr:             int, sampling rate (Hz) of auditory files (set to 44100 Hz by default)
  n_fft:          int, window length of spectrogram
  mps_n_fft:      int, window length for extracting the MPS
  hop_length:     int, step size for extracting MEL spectrogram 
  mps_hop_length: int, step size for extracting MPS (set to mps_n_fft by default for non-overlapping windows)
  
  
optional arguments:
------


</pre>

# Output

The function returns three outputs:

1. a representation of a feature matrix of shape (sample x feature)
2. the reptition time in seconds (int)
3. the names of the features (as string)

**Optional**

The function can return the plotted MPS. By default, this is set to False and has to be indicated if needed otherwise.

