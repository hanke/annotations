from annotations import stims
from annotations.annotators import Annotator
import cv2
from annotations.core import Note


class ImageAnnotator(Annotator):

    target = stims.ImageStim


class CornerDetectionAnnotator(ImageAnnotator):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.fast = cv2.FastFeatureDetector()

    def apply(self, img):
        kp = self.fast.detect(img, None)
        return Note(img, self, {'corners_detected': kp})


class FaceDetectionAnnotator(ImageAnnotator):

    def __init__(self):
        self.cascade = cv2.CascadeClassifier(
            '/Users/tal/Downloads/cascade.xml')
        super(self.__class__, self).__init__()

    def apply(self, img, show=False):
        data = img.data
        gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30),
            flags = cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        if show:
            for (x, y, w, h) in faces:
                cv2.rectangle(data, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow('frame', data)
            cv2.waitKey(1)

        return Note(img, self, {'num_faces': len(faces)})
