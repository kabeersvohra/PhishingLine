from phishingline.src.Classification import Classification


class Module:
    def __init__(self, url, img, html):
        self.url = url
        self.img = img
        self.html = html

    def classify(self):
        Classification(phishing=False)
