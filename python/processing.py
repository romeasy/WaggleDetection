import cv2
import numpy as np

#   get frameCount frames of video starting at startFrame;
#   they are resized to targetSize. 
#   The first two dimensions of the return value
#   are the image dimension, the third the time dimension.
def getVideoMat(video, startFrame, frameCount, targetSize):
    
    video.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, startFrame)
    cont, mat = video.read()
    mat = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
    mat = cv2.resize(mat, targetSize, 0, 0, cv2.INTER_AREA)
    lastFrame = lambda x : x.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) >= (startFrame + frameCount)

    while (not lastFrame(video)):
        cont, nextFrame = video.read()
        if not cont: break
        nextFrame = cv2.cvtColor(nextFrame, cv2.COLOR_BGR2GRAY)
        nextFrame = cv2.resize(nextFrame, targetSize, 0, 0, cv2.INTER_AREA)
        mat = np.dstack((mat, nextFrame))

    return mat


if __name__ == "__main__":
    import sys
    
    video = cv2.VideoCapture(sys.argv[1])
    imgMat = getVideoMat(video, int(sys.argv[2]), 32, (160, 120))
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
