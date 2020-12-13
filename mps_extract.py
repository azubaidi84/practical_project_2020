#!/usr/bin/env python
# coding: utf-8


'''
Author: Janne Nold 

    
MPS Feature Extractor
********************

This is a function to extract the Modulation Power Spectrum based on the MEL Spectrogram with a 2D Fourier Transform from wav files. 
The output is stored in BIDS format. 

'''

import numpy as np
import matplotlib.pyplot as plt
import librosa as lbr
import json
import os
import warnings            
import pandas as pd 
import librosa.display 

def mps_extract(filename, sr = 44100, n_fft = 512, hop_length = 512, mps_n_fft = 500, 
                mps_hop_length = 500, plot_mps = False, **kwargs)

               
'''                
Input

filename:       str, path to wav files to be converted
sr:             int, sampling rate for wav file (Default: 44100 Hz)
n_fft:          int, window size for mel spectrogram extraction (Default: 512)
hop_length:     int, step size for mel spectrogram extraction (Default: 512)
mps_n_fft:      int, window size for mps extraction (Default: 500)
mps_hop_length: int, step size for mps extraction (Default: 500)
plot_mps:       bool, if true the Mel spectrogram for the first window and according mps will be plotted (Default: False)
kwargs:         additional keyword arguments that will be transferred to librosa's melspectrogram function

Output

tuple of a feature representation (2-dimensional array: samples x feature)
repitition time in seconds
names of all features (list of strings of mod/s for each mod/Hz)        

'''

# Extracting wav files from directory
wav, _ = lbr.load(filename, sr=sr) 
# filename = '/data/fg_audio/*.wav'

# Extracting Mel spectrogram
mel_spec = lbr.feature.melspectrogram(y=wav, sr=sr, hop_length=hop_length,
                                              **kwargs)
# Transposing Mel Spectrogram
mel_spec = mel_spec.T

# Checking Input parameters
if mps_n_fft >= mel_spec.shape[0]:
    raise ValueError("The mps window size exceeds the Mel spectrogram. Please enter a smaller integer.")

if mps_hop_length >= mel_spec.shape[0]:
    raise ValueError("The mps step size exceeds the Mel spectrogram. Please enter a smaller integer.")


# Extracting mps
mps_all = []
mps_plot = []
nyquist_mps = int(np.ceil(mel_spec.shape[1]/2))


for i in range(1,101):
    
    #Extract mps for predefined window
    mps = np.fft.fft2(mel_spec[mps_n_fft*(i-1):mps_n_fft*i,:])
   
    # use absoulte and shifted frequencies
    mps = np.abs(np.fft.fftshift(mps))
    
    # Define variable for later plotting
    mps_plot.append(mps)
   
    # Flattening the mps to a vector
    mps = np.reshape(mps,(1,np.size(mps)))
    
    # Append mps to mps all
    mps_all.append(mps)
    
# Convert mps_all into an array outside the loop
mps_all = np.array(mps_all)

# Convert mps_plot into an array outside loop
mps_plot = np.array(mps_plot)

# Concatinating the MPS row-wise
mps_all = np.concatenate(mps_all)
    


# Sampling Rate in Mel Spectrogram
fs_spectrogram = sr/hop_length

# Sampling rate in MPS how many mps per second
fs_mps = fs_spectrogram/mps_hop_length

 
# Extract Axis units for plotting 
# Calculate step sizes for MPS
freq_step_log = np.log(mel_spec[1,:])
freq_step_log = freq_step_log[1] - freq_step_log[0]


# Calculate labels for X and Y axes
mps_freqs = np.fft.fftshift(np.fft.fftfreq(mel_spec.shape[1], d = freq_step_log)) 
mps_times = np.fft.fftshift(np.fft.fftfreq(mps_n_fft, d = 1. /fs_spectrogram)) 


# PLot Spectrogram and MPS for first window alongside each other
if plot_mps = True: 
    
    fig, (ax1,ax2)= plt.subplots(1, 2, figsize=(20, 10))

    first_mel = mel_spec[0:mps_n_fft,:]
    time = np.arange(0,mps_n_fft)*fs_spectrogram
    frequency = np.arange(0,mel_spec.shape[1])*(1/fs_mps)

    image = ax1.imshow(first_mel.T, origin = 'lower', aspect = 'auto')

    ax1.set_xticks(np.arange(0,mps_n_fft,50))
    ax1.set_yticks(np.arange(0,first_mel.shape[1],10))

    x1 = ax1.get_xticks()
    y1 = ax1.get_yticks()

    ax1.set_xticklabels(['{:.0f}'.format(xtick) for xtick in time[x1]])
    ax1.set_yticklabels(['{:.2f}'.format(ytick) for ytick in frequency[y1]])
     
    ax1.set_title('Mel Spectrogram 1st window')
    ax1.set_ylabel('Frequencyband (Hz)')
    ax1.set_xlabel('Time (s)')
    cbar = fig.colorbar(image, ax = ax1, format='%+2.0f dB')
    cbar.set_label('dB')

    img = ax2.imshow(np.log(mps_plot[0,:,nyquist_mps:].T), origin = 'lower', aspect = 'auto')

    mps_freqs2 = mps_freqs[nyquist_mps:,]

    ax2.set_xticks(np.arange(0,len(mps_times),50))
    ax2.set_yticks(np.arange(0,len(mps_freqs2),10))

    x2 = ax2.get_xticks()
    y2 = ax2.get_yticks()

    ax2.set_xticklabels(['{:.0f}'.format(xtick2) for xtick2 in mps_times[x2]])
    ax2.set_yticklabels(['{:.2f}'.format(ytick2) for ytick2 in mps_freqs2[y2]])
     
    ax2.set_title(' MPS for Mel Spectrogram (1st window)')
    ax2.set_xlabel('Temporal Modulation (mod/s)')
    ax2.set_ylabel('Spectral Modulation (cyc/oct)')
    cbar = fig.colorbar(img, ax=ax2)
    cbar.set_label('(log) MPS')


    
# Extracting feature names                     
names_features = ['{0:.2f} mod/s {1:.2f} cyc/oct)'.format(mps_time, mps_freq) 
                  for mps_time in mps_times for mps_freq in mps_freqs]

# Determine MPS repitition time 
mps_rep_time = 1/fs_mps
            
                     
return mps_all, mps_rep_time, names_features

 

