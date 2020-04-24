import Metashape

chunk = Metashape.app.document.chunk
for camera in chunk.cameras:
   yaw = float(camera.photo.meta["DJI/GimbalYawDegree"])
   pitch = float(camera.photo.meta["DJI/GimbalPitchDegree"])
   roll = float(camera.photo.meta["DJI/GimbalRollDegree"])
   camera.reference.rotation = Metashape.Vector([yaw, pitch, roll])