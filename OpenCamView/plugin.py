from Plugins.Plugin import PluginDescriptor
from .ui import MainScreen
from .i18n import tr

def main(session,**kwargs):session.open(MainScreen)
def Plugins(**kwargs):
    return [PluginDescriptor(name='OpenCamView',description=tr('Kamery IP / RTSP / ONVIF'),where=w,icon='plugin.png',fnc=main)
            for w in (PluginDescriptor.WHERE_PLUGINMENU,PluginDescriptor.WHERE_EXTENSIONSMENU)]
