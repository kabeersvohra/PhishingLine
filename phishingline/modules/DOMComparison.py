from html_similarity import *

from modules.Module import Module
from phishingline.src.Classification import Classification


class DOMComparison(Module):

    def classify(self):
        # soup = BeautifulSoup(self.html, 'html.parser')
        # phish1 = BeautifulSoup(open(r"C:\Users\Kabeer\Desktop\phish1.html", encoding='utf8'), 'html.parser')
        # phish2 = BeautifulSoup(open(r"C:\Users\Kabeer\Desktop\phish2.html", encoding='utf8'), 'html.parser')

        # def create_tree(html, tree=dendropy.Tree(), n=0):
        #     tree.taxon_namespace.get_taxon(html.name)
        #     tree = tree.seed_node.new_child()
        #     if n < 3:
        #         for child in html.children:
        #             if child.name is not None:
        #                 create_tree(child, tree, n+1)
        #     return tree
        #
        # A = create_tree(soup)
        # B = create_tree(phish1)
        # C = create_tree(phish2)
        # print(A, B, C)
        # text1 = self.html.read()
        phish = list()
        legit = list()
        phish.append(open(r"C:\Users\Kabeer\Desktop\phish1.html", encoding='utf8').read())
        phish.append(open(r"C:\Users\Kabeer\Desktop\phish2.html", encoding='utf8').read())
        phish.append(open(r"C:\Users\Kabeer\Desktop\phish3.html", encoding='utf8').read())
        legit.append(open(r"C:\Users\Kabeer\Desktop\legitimate1.html", encoding='utf8').read())
        legit.append(open(r"C:\Users\Kabeer\Desktop\legitimate2.html", encoding='utf8').read())
        legit.append(open(r"C:\Users\Kabeer\Desktop\legitimate3.html", encoding='utf8').read())
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        f = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if i == j:
                    break
                # print("phish vs legit struct %i %i: %f" % (i,j, structural_similarity(phish[i], legit[j])))
                # print("phish vs legit style %i %i: %f" % (i,j, style_similarity(phish[i], legit[j])))
                # print("phish vs legit %i %i: %f" % (i,j, similarity(phish[i], legit[j])))
                # print("phish vs phish struct %i %i: %f" % (i, j, structural_similarity(phish[i], phish[j])))
                # print("phish vs phish style %i %i: %f" % (i, j, style_similarity(phish[i], phish[j])))
                # print("phish vs phish %i %i: %f" % (i, j, similarity(phish[i], phish[j])))
                a += structural_similarity(phish[i], legit[j])
                b += style_similarity(phish[i], legit[j])
                c += similarity(phish[i], legit[j])
                d += structural_similarity(phish[i], phish[j])
                e += style_similarity(phish[i], phish[j])
                f += similarity(phish[i], phish[j])
        print(a, b, c, d, e, f)

        return Classification(legitimate=True)
