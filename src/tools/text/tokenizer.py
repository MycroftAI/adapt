__author__ = 'seanfitz'
import re
regex_letter_number = r"[a-zA-Z0-9]"
regex_not_letter_number = r"[^a-zA-Z0-9]"
regex_separator = r"[\\?!()\";/\\|`]"

regex_clitics = r"'|:|-|'S|'D|'M|'LL|'RE|'VE|N'T|'s|'d|'m|'ll|'re|'ve|n't"

abbreviations_list = [ "Co.", "Corp.",
            "vs.", "e.g.", "etc.", "ex.", "cf.", "eg.", "Jan.", "Feb.", "Mar.",
            "Apr.", "Jun.", "Jul.", "Aug.", "Sept.", "Oct.", "Nov.", "Dec.",
            "jan.", "feb.", "mar.", "apr.", "jun.", "jul.", "aug.", "sept.",
            "oct.", "nov.", "dec.", "ed.", "eds.", "repr.", "trans.", "vol.",
            "vols.", "rev.", "est.", "b.", "m.", "bur.", "d.", "r.", "M.",
            "Dept.", "MM.", "U.", "Mr.", "Jr.", "Ms.", "Mme.", "Mrs.", "Dr.",
            "Ph.D."]


class EnglishTokenizer(object):
    def __init__(self):
        pass

    def tokenize(self, string):
        s = string
        s = re.sub('\t', " ", s)
        s = re.sub("(" + regex_separator + ")", " \g<1> ", s)
        s = re.sub("([^0-9]),", "\g<1> , ", s)
        s = re.sub(",([^0-9])", " , \g<1>", s)
        s = re.sub("^(')", "\g<1> ", s)
        s = re.sub("(" + regex_not_letter_number + ")'", "\g<1> '", s)
        s = re.sub("(" + regex_clitics + ")$", " \g<1>", s)
        s = re.sub("(" + regex_clitics + ")(" + regex_not_letter_number + ")", " \g<1> \g<2>", s)

        words = s.strip().split()
        p1 = re.compile(".*" + regex_letter_number + "\\.")
        p2 = re.compile("^([A-Za-z]\\.([A-Za-z]\\.)+|[A-Z][bcdfghj-nptvxz]+\\.)$")

        token_list = []

        for word in words:
            m1 = p1.match(word)
            m2 = p2.match(word)

            if m1 and word not in abbreviations_list and not m2:
                token_list.append(word[0: word.find('.')])
                token_list.append(word[word.find('.')])
            else:
                token_list.append(word)

        return token_list


def tokenize_string(text):
    tk = EnglishTokenizer()
    return tk.tokenize(text)

if __name__ == "__main__":
    print(tokenize_string("Hello world, I'm a happy camper. I don't have any friends?"))