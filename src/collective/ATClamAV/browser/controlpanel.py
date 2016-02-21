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
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import adapts
from zope.interface import implements




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



class ClamAVControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IClamAVControlPanel)

    def __init__(self, context):
        super(ClamAVControlPanelAdapter, self).__init__(context)
        properties = getToolByName(context, 'portal_properties')
        self.context = properties.clamav_properties

    # Connection type
    def get_clamav_connection(self):
        return getattr(self.context, 'clamav_connection', "socket")

    def set_clamav_connection(self, value):
        self.context._updateProperty('clamav_connection', value)

    clamav_connection = property(get_clamav_connection, set_clamav_connection)

    # Socket path
    def get_clamav_socket(self):
        return getattr(self.context, 'clamav_socket', '/var/run/clamd')

    def set_clamav_socket(self, value):
        self.context._updateProperty('clamav_socket', value)

    clamav_socket = property(get_clamav_socket, set_clamav_socket)

    # Host
    def get_clamav_host(self):
        return getattr(self.context, 'clamav_host', 'localhost')

    def set_clamav_host(self, value):
        self.context._updateProperty('clamav_host', value)

    clamav_host = property(get_clamav_host, set_clamav_host)

    # Port
    def get_clamav_port(self):
        return int(getattr(self.context, 'clamav_port', '3310'))

    def set_clamav_port(self, value):
        self.context._updateProperty('clamav_port', value)

    clamav_port = property(get_clamav_port, set_clamav_port)

    # Timeout
    def get_clamav_timeout(self):
        return int(getattr(self.context, 'clamav_timeout', '120'))

    def set_clamav_timeout(self, value):
        self.context._updateProperty('clamav_timeout', value)

    clamav_timeout = property(get_clamav_timeout, set_clamav_timeout)



class ClamAVControlPanelForm(RegistryEditForm):
    schema = IClamAVControlPanel
    schema_prefix = "ClamAV5"
    label = u'ClamaAV Plone 5 Settings'



ClamAVControlPanelView = layout.wrap_form(ClamAVControlPanelForm, ControlPanelFormWrapper)
