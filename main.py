from tkinter import *
from tkinter import filedialog as fd
from PIL import Image, ImageTk, ImageDraw, ImageFont

BKG_COLOR = '#151224'
FRG_COLOR = '#C70039'
ABSOLUTE_PATH = 'C:/Users/Demel/Documents/Python_Projects/Image_Watermarking_Desktop_App/'
# cache refs
font = 'Helvetica'
file_name = ''
image_file_types = [("All Files", "*.*"), ("PNG files", "*.png"), ("JPG files", "*.jpg*"), ("GIF files", "*.gif"),
                    ("TIFF files", "*.tiff")]
window: Tk
water_mark_logo: Label
browse_but: Button
image_frame: Frame
image: Image

# water_mark cache refs
water_mark: StringVar
transparency: IntVar
x_pos: IntVar
y_pos: IntVar

frame_width = 750
frame_height = 450
# # Design
# My Program Will Have Two Different States (Dark Grey BackGround With Red Borders Theme)
# - Start-Up State Where It Welcomes A User Then There Is A Button Prompting Using
#   To Locate The Image
# - Image Editing State That Will Have Sliders And Text Inputs To Watermark Image

# Functionality For Image Editing State
#  - Buttons That Will Create A Popup Window To Explain What The Specific Slider Does
#  - Sliders That Change Opacity, The Number Of Watermarks That Gets Added To Image, Color(Text Watermark)
#  - Back Button To Go Back To The Start-Up State
#  - Save Button THat Prompts a File Dialog To Store At A Specific Location


# -- Ideas____
# - Image template section
# - Invert location of watermark x and y buttons

def start_program():
    global window
    global water_mark_logo
    global browse_but

    window = Tk()
    window.config(bg=BKG_COLOR)
    window.minsize(width=400, height=150)

    water_mark_logo = Label(font=(font, 18, 'bold'), fg=FRG_COLOR, bg=BKG_COLOR, text="~ Image Watermarker ~")
    water_mark_logo.place(anchor=CENTER, x=200, y=75)
    browse_but = Button(window, text="Start", command=find_file)
    browse_but.place(anchor=CENTER, x=200, y=125)

    window.mainloop()


# Find The File Using A File Dialog
def find_file():
    global file_name
    file_name = fd.askopenfilename(filetypes=image_file_types)
    water_mark_logo.place_forget()
    browse_but.place_forget()
    # window.geometry('900x700')
    window.state('zoomed')
    text_image_editing_state()


# Change From Start Screen To Image Editor
def text_image_editing_state():
    global water_mark, transparency, x_pos, y_pos, image_frame
    water_mark = StringVar()
    transparency = IntVar()
    x_pos = IntVar()
    y_pos = IntVar()
    x_pos.set(int(frame_width/2))
    y_pos.set(int(frame_height/2))

    # - Create A Frame With To Hold The Image In
    image_frame = Frame(window, width=frame_width, height=frame_height, borderwidth=4, relief='raised')
    image_frame.grid(column=1, row=1, columnspan=2, padx=(30, 30), pady=(30, 5))

    # - Text Input Box
    water_mark_label = Label(window, text='Water Mark')
    water_mark_label.grid(column=1, row=2, padx=(5, 10))  # Test # 0 padding on left and 10 pixel adding on right

    water_mark_entry = Entry(window, textvariable=water_mark)
    water_mark_entry.grid(column=2, row=2)

    # - Opacity slider
    # TODO # Edit Scale Appearance
    transparency_slider_label = Label(window, text='Transparency')
    transparency_slider_label.grid(column=1, row=3, padx=(8, 10))

    transparency_slider = Scale(window, orient=HORIZONTAL, length=200, from_=0, to=255, variable=transparency)
    transparency_slider.grid(column=2, row=3)

    # - X Pos Sliders (based on the image size)
    # TODO # Edit Scale Appearance
    xpos_slider_label = Label(window, text='X-Position')
    xpos_slider_label.grid(column=3, row=2, padx=(20, 10))

    xpos_slider = Scale(window, orient=HORIZONTAL, length=200, from_=0, to=frame_width, variable=x_pos)
    xpos_slider.grid(column=4, row=2)

    # - Y Pos Sliders (based on the image size)
    # TODO # Edit Scale Appearance
    ypos_slider_label = Label(window, text='Y-Position')
    ypos_slider_label.grid(column=3, row=3, padx=(20, 10))

    ypos_slider = Scale(window, orient=HORIZONTAL, length=200, from_=0, to=frame_height, variable=y_pos)
    ypos_slider.grid(column=4, row=3)

    # - User Help Buttons to explain the tools

    # TODO # Add User Help Buttons

    # - Back Button To Take User TO Start Screen
    back_but = Button(window, text='Menu')
    back_but.grid(column=5, row=2, padx=(30, 10))

    # - Save Button To Save The Image
    save_but = Button(window, text='Save')
    save_but.grid(column=5, row=3, padx=(30, 10))

    update_text_image()


# Update Image
def update_text_image():
    global image
    # print(f'Water Mark: {water_mark.get()}, Transparency: {transparency.get()}, X-Position: {x_pos.get()}'
    #       f', Y-Position: {y_pos.get()},\n Image Path: {file_name}')

    # Open image using Pillow
    image = Image.open(file_name)

    # Resize Image
    resized_image = image.resize((int(image_frame.winfo_screenwidth() / 2), int(image_frame.winfo_screenheight() / 2)),
                                 resample=Image.LANCZOS)

    # Draw Image So It Is Editable
    im = ImageDraw.Draw(resized_image)
    mf = ImageFont.load_default()

    # Add Text to an image
    im.text((x_pos.get(), y_pos.get()), f'{water_mark.get()}', (255, 255, 255, transparency.get()), font=mf)

    # Saving Edited Image
    resized_image.save('images/updated_image.png')

    # Displaying Edited Image
    display_image()

    # Update Image
    window.after(1000, update_text_image)


def display_image():
    # Open Edited Image
    edited_image = Image.open('images/updated_image.png')
    updated_image = ImageTk.PhotoImage(edited_image)
    image_frame.updated_image = updated_image

    # Create A Label
    displayed_image = Label(image_frame, image=updated_image)
    image_frame.displayed_image = displayed_image

    # Place Image
    displayed_image.grid(column=1, row=1, padx=(5, 5), pady=(5, 5))

    # Remove Image For A New One
    displayed_image.pack_forget()


start_program()
