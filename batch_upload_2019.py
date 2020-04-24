import os, requests ,pathlib, shutil,subprocess, time
from ftplib import FTP
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.dom import minidom
from subprocess import PIPE



info  = ['140.116.249.139','geodac','rsej0hk45j/vup','/TCGEO/2019']
ftp   = FTP(info[0])
ftp.login(info[1], info[2])
ftp.encoding='UTF-8'
ftp.cwd(info[3])
ftp_list = ftp.nlst(info[3])


url_front = 'https://geodac.ncku.edu.tw/TCGEO/2019/'
path      = r'\\140.116.228.155\geodac_uav\2019'

i=0
list = []
dic  = {}
tiles= {}
kmls = {}

root = ET.Element('tree',id="0")

def single_upload_folder(list, name):
    for i in list:
        if  i == 'name':
            print(i, '\t', dic[i][34:])
            tile = tiles[i]
            ftp.mkd(i)
            ftp.cwd(i)
            ftp.mkd('cad')
            ftp.mkd('othro')
            ftp.cwd('othro')
            print('[Start] upload tile.\n')
            uploadThis(tile)        
            ftp.mkd('model')
            ftp.cwd('..')


def uploadThis(path):
    if os.path.isdir(path):

        files = os.listdir(path)
        os.chdir(path)
        for f in files:
            if os.path.isfile(path + r'\{}'.format(f)):
                fh = open(f, 'rb')
                ftp.storbinary('STOR %s' % f, fh)
                fh.close()
            elif os.path.isdir(path + r'\{}'.format(f)):
                ftp.mkd(f)
                ftp.cwd(f)
                uploadThis(path + r'\{}'.format(f))
        ftp.cwd('..')
        os.chdir('..')

    else:
        print('[Error] empty folder: ', path[34:], '\n')
 

def upload_folder(list):
    for i in list:
        print(i, '\t', dic[i][34:])
        tile = tiles[i]
        ftp.mkd(i)
        ftp.cwd(i)
        ftp.mkd('cad')
        ftp.mkd('othro')
        ftp.cwd('othro')
        print('[Start] upload tile.\n')
        uploadThis(tile)        
        ftp.mkd('model')
        ftp.cwd('..')
        
        
def upload_tiles(list):
    for i in list[4:]:
        tile = tiles[i]
        dst  = os.path.join(i, 'othro')
        ftp.cwd(dst)
        
        uploadThis(tile)
        
def add_3D(name, date, wgs84, othro_location, cad_location, model_location, output):
    # check(dic['othro']+'index.html')
    # check(dic['cad'])
    # check(dic['model']+'tileset.json')
    one = ET.SubElement(root, "item", text = name[9:], id = name, nocheckbox="1", im0="hd.gif", im1="folderOpen.gif", im2="folderClosed.gif")
    ET.SubElement(one , "item", text = '正射影像_' + date + '(雙擊定位)'       ,  id = wgs84 + ';;18@TileImage_ps@' + othro_location ,  im0='hd.gif',  im1='folderOpen.gif',  im2='folderClosed.gif').text = ' '
    ET.SubElement(one , "item", text = '工程圖說'                              ,  id = wgs84 + ';;18@kml@'          + cad_location   ,  im0='hd.gif',  im1='folderOpen.gif',  im2='folderClosed.gif').text = ' '
    ET.SubElement(one , "item", text = '3D_模型'                               ,  id = wgs84 + ';;18@3DModel@'      + model_location ,  im0='hd.gif',  im1='folderOpen.gif',  im2='folderClosed.gif').text = ' '
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    
    
    with open(output, 'w',encoding = 'utf8') as myXML:
        myXML.write(xmlstr)        

def create_xml(i, wgs84):
    # create each location in ftp
    othro_location = os.path.join(url_front, i, 'othro/').replace('\\', '/')
    cad_location   = os.path.join(url_front, i, 'cad/'  ).replace('\\', '/')
    model_location = os.path.join(url_front, i, 'model/').replace('\\', '/')
    
    # output file path
    output         = path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_8 + '\\'  + r'upload\xml.txt'                           
    
    # chunkname date wgs84 othro_location cad_location model_location outputFile
    add_3D(i, i[0:8], wgs84, othro_location, cad_location, model_location, output)

def get_wgs84(dir_name):
    kml_folder = os.path.join(path, dir_name, '1.測繪產品', '1.8.3DModel_3D模型', dir_name)
    if os.path.isdir(kml_folder):
        for kml in os.listdir(kml_folder):
            if kml.endswith('kml') and os.path.isfile(os.path.join(kml_folder,kml)):
                    kml = os.path.join(kml_folder,kml)
                    with open(kml, 'r',encoding = 'utf8')as f:
                        soup   = BeautifulSoup(f.read(), 'html.parser')
                        lon    = soup.select('longitude')[0].text
                        lat    = soup.select('latitude')[0].text
                        wgs84  = lat+ ';' + lon 
                        return wgs84

