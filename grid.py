from entry import Entry
import math
import heapq
import dataparse as datap
import random

'''
Potential improvements:
1. break ties in temperature for fish to move
2. implement more directions
3. implement velocity/automate migration
4. better visualization
5. More reasonable movement porportion
'''

global_grid = []

'''Initialize grid with time = 1.'''
def initialize_grid_coded(t):
    grid=[[None for _ in range(11)] for _ in range(8)]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            temperature = datap.predictedtemp((j,i), t)
            if not math.isnan(temperature):
                grid[7-i][j] = Entry(100, temperature)
            else: 
                grid[7-i][j] = Entry(0, temperature)
    return grid 

'''This function updates temperatures in the grid given a time t.'''
def update_temperature(old_grid,t):
    grid=[[None for _ in range(11)] for _ in range(8)]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            temperature = datap.predictedtemp((j,i), t)
            if not math.isnan(temperature):
                grid[7-i][j] = Entry(old_grid[7-i][j].get_fishNum(), temperature)
            else: 
                grid[7-i][j] = Entry(0, temperature)
    return grid

'''Direction can be u,d,r,l
    the starting position (x,y) encoded from (0,0) being the top left corner'''
def move_fish(grid, x, y, direction, numbers):
    if x>len(grid[0])-1 or y>len(grid)-1:
        print("Start position out of bound!!!")
        return
    old_entry = grid[y][x]
    fishNum = old_entry.get_fishNum()
    if fishNum >= numbers:
        old_entry.moveOut(numbers)
        
        # match direction:
        #     case "u":
        if direction == "u":
            if y<=0:
                print("Some fish moved out of bound!!!")
                return
            new_entry = grid[y-1][x]
        # case "l":
        if direction == "l":
            if x<=0:
                print("Some fish moved out of bound!!!")
                return
            new_entry = grid[y][x-1]
        # case "r":
        if direction == "r":
            if x>=len(grid[0])-1:
                print("Some fish moved out of bound!!!")
                return
            new_entry = grid[y][x+1]
        # case "d":
        if direction == "d":
            if y>=len(grid)-1:
                print("Some fish moved out of bound!!!")
                return
            new_entry = grid[y+1][x]
        
        new_entry.moveIn(numbers)

def migration(grid):
    new_grid = []
    for row in range(len(grid)): 
        new_grid.append([])
        for cell in range(len(grid[0])): 
            new_grid[row].append(Entry(grid[row][cell].get_fishNum(),grid[row][cell].get_temp()))

    for row in range(len(grid)): 
        for cell in range(len(grid[0])): 
            if grid[row][cell].get_temp() != 7.5 and grid[row][cell].get_fishNum() > 0:
                cur_best_diff = float('inf')
                best_direction = None
                h = []
                direction_list = []
                if row-1 >=0: 
                    cur_diff = abs(grid[row-1][cell].get_temp()-7.5)
                    # if grid[row-1][cell].get_temp() != 0:
                    if not math.isnan(grid[row-1][cell].get_temp()):
                        # print('ajhhahahhaha')
                        direction_list.append("u")
                    if cur_diff < cur_best_diff:
                        cur_best_diff = cur_diff 
                        best_direction = "u"
                if row+1 <=len(grid)-1: 
                    cur_diff = abs(grid[row+1][cell].get_temp()-7.5)
                    # if grid[row+1][cell].get_temp() != 0:
                    if not math.isnan(grid[row+1][cell].get_temp()):
                        direction_list.append("d")
                    if cur_diff < cur_best_diff: 
                        cur_best_diff = cur_diff 
                        best_direction = "d"
                if cell-1 >=0: 
                    cur_diff = abs(grid[row][cell-1].get_temp()-7.5)
                    # if grid[row][cell-1].get_temp() != 0:
                    if not math.isnan(grid[row][cell-1].get_temp()):
                        direction_list.append("l")
                    if cur_diff < cur_best_diff: 
                        cur_best_diff = cur_diff 
                        best_direction = "l"
                if cell+1 <= len(grid[0])-1: 
                    cur_diff = abs(grid[row][cell+1].get_temp()-7.5)
                    # if grid[row][cell+1].get_temp() != 0:
                    if not math.isnan(grid[row][cell+1].get_temp()):
                        direction_list.append("r")
                    if cur_diff < cur_best_diff: 
                        cur_best_diff = cur_diff 
                        best_direction = "r"
        
                # p = 0.5
                # while h:
                #     current_movement_direction = heapq.heappop(h)[1]
                #     fish_num = math.ceil(p*grid[row][cell].get_fishNum())
                #     move_fish(new_grid,cell,row,current_movement_direction,fish_num)
                #     p = p/2

                # percentage = 0.5*abs(grid[row][cell].get_temp()-7.5)
                # V_max = 160 miles/month
                # One degree of latitude equals approximately 69 miles
                # One degree of longitude equals approximately 55 miles
                temp_diff = abs(grid[row][cell].get_temp()-7.5)
                V_max = 160
                if best_direction == "u" or best_direction == "d":
                    if temp_diff <= 2:
                        # 0.43125 = distance of one degree of latitude / V_max
                        velocity = 0.5 * temp_diff * 0.43125 * V_max /2
                        percentage = velocity / 69
                    else: 
                        percentage = 1
                else:
                    if temp_diff <= 2:
                        # 0.34375 = distance of one degree of longitude / V_max
                        velocity = 0.5 * temp_diff * 0.34375 * V_max /2
                        percentage = velocity / 55
                    else: 
                        percentage = 1
                
                cur_fish_num = grid[row][cell].get_fishNum()
                move_fish(new_grid,cell,row,best_direction,math.ceil(cur_fish_num*percentage*0.8))
                if len(direction_list) > 1: 
                    random_move = random.choice([direction for direction in direction_list if direction != best_direction])
                    move_fish(new_grid,cell,row,random_move,math.ceil(cur_fish_num*percentage*0.1))
                elif len(direction_list) == 1: 
                    move = direction_list[0]
                    if move != best_direction:
                        move_fish(new_grid,cell,row,move,math.ceil(cur_fish_num*percentage*0.8))
                # print('random move: ', random_move, ' best move: ', best_direction)
                    
    global global_grid
    global_grid = new_grid
    return new_grid   

def build_vis_arr(t):
    arr = []
    grid = [[None for _ in range(11)] for _ in range(8)]
    fish_grid = initialize_grid_coded(1)
    for i in range(0,8):
        for j in range(0,11):
            grid[7 - i][j] = fish_grid[7 - i][j].get_fishNum()
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    arr.append(grid)
    print(arr)

    for k in range(2,t):
        fish_grid = migration(fish_grid)
    #     # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in fish_grid]))
        fish_grid = update_temperature(fish_grid,k)
        print("t=",k)
        grid = [[None for _ in range(11)] for _ in range(8)]
        for i in range(0,8):
            for j in range(0,11):
                grid[7 - i][j] = fish_grid[7 - i][j].get_fishNum()
    #     print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
        arr.append(grid)
        print(arr)
    #     # 
    # print(arr)
    return arr

def main():
    build_vis_arr(20)
    # fish_grid = initialize_grid_coded(1)
    # print("Initial Stage: ")
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in fish_grid]))
    # fish_grid = migration(fish_grid)
    # print()
    # for t in range(2,20):
    #     fish_grid = update_temperature(fish_grid,t)
    #     print("t=",t)
    #     print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in fish_grid]))
    #     fish_grid = migration(fish_grid)

if __name__ == "__main__":
    main()
