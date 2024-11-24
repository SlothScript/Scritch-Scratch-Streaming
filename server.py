import pyautogui
import scratchattach as sa
from PIL import Image
import math

session = sa.login_by_id(".eJxVkEFvgzAMhf8L540RGgj0Vg7drZUmrdpOUUickgFxR4Iqbdp_nyNxqeLTe87nZ_9ma4DFqxmyfRYmjINBNBOE7CmLOIInuTKKl5YeVxUXpunrQjeV4aLasbKwxf4U6yCPR_3effTr1L1e9OFyPnPOvpEwE16df3Y3IrVtzliTs6LJSybIk2qNg0wRpDNpFDFFKRqyzJfyV5TRzfCDPsU7zLA4rV5OcJefuIyP_wcVBmpSSlvbUzVatJQZ-qpthRW13dW1ptTJsqZM-0GIGnF0CX4nIJhHZK80XSDlShr4SNOjQ59vRsjf4DZtYrc1__0DuGluxw:1tFKHM:K5zyns5VRhRaUwxZjYnXlUMme-4")
cloud = session.connect_scratch_cloud("1101456934")
events = cloud.events()

colors = ((0,0,0), (1,1,1), (0.5,0.5,0.5), (1,0,0), (1,0.5,0), (1,1,0), (0,1,0), (0,1,1), (0,0,1), (1,0,1) , (0.5,0,0), (0.5,0.25,0), (0.5,0.5,0), (0,0.5,0), (0,0.5,0.5), (0,0,0.5), (0.5,0,0.5))

def screen_capture():
    # Step 1: take photo of screen
    pyautogui.screenshot("screenshot.png")

    # Step 2: scale down photo to 96x72
    image = Image.open("screenshot.png")
    image = image.resize((96, 72))
    image.save("screenshot.png")

    # Step 3: encode photo to 16 colors based on how close they are to it
    for x in range(96):
        for y in range(72):
            r, g, b = image.getpixel((x, y))
            closest = (0,0,0)
            closest_distance = math.inf
            for color in colors:
                distance = math.sqrt((r - color[0])**2 + (g - color[1])**2 + (b - color[2])**2)
                if distance < closest_distance:
                    closest = color
                    closest_distance = distance
            image.putpixel((x, y), closest)
    
    image.save("screenshot.png")

@events.event
def on_set(act):
    if act.var == "action":
        if act.value == "1":
            encodedScreen = screen_capture()
            cloud.set_var("data", encodedScreen)
            cloud.set_var("action", "0")

screen_capture()
