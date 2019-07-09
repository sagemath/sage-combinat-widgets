from sage.combinat.parallelogram_polyomino import ParallelogramPolyomino
from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter

class PolyominoAdapter(GridViewAdapter):
    objclass = ParallelogramPolyomino
    celltype = bool
    cellzero = False
    
    @staticmethod
    def compute_cells(obj):
        cells = {}
        lower_heights = obj.lower_heights()
        upper_heights = obj.upper_heights()
        for i in range(obj.width()):
            for j in range(upper_heights[i],lower_heights[i]):
                cells[j,i] = False
        return cells
    
    @staticmethod
    def addable_cells(obj):
        cells = []
        upper_heights = obj.upper_heights()
        for i,c in enumerate(upper_heights[1:]):
            if c != upper_heights[i]:
                cells.append((c-1,i+1))
        lower_heights = obj.lower_heights()
        for i,c in enumerate(lower_heights[1:]):
            if c != lower_heights[i]:
                cells.append((lower_heights[i],i))
        return cells
    
    @staticmethod
    def removable_cells(obj):
        heights = [(0,0)] + list(zip(obj.upper_heights(),obj.lower_heights()))
        heights.append((heights[-1][1],)*2)
        cells = []
        for i in range(1,len(heights)-1):
            x1,y1 = heights[i-1]
            x2,y2 = heights[i]
            x3,y3 = heights[i+1]
            if x2+1 < y2 and x2 != x3 and x2+1 < y1:
                cells.append((x2,i-1))
            if x2 < y2-1 and y1 != y2 and y2-1 > x3:
                cells.append((y2-1,i-1))
            
        return cells
    
    def remove_cell(self, obj, pos, dirty={}):
        heights = list(zip(obj.upper_heights(),obj.lower_heights()))
        upper_path = obj.upper_path()
        lower_path = obj.lower_path()
        i,j = pos
        index = i+j
        if heights[j][0] == i:
            upper_path[index:index+2] = [0,1]
        if heights[j][1]-1 == i:
            lower_path[index:index+2] = [1,0]
            
        return ParallelogramPolyomino([lower_path, upper_path])
    
    def add_cell(self, obj, pos, val, dirty={}):
        heights = list(zip(obj.upper_heights(),obj.lower_heights()))
        upper_path = obj.upper_path()
        lower_path = obj.lower_path()
        i,j = pos
        index = i+j
        if heights[j][0] == i+1:
            upper_path[index:index+2] = [1,0]
        if heights[j][1] == i:
            lower_path[index:index+2] = [0,1]
            
        return ParallelogramPolyomino([lower_path, upper_path])

