import sys
import os
import re
import subprocess
import json

from tkinter import Tk, Canvas, Frame, BOTH, W, LAST

class Box:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center = (x + width / 2, y + height / 2)
        self.edges = [((x,y), (x + width, y)), ((x + width, y), (x + width, y + height)), ((x + width, y + height), (x, y + height)), ((x, y + height), (x, y))]

    def subtract(self, p1, p2):
        return ((p1[0] - p2[0]), (p1[1] - p2[1]))

    def find_line_intersection(self, l1, l2):
        p = l1[0]
        r = self.subtract(l1[1], l1[0])
        q = l2[0]
        s = self.subtract(l2[1], l2[0])
        rxs = r[0] * s[1] - r[1] * s[0]
        qp = self.subtract(q, p)
        qpxs = qp[0] * s[1] - qp[1] * s[0]
        qpxr = qp[0] * r[1] - qp[1] * r[0]
        if rxs == 0 and qpxr == 0:
            return None
        if rxs == 0:
            return None
        t = qpxs / rxs
        u = qpxr / rxs
        if t >= 0 and t <= 1 and u >= 0 and u <= 1:
            x_coord = p[0] + t * r[0]
            y_coord = p[1] + t * r[1]
            return (x_coord, y_coord)
        return None

    def find_first_intersection(self, line):
        intersection_pts = []
        for edge in self.edges:
            inter = self.find_line_intersection(line, edge)
            if not inter == None:
                intersection_pts.append((inter,edge))
        if len(intersection_pts) == 0:
            return None
        min_point = None
        min_edge = None
        min_sq_dist = float("inf")
        for pt,edge in intersection_pts:
            dist = (line[0][0] - pt[0]) * (line[0][0] - pt[0]) + (line[0][1] - pt[1]) * (line[0][1] - pt[1])
            if dist < min_sq_dist:
                min_sq_dist = dist
                min_point = pt
                min_edge = edge
        return min_point, min_edge



class Arrow:
    def __init__(self, startBox, endBox):
        self.start = startBox
        self.end = endBox
        self.key_points = [startBox.center, endBox.center]

    def determineKeyPoints(self, boxes, arrows):
        """Determine the key points of this arrow"""



