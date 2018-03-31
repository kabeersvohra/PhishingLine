import cv2
from PIL import Image

from phishingline.src.Util import rooted


def checkMatch(img1, img2, i):
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    # Match descriptors.
    matches = bf.knnMatch(des1, des2, k=2)
    # Sort them in the order of their distance.
    matches = sorted(matches, key=lambda x: x.distance)
    # Draw first 10 matches.
    img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches, None, flags=2)
    # plt.imshow(img3), plt.show()
    Image.fromarray(img3).save('/home/kabeersvohra/Desktop/image%i.png' % i)
    return len(matches)


i = 0
img2 = cv2.imread(rooted('data/misclassified/benign7.png'), 0)  # trainImage
img1 = cv2.imread(rooted('data/logos/ATT/logo.png'), 0)  # queryImage
print(checkMatch(img1, img2, i))
img1 = cv2.imread(rooted('data/logos/PayPal/logo.png'), 0)  # queryImage
i += 1
print(checkMatch(img1, img2, i))
img1 = cv2.imread(rooted('data/logos/Google/logo.png'), 0)  # queryImage
i += 1
print(checkMatch(img1, img2, i))
img1 = cv2.imread(rooted('data/logos/Microsoft/logo.png'), 0)  # queryImage
i += 1
print(checkMatch(img1, img2, i))
img1 = cv2.imread(rooted('data/logos/Dropbox/logo.png'), 0)  # queryImage
i += 1
print(checkMatch(img1, img2, i))

