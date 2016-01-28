from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from plone.z3cform import layout

from collective.ATClamAV import ATClamAVMessageFactory as _
from collective.ATClamAV.interfaces import IAVScannerSettings
from zope.interface import Interface
from datetime import date
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IContextSourceBinder



clamdConnectionType = SimpleVocabulary(
    [SimpleTerm(value=_(u"Local UNIX Socket"), title=_(u'socket')),
     SimpleTerm(value=_(u"Network"), title=_(u'net'))])
    


class IClamAVControlPanel(Interface):
     
   clamav_connection = schema.Choice(
        title=_(u"Connection type to clamd"),
        description=_(u"Choose whether clamd is accessible through local "
            "UNIX sockets or network."),
        vocabulary=clamdConnectionType)

   clamav_socket = schema.ASCIILine(
        title=_(u"Clamd local socket file"),
        description=_(u"If connected to clamd through local UNIX sockets, "
            "the path to the local socket file."),
        default = '/var/run/clamd',
        required = True)

   clamav_host = schema.ASCIILine(title=_(u"Scanner host"),
        description=_(u"If connected to clamd through the network, "
            "the host running clamd."),
        default = 'localhost',
        required = True)

   clamav_port = schema.Int(title=_(u"Scanner port"),
        description=_(u"If connected to clamd through the network, "
            "the port on which clamd listens."),
        default=3310,
        required = True)

   clamav_timeout = schema.Int(title=_(u"Timeout"),
        description=_(u"The timeout in seconds for communication with "
            "clamd."),
        default=120,
        required = True)



class ClamAVControlPanelForm(RegistryEditForm):
    schema = IClamAVControlPanel
    schema_prefix = "ClamAV5"
    label = u'ClamaAV Plone 5 Settings'
    
    
    def __init__(self, context):
        super(ClamAVControlPanelAdapter, self).__init__(context)
        properties = getToolByName(context, 'portal_properties')
        self.context = properties.clamav_properties



ClamAVControlPanelView = layout.wrap_form(ClamAVControlPanelForm, ControlPanelFormWrapper)
