from zope.interface import Interface
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary

from collective.ATClamAV import ATClamAVMessageFactory as _



class IAVScanner(Interface):

    def ping():
        pass

    def scanBuffer(buffer):
        pass
