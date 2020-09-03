import threading
import time
import random
import sys
import os
import collections
import curses

mod = sys.modules[__name__]

class dice(threading.Thread):
    
    rollList1 = [1,5,6,2]
    rollList2 = [6,3,1,4]
    rollList3 = [2,3,5,4]
    
    def __init__(self, id):
        self.id = id
        threading.Thread.__init__(self)
        
        self.direction = 0
        self.rolldis = random.randint(1,9)
        self.set = False
        self.totalDis = []
        self.num = random.randint(1,6)
        
    #주사위 상태 토글용
    def toggle_set(self):
        self.set = True if self.set == False else False
    
    #쓰레드 분리시 일단 한번 굴린다
    def run(self):
        self._roll()

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
        '''
        print(str(self.id)+ "번 주사위가 굴러간 번호들 => ", end = "")
        print(self.totalDis)
        '''
#현재 5개의 주사위의 상태를 출력
def show_dices_stat(dices):
    print("현재 주사위 상태 : ", end = "")
    for dice in dices:
        temp = "굴림" if dice.set == False else "안굴림"
        print(temp, end = " ")
    print("")

#현재 5개의 주사위의 숫자를 출력
def show_dices_num(dices):
    print("현재 주사위 숫자 : ", end = "")
    for dice in dices:
        print(dice.num, end = " ")
    print("")

#나온 수들에 대한 상황 
def section(dices):
    num_list = []
    for dice in dices:
        num_list.append(dice.num)
    num_list.sort()
    num_counter = collections.Counter(num_list)
    num_most_common = num_counter.most_common(2)
    if num_list == [1,2,3,4,5]:
        print("Small Straight")
    elif num_list == [2,3,4,5,6]:
        print("Large Straight")
    elif num_most_common[0][1] == 5:
        print("Yahtzee!")
    elif num_most_common[0][1] == 4:
        print("Four-Of-A-Kind")
    elif num_most_common[0][1] == 3:
        if num_most_common[1][1] == 2:
            print("Full House")
        else:
            print("Three-Of-A-Kind")
    else:
        print("hou......")

#=======================================================================================메인        
if __name__ == "__main__":
    dices = []
    stdscr = curses.initscr()
    #stdscr.clear()
    

    for i in range(5):
        dices.append(dice(i))

    print("전체 주사위를 굴립니다.")
    #stdscr.addstr(10, 5, "전체 주사위를 굴립니다.")
    
    for i in range(5):
        dices[i].start()
    
    show_dices_num(dices)

    show_dices_stat(dices)

    for i in range(2):
        n = list(map(int,input("상태를 변경할 주사위를 입력해주세요(1~5) : ").split()))

        for i in range(5):
            for j in range(len(n)):
                if n[j]-1 == i:
                    dices[i].toggle_set()

        if all(dice.set == True for dice in dices):
            break

        for i in range(5):
            if dices[i].set == False:
                dices[i]._roll()
        show_dices_num(dices)
        show_dices_stat(dices)
    
    print("총 결과-", end = "")
    show_dices_num(dices)   
    section(dices) 
