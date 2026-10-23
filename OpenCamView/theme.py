# -*- coding: utf-8 -*-
"""OpenCamView AIO dark UI. Colored labels always match remote ColorActions."""
from enigma import getDesktop

# Odpowiedniki kolorowych przyciskow na standardowych pilotach Enigma2.
COLORS = (
    ('red', '#BE3648', '#FFFFFF'),
    ('green', '#237F5C', '#FFFFFF'),
    ('yellow', '#E8B53C', '#101D2E'),
    ('blue', '#246BAE', '#FFFFFF'),
)

def scale():
    sz=getDesktop(0).size()
    w,h=max(960,sz.width()),max(576,sz.height())
    k=min(w/1280.,h/720.)
    return w,h,lambda n:max(1,int(n*k))

def colored_key(name,x,y,width,height,font,bg,fg):
    # eLabel zapewnia prawdziwe tlo; przezroczysta etykieta jest ponad nim.
    return ('<eLabel position="%d,%d" size="%d,%d" backgroundColor="%s" zPosition="3"/>'
            '<widget name="key_%s" position="%d,%d" size="%d,%d" font="Regular;%d" '
            'foregroundColor="%s" halign="center" valign="center" transparent="1" zPosition="4"/>') % (
                x,y,width,height,bg,name,x,y,width,height,font,fg)

def main():
    w,h,s=scale()
    lx=s(38); right=int(w*.64); wide=w-right-s(38)
    ky=h-s(114); button_height=s(39)
    gap=s(10); kw=(w-2*lx-3*gap)//4
    keys=''.join(colored_key(k,lx+i*(kw+gap),ky,kw,button_height,s(21),bg,fg)
                 for i,(k,bg,fg) in enumerate(COLORS))
    # Dwuwarstwowa stopka: pomoc pilota i wyrazna linia informacyjna autora.
    return '''<screen name="OpenCamView" position="0,0" size="{w},{h}" flags="wfNoBorder" backgroundColor="#081426">
<eLabel position="0,0" size="{w},{head}" backgroundColor="#12243A" zPosition="0"/>
<eLabel position="{lx},{head}" size="{line},4" backgroundColor="#26CFCC" zPosition="1"/>
<widget name="header" position="{lx},25" size="{hh},65" font="Regular;{large}" foregroundColor="#FFFFFF" transparent="1" zPosition="2"/>
<widget name="count" position="{right},30" size="{cw},52" font="Regular;{medium}" foregroundColor="#26CFCC" transparent="1" zPosition="2"/>
<widget name="menu" position="{lx},{top}" size="{menuw},{mh}" itemHeight="{item}" font="Regular;{font}" backgroundColor="#172B42" foregroundColor="#FFFFFF" selectionBackgroundColor="#26CFCC" selectionForegroundColor="#081426" scrollbarMode="showOnDemand" zPosition="1"/>
<eLabel position="{right},{top}" size="{rw},{mh}" backgroundColor="#172B42" zPosition="1"/>
<widget name="detail" position="{dx},{dy}" size="{detailw},{dh}" font="Regular;{small}" foregroundColor="#D7E8F5" transparent="1" zPosition="2"/>
<widget name="status" position="{lx},{sy}" size="{fw},{stath}" font="Regular;{small}" foregroundColor="#F5C65B" transparent="1" zPosition="2"/>
{keys}
<widget name="footer" position="{lx},{fy}" size="{fw},{fh}" font="Regular;{tiny}" foregroundColor="#C8D8E4" halign="center" transparent="1" zPosition="2"/>
<eLabel position="0,{credtop}" size="{w},{credit_h}" backgroundColor="#12243A" zPosition="1"/>
<widget name="credits" position="{lx},{credtexttop}" size="{fw},{credit_h}" font="Regular;{tiny}" foregroundColor="#A9C7D8" halign="center" valign="center" transparent="1" zPosition="2"/>
</screen>'''.format(w=w,h=h,head=s(106),lx=lx,line=s(230),hh=s(680),large=s(33),right=right,cw=wide,
    medium=s(22),top=s(135),menuw=right-lx-s(16),mh=h-s(310),item=s(46),font=s(25),rw=wide,dx=right+s(17),dy=s(158),
    detailw=wide-s(30),dh=h-s(355),small=s(19),sy=h-s(154),stath=s(34),keys=keys,
    fy=h-s(66),fh=s(27),tiny=s(17),fw=w-2*lx,credtop=h-s(33),credtexttop=h-s(31),credit_h=s(30))

