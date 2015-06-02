# -*- coding: UTF-8 -*-

import cv2
import numpy as np
from file_input import get_path
from math import pi,sin,cos,pow
from copy import deepcopy


#Framerate -> Samplerate
SR = 100
FRAMES = 32
FREQ_min = 11
FREQ_max = 17
#Die Frequenzen die wir Analysieren wollen
FREQS = [x for x in range(FREQ_min, FREQ_max+1)]
#Die samples der Sinusfunktion
#Erste Dimension ist Frequenz, zweite Dimension sind die Samples
SIN = [[sin(2*pi*r*(1/SR)*k) for k in range(0, SR)] for r in FREQS]
COS = [[cos(2*pi*r*(1/SR)*k) for k in range(0, SR)] for r in FREQS]


#   get frameCount frames of video starting at startFrame;
#   they are resized to targetSize. 
#   The first two dimensions of the return value
#   are the image dimension, the third the time dimension.
def getVideoMat(video, startFrame, frameCount, targetSize):
    
    video.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, startFrame)
    cont, mat = video.read()
    mat = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
    mat = cv2.resize(mat, targetSize, 0, 0, cv2.INTER_AREA)
    lastFrame = lambda : video.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) >= (startFrame + frameCount)

    while (not lastFrame()):
        cont, nextFrame = video.read()
        if not cont: break
        nextFrame = cv2.cvtColor(nextFrame, cv2.COLOR_BGR2GRAY)
        nextFrame = cv2.resize(nextFrame, targetSize, 0, 0, cv2.INTER_AREA)
        mat = np.dstack((mat, nextFrame))

    return mat

#Frequency Score Calculation

#Unsere Score-Funktion
#Erstes Argument sind die Werte eines Pixels über die Zeit
#TODO: Im Paper sind die werte von pix noch auf -1, -1 reduziert.
def score(pix, freq_index):
	valSin = sum([pow(pix[m]*SIN[freq_index][m],2) for m in range (0, FRAMES)])
	valCos = sum([pow(pix[m]*COS[freq_index][m],2) for m in range (0, FRAMES)])
	return(valSin+valCos)

#Signal Generation
#scores sind die Werte der Score Funktion für alle Frequenzen für einen Pixel
#max und min enthält das Maximum bzw. Minimum der Werte des Pixels entlang der Zeit
#TODO: fängt w bei 0 oder 1 an??
def potential(scores, max_val, min_val):
	A = max_val-min_val;
	myScores = deepcopy(scores)
	myScores.sort()
	summe = A * sum([w*myScore[w] for w in range(0, len(myScores))])
	
def signal(threshold, potential):
	if(potential > threshold):
		return(1)
	return(0)

if __name__ == "__main__":
    import sys
    videoFile = None
    video = None
    if(len(sys.argv)>1):
        videoFile = sys.argv[1]
    else:
        videoFile = get_path()
    video = cv2.VideoCapture(videoFile)
    imgMat = getVideoMat(video, int(sys.argv[2]), FRAMES, (160, 120))
    video.release()

#   compute dft along last (time) dimension
    freqDom = np.fft.rfft(imgMat)

#   freq = (i * sampleRate) / numberOfSamples, where i is an index in the dft
#   You can get the computed frequencies of np.fft.rfft with np.fft.rfftfreq(numberOfSamples, d=1./sampleRate).
#   The frequency at index i of rfftfreq corresponds to the amplitude at index i of rfft.
    freqMagn = np.absolute(freqDom[:,:,3]) #Intensity of 13Hz at window size of 32 frames

#   If the magnitudes are very widely spaced we could switch to a log scale:
#   (Hasn't been necessary in my experience)
#    freqMagn += np.ones(freqMagn.shape)
#    fregMagn = np.log(freqMagn)

#   Normalize to 8 bit colour depth
    cv2.normalize(freqMagn, freqMagn, 0, 255, cv2.NORM_MINMAX)

    cv2.imwrite('out.png', freqMagn)
