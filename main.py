import tkinter
from tkinter import *
from tkinter import filedialog as fd
from PIL import Image, ImageTk, ImageDraw, ImageFont

BKG_COLOR = '#151224'
FRG_COLOR = '#C70039'
ABSOLUTE_PATH = 'C:/Users/Demel/Documents/Python_Projects/Image_Watermarking_Desktop_App/'

# cache refs
file_directory_path = 'images'
font = 'Helvetica'
file_name = ''
image_file_types = [("All Files", "*.*"), ("PNG files", "*.png"), ("JPG files", "*.jpg*"), ("GIF files", "*.gif"),
                    ("TIFF files", "*.tiff")]

window: Tk
save_window: Toplevel
water_mark_logo: Label
start_but: Button
image_frame: Frame
image: Image
cached_image: Image

# water_mark cache refs
new_filename: StringVar
water_mark: StringVar
transparency: IntVar
x_pos: IntVar
y_pos: IntVar
image_frame: Frame
water_mark_label: Label
water_mark_entry: Entry
transparency_slider_label: Label
transparency_slider: Scale
xpos_slider_label: Label
xpos_slider: Scale
ypos_slider_label: Label
ypos_slider: Scale
back_but: Button
save_but: Button

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
    global start_but

    window = Tk()
    window.config(bg=BKG_COLOR)
    center_window(window)  # Starts Windows Of Centered

    water_mark_logo = Label(font=(font, 18, 'bold'), fg=FRG_COLOR, bg=BKG_COLOR, text="~ Image Watermarker ~")
    water_mark_logo.place(anchor=CENTER, x=200, y=75)
    start_but = Button(window, text="Start", command=text_or_image_watermark)
    start_but.place(anchor=CENTER, x=200, y=125)

    window.mainloop()


# User Option Of Text Or Image Watermark
def text_or_image_watermark():
    start_but.place_forget()
    # print(f'Screen Width: {window.winfo_width()}, Screen Height: {window.winfo_height()}')
    text_but = Button(window, text="Text WaterMark", command=find_file)
    text_but.place(anchor=CENTER, x=140, y=125)

    image_but = Button(window, text="Logo WaterMark", command=find_file)
    image_but.place(anchor=CENTER, x=260, y=125)


# Find The File Using A File Dialog
def find_file():
    global file_name
    file_name = fd.askopenfilename(filetypes=image_file_types)

    if len(file_name) > 0:
        water_mark_logo.place_forget()
        window.state('zoomed')
        text_image_editing_state()
    else:
        # TODO prompt user to make a selection to continue
        return


# Change From Start Screen To Image Editor
def text_image_editing_state():
    global water_mark, transparency, x_pos, y_pos, image_frame, water_mark_label, water_mark_entry, \
        transparency_slider_label, transparency_slider, xpos_slider_label, xpos_slider, ypos_slider_label, \
        ypos_slider, back_but, save_but
    water_mark = StringVar()
    transparency = IntVar()
    x_pos = IntVar()
    y_pos = IntVar()
    x_pos.set(int(frame_width / 2))
    y_pos.set(int(frame_height / 2))

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
    back_but = Button(window, text='Back', command=selection_screen_transition_from_editing_state)
    back_but.grid(column=5, row=2, padx=(30, 10))

    # - Save Button To Save The Image
    save_but = Button(window, text='Save', command=save_image_window)
    save_but.grid(column=5, row=3, padx=(30, 10))

    update_text_image()


# Update Image
def update_text_image():
    global image
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
    resized_image.save('images/cached_image.png')

    # Displaying Edited Image
    display_image()

    # Update Image
    window.after(1000, update_text_image)


def display_image():
    global cached_image
    # Open Edited Image
    cached_image = Image.open('images/cached_image.png')
    updated_image = ImageTk.PhotoImage(cached_image)
    image_frame.updated_image = updated_image

    # Create A Label
    displayed_image = Label(image_frame, image=updated_image)
    image_frame.displayed_image = displayed_image

    # Place Image
    displayed_image.grid(column=1, row=1, padx=(5, 5), pady=(5, 5))

    # Remove Image For A New One
    displayed_image.pack_forget()


def save_image_window():
    global save_window, new_filename
    new_filename = StringVar()
    save_window = Toplevel(window)
    save_window.config(bg=BKG_COLOR)
    save_window.title("Save File")
    center_window(save_window)
    # Create a Label in New window
    Label(save_window, text="File Name:", font='Helvetica 12 normal',
          bg=BKG_COLOR, fg=FRG_COLOR).grid(column=1, row=1, padx=(90, 5), pady=(70, 0))
    Entry(save_window, textvariable=new_filename).grid(column=2, row=1, pady=(70, 0))
    Button(save_window, text='Save', command=save_file).grid(column=1, row=2, padx=(90, 5), pady=(10, 0))
    Button(save_window, text='Cancel', command=close_save_window).grid(column=2, row=2, pady=(10, 0))


def save_file():
    # If no file name prevent this code from executing ***
    # TODO Prompt User That They Need To Enter A File Name ?????????????????????????????????????
    if len(new_filename.get()) > 1:
        # Resize the image if using tkinter frame
        cached_image.save(f'{file_directory_path}/{new_filename.get()}.png')
        for widgets in save_window.winfo_children():
            widgets.destroy()

        Label(save_window, text="Would you like to add a watermark to another image?", font='Helvetica 12 normal',
              bg=BKG_COLOR, fg=FRG_COLOR).grid(column=1, row=2, padx=(10, 5), pady=(70, 0))
        Button(save_window, text='Yes', command=selection_screen_transition_from_editing_state).grid(column=1, row=3,
                                                                                                     padx=(20, 5),
                                                                                                     pady=(10, 0))
        Button(save_window, text='No', command=close_program).grid(column=2, row=3, pady=(10, 0))
    # else:
    #     popup_label = Label(save_window, text="Please enter a file name before continuing.", font='Helvetica 12 normal',
    #                         bg=BKG_COLOR, fg='blue')
    #     popup_label.grid(column=1, row=1, padx=(10, 5), pady=(70, 0))
    #     # save_window.after(3000, popup_label.destroy())


def close_program():
    window.destroy()


def close_save_window():
    save_window.destroy()


def close_window_state_transition():
    close_save_window()
    selection_screen_transition_from_editing_state()


def selection_screen_transition_from_editing_state():
    global water_mark_logo
    image_frame.grid_forget()
    water_mark_label.grid_forget()
    water_mark_entry.grid_forget()
    transparency_slider_label.grid_forget()
    transparency_slider.grid_forget()
    xpos_slider_label.grid_forget()
    xpos_slider.grid_forget()
    ypos_slider_label.grid_forget()
    ypos_slider.grid_forget()
    back_but.grid_forget()
    save_but.grid_forget()

    window.state('normal')
    window.geometry('400x200')
    water_mark_logo = Label(font=(font, 18, 'bold'), fg=FRG_COLOR, bg=BKG_COLOR, text="~ Image Watermarker ~")
    water_mark_logo.place(anchor=CENTER, x=200, y=75)

    text_or_image_watermark()


def center_window(current_window):
    width = 400
    height = 200
    screen_width = current_window.winfo_screenwidth()  # Width of the screen
    screen_height = current_window.winfo_screenheight()  # Height of the screen

    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    current_window.geometry('%dx%d+%d+%d' % (width, height, x, y))


start_program()
