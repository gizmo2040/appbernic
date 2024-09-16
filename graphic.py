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


def swap_red_blue_hex(hex_color):
	# Remove the leading '#' if present
	hex_color = hex_color.lstrip('#')

	# Ensure the hex color is 6 characters long
	if len(hex_color) != 6:
		raise ValueError("Invalid hex color format. Must be a 6-digit hex color.")

	# Extract red, green, and blue components from the hex color
	r = hex_color[0:2]
	g = hex_color[2:4]
	b = hex_color[4:6]

	# Swap red and blue components
	swapped_hex_color = f"#{b}{g}{r}"

	return swapped_hex_color

fontFile = {}
fontFile[15] = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", 15)
fontFile[13] = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", 13)
fontFile[11] = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", 11)

theme_matrix = {
	"colors": {
     "primary": "#007211",
     "primaryDark": "#004b00",
     "secondary": "#292929",
     "background": "#112211",
     "background1": "#112211",
     "background2": "#000000",
     "text": "#ffffff",
     "textDark": "#000000",
     "textLight": "#ffffff",
     "outline":"#008b00"
    }
}

theme_original = {
	"colors": {
     "primary": "#0072bb",
     "primaryDark": "#004f7f",
     "secondary": "#292929",
     "background": "#292929",
     "background1": "#383838",
     "background2": "#141414",
     "text": "#ffffff",
     "textDark": "#000000",
     "textLight": "#ffffff",
     "outline":None
    }
}
theme_yellow = {
	"colors": {
     "primary": "#bb7200",
     "primaryDark": "#7f4f00",
     "secondary": "#292929",
     "background": "#292929",
     "background1": "#383838",
     "background2": "#141414",
     "text": "#ffffff",
     "textDark": "#000000",
     "textLight": "#ffffff",
     "outline":None
    }
}
theme_red = {
	"colors": {
     "primary": "#720000",
     "primaryDark": "#440000",
     "secondary": "#292929",
     "background": "#292929",
     "background1": "#383838",
     "background2": "#141414",
     "text": "#ffffff",
     "textDark": "#000000",
     "textLight": "#ffffff",
     "outline":None
    }
}

current_theme = 0
theme_list = [theme_matrix,theme_original,theme_yellow,theme_red]
activeImage: Image.Image
activeDraw: ImageDraw.ImageDraw


def set_theme(theme_index):
	global theme, colorBlue, colorBlueD1, colorGray, colorGrayL1, colorGrayD2,current_theme
	# check index in range
	if theme_index < 0 or theme_index >= len(theme_list):
		return
	current_theme = theme_index
	theme = theme_list[theme_index]
	colorBlue = swap_red_blue_hex(theme["colors"]["primary"])
	colorBlueD1 = swap_red_blue_hex(theme["colors"]["primaryDark"])
	colorGray = swap_red_blue_hex(theme["colors"]["background"])
	colorGrayL1 = swap_red_blue_hex(theme["colors"]["background1"])
	colorGrayD2 = swap_red_blue_hex(theme["colors"]["background2"])

set_theme(current_theme)

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
	global activeDraw,theme
	outline=theme["colors"]["outline"]
	activeDraw.rectangle(position, fill=fill, outline=outline, width=width)

def draw_rectangle_r(position, radius, fill=None, outline=theme["colors"]["outline"]):
	global activeDraw,theme
	outline=theme["colors"]["outline"]
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