class MemoryDiagram(Frame):
    def __init__(self, memory, boxWidth = 100, boxHeight = 50):
        super().__init__()
        self.memory = memory
        self.address_mapping = {}
        self.boxWidth = boxWidth
        self.boxHeight = boxHeight
        self.boxes = []
        self.arrows = []
        self.initUI()

    def initUI(self):
        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1)
        self.drawDiagram()

    def drawDiagram(self):
        self.drawStackBoxes()
        self.canvas.create_line(2 * self.boxWidth, 0, 2 * self.boxWidth, 1000, dash=(4,2))
        self.drawHeapBoxes()
        self.generateHeapArrows()
        self.generateStackArrows()
        self.drawArrows()

    def drawArray(self, x, y, width, height, number, vert, objects = None, offset = 0):
        for i in range(number):
            x_loc = 0
            y_loc = 0
            if vert:
                x_loc = x
                y_loc = y + i * (height + offset)
            else:
                x_loc = x + i * (width + offset)
                y_loc = y
            box = Box(x_loc, y_loc, width, height)
            self.drawBox(box)
            if not objects == None:
                if "points-to-base" in objects[i]:
                    circle_radius = 4
                    self.canvas.create_oval(box.center[0] - circle_radius, box.center[1] - circle_radius, box.center[0] + circle_radius, box.center[1] + circle_radius, outline="#000", fill="#000", width=1)
                else:
                    self.canvas.create_text(box.x + box.width / 10, box.y + box.height / 2, anchor=W, font="Roboto", text=int(objects[i]["value"], 16))
                self.address_mapping[int(objects[i]["address"], 16)] = box

    def drawBox(self, box):
        self.canvas.create_rectangle(box.x, box.y, box.x + box.width, box.y + box.height, outline="#000", fill="#fff", width=2)
        self.boxes.append(box)

    def drawStackBoxes(self):
        stack_objs = self.memory["thread stacks"][0]["contents"]
        #stack_objs = stack_objs[1:-1]
        self.drawArray(self.boxWidth / 2, self.boxHeight / 2, self.boxWidth, self.boxHeight, len(stack_objs), True, stack_objs)
        #print(json.dumps(self.address_mapping, indent=4, sort_keys=True))

    def drawHeapBoxes(self):
        heap_objs = self.memory["heap objects"]
        x_loc = int(2.5 * self.boxWidth)
        y_loc = self.boxHeight / 2
        for i in range(len(heap_objs)):
            objs = heap_objs[i]["contents"]
            self.drawArray(x_loc, y_loc, self.boxWidth, self.boxHeight, len(objs), False, objs)
            y_loc += self.boxWidth

    def generateStackArrows(self):
        stack_objs = self.memory["thread stacks"][0]["contents"]
        #stack_objs = stack_objs[1:-1]
        for obj in stack_objs:
            if "points-to-base" in obj:
                if obj["points-to-type"] == "stack":
                    start_box = self.address_mapping[int(obj["address"], 16)]
                    end_box = self.address_mapping[int(obj["value"], 16)]
                    arrow = Arrow(start_box, end_box)
                    self.arrows.append(arrow)
                else:
                    start_box = self.address_mapping[int(obj["address"], 16)]
                    end_box = self.address_mapping[int(obj["value"], 16)]
                    arrow = Arrow(start_box, end_box)
                    self.arrows.append(arrow)

    def generateHeapArrows(self):
        heap_objs = self.memory["heap objects"]
        for heap_obj in heap_objs:
            for obj in heap_obj["contents"]:
                if "points-to-base" in obj:
                    start_box = self.address_mapping[int(obj["address"], 16)]
                    end_box = self.address_mapping[int(obj["value"], 16)]
                    arrow = Arrow(start_box, end_box)
                    self.arrows.append(arrow)

    def organizeArrows(self, edge, arrows):
        step_x = abs((edge[0][0] - edge[1][0])/(len(arrows)+1))
        step_y = abs((edge[0][1] - edge[1][1])/(len(arrows)+1))
        start_x = min(edge[0][0], edge[1][0])
        start_y = min(edge[0][1], edge[1][1])
        for i in range(len(arrows)):
            start_x+=step_x
            start_y+=step_y
            arrows[i] = ((start_x,start_y), arrows[i][1])
        return arrows

    def drawArrows(self):
        sorted_edges = {}
        for arrow in self.arrows:
            arrow.determineKeyPoints(self.boxes, self.arrows)
            for i in range(len(arrow.key_points) - 1):
                inter, edge = arrow.end.find_first_intersection(((arrow.key_points[i][0], arrow.key_points[i][1]), (arrow.key_points[i+1][0], arrow.key_points[i+1][1])))
                if edge not in sorted_edges:
                    sorted_edges[edge] = []
                # Puts the intersection point, as well as the arrow inside the
                # Hash table organized by the edge it intersects with
                sorted_edges[edge].append((inter,arrow))

        for edge in sorted_edges:
            sorted_edges[edge] = sorted(sorted_edges[edge], key = lambda x:(x[0][0], x[0][1]))
            sorted_edges[edge] = self.organizeArrows(edge, sorted_edges[edge])
            for arrow in sorted_edges[edge]:
                self.drawArrow(arrow[0], arrow[1])

    def drawArrow(self, inter, arrow):
        for i in range(len(arrow.key_points) - 1):
            perp_line = (-inter[1]+arrow.key_points[i][1], inter[0]-arrow.key_points[i][0])
            mid_point = ((arrow.key_points[i][0] + inter[0])/2,(arrow.key_points[i][1] + inter[1])/2)
            if inter[1] < arrow.key_points[i][1]:
                new_point_x = mid_point[0]+(perp_line[0]/4)
                new_point_y = mid_point[1]+(perp_line[1]/4)
            else:
                new_point_x = mid_point[0]-(perp_line[0]/4)
                new_point_y = mid_point[1]-(perp_line[1]/4)

            self.canvas.create_line(arrow.key_points[i][0], arrow.key_points[i][1], new_point_x, new_point_y, inter[0], inter[1], arrow = LAST, smooth=True, width=2)


if __name__ == "__main__":
    arguments = " ".join(sys.argv[1::])
    os.system("mkdir -p /tmp/memory_diagram")
    os.system("rm -rf /tmp/memory_diagram/*")
    os.system("g++ " + arguments + " -g -O0 -I/work/drmemory/releases/DrMemory-Linux-2.3.18322/drmf/include /work/drmemory/releases/DrMemory-Linux-2.3.18322/drmf/lib64/release/libdrmemory_annotations.a -o /tmp/memory_diagram/a.out")
    result = subprocess.run("/work/drmemory/releases/DrMemory-Linux-2.3.18322/bin64/drmemory -brief -- /tmp/memory_diagram/a.out", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    json_files = re.findall(r'^\s*~~Dr\.M~~ Memory layout written to: (\/tmp\/Dr\. Memory\/DrMemory-a\.out\..*?\.json)$', result.stderr.decode('utf-8'), re.MULTILINE)
    json_outputs = []
    for file in json_files:
        with open(file) as f:
            json_outputs.append(json.load(f))

    print(json.dumps(json_outputs, indent=4, sort_keys=True))

    root = Tk()
    md = MemoryDiagram(json_outputs[0])
    root.geometry("1000x1000")
    root.mainloop()
