# microduplicate_screener
Python script to eliminate duplicate micrographs
Due to the multihole beamshift nature of data collection, sometimes, there are quite some micrographs duplicate. This can lead to slower data processing and lower resolution structure than expected.

The script works in the following way:
- Normally, the duplicate micrograph would be within next number of micrographs (screenRange, default = 50)
- First, you need to bin your dataset with bin_all_movies.sh
- Then, the script will go through each mirograph, align with the next 50 micrographs (screenRange) using IMOD tiltxcorr.
- After that, the cross correlation coefficient (CCC) between the bandpass filtered micrograph & each of the 50 aligned micrographs is calculated.
- If the cross correlation coeffient > CCCthreshold (default = 0.25), it should be a duplicate micrograph.

NOTE: If multiple shot per hole is used, all the shots from the same holes should be duplicated. You can use this pattern to recognize whether the duplicate is true duplicate.
NOTE: The bandpass filter is essential for the detection since the imperfect gain normalized background in the micrographs can affect the CCC.


'''Installation'''
Software requirement: IMOD, python mrcfile

'''Running'''
You need to run on the mrc file after MotionCorr job. Bin 8 is necessary to reduce the processing time
Output is a text file contain the name of all the duplicate micrographs
