import threading
import curses
from curses.textpad import Textbox, rectangle
import random
import time
import collections


dice_place_list = [[1,51,7,66],[1,69,7,84],[8,42,14,57],[8,60,14,75],[8,78,14,93]]

class Player():
    def __init__(self, name):
        self.name = name
        self.score2 = [0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        self.bonus = 0
        self.score = {
            'Aces' : -1,
            'Twos' : -1,
            "Threes" : -1,
            'Fours' : -1,
            'Fives' : -1,
            "Threes" : -1,
            'Sixes' : -1,
            'Bonus' : -1,
            "Threes" : -1,
            'Three-Of-A-Kind' : -1,
            'Four-Of-A-Kind' : -1,
            "Full House" : -1,
            'Small Straight' : -1,
            'Large Straight' : -1,
            "Chance" : -1,
            'Yahtzee' : -1
        }
        self.total_score = 0

    def update_total_score(self):
        _sum = 0
        for i in range(1, 13):
            if self.score2[i] != -1:
                _sum += self.score2[i]
        _sum += self.bonus
        self.total_score = _sum

    def isAllSet(self):
        if -1 in self.score2:
            return False
        else:
            return True

    def get_bonus(self):
        tempsum = 0
        for i in range(1,6):
            tempsum += self.score2[i]
        if tempsum >= 63:
            self.bonus = 35

class dice(threading.Thread):

    rollList1 = [1,5,6,2]
    rollList2 = [6,3,1,4]
    rollList3 = [2,3,5,4]
    
    def __init__(self, id, screen):
        self.id = id
        threading.Thread.__init__(self)
        self.screen = screen
        
        self.direction = 0
        self.rolldis = random.randint(1,9)
        self.totalDis = []
        self.num = random.randint(1,6)
        
    #쓰레드 분리시 일단 한번 굴린다
    def run(self):
        self._roll()
        self.show_dice(self.screen)

    #주사위 굴리기
    def _roll(self):
        self.totalDis = []
        self.rolldis = random.randint(1,3)
        self.direction = random.randint(5,50)
        #임시로 첫 숫자 변경
        self.num = random.randint(1, 6)

        #딱 면이 맞게 떨어진 경우 == 현재 수 변화없음
        if self.direction <= 10:
            self.num = self.num
            self.totalDis.append(self.num)
        #굴러가는 방향이 위
        elif self.direction <= 20:
            if self.num == 1 or self.num == 3 or self.num == 6 or self.num == 4:
                self.temp = dice.rollList2.index(self.num)
                for i in range(self.rolldis):
                    self.totalDis.append(dice.rollList2[(self.temp + i) % 4])
                self.num = dice.rollList2[(self.temp + self.rolldis-1) % 4]
            else:
                self.temp = dice.rollList1.index(self.num)
                for i in range(self.rolldis):
                    self.totalDis.append(dice.rollList1[(self.temp + i) % 4])
                self.num = dice.rollList1[(self.temp + self.rolldis-1) % 4]
        #굴러가는 방향이 오른쪽
        elif self.direction <= 30:
            if self.num == 2 or self.num == 3 or self.num == 5 or self.num == 4:
                self.temp = dice.rollList3.index(self.num)
                for i in range(self.rolldis):
                    self.totalDis.append(dice.rollList3[(self.temp + i) % 4])
                self.num = dice.rollList3[(self.temp + self.rolldis-1) % 4]
            else:
                self.temp = dice.rollList1.index(self.num)
                for i in range(self.rolldis):
                    self.totalDis.append(dice.rollList1[(self.temp + i) % 4])
                self.num = dice.rollList1[(self.temp + self.rolldis-1) % 4]
        #굴러가는 방향이 아래
        elif self.direction <= 40:
            if self.num == 1 or self.num == 3 or self.num == 6 or self.num == 4:
                self.temp = dice.rollList2.index(self.num)
                for i in range(self.rolldis):
                    self.totalDis.append(dice.rollList2[(self.temp - i) % 4])
                self.num = dice.rollList2[(self.temp - self.rolldis+1) % 4]
            else:
                self.temp = dice.rollList1.index(self.num)
                for i in range(self.rolldis):
                    self.totalDis.append(dice.rollList1[(self.temp - i) % 4])
                self.num = dice.rollList1[(self.temp - self.rolldis+1) % 4]
               
        #굴러가는 방향이 왼쪽
        else:
            if self.num == 2 or self.num == 3 or self.num == 5 or self.num == 4:
                self.temp = dice.rollList3.index(self.num)
                for i in range(self.rolldis):
                    self.totalDis.append(dice.rollList3[(self.temp - i) % 4])
                self.num = dice.rollList3[(self.temp - self.rolldis+1) % 4]
            else:
                self.temp = dice.rollList1.index(self.num)
                for i in range(self.rolldis):
                    self.totalDis.append(dice.rollList1[(self.temp - i) % 4])
                self.num = dice.rollList1[(self.temp - self.rolldis+1) % 4]

    def show_dice(self, screen):
        temp = dice_place_list[self.id]
        y1 = temp[0]
        x1 = temp[1]
        y2 = temp[2]
        x2 = temp[3]
        for i in range(len(self.totalDis)):
            self.clear_dice_field(screen)
            temp = self.totalDis[i]
            draw_dice_num(screen, self.id, self.totalDis[i])
            #draw_dice_num(screen, self.id, self.num)
            screen.refresh()
            curses.napms(100)
        screen.move(20, 80)

#test
    def clear_dice_field(self, screen):
        temp = dice_place_list[self.id]
        y1 = temp[0]
        x1 = temp[1]
        y2 = temp[2]
        x2 = temp[3]
        for i in range(5):
            screen.addstr(y1 + i + 1 , x1 + 1, (14)*" ")

def section(dices, screen):
    num_list = []
    score_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    sum = 0
    temp = ""
    for dice in dices:
        num_list.append(dice.num)
        sum += dice.num
    num_list.sort()
    num_counter = collections.Counter(num_list)
    num_most_common = num_counter.most_common(5)
    for i in range(5 - len(num_most_common)):
        num_most_common.append((0,0))
    if num_list == [1,2,3,4,5]:
        temp = "Small Straight"
        score_list = [0,1,2,3,4,5,0,0,0,0,15,0,15,0]
    elif num_list == [2,3,4,5,6]:
        temp = "Large Straight"
        score_list = [0,0,2,3,4,5,6,0,0,0,0,20,20,0]
    elif num_most_common[0][1] == 5:
        temp = "Yahtzee!"
        score_list[num_most_common[0][0]] = num_most_common[0][0]*5
        score_list[13] = 50
        score_list[12] = sum
    elif num_most_common[0][1] == 4:
        temp = "Four-Of-A-Kind"
        score_list[num_most_common[0][0]] = num_most_common[0][0]*4
        score_list[num_most_common[1][0]] = num_most_common[1][0]
        score_list[8] = num_most_common[0][0]*4 + num_most_common[1][0]
        score_list[12] = sum
    elif num_most_common[0][1] == 3:
        if num_most_common[1][1] == 2:
            temp = "Full House"
            score_list[num_most_common[0][0]] = num_most_common[0][0]*3
            score_list[num_most_common[1][0]] = num_most_common[1][0]*2
            score_list[9] = num_most_common[0][0]*3 + num_most_common[1][0]*2
            score_list[12] = sum
        else:
            temp = "Three-Of-A-Kind"
            score_list[num_most_common[0][0]] = num_most_common[0][0]*3
            score_list[num_most_common[1][0]] = num_most_common[1][0]*num_most_common[1][1]
            score_list[num_most_common[2][0]] = num_most_common[2][0]*num_most_common[2][1]
            score_list[7] = num_most_common[0][0]*3
            score_list[12] = sum
    else:
        temp = "sum of nums"
        score_list[num_most_common[0][0]] = num_most_common[0][0]*num_most_common[0][1]
        score_list[num_most_common[1][0]] = num_most_common[1][0]*num_most_common[1][1]
        score_list[num_most_common[2][0]] = num_most_common[2][0]*num_most_common[2][1]
        score_list[num_most_common[3][0]] = num_most_common[3][0]*num_most_common[3][1]
        score_list[num_most_common[4][0]] = num_most_common[4][0]*num_most_common[4][1]
        score_list[12] = sum
    screen.addstr(16,43,temp)
    return score_list

def draw_field(screen, str1, str2):
    rectangle(screen, 1, 3, 21, 20)
    screen.addstr(2, 22, str1.name)
    screen.addstr(2, 32, str2.name)
    screen.addstr(3, 4, "================")
    screen.addstr(4, 4, "1:Aces")
    screen.addstr(4, 22, str(str1.score2[1]))
    screen.addstr(4, 32, str(str2.score2[1]))
    screen.addstr(5, 4, "2:Twos")
    screen.addstr(5, 22, str(str1.score2[2]))
    screen.addstr(5, 32, str(str2.score2[2]))
    screen.addstr(6, 4, "3:Threes")
    screen.addstr(6, 22, str(str1.score2[3]))
    screen.addstr(6, 32, str(str2.score2[3]))
    screen.addstr(7, 4, "4:Fours")
    screen.addstr(7, 22, str(str1.score2[4]))
    screen.addstr(7, 32, str(str2.score2[4]))
    screen.addstr(8, 4, "5:Fives")
    screen.addstr(8, 22, str(str1.score2[5]))
    screen.addstr(8, 32, str(str2.score2[5]))
    screen.addstr(9, 4, "6:Sixes")
    screen.addstr(9, 22, str(str1.score2[6]))
    screen.addstr(9, 32, str(str2.score2[6]))
    screen.addstr(10, 4, "Bonus")
    screen.addstr(10, 22, str(str1.bonus))
    screen.addstr(10, 32, str(str2.bonus))
    screen.addstr(11, 4, "================")
    screen.addstr(12, 4, "7:Three-Of-A-Kind")
    screen.addstr(12, 22, str(str1.score2[7]))
    screen.addstr(12, 32, str(str2.score2[7]))
    screen.addstr(13, 4, "8:Four-Of-A-Kind")
    screen.addstr(13, 22, str(str1.score2[8]))
    screen.addstr(13, 32, str(str2.score2[8]))
    screen.addstr(14, 4, "9:Full House")
    screen.addstr(14, 22, str(str1.score2[9]))
    screen.addstr(14, 32, str(str2.score2[9]))
    screen.addstr(15, 4, "10:Small Straight")
    screen.addstr(15, 22, str(str1.score2[10]))
    screen.addstr(15, 32, str(str2.score2[10]))
    screen.addstr(16, 4, "11:Large Straight")
    screen.addstr(16, 22, str(str1.score2[11]))
    screen.addstr(16, 32, str(str2.score2[11]))
    screen.addstr(17, 4, "12:Choice")
    screen.addstr(17, 22, str(str1.score2[12]))
    screen.addstr(17, 32, str(str2.score2[12]))
    screen.addstr(18, 4, "13:Yahtzee")
    screen.addstr(18, 22, str(str1.score2[13]))
    screen.addstr(18, 32, str(str2.score2[13]))
    screen.addstr(19, 4, "================")
    screen.addstr(20, 4, "Total Score")
    screen.addstr(20, 22, str(str1.total_score))
    screen.addstr(20, 32, str(str2.total_score))
    rectangle(screen, 1, 21, 21, 30)
    screen.addstr(3, 22, "========")
    screen.addstr(11, 22, "========")
    screen.addstr(19, 22, "========")
    rectangle(screen, 1, 31, 21, 40)
    screen.addstr(3, 32, "========")
    screen.addstr(11, 32, "========")
    screen.addstr(19, 32, "========")

def draw_dices_field(screen):
    rectangle(screen, 1, 51, 7, 66)
    rectangle(screen, 1, 69, 7, 84)
    rectangle(screen, 8, 42, 14, 57)
    rectangle(screen, 8, 60, 14, 75)
    rectangle(screen, 8, 78, 14, 93)

def draw_bottom(screen):
    rectangle(screen, 15, 42, 21 ,93)

def draw_dice_num(screen, id, num):
    temp = dice_place_list[id]
    y1 = temp[0]
    x1 = temp[1]
    y2 = temp[2]
    x2 = temp[3]

    if num == 1:
        screen.addstr(int((y1+y2)/2), int((x1+x2)/2), "*")
    elif num == 2:
        screen.addstr(int((y1 + y2)/2), int((2*x1+x2)/3), "*")
        screen.addstr(int((y1 + y2)/2), int((x1+2*x2)/3), "*")
    elif num == 3:
        screen.addstr(int((y1 + y2)/2), int((x1+3*x2)/4), "*")
        screen.addstr(int((y1 + y2)/2), int((x1+x2)/2), "*")
        screen.addstr(int((y1 + y2)/2), int((3*x1+x2)/4), "*")
    elif num == 4:
        screen.addstr(int((2*y1 + y2)/3), int((x1+2*x2)/3), "*")
        screen.addstr(int((2*y1 + y2)/3), int((2*x1+x2)/3), "*")
        screen.addstr(int((y1 + 2*y2)/3), int((x1+2*x2)/3), "*")
        screen.addstr(int((y1 + 2*y2)/3), int((2*x1+x2)/3), "*")
    elif num == 5:
        screen.addstr(int((2*y1 + y2)/3), int((x1+2*x2)/3), "*")
        screen.addstr(int((2*y1 + y2)/3), int((2*x1+x2)/3), "*")
        screen.addstr(int((y1 + y2)/2), int((x1+x2)/2), "*")
        screen.addstr(int((y1 + 2*y2)/3), int((x1+2*x2)/3), "*")
        screen.addstr(int((y1 + 2*y2)/3), int((2*x1+x2)/3), "*")
    else:
        screen.addstr(int((y1 + 2*y2)/3), int((x1+2*x2)/3), "*")
        screen.addstr(int((y1 + 2*y2)/3), int((2*x1+x2)/3), "*")
        screen.addstr(int((y1 + y2)/2), int((x1+2*x2)/3), "*")
        screen.addstr(int((y1 + y2)/2), int((2*x1+x2)/3), "*")
        screen.addstr(int((2*y1 + y2)/3), int((x1+2*x2)/3), "*")
        screen.addstr(int((2*y1 + y2)/3), int((2*x1+x2)/3), "*")

def refresh_all(screen, p1, p2):
    screen.clear()
    draw_field(screen , p1, p2)
    draw_dices_field(screen)
    screen.refresh()
    #draw_bottom(screen)

def my_raw_input(stdscr, r, c):
    curses.echo() 
    stdscr.refresh()
    input = stdscr.getstr(r, c, 20)
    return input


def main(screen):
    player1 = Player("some")
    player2 = Player("any")
    turn = player1
    total_state = [False, False, False, False, False]
    num_list = []
    dice_list = [0,0,0,0,0]
    for i in range(5):
        dice_list.append(dice(i, screen))

    time.sleep(1)
    
    input_win = curses.newwin(4, 49, 16, 43)
    '''
    rectangle(screen, 7, 0, 17, 100)
    rectangle(screen, 1, 35, 7, 67)
    '''

    while(not(player1.isAllSet() and player2.isAllSet())):
        refresh_all(screen, player1, player2)
        total_state = [False, False, False, False, False]
        dice_list = [0,0,0,0,0]
        num_list = [0,0,0,0,0]
        scores = []

        screen.addstr(20, 43, "대기")

        if(turn.isAllSet()):
            continue

        for i in range(3):
            _tempState = 0
            
            refresh_all(screen, player1, player2)
            for j in range(5):
                if total_state[j] == False:
                    dice_list[j] = dice(j, screen)
                    dice_list[j].start()
            
            time.sleep(0.5)
      
            for j in range(5):
                num_list[j] = dice_list[j].num
                
            for j in range(5):
                if total_state[j] == True:
                    draw_dice_num(screen, j, num_list[j])

            for j in range(5):
                if total_state[j] == False:
                    _tempState = 1
                
            if _tempState == 0:
                break

            screen.addstr(17, 43, str(i) + "번째 턴")

            screen.refresh()
            if i != 2:
                screen.addstr(18,43,"상태변경할 주사위의 번호를 입력해주세요!")
                #curses.echo()
                for i in range(5):
                    screen.addstr(19, 43 +i*4, "굴림" if total_state[i] == False else "고정")
                screen.refresh()


                screen.addstr(20, 43, "입력(하나씩 띄워서!)")
                c = my_raw_input(screen, 20, 80)

                s = c.split()
                for i in s:
                    total_state[int(i)-1] = False if total_state[int(i)-1] == True else True

            #screen.addstr(0,0, s[0])
        
        scores = section(dice_list, screen)
        #이제 여기서 점수를 받아 player객체에 저장
        while(True):
            c = my_raw_input(screen, 21, 80)
            #빈 값이 입력되었을 때
            if(c == b''):
                screen.addstr(21,90,"잘못된 값")
                screen.refresh()
            elif(int(c) >= 1 and int(c)<=13) and turn.score2[int(c)] == -1:
                turn.score2[int(c)] = scores[int(c)]
                #7 이상은 되는데 6 이하가 안된다.
                break
            else:
                screen.addstr(21,90,"잘못된 값")
                screen.refresh()
        screen.refresh()
        turn.get_bonus()
        turn.update_total_score()
        turn = player1 if turn == player2 else player2
        refresh_all(screen, player1, player2)
        #screen.addstr(0,0, str(int(s[0])))

    box = Textbox(input_win)
    box.edit()
    message = box.gather()
    screen.getkey()

if __name__ == "__main__":
    curses.wrapper(main)