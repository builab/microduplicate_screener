% might exclude the edge of image for cc
% This is only for testing: need to have python version later
% A quick script to proof of principle
% The script actually work
screenRange = 48 ; % Range to scan for duplicate
shotperhole = 4; % Group of 4 micro per hole
border = 10; % 10 pixel for each dimension

threshold = 0.2; % Threshold to say duplicate

%imdir = '/london/data0/20210531_TetraCU428/MotionCorr/job005/Movies/CU428_1_5000_bin8';
imdir = 'img';

prefix = 'CU428_';
startidx = 4700;

% Read all image in one cell array


cc = zeros(floor(screenRange/shotperhole), shotperhole);

for i = startidx + shotperhole : 4 : startidx + screenRange
	disp(['Processing image ' prefix  sprintf('%0.5d', startidx)])
	disp(['Correlate with group ' prefix  sprintf('%0.5d', i)])
	for shotid = 1:shotperhole
		imfile = dir([imdir '/' prefix sprintf('%0.5d', startidx + shotid - 1) '*.mrc']);
		targetimfile = dir([imdir '/' prefix sprintf('%0.5d', i + shotid - 1) '*.mrc']);
		im = [imfile.folder '/' imfile.name];
		imfil = ['out/' strrep(imfile.name, '.mrc', '_fil.mrc')];
		targetim = [targetimfile.folder '/' targetimfile.name];
		targetfil = ['out/' strrep(targetimfile.name, '.mrc', '_fil.mrc')];
		cmd = sprintf('tiltxcorr -reference %s -input %s -output out.xf -angles 0 -sigma1 0.03 -radius2 0.25 -sigma2 0.05', im, targetim);
		targetout = ['out/' strrep(targetimfile.name, '.mrc', '_aln.mrc')];
		cmd2 = sprintf('newstack -in %s -ou %s -xform out.xf', targetim, targetout);
		cmd3 = sprintf('mtffilter -input %s -output %s -lowpass 0.25,0.05 -highpass 0.04,0.02', targetout, targetfil);
		cmd4 = sprintf('mtffilter -input %s -output %s -lowpass 0.25,0.05 -highpass 0.04,0.02', im, imfil);
		system(cmd);
		system(cmd2);
		system(cmd3);
		system(cmd4);
		ref = ReadMRC(imfil);
		target = ReadMRC(targetfil);

		% Crop center of ccf only
		cc(floor((i - startidx)/4), shotid) = corr2(ref, target);
		%cc(floor((i - startidx)/4), shotid) = immse(target, ref);
	end
end

csvwrite('test.txt', cc);