def draw_image(image_path, size=(screen_width, screen_height), position=(0, 0), anchor="nw"):
	"""Load a PNG image, resize it maintaining aspect ratio, and draw it at a specified position on the framebuffer."""
	global activeImage
	max_size = size
	try:
		# Load the image
		img = Image.open(image_path).convert("RGBA")
		# Calculate the new size maintaining aspect ratio
		original_width, original_height = img.size
		max_width, max_height = max_size
		aspect_ratio = original_width / original_height
		
		if original_width < original_height:
			new_width = min(original_width, max_width)
			new_height = int(new_width / aspect_ratio)
		else:
			new_height = min(original_height, max_height)
			new_width = int(new_height * aspect_ratio)
		
		# Resize the image to the new size
		img = img.resize((new_width, new_height), Image.ANTIALIAS)
		img = swap_red_blue(img)
		# Adjust position based on anchor
		x, y = position
		if anchor == "mm":  # middle-middle
			x -= new_width // 2
			y -= new_height // 2
		elif anchor == "lm":  # left-middle
			y -= new_height // 2
		elif anchor == "rm":  # right-middle
			x -= new_width
			y -= new_height // 2
		elif anchor == "tm":  # top-middle
			x -= new_width // 2
		elif anchor == "bm":  # bottom-middle
			x -= new_width // 2
			y -= new_height
		elif anchor == "tr":  # top-right
			x -= new_width
		elif anchor == "br":  # bottom-right
			x -= new_width
			y -= new_height
		elif anchor == "bl":  # bottom-left
			y -= new_height
		
		# Create a new image for drawing
		activeImage.paste(img, (x, y))
		
		# Paint the image onto the framebuffer
		draw_paint()
		
	except Exception as e:
		print(f"Error loading or drawing image: {e}")

def draw_tabs(tablist, selected,  size=(640, 40),position=(0, 0)):
    global colorGray, colorBlue
    x_offset, y_offset = position
    width, height = size
    tab_width = width / len(tablist)
    for i, tab in enumerate(tablist):
        x_start = x_offset + i * tab_width
        x_end = x_offset + (i + 1) * tab_width
        draw_rectangle([x_start, y_offset, x_end, y_offset + height], fill=colorGray)
        if i == selected:
            draw_rectangle([x_start, y_offset, x_end, y_offset + height], fill=colorBlue)
        draw_text((x_start + tab_width / 2, y_offset + height / 2), tab, anchor="mm")

def draw_image_old(image_path, size=(screen_width, screen_height), position=(0, 0)):
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
	
def draw_button(pos, button, text,fill=None):
	global theme,colorBlue
	fill = colorBlue
	draw_circle(pos, 15, fill=fill, outline=None)
	draw_text(pos, button, anchor="mm")
	draw_text((pos[0] + 20, pos[1]), text, font=13, anchor="lm")

def draw_row(text, pos, width, selected):
	global colorBlue, colorGrayL1
	draw_rectangle_r([pos[0], pos[1], pos[0]+width, pos[1]+32], 5, fill=(colorBlue if selected else colorGrayL1))
	draw_text((pos[0]+5, pos[1] + 5), text)

def draw_list(arr,selected_position,max_elem = 11):
	start_idx = int(selected_position / max_elem) * max_elem
	end_idx = start_idx + max_elem
	for i, c in enumerate(arr[start_idx:end_idx]):
		draw_row(c, (20, 50 + (i * 35)), 600, i == (selected_position % max_elem))

def draw_half_list(arr,selected_position,max_elem = 11):
	global colorGrayD2
	start_idx = int(selected_position / max_elem) * max_elem
	end_idx = start_idx + max_elem
	for i, c in enumerate(arr[start_idx:end_idx]):
		draw_row(c, (20, 50 + (i * 35)), 290, i == (selected_position % max_elem))
	# cut out the overflow of text
	activeDraw.rectangle([311, 41, 629, 439] , fill=colorGrayD2, outline=None)
	#draw_rectangle([310, 40, 630, 440],  fill=colorGrayD2, outline=None)
	#draw_rectangle([10, 40, 20, 440],  fill=colorGrayD2, outline=None)
	#draw_rectangle([0, 40, 9, 440],  fill="#000000", outline=None)

def draw_reticle(px=10,position=(0, 0), size=(screen_width, screen_height), color=(80,80, 80, 30)):
    """Draw a reticle at the specified position to help place elements during development."""
    x, y = position # todo: implement position
    width, height = size
    
    # Draw horizontal lines every 10 pixels
    for i in range(0, height, px):
        draw_rectangle([0, i, width, i], fill=color, outline=None)
    
    # Draw vertical lines every 10 pixels
    for i in range(0, width, px):
        draw_rectangle([i, 0, i, height], fill=color, outline=None)



draw_start()
screen_reset()

imgMain = crate_image()
draw_active(imgMain)
