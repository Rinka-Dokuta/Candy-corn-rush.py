import pygame
import random

#Initialize pygame
pygame.init()

#Set screen
SCREEN_SIZE = (400, 600)
screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1 ]))
pygame.display.set_caption("Candy corn rush")
clock = pygame.time.Clock()

#color orange
background_color = (255, 165, 0)

#background
Background = pygame.image.load("Night.png")
#load player sprites
candy_corn = pygame.image.load("Candy corn.png")
#Resize candy corn
candy_corn = pygame.transform.scale(candy_corn, (30, 30))

#Candy corn (player) starting postion
x, y = 175, 500 #center screen
speed = 5 #Movement speed

#Game over 
game_over_image = pygame.image.load("Game over .png")
game_over_image = pygame.transform.scale(game_over_image, (400, 600))

#Hands image
HAND_SIZE = 200
HAND_ASPECT_RATIO = 15/8
hand_image = pygame.image.load("Hand.png")
hand_image = pygame.transform.scale(hand_image, (HAND_SIZE, HAND_SIZE / HAND_ASPECT_RATIO))
Flipped_hand_image = pygame.transform.flip(hand_image, True, False)


#Hand properties
hands = []
hand_speed = 5
num_hands = 5

#Background music
pygame.mixer.music.load("Pixel.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#Game over music
game_over_sound = pygame.mixer.Sound("Game over music.mp3")
game_over_sound.set_volume(0.7)

#Hit sound
HIT_sound = pygame.mixer.Sound("Damage.mp3")
HIT_sound.set_volume(50)

#Score
score = 0
font = pygame.font.Font(None, 36)
score_text = font.render(f"Score: {score}", True, (255, 255, 255))

#Creates hands on the side
for i in range(num_hands):
    hand_x = random.choice([0, SCREEN_SIZE[0] - HAND_SIZE])
    hand_y = random.randint(-600, -64)
    hands.append([hand_x, hand_y])


#Lives
Lives = 3 
font = pygame.font.Font(None, 36)



#Game loop-------------------------------------
running = True
while running:
     screen.blit(Background, (0, 0))
     #screen.fill(background_color)#Set background to orange
   
    #Event
     for event in pygame.event.get():
         if event.type == pygame.QUIT:
             running = False
   
    #Movement controls
     keys = pygame.key.get_pressed()
     if keys[pygame.K_LEFT]:
         x -= speed #move left
     if keys[pygame.K_RIGHT]:
         x += speed #move right
   
     #Keep candy corn within screen bounds
     x = max(0, min(x, 400 - 64)) #Makes sure player stays within screen width


     #Update and draw hands
     for hand in hands:
        hand[1] += hand_speed #moves hands down
        if hand[1] > 600:
            hand[1] = random.randint(-600, -64) #reset to top
            hand[0] = random.choice([0, SCREEN_SIZE[0] - HAND_SIZE]) #choose random side 

            score += 1 #Each time a hand reaches the bottom, the player gets 1+
            print(f"SCORE: {score}")#Print in Terminal 


        #Flipped hands to face center
        if hand[0] == 0:
            screen.blit(Flipped_hand_image, hand)
        else: 
            screen.blit(hand_image, hand)
    

        #Collision detection 
        candy_rect = candy_corn.get_rect() #Player hitbox
        candy_rect.topleft = (x, y)
        
        
        hand_width = HAND_SIZE
        hand_height = int(HAND_SIZE / HAND_ASPECT_RATIO)
        hand_rect = pygame.Rect(hand[0] + 20, hand[1], hand_width - 50, hand_height - 50) #hand hitbox
        
        if candy_rect.colliderect(hand_rect): #Check for overlap
            HIT_sound.play()
            Lives -= 1
            print(f"Lives left: {Lives}")
            x, y = 175, 500 #Reset player postion 


            #Flashes a red transparent screen whenever player loses life
            overlay = pygame.Surface(SCREEN_SIZE)
            overlay.fill((255,0,0))
            overlay.set_alpha(128)

            screen.blit(overlay, (0,0))
            pygame.display.flip()
            pygame.time.wait(200)


            #Supposed to reset hands to top whenever player gets hit
            if hand in hands:
                hand[1] = random.randint(-600, 64)

            if Lives == 0:
                #Game over logic
                pygame.mixer.music.stop()
                game_over_sound.play()
                screen.blit(game_over_image, (0, 0))
                pygame.display.flip()
                pygame.time.wait(12000)
                running = False
    
       
       
        #Displays both lives and score on top of the screen
        Lives_text = font.render(f"LIVES: {Lives}", True, (128, 255, 0))
        score_text = font.render(f"Score: {score}", True, (128, 255, 0))

        screen.blit(Lives_text, (10, 10))
        screen.blit(score_text, (280, 10))


           
            

        
           

        
           
   
    #Draws candy corn
     screen.blit(candy_corn, (x, y))


    #Test to see where the hitbox are
     #pygame.draw.rect(screen, (255, 0, 0), hand_rect, 2)
     #pygame.draw.rect(screen, (0, 255, 0), candy_rect, 2)

   

     
     
     

    #Update the screen
     pygame.display.flip()
     clock.tick(60)#Set FPS
   
   
pygame.quit()
