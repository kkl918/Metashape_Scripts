import Metashape, sys

myCSV = sys.argv[1]
# r'C:\Users\DarrenJJY\Documents\ATTwithTime.csv'
    
time2att = {}    
 
def get_att_time():    
    att_time = []
    with open(myCSV, 'r') as f:
        for row in f.readlines():
            # print(row.split(',')[0].split(' ')[1])
            #建立姿態時間陣列
            att_time.append(row.split(',')[0].split(' ')[1])

            # 把姿態加入字典中
            time2att[row.split(',')[0].split(' ')[1]] = "{},{},{}".format(row.split(',')[2], row.split(',')[3], row.split(',')[4])
    # print(time2att)
    return att_time

def final():
    # 先呼叫建立time2att裡面的資料
    get_att_time()
    
    chunk = Metashape.app.document.chunk
    
    # 找CHUNK裡面的照片時間，找出來後塞進字典找對應的姿態。
    for cam in chunk.cameras:
        cam_time = cam.photo.meta['Exif/DateTime'].split(' ')[1]
        roll  = float(time2att[cam_time].split(',')[0])
        pitch = float(time2att[cam_time].split(',')[1])
        yaw   = float(time2att[cam_time].split(',')[2])
        cam.reference.rotation = Metashape.Vector([yaw, pitch, roll])
    print('\n[OK] Write ATT to all camers!\n')
        
def main():

    print("Script started...")
   
    final()

    print("Script finished!")
    
main()