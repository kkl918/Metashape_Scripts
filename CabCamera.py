import Metashape, sys

# Checking compatibility
# compatible_major_version = "1.6"
# found_major_version = ".".join(Metashape.app.version.split('.')[:2])
# if found_major_version != compatible_major_version:
    # raise Exception("Incompatible Metashape version: {} != {}".format(found_major_version, compatible_major_version))


def add_altitude():
    """
    Adds user-defined altitude for camera instances in the Reference pane
    """

    doc = Metashape.app.document
    if not len(doc.chunks):
        raise Exception("No chunks!")

    # alt = Metashape.app.getFloat("Please specify the height to be added:", 100)
    alt = float(sys.argv[1])


    chunk = doc.chunk

    for camera in chunk.cameras:
        if camera.reference.location:
            coord = camera.reference.location
            camera.reference.location = Metashape.Vector([coord.x, coord.y, coord.z + alt])
    print("Add : "+str(sys.argv[1]))



# label = "Custom menu/Add reference altitude"
# Metashape.app.addMenuItem(label, add_altitude)
# print("To execute this script press {}".format(label))

def cab_att():
    chunk = Metashape.app.document.chunk
    for camera in chunk.cameras:
       yaw = float(camera.photo.meta["DJI/GimbalYawDegree"])
       pitch = float(camera.photo.meta["DJI/GimbalPitchDegree"])
       roll = float(camera.photo.meta["DJI/GimbalRollDegree"])
       camera.reference.rotation = Metashape.Vector([yaw, pitch, roll])


def main():
    print("Script started...")
    add_altitude()
    cab_att()

    print("Script finished!")
    
main()