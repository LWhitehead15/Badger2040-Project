import time
import badger2040
import badger_os

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

IMAGE_WIDTH = 104

COMPANY_HEIGHT = 30
DETAILS_HEIGHT = 20
NAME_HEIGHT = HEIGHT - COMPANY_HEIGHT - (DETAILS_HEIGHT * 2) - 2
TEXT_WIDTH = WIDTH - IMAGE_WIDTH - 11

COMPANY_TEXT_SIZE = 0.6
DETAILS_TEXT_SIZE = 0.5

LEFT_PADDING = 5
NAME_PADDING = 20
DETAIL_SPACING = 10

DEFAULT_TEXT = """Fancy Fruit
Mango Birb

CS Student/Designer

mangobirb.carrd.co"""

BADGE_IMAGE = bytearray(int(IMAGE_WIDTH * HEIGHT / 8))

current_state = 1
total_states = 3

current_image = 1
total_images = 7


#      Utility functions

# Reduce the size of a string until it fits within a given width
def truncatestring(text, text_size, width):
    while True:
        length = display.measure_text(text, text_size)
        if length > 0 and length > width:
            text = text[:-1]
        else:
            text += ""
            return text

def imageswap(imagename):
    try:
        global BADGE_IMAGE
        open(imagename, "rb").readinto(BADGE_IMAGE)
    except OSError:
        try:
            import badge_image
            BADGE_IMAGE = bytearray(badge_image.data())
            del badge_image
        except ImportError:
            pass
    return BADGE_IMAGE

#      Drawing functions

def draw_badge_menu():
    # Top Arrow (Side panel) - REDO
    display.pen(15)
    display.rectangle(WIDTH - 10, 0, 11, 128) # top arrow
    #display.line(WIDTH, 1, WIDTH, HEIGHT)
    display.pen(0)
    if(current_state >= total_states):
        display.rectangle(WIDTH - 7, 28, 7, 7) # top arrow
    if(current_state == 2):
        display.rectangle(WIDTH - 7, 28, 7, 7) # top arrow
        display.rectangle(WIDTH - 7, 90, 7, 7) # top arrow
    if(current_state < total_states):
        display.rectangle(WIDTH - 7, 90, 7, 7) # top arrow


