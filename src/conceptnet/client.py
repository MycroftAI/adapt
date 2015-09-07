__author__ = 'seanfitz'
import requests


class ConceptNetClient(object):
    def __init__(self, baseUrl='http://conceptnet5.media.mit.edu/data/5.2'):
        self.baseUrl = baseUrl

    def _execute(self, subresource, params):
        return requests.get(self.baseUrl + subresource, params=params).json()

    def search(self, text):
        return self._execute('/search', params={'text': text})