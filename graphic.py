from fcntl import ioctl
from PIL import Image, ImageDraw, ImageFont
import mmap
import os

fb: any
mm: any
screen_width=640
screen_height=480
bytes_per_pixel = 4
screen_size = screen_width * screen_height * bytes_per_pixel

fontFile = {}
fontFile[15] = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", 15)
fontFile[13] = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", 13)
fontFile[11] = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", 11)
colorBlue = "#bb7200"
colorBlueD1 = "#7f4f00"
colorGray = "#292929"
colorGrayL1 = "#383838"
colorGrayD2 = "#141414"

activeImage: Image.Image
activeDraw: ImageDraw.ImageDraw

def screen_reset():
	ioctl(fb, 0x4601, b'\x80\x02\x00\x00\xe0\x01\x00\x00\x80\x02\x00\x00\xc0\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00^\x00\x00\x00\x96\x00\x00\x00\x00\x00\x00\x00\xc2\xa2\x00\x00\x1a\x00\x00\x00T\x00\x00\x00\x0c\x00\x00\x00\x1e\x00\x00\x00\x14\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
	ioctl(fb, 0x4611, 0)

def draw_start():
	global fb, mm
	fb = os.open('/dev/fb0', os.O_RDWR)
	mm = mmap.mmap(fb, screen_size)

def draw_end():
	global fb, mm
	mm.close()
	os.close(fb)

def crate_image():
	image = Image.new('RGBA', (screen_width, screen_height), color='black')
	return image

def draw_active(image):
	global activeImage, activeDraw
	activeImage = image
	activeDraw = ImageDraw.Draw(activeImage)

def draw_paint():
	global activeImage
	mm.seek(0)
	mm.write(activeImage.tobytes())

def draw_clear():
	global activeDraw
	activeDraw.rectangle([0, 0, screen_width, screen_height], fill='black')

def draw_text(position, text, font=15, color='white', **kwargs):
	global activeDraw
	activeDraw.text(position, text, font=fontFile[font], fill=color, **kwargs)

def draw_rectangle(position, fill=None, outline=None, width=1):
	global activeDraw
	activeDraw.rectangle(position, fill=fill, outline=outline, width=width)

def draw_rectangle_r(position, radius, fill=None, outline=None):
	global activeDraw
	activeDraw.rounded_rectangle(position, radius, fill=fill, outline=outline)

def draw_circle(position, radius, fill=None, outline='white'):
	global activeDraw
	activeDraw.ellipse([position[0]-radius, position[1]-radius, position[0]+radius, position[1]+radius], fill=fill, outline=outline)

def draw_log(text, fill="Black", outline="black"):
	draw_rectangle_r([170, 200, 470, 280], 5, fill=fill, outline=outline)
	draw_text((175, 230), text)
 
def swap_red_blue(image):
	r, g, b, a = image.split()
	return Image.merge("RGBA", (b, g, r, a))

def draw_image(image_path, size=(screen_width, screen_height), position=(0, 0)):
	"""Load a PNG image, resize it, and draw it at a specified position on the framebuffer."""
	global activeImage
	try:
		# Load the image
		img = Image.open(image_path).convert("RGBA")
		print(img)		
		# Resize the image to the specified size
		img = img.resize(size, Image.ANTIALIAS)
		img = swap_red_blue(img)
		# Create a new image for drawing
		activeImage.paste(img, position)
		
		# Paint the image onto the framebuffer
		draw_paint()
		
	except Exception as e:
		print(f"Error loading or drawing image: {e}")
	
def draw_button(pos, button, text):
	draw_circle(pos, 15, fill=colorBlueD1, outline=None)
	draw_text(pos, button, anchor="mm")
	draw_text((pos[0] + 20, pos[1]), text, font=13, anchor="lm")

def draw_row(text, pos, width, selected):
	draw_rectangle_r([pos[0], pos[1], pos[0]+width, pos[1]+32], 5, fill=(colorBlue if selected else colorGrayL1))
	draw_text((pos[0]+5, pos[1] + 5), text)

def draw_list(arr,selected_position,max_elem = 11):
	start_idx = int(selected_position / max_elem) * max_elem
	end_idx = start_idx + max_elem
	for i, c in enumerate(arr[start_idx:end_idx]):
		draw_row(c, (20, 50 + (i * 35)), 600, i == (selected_position % max_elem))

def draw_half_list(arr,selected_position,max_elem = 11):
	start_idx = int(selected_position / max_elem) * max_elem
	end_idx = start_idx + max_elem
	for i, c in enumerate(arr[start_idx:end_idx]):
		draw_row(c, (20, 50 + (i * 35)), 300, i == (selected_position % max_elem))
	# cut out the overflow of text
	draw_rectangle_r([400, 40, 630, 440], 0, fill=colorGrayD2, outline=None)
	draw_rectangle_r([10, 40, 20, 440], 0, fill=colorGrayD2, outline=None)
	draw_rectangle_r([0, 40, 9, 440], 0, fill="#000000", outline=None)



draw_start()
screen_reset()

imgMain = crate_image()
draw_active(imgMain)
