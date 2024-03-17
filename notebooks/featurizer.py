from UrlFeaturizer import UrlFeaturizer

def featurize_batch(batch):
    featurized_batch = []
    for url in batch:
        featurizer = UrlFeaturizer(url)
        features = {
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
        featurized_batch.append(features)
    return featurized_batch