def draw_badge_1():
    display.pen(0)
    display.clear()
    
    draw_badge_menu()

    # Draw badge image
    display.image(BADGE_IMAGE, IMAGE_WIDTH, HEIGHT, WIDTH - IMAGE_WIDTH - 10, 0)

    # Draw a border around the image
    display.pen(0)
    display.thickness(1)
    display.line(WIDTH - IMAGE_WIDTH-10, 0, WIDTH - 10, 0)
    display.line(WIDTH - IMAGE_WIDTH-10, 0, WIDTH - IMAGE_WIDTH-10, HEIGHT - 1)
    display.line(WIDTH - IMAGE_WIDTH-10, HEIGHT - 1, WIDTH - 10, HEIGHT - 1)
    display.line(WIDTH - 10, 0, WIDTH - 10, HEIGHT - 1)

    # Draw the company
    display.pen(15)  # Change this to 0 if a white background is used
    display.font("sans")
    display.thickness(2)
    display.text(company, LEFT_PADDING, (COMPANY_HEIGHT // 2) + 1, COMPANY_TEXT_SIZE)

    # Draw a white background behind the name
    display.pen(15)
    display.thickness(1)
    display.rectangle(1, COMPANY_HEIGHT + 1, TEXT_WIDTH, NAME_HEIGHT)

    # Draw the name, scaling it based on the available width
    display.pen(0)
    display.font("sans")
    display.thickness(4)
    name_size = 2.0  # A sensible starting scale
    while True:
        name_length = display.measure_text(name, name_size)
        if name_length >= (TEXT_WIDTH - NAME_PADDING) and name_size >= 0.1:
            name_size -= 0.01
        else:
            display.text(name, (TEXT_WIDTH - name_length) // 2, (NAME_HEIGHT // 2) + COMPANY_HEIGHT + 1, name_size)
            break

    # Draw a white backgrounds behind the details
    display.pen(15)
    display.thickness(1)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT * 2, TEXT_WIDTH, DETAILS_HEIGHT - 1)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT, TEXT_WIDTH, DETAILS_HEIGHT - 1)

    # Draw the first detail's title and text
    display.pen(0)
    display.font("sans")
    display.thickness(2)
    name_length = display.measure_text(detail1_title, DETAILS_TEXT_SIZE)
    display.text(detail1_title, LEFT_PADDING, HEIGHT - ((DETAILS_HEIGHT * 3) // 2), DETAILS_TEXT_SIZE)
    display.thickness(2)
    display.text(detail1_text, 5 + name_length + DETAIL_SPACING, HEIGHT - ((DETAILS_HEIGHT * 3) // 2), DETAILS_TEXT_SIZE)

    # Draw the second detail's title and text
    display.thickness(2)
    name_length = display.measure_text(detail2_title, DETAILS_TEXT_SIZE)
    display.text(detail2_title, LEFT_PADDING, HEIGHT - (DETAILS_HEIGHT // 2), DETAILS_TEXT_SIZE)
    display.thickness(2)
    display.text(detail2_text, LEFT_PADDING + name_length + DETAIL_SPACING, HEIGHT - (DETAILS_HEIGHT // 2), DETAILS_TEXT_SIZE)

def draw_badge_2():
    display.pen(0)
    display.clear()
    
    draw_badge_menu()
    # Draw badge image
    display.image(BADGE_IMAGE, IMAGE_WIDTH, HEIGHT, 0, 0)
    display.line(WIDTH - 10, 0, WIDTH - 10, HEIGHT)
    
    # Draw a border around the image
    display.pen(0)
    display.thickness(1)
    display.line(0, 0, IMAGE_WIDTH, 0) #top
    display.line(0, 0, 0, HEIGHT - 1) #left
    display.line(0, HEIGHT - 1, IMAGE_WIDTH, HEIGHT - 1) #bottom
    display.line(IMAGE_WIDTH - 1, 0, IMAGE_WIDTH - 1, HEIGHT - 1) #right
    
    # Extra border
    display.pen(15)
    
    USEABLE_AREA_X = IMAGE_WIDTH
    USEABLE_AREA_Y = 1
    USEABLE_AREA_WIDTH = (WIDTH - IMAGE_WIDTH) - 10
    USEABLE_AREA_HEIGHT = HEIGHT - 2
    
    display.font("sans")
    display.thickness(2)
    badge_title = 'Details:'
    badge_size = DETAILS_TEXT_SIZE
    name_length = display.measure_text(badge_title, badge_size)
    badge_height = 24
    display.rectangle(IMAGE_WIDTH, 1, USEABLE_AREA_WIDTH, badge_height) # top arrow
    display.pen(0)
    display.text(badge_title, USEABLE_AREA_X + 2, 14, 0.8)
    
    room_title = 'Over 18'
    room_size = 0.6
    room_height = 36
    room_length = display.measure_text(room_title, room_size)
    display.pen(15)
    display.text(room_title, USEABLE_AREA_X + 2, 48, room_size)
    
    display.pen(15)
    display.rectangle(IMAGE_WIDTH + room_length + DETAIL_SPACING, 27, USEABLE_AREA_WIDTH - room_length - LEFT_PADDING - 5, room_height)
    
    room_num_size = 0.8
    display.pen(0)
    display.thickness(2)
    display.text('Gay', LEFT_PADDING + IMAGE_WIDTH + room_length + DETAIL_SPACING, 46, room_num_size)
    
    display.pen(15)
    badge_detail_1_height = ((USEABLE_AREA_HEIGHT - badge_height - room_height - 9)//2) + 1
    badge_detail_1_size = 0.6
    badge_detail_1_title = 'Species |'
    badge_detail_1_title_length = display.measure_text(badge_detail_1_title, badge_detail_1_size)
    badge_detail_1_value = 'Sun Conure'
    badge_detail_1_text_line = badge_height + badge_detail_1_height + (badge_detail_1_height // 2) + 12
    
    display.rectangle(IMAGE_WIDTH + 1, badge_height + room_height + 5, USEABLE_AREA_WIDTH - 1, badge_detail_1_height)
    display.pen(0)
    display.text(badge_detail_1_title, USEABLE_AREA_X + 2, badge_detail_1_text_line, badge_detail_1_size)
    display.text(badge_detail_1_value, LEFT_PADDING + 4 + IMAGE_WIDTH + badge_detail_1_title_length, badge_detail_1_text_line, 0.5)
    
    display.pen(15)
    badge_detail_2_height = ((USEABLE_AREA_HEIGHT - badge_height - room_height - 8)//2) + 2
    display.rectangle(IMAGE_WIDTH + 1, (badge_height + room_height + 5) + ((USEABLE_AREA_HEIGHT - badge_height - room_height - 7)//2) + 2, USEABLE_AREA_WIDTH - 1, badge_detail_2_height)
    
    badge_detail_2_size = 0.5
    badge_detail_2_title = 'Pronouns |'
    badge_detail_2_title_length = display.measure_text(badge_detail_2_title, badge_detail_2_size)
    badge_detail_2_value = 'He/Him'
    badge_detail_2_text_line = badge_height + badge_detail_1_height + badge_detail_2_height + (badge_detail_2_height // 2) + 14
    
    display.pen(0)
    display.text(badge_detail_2_title, USEABLE_AREA_X + 2, badge_detail_2_text_line, badge_detail_2_size)
    display.text(badge_detail_2_value, LEFT_PADDING + IMAGE_WIDTH + badge_detail_2_title_length, badge_detail_2_text_line, 0.6)
    
def draw_badge_3():
    display.pen(0)
    display.clear()
    
    draw_badge_menu()

    # Draw badge image
    display.image(BADGE_IMAGE, IMAGE_WIDTH, HEIGHT, WIDTH - IMAGE_WIDTH - 10, 0)

    # Draw a border around the image
    display.pen(0)
    display.thickness(1)
    display.line(WIDTH - IMAGE_WIDTH-10, 0, WIDTH - 10, 0)
    display.line(WIDTH - IMAGE_WIDTH-10, 0, WIDTH - IMAGE_WIDTH-10, HEIGHT - 1)
    display.line(WIDTH - IMAGE_WIDTH-10, HEIGHT - 1, WIDTH - 10, HEIGHT - 1)
    display.line(WIDTH - 10, 0, WIDTH - 10, HEIGHT - 1)

    # Draw the company
    display.pen(15)  # Change this to 0 if a white background is used
    display.font("serif_italic")
    display.thickness(2)
    display.text("University Of Lincoln", LEFT_PADDING, (COMPANY_HEIGHT // 2) + 1, 0.48)

    # Draw a white background behind the name
    display.pen(15)
    display.thickness(1)
    display.rectangle(1, COMPANY_HEIGHT + 1, TEXT_WIDTH, NAME_HEIGHT)

    # Draw the name, scaling it based on the available width
    display.pen(0)
    display.font("sans")
    display.thickness(3)
    name_size = 2.0  # A sensible starting scale
    while True:
        name_length = display.measure_text("Liam Whitehead", name_size)
        if name_length >= (TEXT_WIDTH - NAME_PADDING) and name_size >= 0.1:
            name_size -= 0.01
        else:
            display.text("Liam Whitehead", (TEXT_WIDTH - name_length) // 2, (NAME_HEIGHT // 2) + COMPANY_HEIGHT + 1, name_size)
            break

    # Draw a white backgrounds behind the details
    display.pen(15)
    display.thickness(1)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT * 2, TEXT_WIDTH, DETAILS_HEIGHT - 1)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT, TEXT_WIDTH, DETAILS_HEIGHT - 1)

    # Draw the first detail's title and text
    display.pen(0)
    display.font("sans")
    display.thickness(2)
    name_length = display.measure_text(detail1_title, DETAILS_TEXT_SIZE)
    display.text(detail1_title, LEFT_PADDING, HEIGHT - ((DETAILS_HEIGHT * 3) // 2), DETAILS_TEXT_SIZE)
    display.thickness(2)
    display.text(detail1_text, 10 + name_length, HEIGHT - ((DETAILS_HEIGHT * 3) // 2), DETAILS_TEXT_SIZE)

    # Draw the second detail's title and text
    display.thickness(2)
    name_length = display.measure_text(detail2_title, DETAILS_TEXT_SIZE)
    display.text(detail2_title, LEFT_PADDING, HEIGHT - (DETAILS_HEIGHT // 2), DETAILS_TEXT_SIZE)
    display.thickness(1)
    display.text("Liam.P.Whitehead@gmail.com", LEFT_PADDING + name_length, HEIGHT - (DETAILS_HEIGHT // 2), 0.40)
    
# Draw the badge, including user text
def draw_badge():
    if current_state == 1:
        draw_badge_1()
    if current_state == 2:
        draw_badge_2()
    if current_state == 3:
        draw_badge_3()
        
def select_image():
    # each index is a different image
    if current_image == 1:
        BADGE_IMAGE = imageswap("badge-image.bin")
    if current_image == 2:
        BADGE_IMAGE = imageswap("badge-image_2.bin")
    if current_image == 3:
        BADGE_IMAGE = imageswap("badge-image_3.bin")
    if current_image == 4:
        BADGE_IMAGE = imageswap("badge-image_4.bin")
    if current_image == 5:
        BADGE_IMAGE = imageswap("badge-image_5.bin")
    if current_image == 6:
        BADGE_IMAGE = imageswap("badge-image_6.bin")
    if current_image == 7:
        BADGE_IMAGE = imageswap("badge-image_7.bin")
    return BADGE_IMAGE
        
#        Program setup

# Create a new Badger and set it to update NORMAL
display = badger2040.Badger2040()
display.led(128)
display.update_speed(badger2040.UPDATE_NORMAL)

# Open the badge file
try:
    badge = open("badge.txt", "r")
except OSError:
    with open("badge.txt", "w") as f:
        f.write(DEFAULT_TEXT)
        f.flush()
    badge = open("badge.txt", "r")

# Read in the next 6 lines
company = badge.readline()        
name = badge.readline()           
detail1_title = badge.readline()  
detail1_text = badge.readline()   
detail2_title = badge.readline()  
detail2_text = badge.readline()  

# Truncate all of the text (except for the name as that is scaled)
company = truncatestring(company, COMPANY_TEXT_SIZE, TEXT_WIDTH)

detail1_title = truncatestring(detail1_title, DETAILS_TEXT_SIZE, TEXT_WIDTH)
detail1_text = truncatestring(detail1_text, DETAILS_TEXT_SIZE,
                              TEXT_WIDTH - DETAIL_SPACING - display.measure_text(detail1_title, DETAILS_TEXT_SIZE))

detail2_title = truncatestring(detail2_title, DETAILS_TEXT_SIZE, TEXT_WIDTH)
detail2_text = truncatestring(detail2_text, DETAILS_TEXT_SIZE,
                              TEXT_WIDTH - DETAIL_SPACING - display.measure_text(detail2_title, DETAILS_TEXT_SIZE))



#       Main program

select_image()

draw_badge()
display.update()
do_update = 0

while True:
    if display.pressed(badger2040.BUTTON_A):
        if (current_state < 3):
            # preserve loop of images
            if(current_image >= 1):
                current_image += 1
                do_update = 1
            if (current_image > total_images):
                current_image = 1
        else:
            if(current_image >= 6):
                current_image += 1
                do_update = 1
            if (current_image > total_images):
                current_image = 6
    
    if display.pressed(badger2040.BUTTON_UP):
        # increase current state
        if(current_state > 1):
            current_state -= 1
            do_update = 1

    if display.pressed(badger2040.BUTTON_DOWN):
        # decrease button state
        if(current_state < 3):
            current_state += 1
            do_update = 1
    
    if(do_update):
        if (current_state >= 3) and (current_image < 6):
            current_image = 6
        elif (current_state < 3) and (current_image >= 6):
            current_image = 1
        
        # get current image
        select_image()
        #draw badge
        draw_badge()
        display.update()
        do_update = 0


    # If on battery, halt the Badger to save power, it will wake up if any of the front buttons are pressed
    display.halt()