def video():
    w,h,s=scale()
    red=colored_key('red',s(30),h-s(79),s(138),s(40),s(20),COLORS[0][1],COLORS[0][2])
    return ('''<screen name="OCVPlayer" position="0,0" size="{w},{h}" flags="wfNoBorder" backgroundColor="#00000000">
<widget name="video" position="0,0" size="{w},{h}" zPosition="-1"/>
<eLabel position="0,{paneltop}" size="{w},{panelh}" backgroundColor="#12243A" zPosition="1"/>
{red}
<widget name="info" position="{infostart},{infotop}" size="{infow},{infoh}" font="Regular;{main_font}" foregroundColor="#FFFFFF" transparent="1" zPosition="2"/>
<widget name="credits" position="0,{credtop}" size="{w},{credh}" font="Regular;{small}" foregroundColor="#A9C7D8" halign="center" valign="center" transparent="1" zPosition="2"/>
</screen>''').format(w=w,h=h,red=red,paneltop=h-s(85),panelh=s(85),infostart=s(190),infotop=h-s(77),infow=w-s(206),infoh=s(38),
                              main_font=s(23),credtop=h-s(35),credh=s(28),small=s(17))

def overlay(n=1):
    w,h,s=scale();n=4 if n==4 else 1
    ow=s(520) if n==1 else w-s(60)
    oh=s(330) if n==1 else h-s(158)
    x=w-ow-s(34) if n==1 else s(30)
    y=s(73)
    cw=(ow-s(28))//(2 if n==4 else 1)
    ch=(oh-s(50))//(2 if n==4 else 1)
    text='<screen name="OCVOverlay" position="0,0" size="%d,%d" flags="wfNoBorder" backgroundColor="#00000000" transparent="1">'%(w,h)
    text+='<eLabel position="%d,%d" size="%d,%d" backgroundColor="#12243A" zPosition="1"/>'%(x,y,ow,oh)
    for i in range(n):
        cx=x+s(10)+(i%2 if n==4 else 0)*(cw+s(7));cy=y+s(9)+(i//2 if n==4 else 0)*(ch+s(7))
        text+='<widget name="pic%d" position="%d,%d" size="%d,%d" zPosition="2"/>'%(i,cx,cy,cw,ch-s(32))
        text+='<widget name="name%d" position="%d,%d" size="%d,%d" font="Regular;%d" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>'%(i,cx,cy+ch-s(28),cw,s(28),s(18))
    yline=y+oh+s(6);bw=s(118);bh=s(30)
    text+=colored_key('red',x,yline,bw,bh,s(17),COLORS[0][1],COLORS[0][2])
    text+=colored_key('blue',x+bw+s(7),yline,bw,bh,s(17),COLORS[3][1],COLORS[3][2])
    stat_x=x+2*(bw+s(7))
    text+='<widget name="status" position="%d,%d" size="%d,%d" font="Regular;%d" foregroundColor="#F5C65B" valign="center" transparent="1" zPosition="3"/>'%(
        stat_x,yline,ow-(stat_x-x),bh,s(16))
    # Widoczny podpis bez zaslaniania centralnego podgladu TV.
    text+='<eLabel position="0,%d" size="%d,%d" backgroundColor="#12243A" zPosition="1"/>'%(h-s(32),w,s(32))
    text+='<widget name="credits" position="%d,%d" size="%d,%d" font="Regular;%d" foregroundColor="#A9C7D8" halign="center" valign="center" transparent="1" zPosition="3"/>'%(
        s(24),h-s(31),w-s(48),s(28),s(17))
    text+='</screen>'
    return text
