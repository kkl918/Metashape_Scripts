########################################
## Created on 2018/07/01              ##
## author: Chia-Ching Lin             ##
##                                    ##
## 專案CHUNK名字必須與155上資料夾一致 ##
########################################
import os, sys, zipfile, pathlib,  datetime, shutil, subprocess
import PhotoScan, chardet
from tkinter.filedialog import *
from bs4 import BeautifulSoup
from subprocess import PIPE
from ftplib import FTP
import xml.etree.ElementTree as ET
from xml.dom import minidom

tw97   = PhotoScan.CoordinateSystem("EPSG::3826")
ws84   = PhotoScan.CoordinateSystem("EPSG::3857")
ds84  = PhotoScan.CoordinateSystem("EPSG::4326") 
crs    = PhotoScan.CoordinateSystem('LOCAL_CS["Local CS",LOCAL_DATUM["Local Datum",0],UNIT["metre",1]]')


path = r'\\140.116.228.155\geodac_uav\2019'
dir  = r'C:\Users\RSLAB\Desktop\dir\\'

dir_1   = '1.測繪產品'
dir_1_1 = '1.1.Ortho_正射影像(包含附加檔)'
dir_1_2 = '1.2.OrigPhoto_原始照片'
dir_1_3 = '1.3.PrecEval_精度評估報告'
dir_1_4 = '1.4.ContCoor_控制點座標)'
dir_1_5 = '1.5.ContPhoto_控制點照片'
dir_1_6 = '1.6.FlyRec_飛行記錄'
dir_1_7 = '1.7.DSM_數值地表模型'
dir_1_8 = '1.8.3DModel_3D模型'

info  = ['140.116.249.139','geodac','rsej0hk45j/vup','/TCGEO/2019']
ftp   = FTP(info[0], info[1], info[2])
ftp.encoding = 'big5'
ftp.cwd(info[3])
# ftp_list = ftp.nlst(info[3])

print("\n- - - - - - - - Script started - - - - - - - - \n")

def workflow():
    pass

def create_dir(name):
    #pathlib.Path(path+ name).mkdir(parents=True, exist_ok=0)
    pathlib.Path(path+'\\'+ name + '/1.測繪產品').mkdir(parents=True, exist_ok=0)
    pathlib.Path(path+'\\'+ name + '/2.環景照片').mkdir(parents=True, exist_ok=0)
    pathlib.Path(path+'\\'+ name + '/3.一般產品').mkdir(parents=True, exist_ok=0)
    pathlib.Path(path+'\\'+ name + '/4.影片').mkdir(parents=True, exist_ok=0)
    pathlib.Path(path+'\\'+ name + '/Photoscan').mkdir(parents=True, exist_ok=0)
    #open('.\\'+ name + '\\Photoscan' + '\\' + name + '.psx','w')
    pathlib.Path(path+'\\'+ name + '/1.測繪產品' + './1.1.Ortho_正射影像(包含附加檔)').mkdir(parents=True, exist_ok=0)
    pathlib.Path(path+'\\'+ name + '/1.測繪產品' + './1.2.OrigPhoto_原始照片').mkdir(parents=True, exist_ok=0)
    pathlib.Path(path+'\\'+ name + '/1.測繪產品' + './1.3.PrecEval_精度評估報告').mkdir(parents=True, exist_ok=0)
    pathlib.Path(path+'\\'+ name + '/1.測繪產品' + './1.4.ContCoor_控制點座標)').mkdir(parents=True, exist_ok=0)
    pathlib.Path(path+'\\'+ name + '/1.測繪產品' + './1.5.ContPhoto_控制點照片').mkdir(parents=True, exist_ok=0)
    pathlib.Path(path+'\\'+ name + '/1.測繪產品' + './1.6.FlyRec_飛行記錄').mkdir(parents=True, exist_ok=0)
    pathlib.Path(path+'\\'+ name + '/1.測繪產品' + './1.7.DSM_數值地表模型').mkdir(parents=True, exist_ok=0)
    pathlib.Path(path+'\\'+ name + '/1.測繪產品' + './1.8.3DModel_3D模型').mkdir(parents=True, exist_ok=0)

def add_3D(name, date, wgs84, othro_location, cad_location, model_location, output):
    # check(dic['othro']+'index.html')
    # check(dic['cad'])
    # check(dic['model']+'tileset.json')
    root = ET.Element('tree',id="0")
    one = ET.SubElement(root, "item", text = name[9:], id = name, nocheckbox="1", im0="hd.gif", im1="folderOpen.gif", im2="folderClosed.gif")
    ET.SubElement(one , "item", text = '正射影像_' + date + '(雙擊定位)'       ,  id = wgs84 + ';;18@TileImage_ps@' + othro_location ,  im0='hd.gif',  im1='folderOpen.gif',  im2='folderClosed.gif').text = ' '
    ET.SubElement(one , "item", text = '工程圖說'                              ,  id = wgs84 + ';;18@Kml@'          + cad_location   ,  im0='hd.gif',  im1='folderOpen.gif',  im2='folderClosed.gif').text = ' '
    ET.SubElement(one , "item", text = '3D_模型'                               ,  id = wgs84 + ';;18@3DModel@'      + model_location ,  im0='hd.gif',  im1='folderOpen.gif',  im2='folderClosed.gif').text = ' '
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    
    
    with open(output, 'w',encoding = 'utf8') as myXML:
        myXML.write(xmlstr)        

