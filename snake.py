from time import sleep
import os
import sys, termios
import random
import threading

fd = sys.stdin.fileno()
old = termios.tcgetattr(fd)
new = termios.tcgetattr(fd)
# turn off echo and press-enter
new[3] = new[3] & ~termios.ECHO & ~termios.ICANON


# l = ['　'*10]*10
# l[0][0] = '－'
snake = [[2,0], [1,0], [0,0]]	# 开局蛇位置
# snake = [[4,0], [3,0], [2,0], [1,0], [0,0]]

def getapple(snake):
	# 生成苹果位置
	l = [ [x,y] for y in range(10) for x in range(10) ]
	for i in snake:
		if i in l:
			del l[l.index(i)]
	apple = random.choice(l)
	return apple


def display(snake, apple):
	l = [ [ '　' for x in range(10) ] for x in range(10) ]
	# 标出苹果，蛇头，蛇身，其他为空格
	l[apple[1]][apple[0]] = '＊'
	l[snake[0][1]][snake[0][0]] = 'Ｏ'
	for i in snake[1:]:
		l[i[1]][i[0]] = '＃'
		
	os.system('clear')
	print('＋{}＋'.format('－'*10))
	for i in l:
		print('｜{}｜'.format(''.join(i)))
	print('＋{}＋'.format('－'*10))


def getchar():
	#获取按键
	global char
	while 1:
		termios.tcsetattr(fd, termios.TCSADRAIN, new)
		char = sys.stdin.read(1)
		# finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old)
	
# print(snake)
char = 'd'						# 开局方向
char_d = {'a':'d','w':'s','d':'a','s':'w'} # 对应逆方向字典
char_no = 'a'							   # 开局逆方向
eat = 1									   # 苹果被吃掉时为1
t = threading.Thread(target=getchar)
t.setDaemon(True)
t.start()
while 1:
	if eat:						# 苹果被吃掉，生成新苹果
		apple = getapple(snake)
		eat = 0
	display(snake, apple)
	sleep(1)
	# try:

	# 按q退出，按成反方向无效
	if char == 'q':
		break
	elif char == char_no:
		continue

	# 预计蛇头位置
	head = snake[0][:]
	if char == 'd':
		head[0] += 1
	elif char == 's':
		head[1] += 1
	elif char == 'a':
		head[0] -= 1
	elif char == 'w':
		head[1] -= 1

	char_no = char_d[char]
	# 咬到蛇身或撞墙，game over;吃到苹果增长身体
	if head in snake[:-1] or [ i for i in head if i < 0 or i > 9]:
		break
	elif head == apple:
		eat = 1
		snake = [head] + snake
		continue

	#移动身体和头
	for i in range(1,len(snake)):
		# print(snake)
		snake[-i] = snake[-i-1][:]
		
	snake[0] = head
		
	# display(snake, apple)
	# print(snake)

	
