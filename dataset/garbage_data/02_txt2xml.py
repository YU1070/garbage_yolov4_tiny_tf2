import cv2

out0 = '''<?xml version="1.0" encoding="utf-8"?>
<annotation>
    <folder>train</folder>
    <filename>%(filename)s</filename>
    <path>%(path)s</path>
    <source>
        <database>Unknown</database>
    </source>
    <size>
        <width>%(width)d</width>
        <height>%(height)d</height>
        <depth>3</depth>
    </size>
    <segmented>0</segmented>
'''
out1 = '''    <object>
        <name>%(class)s</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%(xmin)d</xmin>
            <ymin>%(ymin)d</ymin>
            <xmax>%(xmax)d</xmax>
            <ymax>%(ymax)d</ymax>
        </bndbox>
    </object>
'''
out2 = '''</annotation>
'''


def translate(lists):
    source = {}
    index = 0
    for jpg in lists:
        print(jpg.split())
        path = jpg.split()[0]
        image = cv2.imread(path)
        h, w, _ = image.shape
        filename = path[path.rfind('/', 1) + 1:]
        with open('./garbage.names', 'r') as f:
            garbage_lines = [i.replace('\n', '') for i in f.readlines()]
        source['filename'] = filename
        source['path'] = path
        source['width'] = w
        source['height'] = h
        fxmlpath = "./Annotations/" + str(index) + '.xml'
        with open(fxmlpath, 'w') as fxml:
            fxml.write(out0 % source)
            split_ = len(jpg.split()) // 5
            for i in range(1, split_ + 1):
                label = {}
                num = jpg.split()[5 * i]
                label['class'] = garbage_lines[int(num)]
                label['xmin'] = int(jpg.split()[1 * i])
                label['ymin'] = int(jpg.split()[2 * i])
                label['xmax'] = int(jpg.split()[3 * i])
                label['ymax'] = int(jpg.split()[4 * i])
                fxml.write(out1 % label)
            fxml.write(out2)
        index += 1


if __name__ == '__main__':
    with open('ImageSets/train.txt', 'r') as f:
        lines = [i.replace('\n', '') for i in f.readlines()]
        print(lines)
        translate(lines)
