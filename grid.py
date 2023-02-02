from entry import Entry
import math
import heapq
import dataparse as datap

'''
Potential improvements:
1. break ties in temperature for fish to move
2. implement more directions
3. implement velocity/automate migration
4. better visualization
5. More reasonable movement porportion
'''

global_grid = []

def initialize_grid_basic():
    grid = []
    for i in range(5):
        grid.append([])
        for j in range(5):
            # A place to modify temp
            newEntry = Entry(5,i+10)
            grid[i].append(newEntry)
    return grid


def initialize_grid_coded(t):
    grid=[[None for _ in range(11)] for _ in range(8)]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            temperature = datap.predictedtemp((j,i), t)
            # print(temperature)
            if not math.isnan(temperature):
                # temperature = None
                grid[7-i][j] = Entry(100, temperature)
            else: 
                grid[7-i][j] = Entry(0, temperature)
    print(grid)
    # grid = [[Entry(5,30),Entry(5,35),Entry(5,40),Entry(5,45),Entry(5,50)],
    # [Entry(5,35),Entry(5,40),Entry(5,45),Entry(5,50),Entry(5,55)],
    # [Entry(5,40),Entry(5,45),Entry(5,50),Entry(5,55),Entry(5,60)],
    # [Entry(5,45),Entry(5,50),Entry(5,55),Entry(5,60),Entry(5,65)],
    # [Entry(5,50),Entry(5,55),Entry(5,60),Entry(5,65),Entry(5,70)]]
    # grid = [[Entry(5,30),Entry(0,35),Entry(0,40),Entry(0,45),Entry(0,50)],
    # [Entry(0,35),Entry(0,40),Entry(0,45),Entry(0,50),Entry(0,55)],
    # [Entry(0,40),Entry(0,45),Entry(0,50),Entry(0,55),Entry(0,60)],
    # [Entry(0,45),Entry(0,50),Entry(0,55),Entry(0,60),Entry(0,65)],
    # [Entry(0,50),Entry(0,55),Entry(0,60),Entry(0,65),Entry(0,70)]]
    
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
        
        match direction:
            case "u":
                if y<=0:
                    print("Some fish moved out of bound!!!")
                    return
                new_entry = grid[y-1][x]
            case "l":
                if x<=0:
                    print("Some fish moved out of bound!!!")
                    return
                new_entry = grid[y][x-1]
            case "r":
                if x>=len(grid[0])-1:
                    print("Some fish moved out of bound!!!")
                    return
                new_entry = grid[y][x+1]
            case "d":
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
            if grid[row][cell].get_temp() != 7.3 and grid[row][cell].get_fishNum() > 0:
                cur_best_diff = float('inf')
                best_direction = None
                h = []
                if row-1 >=0: 
                    cur_diff = abs(grid[row-1][cell].get_temp()-7.3)
                    # heapq.heappush(h,(cur_diff,"u"))
                    if cur_diff < cur_best_diff:
                        cur_best_diff = cur_diff 
                        best_direction = "u"
                if row+1 <=len(grid)-1: 
                    cur_diff = abs(grid[row+1][cell].get_temp()-7.3)
                    # heapq.heappush(h,(cur_diff,"d"))
                    if cur_diff < cur_best_diff: 
                        cur_best_diff = cur_diff 
                        best_direction = "d"
                if cell-1 >=0: 
                    cur_diff = abs(grid[row][cell-1].get_temp()-7.3)
                    # heapq.heappush(h,(cur_diff,"l"))
                    if cur_diff < cur_best_diff: 
                        cur_best_diff = cur_diff 
                        best_direction = "l"
                if cell+1 <= len(grid[0])-1: 
                    cur_diff = abs(grid[row][cell+1].get_temp()-7.3)
                    # heapq.heappush(h,(cur_diff,"r"))
                    if cur_diff < cur_best_diff: 
                        cur_best_diff = cur_diff 
                        best_direction = "r"
                
                
                # p = 0.5
                # while h:
                #     current_movement_direction = heapq.heappop(h)[1]
                #     fish_num = math.ceil(p*grid[row][cell].get_fishNum())
                #     move_fish(new_grid,cell,row,current_movement_direction,fish_num)
                #     p = p/2
                percentage = 0.5*abs(grid[row][cell].get_temp()-7.3)
                
                move_fish(new_grid,cell,row,best_direction,math.ceil(grid[row][cell].get_fishNum()*percentage))
    # global global_grid
    # global_grid = new_grid
    # return new_grid            
                # print("grid:")
                # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
                # print("new grid: ")
                # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in new_grid]))
    print('hhhhhhhhhhhhhh')
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in new_grid]))
    # print()
    # migration(new_grid, v_step-1,fish_percentage)


def move_with_velocity(grid):
    global global_grid
    global_grid = grid
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in global_grid]))
    for month in range(9):
        # cur_grid = migration(cur_grid, v_step, fish_percentage)
        # cur_grid = []
        # for row in range(len(grid)): 
        #     cur_grid.append([])
        #     for cell in range(len(grid[0])): 
        #         cur_grid[row].append(Entry(grid[row][cell].get_fishNum(),grid[row][cell].get_temp()))

        migration(global_grid)
        print("Current Month:", month)
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in global_grid]))
        print()
    



def main():
    #Basic
    # dataset = datap.cell_info()
    fish_grid = initialize_grid_coded(1)
    # move_fish(grid, 3, 2, "u",2)
    print("Initial Stage: ")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in fish_grid]))
    print()
    migration(fish_grid)
    # move_with_velocity(fish_grid) 

    # for month in range(1,10): 
    #     temp_grid = initialize_grid_coded(month)
    #     migration(temp_grid, fish_grid)

if __name__ == "__main__":
    main()