def check(url, name):
    
    res = requests.get(url)
    if   res.status_code == 200:
        
        # print(url, '[ok] -> 圖資在線!')
        return None
    else:
        print('\n[Error] 請確認圖資是否掛載:', url, '\n')
        return name

def nain_upload():
    for i in list[4:]:
        name  = dic[i][34:]
        date  = dic[i][34:42]
        wgs84 = get_wgs84(dic[i][34:])
        othro_location = os.path.join(url_front, i, 'othro/').replace('\\', '/')
        cad_location   = os.path.join(url_front, i, 'cad/'  ).replace('\\', '/')
        model_location = os.path.join(url_front, i, 'model/').replace('\\', '/')
        output         = path + '\\' + name + '\\' +'xml.txt'
        
        # # debug
        # print(name)
        # print(date)
        # print(wgs84)
        # print(othro_location)
        # print(cad_location)
        # print(model_location)
        # print(output)
        # print('\n')
        
        tile_location = os.path.join(url_front, i, 'othro/index.html').replace('\\', '/')
        check(tile_location, name)
        # if after_check != None:
          # single_upload_folder(list, after_check)
          # print('[excute] single_upload_folder')
          
        
        if wgs84 == None:
            print('[Error] WGS84 is None:',name, '\n')
        else:
            add_3D(name, date, wgs84, othro_location, cad_location, model_location, output)        




#  - - - - - - - - - main - - - - - - - - -
for dir in os.listdir(path):
    
    if os.path.isdir(os.path.join(path,dir)):
        full_path = os.path.join(path,dir)
        tile_path = os.path.join(path,dir,'1.測繪產品','1.1.Ortho_正射影像(包含附加檔)',dir)
        kml_path  = os.path.join(path,dir,'1.測繪產品','1.1.Ortho_正射影像(包含附加檔)',dir)
        dir = dir[:8]
        if dir not in list: 
            i=0
            list.append(dir)
            dic[dir] = full_path
            tiles[dir] = tile_path
        else:
            list.append(dir+str(chr(i+65)))
            dic[dir+str(chr(i+65))] = full_path
            tiles[dir+str(chr(i+65))] = tile_path
            i = i + 1


# index_file = os.path.join(path, 'index.txt')
# with open(index_file, 'a', encoding = 'utf8') as f:            
    # for k, v in dic.items():
        # f.write(k)
        # f.write('\t')
        # f.write(v+'\n')
        
# move file and call tran3d
def tran_3d_init():
    # init
    path_155 = r'\\140.116.228.155\geodac_uav\2018'
    path_174 = r'\\140.116.228.174\geodac_data_test\RAW\RSImage\UAV\3DModel'
    cmd = {}
    need_tran = []
    # i == index
    for i in list[4:]:
        # print(i, dic[i][34:])
        dir_155 = os.path.join(dic[i], '1.測繪產品', '1.8.3DModel_3D模型')

        for item in os.listdir(dir_155):
            dir_174 = os.path.join(path_174, i)
            pathlib.Path(dir_174).mkdir(parents=True, exist_ok=1)
            if item[-3:] == 'txt':
                lat = item[0:13]
                lon = item[14:28]
                tran = "ssh user1@140.116.228.180 -p 2202 './trans3d "+i+' '+lon+' '+lat+ "'"
                cmd[i] = tran

            if len(os.listdir(dir_174)) == 0:
                # print(len(os.listdir(dir_174)), '\t', dir_174)
                #shutil.copyfile(src, dst)  
                # print('[move]: ', i)
                if item[-3:] == 'obj':
                    shutil.copyfile(os.path.join(dir_155,item),os.path.join(dir_174,item))

                elif item[-3:] == 'mtl':
                    shutil.copyfile(os.path.join(dir_155,item),os.path.join(dir_174,item))
                elif item[-3:] == 'jpg':
                    shutil.copyfile(os.path.join(dir_155,item),os.path.join(dir_174,item))    
            
            elif len(os.listdir(dir_174)) == 3:
                if i not in need_tran:
                    print('[add]: ', i)
                    need_tran.append(i)
    print('\n')
    for i in need_tran:
        print('[' + i + ']' + cmd[i])
        process  = subprocess.Popen('powershell.exe ' + cmd[i], stdout=PIPE, stderr=PIPE, stdin=PIPE)
        out, err = process.communicate()
        print('[stdout]: ', out)
        print('[stderr]: ', err)
        print('\n')
        


    

  