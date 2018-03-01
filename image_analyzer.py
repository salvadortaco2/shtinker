import subprocess
import time
import os 

def run_command(command, wait=False):

    p = subprocess.Popen(
                command, 
                stdout = subprocess.PIPE, 
                stderr = subprocess.PIPE,
                shell = True)

    (result, error) = p.communicate()
    
    return result

start_time = time.time()
results =[]
lookup_words = [b'military', b'plane', b'aircraft', b'missile', b'stretcher', b'lab coat']

def bad_image(imgOutput):
    for f in lookup_words:
        if f in imgOutput:
            return True
    return False

def shtink(image):
    if bad_image(run_command(r'C:\ProgramData\Anaconda3\python.exe C:\modeldir\models-master\tutorials\image\imagenet\classify_image.py --image_file {}'.format(image))):
        return True
    return False
    
def shtink_user(file_dic):
    bad_urls = []
    for file_path in file_dic:
        shtink_flag = shtink(file_path)
        print("path: " + file_path + " military: " + str(shtink_flag))
        if shtink_flag:
            bad_urls.append(file_dic[file_path])
    return bad_urls
            
#def onFolder(imagedir):
    #for root, dirs, filenames in os.walk(imagedir):
        #for f in filenames:
            #results.append(shtink("{}\{}".format(imagedir, f)))
            #print("%s , --- %s seconds ---" % (f, time.time() - start_time))
    #return results

#start_time = time.time()
