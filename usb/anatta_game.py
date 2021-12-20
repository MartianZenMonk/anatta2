#!/usr/bin/env python3

import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import json
import pygame
import random
import pyautogui
import time

# Define some colors
BLACK = (  0,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

Kleshas16 = ["greed","hatred","anger","grudge","detraction","domineering","envy","stinginess","deceit","hypocrisy","rigidity","vying","conceit","contempt","vanity","negligence"]
 
class Block(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """
 
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its size. """
 
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)


        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
 


q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    if q.qsize() > 15:
        with q.mutex:
            q.queue.clear()
    else:
        q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.model is None:
        args.model = "model"
    if not os.path.exists(args.model):
        print ("Please download a model for your language from https://alphacephei.com/vosk/models")
        print ("and unpack as 'model' in the current folder.")
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            # Initialize Pygame
            pygame.init()
            pygame.font.init()
             
            # Set the height and width of the screen
            screen_width = 700
            screen_height = 400
            screen = pygame.display.set_mode([screen_width, screen_height])
            font = pygame.font.SysFont("ubuntu", 16)

            text_xy = []


            # This is a list of 'sprites.' Each block in the program is
            # added to this list. The list is managed by a class called 'Group.'
            block_list = pygame.sprite.Group()
             
            # This is a list of every sprite. 
            # All blocks and the player block as well.
            all_sprites_list = pygame.sprite.Group()
             
            for i in range(16):
                # This represents a block
                block = Block(BLACK, 50, 20)
             
                # Set a random location for the block
                block.rect.x = random.randrange(screen_width-50)
                block.rect.y = random.randrange(20,screen_height-20)
                # text_xy.append([block.rect.x,block.rect.y])
                             
                # Add the block to the list of objects
                block_list.add(block)
                all_sprites_list.add(block)
             
            # Create a RED player block
            player = Block(RED, 50, 20)
            all_sprites_list.add(player)
             
            # Loop until the user clicks the close button.
            done = False
             
            # Used to manage how fast the screen updates
            clock = pygame.time.Clock()
             
            score = 0

            random.shuffle(Kleshas16)

            runv  = '["hi hello anat ta mouse left right up down click exit"]' 

            rec = vosk.KaldiRecognizer(model, args.samplerate, runv)

            screenWidth, screenHeight = pyautogui.size()
            pyautogui.moveTo(int(screenWidth/2), int(screenHeight/2))
 
            # -------- Main Program Loop -----------
            while not done:


                for event in pygame.event.get(): 
                    if event.type == pygame.QUIT: 
                        done = True

                words = []
                data = q.get()
                # print(q.qsize())
                if rec.AcceptWaveform(data):
                    w = rec.Result()
                    z = json.loads(w)
                    words += z["text"].split()
                else:
                    pass


                #MOUSE CONTROL https://pypi.org/project/PyAutoGUI/
                if len(words) > 1:
                    
                    print(words)

                    if "mouse" in words and "center" in words:
                        screenWidth, screenHeight = pyautogui.size()
                        pyautogui.moveTo(int(screenWidth/2), int(screenHeight/2))
                    elif "mouse" in words and "up" in words:
                        pyautogui.move(0, -23)
                    elif "mouse" in words and "down" in words:
                        pyautogui.move(0, 25)
                    elif "mouse" in words and "left" in words:
                        pyautogui.move(-32, 0)
                    elif "mouse" in words and "right" in words:
                        pyautogui.move(30, 0)
                    elif "mouse" in words and "click" in words:
                        pyautogui.click(button='left')
                    elif "anat" in words and "ta" in words and "exit" in words:
                        done = True
                    elif "hi" in words and "hello" in words:
                        os.system('espeak -a 10 "Hello!"')
     
                # Clear the screen
                screen.fill(WHITE)

                text_surface = font.render('Anatta Game : The Sixteen Mental Defilements , voice cotrol sati-red block to remove Kleshas16', False, (0, 0, 0))
                screen.blit(text_surface, (0, 0))
             
                # Get the current mouse position. This returns the position
                # as a list of two numbers.
                pos = pygame.mouse.get_pos()
             
                # Fetch the x and y out of the list,
                   # just like we'd fetch letters out of a string.
                # Set the player object to the mouse location
                player.rect.x = pos[0]
                player.rect.y = pos[1]
                # text_surface = font.render('sati', False, (0, 0, 0))
                # screen.blit(text_surface, (pos[0]+5, pos[1]+40))
             
                # See if the player block has collided with anything.
                blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)
             
                # Check the list of collisions.
                for block in blocks_hit_list:
                    score += 1
                    print(score)
                    # i = random.randint(0,15)
                    kiles = Kleshas16[score-1]
                    # kiles = random.choice(Kleshas16)
                    os.system("espeak -a 10 " + kiles)
                    os.system("mpg123 -q -f 2000 ../thaivoices/english/" + kiles + ".mp3")
                    print(kiles)
                    text_xy.append([block.rect.x,block.rect.y])                  
             
                # Draw all the spites
                all_sprites_list.draw(screen)
                text_surface = font.render('sati', False, (0, 0, 0))
                screen.blit(text_surface, (pos[0]+10, pos[1]))

                for i in range(len(text_xy)):
                    text_surface = font.render(Kleshas16[i], False, (0, 255, 0))
                    screen.blit(text_surface, (text_xy[i][0],text_xy[i][1]))
             
                # Go ahead and update the screen with what we've drawn.
                pygame.display.flip()
          
                # Limit to 60 frames per second
                clock.tick(60)
                 
            pygame.quit()


except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
