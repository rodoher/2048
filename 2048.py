from tkinter import *
import numpy as np
from tkinter import messagebox


class Game2048:

    def __init__(self, n_rows=6):
        # the number of rows can be indicated to make a bigger or a smaller board, if it is not indicated,
        # the standard size is 6x6
        self.n_rows = n_rows
        self.root = None
        self.c_boxes = np.zeros((self.n_rows * self.n_rows), dtype=int)
        self.total_boxes = self.n_rows * self.n_rows
        self.check_over_2048 = False
        self.check_game_over = False
        self.options = [2, 2, 2, 4]

    def start_game(self):
        self.root = Tk()
        self.create_boxes()
        self.root.mainloop()

    def create_boxes(self):
        winner = False
        if not self.check_lost():
            # if the gamer hasn't lost, one of the empty boxes is chosen randomly to make the new number appear
            self.choose_one()
            for i in range(self.n_rows):
                for j in range(self.n_rows):
                    x = Label(self.root, width=5, height=2, text=self.c_boxes[(i * self.n_rows + j)], borderwidth=2,
                              relief="solid")
                    x.grid(row=i, column=j)
                    if self.c_boxes[(i * self.n_rows + j)] == 0:
                        x['text'] = ""
                        x["bg"] = "yellow"
                    elif self.c_boxes[(i * self.n_rows + j)] == 2:
                        x["bg"] = "pink"
                    elif self.c_boxes[(i * self.n_rows + j)] == 4:
                        x["bg"] = "orange"
                    elif self.c_boxes[(i * self.n_rows + j)] == 8:
                        x["bg"] = "blue"
                    elif self.c_boxes[(i * self.n_rows + j)] == 16:
                        x["bg"] = "green"
                    elif self.c_boxes[(i * self.n_rows + j)] == 32:
                        x["bg"] = "red"
                    elif self.c_boxes[(i * self.n_rows + j)] == 64:
                        x["bg"] = "brown"
                    elif self.c_boxes[(i * self.n_rows + j)] == 128:
                        x["bg"] = "purple"
                    elif self.c_boxes[(i * self.n_rows + j)] == 256:
                        x["bg"] = "pale turquoise"
                    elif self.c_boxes[(i * self.n_rows + j)] == 512:
                        x["bg"] = "LemonChiffon4"
                    elif self.c_boxes[(i * self.n_rows + j)] == 1024:
                        x["bg"] = "dim gray"
                    elif self.c_boxes[(i * self.n_rows + j)] == 2048:
                        x["bg"] = "NavajoWhite2"
                        winner = True
            if winner:
                self.win()

            self.root.bind('<Left>', self.left_key)
            self.root.bind('<Right>', self.right_key)
            self.root.bind('<Up>', self.top_key)
            self.root.bind('<Down>', self.down_key)

    def choose_one(self):
        vals = np.argwhere(self.c_boxes == 0).reshape(-1)
        i = np.random.choice(vals, 1)
        # likelihood of getting a 2 is in this case 3 times more than getting a 4 - can be changed
        value = np.random.choice(self.options, 1)
        self.c_boxes[i] = value
        self.check_game_over = False

    def left_key(self, event):
        self.c_boxes = self.c_boxes.reshape(self.n_rows, self.n_rows)
        for a in range(len(self.c_boxes)):
            arr = self.c_boxes[a]
            nums = np.argwhere(arr != 0)
            val = 0
            for i in range(len(nums)):
                if val != 0:
                    if arr[nums[i]] == arr[nums[i - 1]]:
                        arr[nums[i - 1]] *= 2
                        arr[nums[i]] = 0
                else:
                    val = 1
            arr = np.delete(arr, np.where(arr == 0))
            missing_zeros = self.n_rows - len(arr)
            for i in range(missing_zeros):
                arr = np.append(arr, 0)
            self.c_boxes[a] = arr
        self.c_boxes = self.c_boxes.reshape(self.total_boxes)
        self.destroy_boxes()
        self.create_boxes()

    def destroy_boxes(self):
        if not self.check_lost():
            elems = self.root.winfo_children()
            for i in elems:
                i.destroy()

    def win(self):
        if not self.check_over_2048:
            messagebox.showinfo("Victory!", "You've won! Congratulations!")
            self.check_over_2048 = True

    def right_key(self, event):
        self.c_boxes = self.c_boxes.reshape(self.n_rows, self.n_rows)
        for a in range(len(self.c_boxes)):
            arr = self.c_boxes[a]
            nums = np.argwhere(arr != 0)

            for i in range(len(nums) - 1, -1, -1):
                if i + 1 < len(nums):
                    if arr[nums[i]] == arr[nums[i + 1]]:
                        arr[nums[i + 1]] *= 2
                        arr[nums[i]] = 0

            arr = np.delete(arr, np.where(arr == 0))
            missing_zeros = self.n_rows - len(arr)
            for i in range(missing_zeros):
                arr = np.insert(arr, 0, 0)
            self.c_boxes[a] = arr
        self.c_boxes = self.c_boxes.reshape(self.total_boxes)
        self.destroy_boxes()
        self.create_boxes()

    def top_key(self, event):
        self.c_boxes = self.c_boxes.reshape(self.n_rows, self.n_rows).T
        for a in range(len(self.c_boxes)):
            arr = self.c_boxes[a]
            nums = np.argwhere(arr != 0)
            val = 0
            for i in range(len(nums)):
                if val != 0:
                    if arr[nums[i]] == arr[nums[i - 1]]:
                        arr[nums[i - 1]] *= 2
                        arr[nums[i]] = 0
                else:
                    val = 1
            arr = np.delete(arr, np.where(arr == 0))
            missing_zeros = self.n_rows - len(arr)
            for i in range(missing_zeros):
                arr = np.append(arr, 0)
            self.c_boxes[a] = arr
        self.c_boxes = self.c_boxes.T
        self.c_boxes = self.c_boxes.reshape(self.total_boxes)
        self.destroy_boxes()
        self.create_boxes()

    def down_key(self, event):
        self.c_boxes = self.c_boxes.reshape(self.n_rows, self.n_rows).T
        for a in range(len(self.c_boxes)):
            arr = self.c_boxes[a]
            nums = np.argwhere(arr != 0)

            for i in range(len(nums) - 1, -1, -1):
                if i + 1 < len(nums):
                    if arr[nums[i]] == arr[nums[i + 1]]:
                        arr[nums[i + 1]] *= 2
                        arr[nums[i]] = 0

            arr = np.delete(arr, np.where(arr == 0))
            missing_zeros = self.n_rows - len(arr)
            for i in range(missing_zeros):
                arr = np.insert(arr, 0, 0)
            self.c_boxes[a] = arr
        self.c_boxes = self.c_boxes.T
        self.c_boxes = self.c_boxes.reshape(self.total_boxes)
        self.destroy_boxes()
        self.create_boxes()

    def check_lost(self):
        zeros_available = np.argwhere(self.c_boxes == 0).reshape(-1)
        if len(zeros_available) == 0:
            self.game_over()
            return True
        return False

    def game_over(self):
        if not self.check_game_over:
            messagebox.showinfo("Game over!", "The game can't be continued")
            self.check_game_over = True
        # self.root.destroy()


game = Game2048(6)
game.start_game()
