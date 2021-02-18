# Validating the Voxelwiseencoding Model
***

### This step-by-step guide provides guidance for running the voxelwiseencoding app (moritz boos) for the Modulation Power Spectrum and different parameters 
for stimulus length and offset of the fMRI data

***


# Extracting Modulation Power Spectrum 
import json
from nilearn.masking import unmask
import nilearn
from nilearn.masking import apply_mask
from nilearn.plotting import plot_stat_map
from nilearn.image import mean_img
from nilearn import plotting 
import nibabel
import numpy as np
from nilearn.image import threshold_stats_img
from nilearn.input_data import MultiNiftiMasker
from nilearn.masking import compute_brain_mask


mel_params = {'n_mels': 64, 'sr': 44100, 'hop_length': 882, 'n_fft': 882, 'fmax': 8000,'mps_hop_length': 100, 'mps_n_fft':100}
with open('config.json', 'w+') as fl:
    json.dump(mel_params, fl)
    
!git clone https://github.com/jannenold/audio2bidsstim/

!pip install -r audio2bidsstim/requirements.txt

# Extracting Modulation Power Spectrum 
#!python audio2bidsstim/wav_files_to_bids_tsv_2.py /data/fg_audio/*.wav -c config.json


from voxelwiseencoding.process_bids import run_model_for_subject

# these are the parameters used for preprocessing the BOLD fMRI files
bold_prep_params = {'standardize': 'zscore', 'detrend': True}

# and for lagging the stimulus as well - we want to include 6 sec stimulus segments to predict fMRI
lagging_params = {'lag_time': 6, 'offset_stim': 2}

# these are the parameters for sklearn's Ridge estimator
ridge_params = {'alphas': [1e-1, 1, 100, 1000],'cv': 2, 'normalize': True}


ridges, scores, computed_mask = run_model_for_subject('01', '/data/jnold/aligned_mps/',
                                                      task='aomovie', mask='epi', bold_prep_kwargs=bold_prep_params,
                                                      preprocess_kwargs=lagging_params, encoding_kwargs=ridge_params)
mps_scores01_6lag_2off = scores
