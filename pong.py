# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
ball_pos=[WIDTH/2, HEIGHT/2]
ball_vel=[0,0]
score1 = 0
score2 = 0
#paddle position
paddle1_pos = [PAD_WIDTH/2, HEIGHT/2] 
paddle2_pos = [WIDTH-(PAD_WIDTH/2),HEIGHT/2]
#paddle velocity
paddle1_vel = 0
paddle2_vel = 0


# initialize ball_pos and ball_vel for new bal in middle of table

def spawn_ball(direction):
    global ball_pos, ball_vel 
    ball_pos=[WIDTH/2, HEIGHT/2]
    ball_vel=[random.randrange(120/60, 240/60), random.randrange(60/60, 180/60)]

    if (direction=="RIGHT"):
        ball_vel[0]=ball_vel[0]
    elif(direction=="LEFT"):
        ball_vel[0]=-ball_vel[0]
    ball_pos+=ball_vel
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = [PAD_WIDTH/2, HEIGHT/2] 
    paddle2_pos = [WIDTH-(PAD_WIDTH/2),HEIGHT/2]
    score1 = 0
    score2 = 0
    spawn_ball("RIGHT")
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0]=ball_pos[0]+ball_vel[0]
    ball_pos[1]=ball_pos[1]+ball_vel[1]
    if(ball_pos[1]<=BALL_RADIUS):
        ball_vel[1]=-ball_vel[1]
    if(ball_pos[1]>=HEIGHT-BALL_RADIUS):
        ball_vel[1]=-ball_vel[1]
        
    # draw ball
    canvas.draw_circle( (ball_pos[0],ball_pos[1]), BALL_RADIUS, 2, "Red", "White")
    # update paddle's vertical position, keep paddle on the screen
    if ((paddle1_pos[1]) >= HALF_PAD_HEIGHT and (paddle1_pos[1]) <= (HEIGHT - HALF_PAD_HEIGHT)):
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel
    
    if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] += paddle2_vel

    # draw paddles
    canvas.draw_polygon([[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], PAD_WIDTH, 'White')
    canvas.draw_polygon([[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], PAD_WIDTH, 'White')

    # determine whether paddle and ball collide    
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(paddle1_pos[1] - HALF_PAD_HEIGHT,paddle1_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 2
        ball_vel[1] *= 2
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        score2 += 1
        spawn_ball('RIGHT')
        
    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(ball_pos[1]) in range(paddle2_pos[1] - HALF_PAD_HEIGHT,paddle2_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 2
        ball_vel[1] *= 2
    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
        score1 += 1
        spawn_ball('LEFT')
    # draw scores
    canvas.draw_text(str(score1), (WIDTH/2 - 100,80), 40, 'White')
    canvas.draw_text(str(score2), (WIDTH/2 + 60,80), 40, 'White')

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -4
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 4
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -4
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 4
    elif key == simplegui.KEY_MAP['space']:
        spawn_ball(random.choice(['LEFT','RIGHT']))
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
b=frame.add_button("Restart", new_game,55)

# start frame
new_game()
frame.start()
