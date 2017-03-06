import sys
import re
import shapefile
import matplotlib.pyplot as plt
import utm
import os


# keeping sub 'extractnames' here for syntax notes.

def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.

  #open a csv of lat/lons and return shape attributes and distance

  cwd = os.getcwd()
  shp_f = r'World_Geological_Storage_Suitability_09032011_BIS.shp'
  csv_f = r'lat_lon.csv'
  shp_filename = os.path.join(cwd,shp_f)
  csv_filename = os.path.join(cwd,csv_f)

  #parse lat/lons from CSV
  conts = read_csv(csv_filename)
  print conts


  #convert lat/lons to UTM
  conts_utm=[]
  print utm.from_latlon(51.2,7.5)
  for each in conts:
    print each
    temp = utm.from_latlon(float(each[0]),float(each[1]))
    conts_utm.append([temp[0],temp[1]])
  print conts_utm




  print 'hi'
  #pull this from args later
  sf = shapefile.Reader(shp_filename)
  shapes=sf.shapes()
  fields = sf.fields
  print fields

  records = sf.records()
  print records


  output = []
  for j in range(len(fields)-1):
    if j==(len(fields)-2):
      temp=['lat','lon',fields[j+1][0]]
    else:
      temp=['','',fields[j+1][0]]
    for i in range(len(shapes)):
      temp.append(records[i][j])
    output.append(temp)

  print 'output:'
  print output

  #master loop of all shapes
  #for k in range(len(shapes)):
    
  

  ### Parser for sub-parts
  #shp0 is a list of subcoords
  shp0=[]
  #print len(shapes[0].parts)
  #print shapes[0].parts
  for i in range(len(shapes[0].parts)):
    j=shapes[0].parts[i]
    #print j
    #print shapes[0].parts[i+1]
    subshp=[]

    if j == shapes[0].parts[-1]:
      maxj=len(shapes[0].points)
    else:
      maxj=shapes[0].parts[i+1]
    while j<maxj:
      #print j
      subshp.append(shapes[0].points[j])
      j=j+1


    shp0.append(subshp)
    #print len(shp0)

  


  #output to check lat-long and shapes

  for j in range(len(shp0)):
  #for j in range(96):
  #j=96
    x=[]
    y=[]

    #print shp0[j]

    for i in range(len(shp0[j])):
      #print i
      x.append(shp0[j][i][0])
      y.append(shp0[j][i][1])          
      
      #if j==96:
        #plt.plot(x,y)
      plt.plot(x,y)




  #check whether shapes are inside or not

 #OUTPUT=[]
  for each in conts_utm:
    testpt = [each[0],each[1]]
    plt.plot(testpt[0],testpt[1],'ro')
    i=0
    dist = []
    inside = 0
    while (i<=(len(shp0)-1)and inside==0):
      inside = point_inside_polygon(testpt[0],testpt[1],shp0[i])
      dist.append(min(point_poly_dist(testpt[0],testpt[1],shp0[i])))
      i=i+1
    print 'for point %f %f'%(each[0],each[1])
    print i
    print inside
    print min(dist)

  plt.ylabel('some numbers')


  #inside = point_inside_polygon(testpt[0],testpt[1],shp0[96])
  #distance = min(point_poly_dist(testpt[0],testpt[1],shp0[96]))
  #print inside
  #print distance

  #for i in range(len(shp0[96])):
  #  print shp0[96][i][1]

  #print point_poly_dist(0,0,[[1,1],[3,2],[0,4]])
  

  plt.show()


def read_csv(filename):

  conts=[]

  f = open(filename, 'r')
  for line in f:
    print line
    temp = line.strip()
    #temp = line[:-2]
    #line.strip('\r')
    #line.strip('\n')
    conts.append(temp.split(','))

  f.close()

  return conts

  """args = sys.argv[1:]

  if not args:
    print 'usage: [--summaryfile] file [file ...]'
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]

  # +++your code here+++
  # For each filename, get the names, then either print the text output
  # or write it to a summary file
  # LAB(begin solution)
  for filename in args:
    names = extract_names(filename)

    # Make text out of the whole list
    text = '\n'.join(names)

    if summary:
      outf = open(filename + '.summary', 'w')
      outf.write(text + '\n')
      outf.close()
    else:
      print text
  # LAB(end solution)"""

