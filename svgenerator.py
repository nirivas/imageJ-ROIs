import sys
from java.awt import Color
from java.io import File
from ij import IJ
from ij.gui import ShapeRoi
from ij.plugin.frame import RoiManager
from org.jfree.graphics2d.svg import SVGGraphics2D, SVGUtils
 
imp = IJ.getImage()
rm = RoiManager.getInstance()
if rm is None:
	print 'None'
	sys.exit()  
 
# convert ROIs in RoiManager to an array of shapeRois
jrois = rm.getRoisAsArray()
srois = [ShapeRoi(jroi) for jroi in jrois]
 
# http://www.jfree.org/jfreesvg/javadoc/
g2 = SVGGraphics2D(imp.getWidth(), imp.getHeight())
g2.setPaint(Color.BLACK)
px = 0.0
py = 0.0
for sroi in srois:
	g2.translate(px*-1, py*-1)
	px = sroi.getBounds().x
	py = sroi.getBounds().y
	g2.translate(px, py)   
	g2.draw(sroi.getShape())
	
se = g2.getSVGElement()
 
# writing the file
path = "C:/Users/nicor/Downloads/testsvg3.svg"
SVGUtils.writeToSVG(File(path), se)