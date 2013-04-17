import bpy,os,re,sys

 
def render(title):
  global renderpath,renderpathabs,sndfile
  
  #bpy.context.scene.render.resolution_percentage =
  #bpy.context.scene.render.use_compositing = 0
  #bpy.context.scene.render.use_sequencer = 1
  renderpath = '//out/'+title
  
  if (not os.path.isdir(renderpath)):
    print('yay')
    #bpy.ops.render.render(animation=True)
  else:
    print('already rendered',bpy.context.scene.render.frame_path())

  
#translates strings and calls render
def main():
  print(sys.argv)
  if (len(sys.argv)>2):
    #
    #bpy.data.objects[textobj.get('id')].data.body = textobj.text
    #bpy.data.objects['usermenuuser'].data.body = bpy.data.objects['user'].data.body #due to different alignment
    render("oops")
  else:
    print('supply the title as a parameter');
    
if __name__ == '__main__':
    main()
