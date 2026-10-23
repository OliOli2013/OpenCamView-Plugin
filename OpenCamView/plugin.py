from Plugins.Plugin import PluginDescriptor
from .ui import MainScreen

def main(session,**kwargs):session.open(MainScreen)
def Plugins(**kwargs):
    return [PluginDescriptor(name='OpenCamView',description='Kamery IP / RTSP / ONVIF',where=w,icon='plugin.png',fnc=main)
            for w in (PluginDescriptor.WHERE_PLUGINMENU,PluginDescriptor.WHERE_EXTENSIONSMENU)]
