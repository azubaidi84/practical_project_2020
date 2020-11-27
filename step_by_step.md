# MPS Feature Extractor
***

### This is a function to extract the Modulation Power Spectrum based on the MEL Spectrogram with a 2D Fourier Transform from wav files. 
***

The output is stored in BIDS format. 



```python
def mps_extract(filename, sr = 44100, n_fft, hop_length = 512, mps_n_fft, 
                mps_hop_length = mps_n_fft, plot_mps = True, **kwargs) 
```
    


### Input

- filename:        str, path to wav files to be converted
- output path:?
- sr:              int, sampling rate for wav file (*Default*: 44100 Hz)
- n_fft:           int, window size for mel spectrogram extraction
- hop_length:      int, step size for mel spectrogram extraction
- mps_n_fft:       int, window size for mps extraction
- mps_hop_length:  int, step size for mps extraction (*Default*: mps_hop_length = mps_n_fft)
- plot_mps:        bool, if true mps will be plotted (*Default*: True)
- kwargs:          additional keyword arguments that will be transferred to librosa's melspectrogram function

### Output

- tuple of a feature representation (2-dimensional array: samples x feature)
- repitition time in seconds 
- names of all features (list of strings of mod/s for each mod/Hz)
   

**Load Packages**


```python
import numpy as np
import matplotlib.pyplot as plt
import librosa as lbr
import json
import os
import warnings            
import pandas as pd 
```

**Step 1.**

Extract wav files from directory


```python
wav, _ = lbr.load(filename, sr=sr) 
```

**Step 2.**

Extract MEL Spectogram from wav files


```python
mel_spec = lbr.feature.melspectrogram(y=wav, sr=sr, hop_length=hop_length,
                                              **kwargs)
```

**Step 3.**

Check input parameters


```python
if mps_n_fft >= mel_spec.shape[1]
    raise ValueError("The mps window size exceeds the Mel spectrogram. Please enter a smaller integer.")

if mps_hop_length >= mel_spec.shape[1]
    raise ValueError("The mps step size exceeds the Mel spectrogram. Please enter a smaller integer.")
```

**Step 4.**

Extract MPS by looping through spectrogram with pre-set window size (mps_n_fft) and pre-set hop_length (mps_hop_length). Also extracting the Nyquist Frequency. mps_all will be converted to a numpy array. 


```python
mps_all = []
start = range(0,mel_spec.shape[1]//mps_n_fft)
nyquist_mps = np.ceil(mel_spec.shape[0]/2)


for i in range(1,101)
    
    mps = fft2(mel_spec[:,mps_n_fft*start:mps_n_fft*i])
    
    # Flattening the mps to a vector
    mps = np.reshape(mps,(1,np.size(mps)) 
    
    mps_all.append(np.abs(fftshift(mps)))
    
    
 np.array(mps_all)
    
    
    

```

**Step 5.**

Plot MPS 



```python
# Extract Axis units for plotting 

# Calculate axes step sizes for MEL spectrogram
sinal_sec = n_fft/sr
mel_Hz_s = sr/n_fft # step size for MEL spectrogram Hz/sample (fundamental frequency)
mel_time_s = hop_length/sr # step size for MEL spectrogram sec/sample 

# Calculate step sizes for MPS
mod_per_s = mps_hop_length*mel_time_s
mod_per_oct = 

# Calculate labels for X and Y axes
mps_times = fftshift(fftfreq(0:mps_n_fft)
mps_freqs = fftshift(fftfreq(mel_spec.shape[0],))

if plot_mps
fig, ax = plt.subplot()




```

**Step 6.**

Extract names of the features in the MPS


```python
 freqs = ['{0:.0f} Hz ({1}Mel)'.format(freq, log_dict[log]) for freq in freqs]
```

**Step 7.**

Determine the repitition time between two mps.


```python
return mps_all, mps_rep_time, names_features
```