def create_xml(i, wgs84):
    url_front = 'https://geodac.ncku.edu.tw/TCGEO/2019/'
    # create each location in ftp
    othro_location = os.path.join(url_front, i, 'othro/').replace('\\', '/')
    cad_location   = os.path.join(url_front, i, 'cad/'  ).replace('\\', '/')
    model_location = os.path.join(url_front, i, 'model/').replace('\\', '/')
    
    # output file path
    output         = path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_8 + '\\'  + r'xml.txt'                           
    
    # chunkname date wgs84 othro_location cad_location model_location outputFile
    add_3D(i, i[0:8], wgs84, othro_location, cad_location, model_location, output)

# 自動產生 TIFF、KMZ、TILE、MODEL(含解壓縮及中心座標檔案)
def export():
    
    for chunk in PhotoScan.app.document.chunks:
        for i in os.listdir(path):
            # print('chunk name: ' + chunk.label)
            if i == chunk.label:
            
                    #create_dir(i)
                    
                    
                    # 1.1.Ortho_正射影像
                    #------- 路徑 ---- 資料夾檔名 - 1.測繪產品 ------ 1.1 ----- 檔案名稱+副檔名 
                    othro  = path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_1 + '\\' + i + '.tif'
                    tile   = path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_1 + '\\' + i + '.zip'
                    report = path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_3 + '\\' + i + '.pdf'
                    kmz    = path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_1 + '\\' + i + '.kmz'
                    
                    # 1.4.ContCoor_控制點座標)
                    path_marker = path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_4 + '\\' + i + '.txt'
                    
                    # 1.7.DSM_數值地表模型
                    dsm97    = path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_7 + '\\' + i + '_tw97.tif'
                    dsm84    = path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_7 + '\\' + i + '_wgs84.tif'
                    
                    # 1.8.3DModel_3D模型
                    obj    = path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_8 + '\\' + 'model' + '.obj'
                    kmz_3d = path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_8 + '\\' + i + '.kmz'
                    

                    
                    # T = chunk.transform.matrix
                    # f = open(path_marker, 'wt')
                    # for marker in chunk.markers:
                       # if not marker.position:
                          # continue
                       # v_t = T.mulp(marker.position)
                       # chunk.crs = PhotoScan.CoordinateSystem("EPSG::4326")
                       # v_out = chunk.crs.project(v_t)
                       # f.write(marker.label + ',' + str(v_out[0]) + ',' + str(v_out[1]) + ',' + str(v_out[2]) + '\n')
                       # print(marker.label + ',' + str(v_out[0]) + ',' + str(v_out[1]) + ',' + str(v_out[2]) + '\n')
                    # f.close()
                    
                    
                    ## 正射影像 TIFF
                    # chunk.exportOrthomosaic(othro,image_format=PhotoScan.ImageFormatTIFF,projection=tw97,raster_transform=PhotoScan.RasterTransformNone,write_kml=True,write_world=True,white_background=False)
                    # print('[OK] export othro.')
                    
                    ## 正射影像 KMZ
                    chunk.exportOrthomosaic(kmz  ,format=PhotoScan.RasterFormatKMZ,raster_transform=PhotoScan.RasterTransformNone,write_kml=True,write_world=True)
                    print('[OK] export kmz.')

                    ## 報告
                    chunk.exportReport(report, title = i, description = 'Made by GEODAC')
                    print('[OK] export report.')

                    ## 圖專
                    chunk.exportOrthomosaic(tile,format=PhotoScan.RasterFormatXYZ,image_format=PhotoScan.ImageFormatPNG,raster_transform=PhotoScan.RasterTransformNone,projection=ws84,write_kml=True)
                    print('[OK] export tile.')
                    
                    ## DSM
                    chunk.exportDem(path=dsm97,format=PhotoScan.RasterFormatTiles,image_format=PhotoScan.ImageFormatTIFF,projection= tw97, nodata=-32767)
                    chunk.exportDem(path=dsm84,format=PhotoScan.RasterFormatTiles,image_format=PhotoScan.ImageFormatTIFF,projection= ds84, nodata=-32767)
                    print('[OK] export dsm.')            
                    
                    ##三維模型 OBJ
                    chunk.exportModel(obj   , binary=False, precision=6, texture_format=PhotoScan.ImageFormatJPEG, texture=True, normals=False, colors=False, cameras=False, udim=False, strip_extensions=False, format=PhotoScan.ModelFormatOBJ, projection=crs)
                    print('[OK] export obj.')

                    ##三維模型 KMZ
                    chunk.exportModel(kmz_3d   , binary=False, precision=6, texture_format=PhotoScan.ImageFormatJPEG, texture=True, normals=False, colors=False, cameras=False, udim=False, strip_extensions=False, format=PhotoScan.ModelFormatKMZ, projection=crs)
                    print('[OK] export kmz_3d.')

                    ## 解壓縮KMZ_3D
                    with zipfile.ZipFile(kmz_3d, 'r') as kmz:
                        pathlib.Path(path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_8 + '\\' + i).mkdir(parents=True, exist_ok=1)
                        #os.mkdir(path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_8 + '\\' + i)
                        kmz.extractall(path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_8 + '\\' + i + '\\')
                        print('[OK] unzip kmz_3d')
                                        
                    # ## 輸出至D槽，創建資料夾
                    # out_case  = os.path.join('D:\Backup139\\', i)
                    # out_tile  = os.path.join(out_case, 'othro')
                    # out_cad   = os.path.join(out_case, 'cad')
                    # out_model = os.path.join(out_case, 'model')
                    
                    # pathlib.Path(out_case).mkdir(parents=True, exist_ok=1)
                    # pathlib.Path(out_tile).mkdir(parents=True, exist_ok=1)
                    # pathlib.Path(out_cad).mkdir(parents=True, exist_ok=1)
                    # # pathlib.Path(out_model).mkdir(parents=True, exist_ok=1)


                    # ## 讀取中心座標    
                    # kml = path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_8 + '\\' + i + '\\' + 'doc.kml'
                    # with open(kml, 'r', encoding = 'utf8')as f:

                        # soup = BeautifulSoup(f.read(), 'html.parser')
                        # lon = soup.select('longitude')[0].text
                        # lat = soup.select('latitude')[0].text
                        # center = lat+ ',' + lon  
                        # wgs84  = lat+ ';' + lon
                        # output = path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_8 + '\\' + center + '.txt'
                        # open(output, 'a',encoding = 'utf8')
                        # print('[OK] create center file')
                        
                        
                        # path_174 = r'\\140.116.228.174\geodac_data_test\RAW\RSImage\UAV\3DModel'
                        # dst_path = ''
                        # folder = path + '\\' + i + '\\' + dir_1 + '\\' + dir_1_8
                        # nowtime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                        # tran = ''
                        # ## print(folder, '\n\n', nowtime)
                        # for item in os.listdir(folder):
                            # ## dir_174 .b3d所在的地方
                            # dir_174  = os.path.join(path_174, nowtime)
                            # dst_path = dir_174 
                            # pathlib.Path(dir_174).mkdir(parents=True, exist_ok=1)
                            # if item[-3:] == 'txt':
                                # if item != 'xml.txt':
                                    # # print(nowtime, item)
                                    # lat = item[0:13]
                                    # lon = item[14:28]
                                    # tran = "ssh user1@140.116.228.180 -p 2202 './trans3d " + nowtime + ' ' + lon + ' ' + lat + "'"
                                    # print(tran)

                            # if item[-3:] == 'obj':
                                # shutil.copyfile(os.path.join(folder,item),os.path.join(dir_174,item))
                            # elif item[-3:] == 'mtl':
                                # shutil.copyfile(os.path.join(folder, item),os.path.join(dir_174,item))
                            # elif item[-3:] == 'jpg':
                                # shutil.copyfile(os.path.join(folder, item),os.path.join(dir_174,item))
                            
                        
                        # process  = subprocess.Popen('powershell.exe ' + tran, stdout=PIPE, stderr=PIPE, stdin=PIPE)
                        # out, err = process.communicate()
                        # print('[stdout]: ', out)
                        # print('[stderr]: ', err)
                        # print('\n')
 
                        # ## move tran3d from 174 to 155
                        # after_tran = path_174 + '\\' + nowtime + '\\' + 'Batchedmodel'
                        # dst_155    = path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_8 + '\\' + 'tran3d'
                        # shutil.copytree(after_tran, dst_155)
                        
                        # ## D槽也一份 
                        # shutil.copytree(after_tran, out_model)
                        
            
                        # ## 自動產生xml
                        # create_xml(i, wgs84)
                        # shutil.copyfile(path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_8 + '\\'  + r'xml.txt', out_case + '\\xml.txt')
                        
                       


                        
                    # # 解壓縮圖專
                    # print('Start unzip tile')
                    # with zipfile.ZipFile(tile, 'r') as zf:
                        # # pathlib.Path(path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_1 + '\\' + i).mkdir(parents=True, exist_ok=1)
                        # # os.mkdir(path + '\\' + i + '\\' + dir_1 + '\\'+ dir_1_1 + '\\' + i)
                        # zf.extractall(out_tile)
                        # print('[OK] unzip tile')


                        # ## 寫入處理名單
                        # with open(r'\\140.116.228.155\geodac_uav\uav.txt', 'a', encoding = 'utf8') as txt:
                            # txt.write(i + ',' + center+'\n')
                            # print('[OK] add to uav.txt')
                    
    
def main():
    export()

main()

print("\n- - - - - - - - Script End - - - - - - - - \n")