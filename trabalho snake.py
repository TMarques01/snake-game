#somos o 6
import time
import random
import functools
import turtle

MAX_X = 600
MAX_Y = 800
DEFAULT_SIZE = 20
SNAKE_SHAPE = 'square'
HIGH_SCORES_FILE_PATH = 'high_scores.txt'
SPEED = 0.1
def load_high_score(state):
    high_score=open('HIGH_SCORES_FILE_PATH','r')
    score_high=high_score.read().splitlines()
    #print(score_high)
    for i in range(len(score_high)):
        if int((score_high[i]))>int(state['high_score']):
            state['high_score']=score_high[i]
    high_score.close()
    update_score_board(state)
    # se já existir um high score devem guardar o valor em state['high_score']
    pass

def write_high_score_to_file(state):
    high_score=open('HIGH_SCORES_FILE_PATH','a')
    high_score.write(str(state['high_score']))
    high_score.write("\n")
    high_score.close()
    #update_score_board(state)
    # devem escrever o valor que está em state['high_score'] no ficheiro de high scores
    pass

def create_score_board(state):
    score_board = turtle.Turtle()
    score_board.speed(0)
    score_board.shape("square")
    score_board.color("black")
    score_board.penup()
    score_board.hideturtle()
    score_board.goto(0, MAX_Y / 2.2)
    state['score_board'] = score_board
    load_high_score(state)
    update_score_board(state)

def update_score_board(state):
    state['score_board'].clear()
    state['score_board'].write("Score: {} High Score: {}".format(state['score'], state['high_score']), align="center", font=("Helvetica", 24, "normal"))

def go_up(state):
    if state['snake']['current_direction'] != 'down':
        state['snake']['current_direction'] = 'up'

def go_down(state):
    if state['snake']['current_direction'] != 'up':
        state['snake']['current_direction'] = 'down'
        
def go_left(state):
    if state['snake']['current_direction'] != 'right':
        state['snake']['current_direction'] = 'left'

def go_right(state):
    if state['snake']['current_direction'] != 'left':
        state['snake']['current_direction'] = 'right'

def init_state():
    state = {}
    # Informação necessária para a criação do score board
    state['score_board'] = None
    state['new_high_score'] = False
    state['high_score'] = 0
    state['score'] = 0
    # Para gerar a comida deverá criar um nova tartaruga e colocar a mesma numa posição aleatória do campo
    state['food'] = turtle.Turtle()
    state['window'] = None
    state['body']= []
    snake = {
        'head': None,                  # Variável que corresponde à cabeça da cobra
        'current_direction': None     # Indicação da direcção atual do movimento da cobra
        
    }
    state['snake'] = snake
    return state

def setup(state):
    window = turtle.Screen()
    window.bgcolor('beige')
    window.setup(width=MAX_X, height=MAX_Y)
    window.listen()
    window.onkey(functools.partial(go_up, state), 'w')
    window.onkey(functools.partial(go_down, state), 's')
    window.onkey(functools.partial(go_left, state), 'a')
    window.onkey(functools.partial(go_right, state), 'd')
    window.tracer(0)
    state['window'] = window
    snake = state['snake']
    snake['current_direction'] = 'stop'
    snake['head'] = turtle.Turtle()
    snake['head'].shape(SNAKE_SHAPE)
    snake['head'].showturtle()
    snake['head'].pu()
    snake['head'].color('green')
    create_score_board(state)
    create_food(state)
def move(state):
    if state['snake']['current_direction']=='up':
        go_up(state)
        y=state['snake']['head'].ycor()
        state['snake']['head'].sety(y+20)        
    elif state['snake']['current_direction']=='down':
        go_down(state)
        y=state['snake']['head'].ycor()
        state['snake']['head'].sety(y-20)
    elif state['snake']['current_direction']=='left':
        go_left(state)
        x=state['snake']['head'].xcor()
        state['snake']['head'].setx(x-20)        
    elif state['snake']['current_direction']=='right':
        go_right(state)
        x=state['snake']['head'].xcor()
        state['snake']['head'].setx(x+20)        
    snake = state['snake']
    
