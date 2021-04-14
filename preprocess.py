import xml.etree.cElementTree as ET
import os

def main():
    folder_path = './data/'
    for filename in os.listdir(folder_path):
        if not filename.endswith('.xml'): continue
        fullname = os.path.join(folder_path, filename)
        f = open(filename[:-4]+".txt", "w+")
        tree = ET.parse(fullname)
            # path = '001290138'
            # tree = ET.parse('./data/'+ path + '.xml')
        root = tree.getroot()
        for child in root:
            line = ''
            if(child.tag == 'object'):
                for grandchild in child:
                    if(grandchild.tag == 'name'):
                        # print(grandchild.tag, grandchild.text)
                        # print(parseCardName(grandchild.text))
                        line = str(parseCardName(grandchild.text))
                    elif(grandchild.tag == "bndbox"):
                        # print(grandchild[0].tag, grandchild[0].text) #x min
                        # print(grandchild[1].tag, grandchild[1].text) #y min
                        # print(grandchild[2].tag, grandchild[2].text) #x max
                        # print(grandchild[3].tag, grandchild[3].text) #y max
                        x_dif = int(str(grandchild[2].text)) - int(str(grandchild[0].text))
                        y_dif = int(str(grandchild[3].text)) - int(str(grandchild[1].text))
                        x_center = str(int(str(grandchild[2].text)) - (x_dif / 2))
                        y_center = str(int(str(grandchild[3].text)) - (y_dif / 2))
                        width = str(x_dif)
                        height = str(y_dif)
                        line = line +' '+ x_center +' '+  y_center +' '+  width +' '+  height
                        #returning last card twice: the top card's suit and label 
                        #are visible at the top and bottom
            if(line != ''):
                print(line)
                f.write(line+"\n")

def parseCardName(name):
    suits = ['d', 'h', 'c', 's']
    suit_values = [0, 13, 26, 39]
    cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    card_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    curr_suit = name[1] #d, h, c, s
    curr_card = name[0] #A, 1...10, J, K, Q
    if(len(name) > 2):
        curr_suit = name[2] #d, h, c, s
        curr_card = name[0:2]
        
    suit_index = suits.index(curr_suit)
    card_index = cards.index(curr_card)
    card_num = suit_values[suit_index] + card_values[card_index]
    return card_num

if __name__ == "__main__":
    main()