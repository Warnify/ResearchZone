from datetime import datetime
import math
import whois
from requests import get
from pyquery import PyQuery

class UrlFeaturizer(object):
    """
    UrlFeaturizer class is designed to extract various features from a given URL.
    These features include characteristics of the URL string itself, domain-specific attributes, and page features.
    """
    
    def __init__(self, url):
        self.url = url
        self.domain = url.split('//')[-1].split('/')[0]
        self.today = datetime.now().replace(tzinfo=None)

        try:
            self.whois = whois.query(self.domain).__dict__
        except:
            self.whois = None

        try:
            self.response = get(self.url)
            self.pq = PyQuery(self.response.text)
        except:
            self.response = None
            self.pq = None

    ## URL string Features
    def entropy(self):
        """
        Calculate the entropy of the URL string.
        """
        string = self.url.strip()
        prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
        entropy = sum([(p * math.log(p) / math.log(2.0)) for p in prob])
        return entropy

    def ip(self):
        """
        Check if the URL contains an IP address.
        """
        string = self.url
        flag = False
        if ("." in string):
            elements_array = string.strip().split(".")
            if(len(elements_array) == 4):
                for i in elements_array:
                    if (i.isnumeric() and int(i)>=0 and int(i)<=255):
                        flag=True
                    else:
                        flag=False
                        break
        if flag:
            return 1 
        else:
            return 0

    def numDigits(self):
        """
        Count the number of digits in the URL
        """
        
        digits = [i for i in self.url if i.isdigit()]
        return len(digits)

    def urlLength(self):
        """
        Calculate the length of the URL
        """
        return len(self.url)

    def numParameters(self):
        """
        Count the number of parameters in the URL.
        """
        params = self.url.split('&')
        return len(params) - 1

    def numFragments(self):
        """
        Count the number of fragments in the URL
        """
        fragments = self.url.split('#')
        return len(fragments) - 1

    def numSubDomains(self):
        """
        Count the number of subdomains in the URL
        """
        subdomains = self.url.split('http')[-1].split('//')[-1].split('/')
        return len(subdomains)-1

    def domainExtension(self):
        ext = self.url.split('.')[-1].split('/')[0]
        return ext

    ## URL domain features
    def hasHttp(self):
        return 'http:' in self.url

    def hasHttps(self):
        return 'https:' in self.url

    def daysSinceRegistration(self):
        if self.whois and self.whois['creation_date']:
            diff = self.today - self.whois['creation_date'].replace(tzinfo=None)
            diff = str(diff).split(' days')[0]
            return diff
        else:
            return 0

    def daysSinceExpiration(self):
        if self.whois and self.whois['expiration_date']:
            diff = self.whois['expiration_date'].replace(tzinfo=None) - self.today
            diff = str(diff).split(' days')[0]
            return diff
        else:
            return 0
    
     ## URL Page Features
    def bodyLength(self):
        if self.pq is not None:
            return len(self.pq('html').text()) if self.urlIsLive else 0
        else:
            return 0

    def numTitles(self):
        if self.pq is not None:
            titles = ['h{}'.format(i) for i in range(7)]
            titles = [self.pq(i).items() for i in titles]
            return len([item for s in titles for item in s])
        else:
            return 0

    def numImages(self):
        if self.pq is not None:
            return len([i for i in self.pq('img').items()])
        else:
            return 0

    def numLinks(self):
        if self.pq is not None:
            return len([i for i in self.pq('a').items()])
        else:
            return 0

    def scriptLength(self):
        if self.pq is not None:
            return len(self.pq('script').text())
        else:
            return 0

    def specialCharacters(self):
        if self.pq is not None:
            bodyText = self.pq('html').text()
            schars = [i for i in bodyText if not i.isdigit() and not i.isalpha()]
            return len(schars)
        else:
            return 0

    def scriptToSpecialCharsRatio(self):
        v = self.specialCharacters()
        if self.pq is not None and v!=0:
            sscr = self.scriptLength()/v
        else:
            sscr = 0
        return sscr

    def scriptTobodyRatio(self):
        v = self.bodyLength()
        if self.pq is not None and v!=0:
            sbr = self.scriptLength()/v
        else:
            sbr = 0
        return sbr

    def bodyToSpecialCharRatio(self):
        v = self.bodyLength()
        if self.pq is not None and v!=0:
            bscr = self.specialCharacters()/v
        else:
            bscr = 0
        return bscr

    def urlIsLive(self):
        return self.response == 200
    

def featurize_url(url):
    featurizer = UrlFeaturizer(url)
    return {
        'url': url,
        'entropy': featurizer.entropy(),
        'ip': featurizer.ip(),
        'numDigits': featurizer.numDigits(),
        'urlLength': featurizer.urlLength(),
        'numParameters': featurizer.numParameters(),
        'numFragments': featurizer.numFragments(),
        'numSubDomains': featurizer.numSubDomains(),
        'domainExtension': featurizer.domainExtension(),
        'hasHttp': featurizer.hasHttp(),
        'hasHttps': featurizer.hasHttps(),
        'daysSinceRegistration': featurizer.daysSinceRegistration(),
        'daysSinceExpiration': featurizer.daysSinceExpiration(),
        'bodyLength': featurizer.bodyLength(),
        'numTitles': featurizer.numTitles(),
        'numImages': featurizer.numImages(),
        'numLinks': featurizer.numLinks(),
        'scriptLength': featurizer.scriptLength(),
        'specialCharacters': featurizer.specialCharacters(),
        'scriptToSpecialCharsRatio': featurizer.scriptToSpecialCharsRatio(),
        'scriptTobodyRatio': featurizer.scriptTobodyRatio(),
        'bodyToSpecialCharRatio': featurizer.bodyToSpecialCharRatio(),
        'urlIsLive': featurizer.urlIsLive(),
    }
