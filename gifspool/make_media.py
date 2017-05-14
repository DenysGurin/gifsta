from PIL import Image
import moviepy.editor as mp

def gif_to_jpg(path, new_path):
	try:
	    im = Image.open(path)
	    bg = Image.new("RGB", im.size, (255,255,255))
	    bg.paste(im, (0,0))
	    bg.save("%s.jpg"%new_path, quality=95)
	except:
		pass

def gif_to_mp4(path, new_path):
    try:
        clip = mp.VideoFileClip(path)
        clip.write_videofile("%s.mp4"%new_path)
    except OSError:
        pass