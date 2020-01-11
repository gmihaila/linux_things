import pygame

import pygame.camera



# Captured image dimensions. It should be less than or equal to the maximum dimensions acceptable by the camera.

width = 320

height = 240



# Initializing PyGame and the camera.

pygame.init()

pygame.camera.init()



# Specifying the camera to be used for capturing images. If there is a single camera, then it has the index 0.

cam = pygame.camera.Camera("/dev/video0", (width, height))



# Preparing a resizable window of the specified size for displaying the captured images.

window = pygame.display.set_mode((width, height), pygame.RESIZABLE)



# Starting the camera for capturing images.

cam.start()



for im_num in range(0, 1000):

    print("Image : ", im_num)



    # Capturing an image.

    image = cam.get_image()



    # Displaying the image on the window starting from the top-left corner.

    window.blit(image, (0, 0))



    # Refreshing the window.

    pygame.display.update()



    # Saving the captured image.

    pygame.image.save(window, '../pygame_images/image_' + str(im_num) + '.jpg')



# Stopping the camera.

cam.stop()


