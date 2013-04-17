import bpy,os,re
from xml.etree import ElementTree as ET

 
def render(lang):
  global renderpath,renderpathabs,sndfile
  
  #bpy.context.scene.render.resolution_percentage =
  #bpy.context.scene.render.use_compositing = 0
  bpy.context.scene.render.use_sequencer = 1
  renderpath = '//sequence/'+lang
  
  regexobj = re.search(r"^(.*\/)*(.*)(\.blend)$", bpy.data.filepath)
  bpy.context.scene.render.filepath = "%s/%s/" % (renderpath,regexobj.group(2))
  renderpathabs = "%ssequence/%s/%s" % (regexobj.group(1),lang,regexobj.group(2))
  sndpath = "%s/snd" % (renderpathabs)
  sndfile = "%s/snd.flac" % (sndpath)
  if (not os.path.isdir(renderpathabs)):
    bpy.ops.render.render(animation=True)
  if (not os.path.isdir(sndpath)):
    os.mkdir(sndpath)
    bpy.ops.sound.mixdown(filepath=sndfile)
  else:
    print('already rendered',bpy.context.scene.render.frame_path())

def transcode(lang):
  global renderpath,renderpathabs,sndfile

  regexobj = re.search(r"^(.*\/)*(.*)(\.blend)$", bpy.data.filepath)
  framepath = renderpathabs
  webmfile = "%s.webm" % (regexobj.group(2))
  transcodepath = "../gnome-help/%s/figures/" % (lang)
  
  #print(transcodepath,webmfile,sndfile,framepath)
  transcodecmd = "gst-launch-1.0 webmmux name=mux ! filesink location=\"%s/%s\"    file://%s ! decodebin ! audioconvert ! vorbisenc bitrate=96000 ! mux.     multifilesrc location=\"%s/%%04d.png\" index=1 caps=\"image/png,framerate=\(fraction\)24/1\" ! pngdec ! videoconvert ! videoscale ! video/x-raw, width=854,height=480 ! videorate ! vp8enc threads=12 target-bitrate=200000 ! mux." % (transcodepath,webmfile,sndfile,framepath)
  if (not os.path.isfile(transcodepath+webmfile)):
    os.system(transcodecmd)
  else:
    print('already transcoded',transcodepath + webmfile)  
  
#translates strings and calls render
def main():
  
  t = {}
  #unfortunately no decent fonts have ↲
  langs = open('language-whitelist.txt').readlines()
  for lang in langs:
    lang = lang.strip()
    xmlfile = ET.parse('../gnome-help/' + lang + '/gs-animation.xml')
    t[lang] = xmlfile.getroot()
  
  for lang in t:
    for textobj in t[lang].findall('t'):
      if textobj.get('id') in bpy.data.objects: #prelozit jestli existuje jako index
        bpy.data.objects[textobj.get('id')].data.body = textobj.text
    bpy.data.objects['usermenuuser'].data.body = bpy.data.objects['user'].data.body #due to different alignment
    render(lang)
    transcode(lang)
    
if __name__ == '__main__':
    main()