def create_food(state):
    state['food'].shapesize(0.5)
    state['food'].shape('circle')
    state['food'].color('red')
    state['food'].penup()
    state['food'].goto(random.randrange(-((MAX_X/2)-20),((MAX_X/2)-20)),random.randrange(-((MAX_Y/2)-30),((MAX_Y/2)-30)))
    ''' 
        Função responsável pela criação da comida. Note que elas deverão ser colocadas em posições aleatórias, mas dentro dos limites do ambiente.
    '''
    # a informação sobre a comida deve ser guardada em state['food']

def check_if_food_to_eat(state):
    if state['snake']['head'].distance(state['food'])<=15:
        create_food(state)
        body=turtle.Turtle()
        body.shape(SNAKE_SHAPE)
        body.color('black')
        state['body'].append(body)
        state['score']=state['score']+10
        update_score_board(state)
    for index in range(len(state['body'])-1,0,-1): 
        x = state['body'][index-1].xcor() 
        y = state['body'][index-1].ycor()
        state['body'][index].penup()
        state['body'][index].goto(x, y)
    if len(state['body']) > 0: 
        x = state['snake']['head'].xcor() 
        y = state['snake']['head'].ycor()
        state['body'][0].penup()
        state['body'][0].goto(x, y)
    if (state['score'])>(int(state['high_score'])): #se o score atual for maior que o high_score, a função vai igualando o high score ao score, nesse casso o new_high_score fica true, o que vai ativar a parte do ficheiro. Por fim, os valores sao apresentados na tela.
        state['high_score']=state['score']
        state['new_high_score']= True
        update_score_board(state)
    ''' 
        Função responsável por verificar se a cobra tem uma peça de comida para comer. Deverá considerar que se a comida estiver a uma distância inferior a 15 pixels a cobra pode comer a peça de comida. 
    '''
    food = state['food']
    # para ler ou escrever os valores de high score, score e new high score, devem usar os respetivos campos do state: state['high_score'], state['score'] e state['new_high_score']

def boundaries_collision(state):
    if state['snake']['head'].xcor()>=(MAX_X/2) or state['snake']['head'].xcor()<=-(MAX_X/2) or state['snake']['head'].ycor()<-(MAX_Y/2) or state['snake']['head'].ycor()>(MAX_Y/2):
        return True
    else :
        return False
def check_collisions(state):
    for index in range(len(state['body'])):
        if state['body'][index].distance(state['snake']['head'])<20 or boundaries_collision(state):
            snake = state['snake']
            return True
    return boundaries_collision(state)
def modo_extra(state,SPEED):
    for i in range(1,250):
        if state['score'] >= 50 * i:
            SPEED = SPEED - 0.01
    return(SPEED)
def modo_derrota(state):
    turtle.clearscreen()
    state['score_board'].clear()
    state['score_board'].hideturtle()    
    if (state['score'])>=int(state['high_score']):
        time.sleep(0.5)
        turtle.hideturtle()
        turtle.write("       YOU ROCK!\n New high score is: {}".format(state['score']), align="center", font=("Helvetica", 40, "normal"))        
    else:
        time.sleep(0.5)
        turtle.hideturtle()
        turtle.write("     YOU LOSE!\nYour Score was: {}".format(state['score']), align="center", font=("Helvetica", 40, "normal"))
def main():
    state = init_state()
    setup(state)
    while not check_collisions(state):
        state['window'].update()
        check_if_food_to_eat(state)
        move(state)
        modo_extra(state,SPEED)
        time.sleep(modo_extra(state,SPEED))
    modo_derrota(state)
    if state['new_high_score']:
        write_high_score_to_file(state)    
main()
turtle.exitonclick()