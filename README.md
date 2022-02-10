# Microduplicate_screener
Python script to eliminate duplicate micrographs.
Due to the multihole beamshift nature of data collection, sometimes, there are duplications of micrographs. This can lead to slower data processing and lower resolution structure than expected.

## How it works
The script works in the following way:
- The duplication should not be in the image groups during one stage movement. In McGill, it is 4 holes per movement and 4 pictures per hole (16 images per move).
- The duplicate micrograph should be within next number of micrographs (scanRange, default = 32)
- Since there will be several images collected per hole (4 in cases of McGill data), the duplicate images will be spaced at a multiple of number of images per hole (multiple of 4 in case of McGill)
- The duplication search is done by aligning each image with the corresponding images within the scan range (using IMOD tiltxcorr). The duplicate image will be identified if the cross correlation coefficient (CCC) threshold is above 0.15 - 0.3.

In addition:
- The dataset is binned down for quick processing using IMOD newstack (8 times is enough)
- It is essential to bandpass filter the image to remove the gradient and high resolution detail in the images for accurate comparison. The parameter for bandpass filter is hardcoded in the script (LOWPASS, HIGHPASS, LPSIGMA, HPSIGMA)

**NOTE:** If multiple shot per hole is used, all the shots from the same holes should be duplicated. You can use this pattern to recognize whether the duplicate is true duplicate.

**NOTE:** The micrograph order is sorted by alphabettical after reading from the star file. So if your micrographs are not in alphabetial order, the script will not work.



## Installation

Software requirement: IMOD
python mrcfile, starfile, numpy, panda

Easy installation involved anaconda:
- Set up a fresh conda environment with Python >= 3.6: **conda create -n ds python=3.6**
- Activate the environment: conda activate ds
- Install starfile, mrcfile: 
**_pip install mrcfile_**
**_pip install starfile_***

- Clone the duplicate scanner: git clone https://github.com/builab/microduplicate_screener.git


## Running

You need to run on the mrc file after MotionCorr job. Bin 8 is necessary to reduce the processing time
Output is a csv file contain the name of all the duplicate micrographs

```
python3 microduplicate_screener/microduplicate_screener.py --i MotionCorr/job002/corrected_micrographs.star --bin 8 --scanrange 34 --imagespermove 16 --imagesperhole 4 --j 12 --csvout duplicate.csv
```

**--bin 8**: Binning of the original micrographs

**--scanrange 34** Should be multiple of imagespermove + 1

**--imagespermove 16** Number of images per stage movement. Set this to 1 to be really exhausive

**--imagesperhole 4**  Number of images per hole

**--csvout duplicate.csv** Output csv file showing the original & duplicate micrographs

**--j 12** Number of cores used

**--threshold 0.2** CCC threshold

**--opticsless 1** Only use for Relion star lower than 3.0 (default 0)


It takes about 2hr to scan through 5000 images from Gatan K3 collected in non-superresolution mode with 12 cores.

You can also use the slurm_dupscanner.sh for SLURM submission

You can then eliminate the duplicate micrographs from star file using some star file manipulator such as [starparser](https://github.com/sami-chaaban/starparser) from Sami Chabaan.

#### Remove duplicate micrographs only
```
grep -v 'Duplicate'  duplicate.csv | awk -F, '{print $2}' > micrographs_to_be_removed.txt

starparser --i MotionCorr/job002/corrected_micrographs.star --o clean_micrographs.star --remove_mics_fromlist --f micrographs_to_be_removed.txt 
```
