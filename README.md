# practical_project_2020
The code was created as part of a Practical Project at the University of Oldenburg in 2020 under supervision of Moritz Boos and Dr. Arkan Al-Zubaidi. 

1) **Extracting** the Modulation Power Spectrum: This function extracts the Modulation Power Spectrum from an auditory stimulus in a BIDS compliant format.
The function is based on the MEL spectrogram and the 2D Fourier Transform. 

Use with `python wav_files_to_bids_tsv_2.py path/to/your/wavfiles/*.wav -c path/to/your/config.json`. By default extracts the Mel Spectrogram. 
For a fully commented script and step by step explanation please refer to the [step-by-step Markdown File](https://github.com/jannenold/practical_project_2020/blob/main/step_by_step.md) here.

2) **Validate** the model: Use the Voxelwiseencoding App by Moritz Boos (for a step by step application, see [Validating VWE](https://github.com/jannenold/practical_project_2020/blob/main/step_by_step_validating_VWE.md))

# Usage for extracting the MPS 
<pre> 
positional arguments:
-------
  filename :      str, path to wav files to be converted. Can be used with wildcard *.wav. 

keyword arguments:
------
  sr:             int, sampling rate of auditory files (samples per second: 44100 Hz by default)
  n_fft:          int, window length of spectrogram (default 882)
  mps_n_fft:      int, window length for extracting the MPS (default 100)
  hop_length:     int, step size for extracting MEL spectrogram (default 882)
  mps_hop_length: int, step size for extracting MPS (default 100)
  n_mels:         int, number of mels used (default 64)
  
  
optional arguments:
------
  plot_mps:       bool, plotting the mel spectrogram and mps forthe first window side by side (by default set to True)


</pre>

# Output

The function returns three outputs:

1. a representation of a feature matrix of shape (samples x features)
2. Stimulus Repetition Time (int)
3. the names of the features (as list of strings)

**Optional**

The function can return the plotted MPS. By default, this is set to True and has to be indicated if needed otherwise.

*Note*: Default settings are set so the windows for the extraction of the Mel spectrogram and the MPS each are non-overlapping.