def point_inside_polygon(x,y,poly):
  # determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.

    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

def point_poly_dist(x,y,poly):
  #determine the distance away a point is from a polygon
  #poly is a list of x,y pairs
  dist=[]

  n = len(poly)
  #print n

  #for i in range(n):
   #vertices = poly[i]
  for j in range(n):

    if j==(len(poly)-1):
      #last vertex connects back to the first
      x1=poly[j][0]
      y1=poly[j][1]
      x2=poly[0][0]
      y2=poly[0][1]
    else:
      x1=poly[j][0]
      y1=poly[j][1]
      x2=poly[j+1][0]
      y2=poly[j+1][1]

    
    Mnorm = (x2-x1)**2+(y2-y1)**2
    if Mnorm !=0:
      Mnorm=(Mnorm)**(0.5)
      normx = (x2-x1)/Mnorm
      normy = (y2-y1)/Mnorm
      M=normx*(x-x1)+normy*(y-y1)
    else:
      print 'same pt'
      M=0
    #print Mnorm

    #print normx
    #print normy
    
    #print M
    #print Mnorm
    if M>=Mnorm:
      D = ((x2-x)**2+(y2-y)**2)**0.5
    elif M<=0:
      D = ((x1-x)**2+(y1-y)**2)**0.5
    else:
      D=((x-x1)**2+(y-y1)**2-M**2)**0.5
    #print D

    dist.append(D)

    #if M>Mnorm: Dp2; if M<0: Dp1; else 
      
    
  """
  n = len(poly)

  for j in poly:
    if j!=(n-1):
      A=
      B=
      C=
      D=

  """
  
  return dist


def extract_names(filename):
  """
  Given a file name for baby.html, returns a list starting with the year string
  followed by the name-rank strings in alphabetical order.
  ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """
  # +++your code here+++
  # LAB(begin solution)
  # The list [year, name_and_rank, name_and_rank, ...] we'll eventually return.
  names = []

  # Open and read the file.
  f = open(filename, 'rU')
  text = f.read()
  # Could process the file line-by-line, but regex on the whole text
  # at once is even easier.

  # Get the year.
  year_match = re.search(r'Popularity\sin\s(\d\d\d\d)', text)
  if not year_match:
    # We didn't find a year, so we'll exit with an error message.
    sys.stderr.write('Couldn\'t find the year!\n')
    sys.exit(1)
  year = year_match.group(1)
  names.append(year)

  # Extract all the data tuples with a findall()
  # each tuple is: (rank, boy-name, girl-name)
  tuples = re.findall(r'<td>(\d+)</td><td>(\w+)</td>\<td>(\w+)</td>', text)
  #print tuples

  # Store data into a dict using each name as a key and that
  # name's rank number as the value.
  # (if the name is already in there, don't add it, since
  # this new rank will be bigger than the previous rank).
  names_to_rank =  {}
  for rank_tuple in tuples:
    (rank, boyname, girlname) = rank_tuple  # unpack the tuple into 3 vars
    if boyname not in names_to_rank:
      names_to_rank[boyname] = rank
    if girlname not in names_to_rank:
      names_to_rank[girlname] = rank
  # You can also write:
  # for rank, boyname, girlname in tuples:
  #   ...
  # To unpack the tuples inside a for-loop.

  # Get the names, sorted in the right order
  sorted_names = sorted(names_to_rank.keys())

  # Build up result list, one element per line
  for name in sorted_names:
    names.append(name + " " + names_to_rank[name])

  return names
  # LAB(replace solution)
  # return
  # LAB(end solution)


if __name__ == '__main__':
  main()
