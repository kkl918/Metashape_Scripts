import Metashape
import os, glob
# from PySide2 import QtWidgets

path_in = Metashape.app.getExistingDirectory("Specify the path for input TIFFs:")
path_out = Metashape.app.getExistingDirectory("Specify the path for output TIFFs:")

# app = QtWidgets.QApplication.instance()
print("script started...")
# app.processEvents()

image_list = [photo for photo in glob.iglob(path_in + "\\*.*", recursive = False) if (os.path.isfile(photo) and os.path.splitext(photo)[1][1:].lower() in ["tif"])]
input_photos = list()
for file in image_list:
	image = Metashape.Image()
	image = image.open(file, datatype="F16", channels = "RGB ")
	export_path = path_out + "//_" + os.path.basename(file)
	image.save(export_path)
	input_photos.append(export_path)
	print("Written image ", export_path)
	app.processEvents()

chunk = Metashape.app.document.addChunk()
chunk.label = "Re-saved TIFFs"
chunk.addPhotos(input_photos)
doc.chunk = chunk
print("script finished")