"""
File:    boxes_and_items.py
Author:  Sriram Vema
Date:    11/13/2020
Section: 43
E-mail:  sriramv1@umbc.edu
Description:
  This program adds and removes items in a box
"""
class Box:
    def __init__(self,x,y,z):
        self.volume = x * y * z
        self.items = []
        self.unoccupied_space = self.volume
    def place(self, item):
        if item.volume <= self.unoccupied_space:
            self.items.append(item)
            self.unoccupied_space -= item.volume
    def remove (self, item):
        if item in self.items:
            self.items.remove(item)
            self.unoccupied_space += item.volume
        else:
            print("The item" , item.name, "is not in the box")
    pass

class Item:
    def __init__(self,name, length,width,height):
        self.name = name
        self.volume = length * width * height
    pass


if __name__ == '__main__':
    box_list = []
    item_list = []
    command = input('What do you want to do? ')
    while command.strip().lower() != 'quit':
        if command.strip().startswith('create box'):
            try:
                x, y, z = [int(x) for x in command.split()[2:]]
                box_list.append(Box(x, y, z))
            except:
                print('oops probably the wrong number of arguments')
        elif command.strip().startswith('create item'):
            name = command.split()[2]
            try:
                x, y, z = [int(x) for x in command.split()[3:]]
                item_list.append(Item(name, x, y, z))
            except:
                print('oops probably wrong number of arguments')
        elif command.strip().startswith('display boxes'):
            for i, box in enumerate(box_list):
                print("Box {}: with volume {} with {} space left".format(i + 1, box.volume, box.unoccupied_space))
                for item in box_list[i].items:
                    print('\t', item.name, 'is in the box.')
        elif command.strip().startswith('display items'):
            for i, item in enumerate(item_list):
                print("Item {}: with volume {}".format(item.name, item.volume))
        elif command.strip().startswith('place'):
            name_of_item = command.split()[1]
            the_item = None
            for item in item_list:
                if item.name == name_of_item:
                    the_item = item
            number_of_box = int(command.split()[3]) - 1
            if number_of_box in range(len(box_list)) and the_item:
                box_list[number_of_box].place(the_item)
            else:
                print('Error with box number or item name')
        elif command.strip().startswith('remove'):
            name_of_item = command.split()[1]
            the_item = None
            for item in item_list:
                if item.name == name_of_item:
                    the_item = item
            number_of_box = int(command.split()[3]) - 1
            if number_of_box in range(len(box_list)) and the_item:
                box_list[number_of_box].remove(the_item)
            else:
                print('Error with box number or item name')
        command = input('What do you want to do? ')

