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


def mps_extract(filename, sr = 44100, n_fft = 512, hop_length = 512, mps_n_fft = 500, 
                mps_hop_length = 500, plot_mps = False, **kwargs)

               
'''                
Input

filename:       str, path to wav files to be converted
sr:             int, sampling rate for wav file (Default: 44100 Hz)
n_fft:          int, window size for mel spectrogram extraction
hop_length:     int, step size for mel spectrogram extraction
mps_n_fft:      int, window size for mps extraction
mps_hop_length: int, step size for mps extraction (Default: mps_hop_length = mps_n_fft)
plot_mps:       bool, if true mps will be plotted (Default: True)
kwargs:         additional keyword arguments that will be transferred to librosa's melspectrogram function

Output

tuple of a feature representation (2-dimensional array: samples x feature)
repitition time in seconds
names of all features (list of strings of mod/s for each mod/Hz)        

'''

# Extracting wav files from directory
wav, _ = lbr.load(filename, sr=sr) 


# Extracting Mel spectrogram
mel_spec = lbr.feature.melspectrogram(y=wav, sr=sr, hop_length=hop_length,
                                              **kwargs)
mel_spec = mel_spec.T

# Checking Input parameters
if mps_n_fft >= mel_spec.shape[0]:
    raise ValueError("The mps window size exceeds the Mel spectrogram. Please enter a smaller integer.")

if mps_hop_length >= mel_spec.shape[0]:
    raise ValueError("The mps step size exceeds the Mel spectrogram. Please enter a smaller integer.")


# Extracting mps
mps_all = []
nyquist_mps = np.ceil(mel_spec.shape[1]/2)



for i in range(1,101):
    mps = np.fft.fft2(mel_spec[mps_n_fft*(i-1):mps_n_fft*i,:])
    
    mps = np.abs(np.fft.fftshift(mps))
    mps_plot = np.abs(np.fft.fftshift(mps))
    # Flattening the mps to a vector
    mps = np.reshape(mps,(1,np.size(mps)))
   
    mps_all = np.append(mps_all,mps)
    
    mps_all = np.array(mps_all)
   
    # Concatinating the MPS row-wise
    mps_all = np.concatenate(mps_all)
    

# Raw Signal
raw_length_sec = (len(wav)/sr)
raw_length_min = raw_length_sec/60

#number_samples = sr*len(wav)/1000 ?

# Sampling Rate in Mel Spectrogram
fs_spectrogram = round(len(mel_spec)/(raw_length_sec))

# Sampling rate in MPS 
fs_mps = round(mps_n_fft/(raw_length_min))

 
# Extract Axis units for plotting 
# Calculate step sizes for MPS
freq_step_log = np.log(mel_spec[1,:])
freq_step_log = freq_step_log[1] - freq_step_log[0]

time_step_log = mel_spec[:,1]
time_step_log = time_step_log[1] - time_step_log[0]

# Calculate labels for X and Y axes
mps_freqs = np.fft.fftshift(np.fft.fftfreq(mel_spec.shape[1], d = freq_step_log)) # returns fourier transformed freuqencies which are already shifted (lower freq in center))
mps_times = np.fft.fftshift(np.fft.fftfreq(mps_n_fft, d = time_step_log/fs_spectrogram/fs_mps)) #????


if plot_mps = True:
    fig, ax = plt.subplots()
    image = ax.imshow(np.log(mps_all[0]))
    ax.pcolormesh(mps_times, mps_freqs, image, cmap ='viridis')
    ax.contour(mps_times, mps_freqs, image,np.percentile(image,[80,90,95,99]))       
    ax.set_title('Modulation Power Spectrum')
    ax.set_xlabel('mod/s')
    ax.set_ylabel('cyc/oct')
    plt.setp(ax, xlim = [-10,10], ylim=[0,9])

    
# Determine MPS repition time
mps_rep_time = fs_spectrogram/mps_hop_length
    

# Extracting feature names                     
names_features = ['{0:.2f} mod/s {1:.2f} cyc/oct)'.format(mps_time, mps_freq) for mps_time in mps_times for mps_freq in mps_freqs]
                     
                     
return mps_all, mps_rep_time, names_features

 

