import xml.etree.cElementTree as ET
import os

folder_path = './data/'
for filename in os.listdir(folder_path):
    if not filename.endswith('.xml'): continue
    fullname = os.path.join(folder_path, filename)
    tree = ET.parse(fullname)
        # path = '001290138'
        # tree = ET.parse('./data/'+ path + '.xml')
    root = tree.getroot()
    for child in root:
        line = ''
        #print(child.tag, child.attrib, child.text)
        print("")
        if(child.tag == 'object'):
            for grandchild in child:
                if(grandchild.tag == 'name'):
                    print(grandchild.tag, grandchild.text)
                    line = grandchild.text
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
                    #returning last card twice?
        print(line)

