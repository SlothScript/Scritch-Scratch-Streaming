import pyautogui
import scratchattach as sa
import math

# Login to Scratch session and connect to cloud
session = sa.login_by_id(".eJxVkEFvgzAMhf8L540RGgj0Vg7drZUmrdpOUUickgFxR4Iqbdp_nyNxqeLTe87nZ_9ma4DFqxmyfRYmjINBNBOE7CmLOIInuTKKl5YeVxUXpunrQjeV4aLasbKwxf4U6yCPR_3effTr1L1e9OFyPnPOvpEwE16df3Y3IrVtzliTs6LJSybIk2qNg0wRpDNpFDFFKRqyzJfyV5TRzfCDPsU7zLA4rV5OcJefuIyP_wcVBmpSSlvbUzVatJQZ-qpthRW13dW1ptTJsqZM-0GIGnF0CX4nIJhHZK80XSDlShr4SNOjQ59vRsjf4DZtYrc1__0DuGluxw:1tFLLs:SW4srBrZZO9OdExXfVKFSXUqxxw")
cloud = session.connect_scratch_cloud("1101456934")
events = cloud.events()

RES = 10  # Resolution scaling factor
SEPARATOR = ""  # Predefined numeric separator

def screen_capture():
    # Capture a screenshot and resize
    screenshot = pyautogui.screenshot()
    image = screenshot.resize((480 // RES, 360 // RES))
    
    pixels = []
    colors = []
    
    # Process pixels into numeric format
    for y in range(360 // RES):
        for x in range(480 // RES):
            pixel = image.getpixel((x, y))
            r, g, b = (pixel[:3] if len(pixel) == 4 else pixel)
            color = (round(r / 255), round(g / 255), round(b / 255))
            
            if color in colors:
                pixels.append(str(colors.index(color)))
            else:
                pixels.append(str(len(colors)))
                colors.append(color)
    
    # Save the image for debugging purposes
    image.save("screenshot.png")
    
    # Convert colors to a numeric representation
    numeric_colors = [str(r * 1000000 + g * 1000 + b) for r, g, b in colors]
    color_data = SEPARATOR.join(numeric_colors)
    pixel_data = SEPARATOR.join(pixels)
    compressed = f"{color_data}{SEPARATOR}{pixel_data}"
    
    # Convert the entire compressed data to ASCII numeric
    numeric_data = SEPARATOR.join(str(ord(c)) for c in compressed)
    return numeric_data

chunkStep = 0

encodedScreen = screen_capture()

total_chunks = 14
chunk_size = len(encodedScreen) // total_chunks

print("Estimated optimal chunk size: " + str(math.ceil((chunk_size / 256) * total_chunks)))

if chunk_size > 256:
    print("Chunk size to large, increase number of chunks. Chunk size: " + str(chunk_size) + ", estimated new size: " + str(math.ceil((chunk_size / 256) * total_chunks)))
    exit()

chunks = [
    encodedScreen[i * chunk_size:(i + 1) * chunk_size] 
    for i in range(total_chunks - 1)
]
chunks.append(encodedScreen[(total_chunks - 1) * chunk_size:])  # Add remaining data

@events.event
def on_set(act):
    if act.var == "action":
        if act.value == "1":
            if chunkStep == 0:
                encodedScreen = screen_capture()
            
            cloud.set_var("chunks", len(chunks))  # Inform Scratch of the number of chunks
            cloud.set_var("chunkSize", chunk_size)  # Inform Scratch of chunk size
            
            cloud.set_var("data", chunks[chunkStep])
            cloud.set_var("action", "0")

# Start listening to cloud events
events.start()