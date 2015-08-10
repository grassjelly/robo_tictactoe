class Regions(object):

    def __init__(self, a, b, c, d, x, y):
        self.minY = a
        self.maxX = b
        self.maxY = c
        self.minX = d
        self.totalColumns = x
        self.totalRows = y
        self.totalXintercepts = x + 1
        self.totalYintercepts = y + 1
        self.totalIntercepts = x + y
        self.totalRegions = x * y

    def resolution(self):
        return self.width(), self.height()

    def width(self):
        width = self.maxX - self.minX
        return width

    def height(self):
        height = self.maxY - self.minY
        return height

    def xIntercepts(self):
        '''
        Returns all x-intercepts.
        Calculates all x-intercepts by adding the quotient of width and max no.
        of columns to the left most x-intercept.
        '''
        totalIntercepts =self.totalXintercepts
        constant = self.width() / self.totalRows
        intercepts =  [[] for i in xrange(totalIntercepts)]
        reference = self.minX
        for i in xrange(totalIntercepts):
            intercepts[i] = reference
            reference = reference + constant
        return intercepts

    def yIntercepts(self):
        '''
        Returns all y-intercepts.
        Calculates all y-intercepts by adding the quotient of height and max no.
        of rowsto the top most y-intercept.
        '''

        totalIntercepts = self.totalYintercepts
        constant = self.height() / self.totalRows
        intercepts =  [ [] for i in xrange(totalIntercepts)]
        reference = self.minX
        for i in xrange(totalIntercepts):
            intercepts[i] = reference
            reference = reference + constant
        return intercepts

    def regions(self):
        '''
        Returns (minY,maxX, maxY, minX) intercepts for each region.
        Merges x and y intercepts to create min and max intercepts for each
        region by populating the list in this pattern: (minY,maxX,maxY,minX)
        Regions starts from 1 - (total number of regions).From left to right
        SAMPLE INTERCEPTS:
        x-intercepts = [0, 213, 426, 639]
        y-intercepts = [0, 160, 320, 480]

        SAMPLE REGIONS
        region1 = (0  , 213, 160, 0  )
        region2 = (213, 426, 160, 0  )
        region3 = (426, 639, 160, 0)
        region4 = (0  , 213, 320, 160)
        region5 = (213, 426, 320, 160)
        region6 = (426, 639, 320, 160)
        region7 = (0  , 213, 480, 320)
        region8 = (213, 426, 480, 320)
        region9 = (426, 639, 480, 320)

        ALGORITHM
        The list is populated based on the pattern seen on each region created
        by merging x and y intercepts.

        *index of minY increases every iteration. Restarts every (total no of
         columns),

        *index of maxX is +1 of minY's index and increases every iteration.
         Restarts every (total no of columns) iterations,

        *index of maxY is +1 of maxY's index  and is the same for (total no of
         columns) iteration. Index increases after (total no of columns)
         iterations.

        *index of minX is the same for (total no of columns) iteration. Index
         increases after (total no of columns) iterations,
        '''

        totalLists = self.totalRegions
        #create a list
        regions = [ [] for i in xrange(totalLists)]
        indexX = 0
        indexY = 0
        rowCount = 0
        columnCount = 0
        for i in xrange(totalLists):
            a = self.xIntercepts()[indexX]      # minY
            b = self.xIntercepts()[indexX + 1]  # maxX
            c = self.yIntercepts()[indexY + 1]  # maxY
            d = self.yIntercepts()[indexY]      # minX
            regions[i]=(a,b,c,d)

            rowCount = rowCount + 1
            columnCount = columnCount + 1

            if rowCount < self.totalColumns:
                indexX = indexX + 1

            elif rowCount == self.totalColumns:
                indexX = 0
                rowCount = 0

            if columnCount == self.totalColumns:
                indexY = indexY + 1
                columnCount = 0

        return regions

    def checkRegion(self, x, y):
        # Returns the region of a given point (x,y)
        index = 0
        for a in self.regions():
            xMin = a[0]
            xMax = a[1]
            yMin = a[3]
            yMax = a[2]
            index += 1
            if((x >= xMin) and (x <= xMax)) and ((y >= yMin) and (y <= yMax)):
                    return index

    def center(self):
        index = 0
        centers =  [ [] for i in xrange(self.totalRegions)]
        for i in xrange(self.totalYintercepts-1):
            for ii in xrange(self.totalXintercepts-1):
                x1 = self.xIntercepts()[ii]
                x2 = self.xIntercepts()[ii + 1]
                y1 = self.yIntercepts()[i]
                y2 = self.yIntercepts()[i+1]

                x = (x2 - x1) / 2
                y = (y2 - y1) / 2
                centers[index] = x1 + x, y1 + y
                index = index + 1

        return centers

if __name__ == "__main__":
    region = Regions(0, 480, 480,0, 3, 3)
    print region.totalXintercepts
