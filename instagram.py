from instaLooter import InstaLooter
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
import threading
import queue
from random import randint

INSTAGRAM_URL = r'https://www.instagram.com'
TEMP_FOLDER_PATH = r"C:\Users\u87989\Desktop\shtinker-master"
THREAD_COUNT = 16

class Instagram:
    def __init__(self, userName, userFolder): #donePicturesQueue, userName):
        self.donePicturesQueue = queue.Queue()#donePicturesQueue
        self.userName = userName
        self.userFolder = userFolder
        self.looter = InstaLooter(profile=userName)
        self.fullName = self.looter.get_metadata()['full_name']
        self.profilePicture = self.looter.get_metadata()['profile_pic_url']
        self.profileUrl = 'r{}/{}'.format(INSTAGRAM_URL, userName)[1:]
        self.isPrivate = self.looter.get_metadata()['is_private']
        self.pics_dic = {}
        self.counter = 0
        self.scan()
        #self.connectedFacebookPage = self.looter.get_metadata()['connected_fb_page'] --> Connected Facebook page, can be None.

    def scan(self):
        http = urllib3.PoolManager()
        # Write the profile picture
        with open(r'{}\profile.jpg'.format(self.userFolder), 'wb') as profile_picture:
            profile_picture.write(http.request("GET",self.profilePicture).data)
        
        if self.looter.get_metadata()['media']['count'] <= 0:
            return #No Pictures
        
        availablePicturesQueue = queue.Queue()
        threads = []
        
        for media in self.looter.medias():
            if not media['is_video']:
                availablePicturesQueue.put(media)
                self.counter+=1
        
        for thread in range(THREAD_COUNT):
            thread = threading.Thread(target=self.write_picture, args=(availablePicturesQueue, ))   
            thread.start()
            
        for thread in threads:
            thread.join()

    def write_picture(self, availablePicturesQueue):
        http = urllib3.PoolManager()
        
        while not availablePicturesQueue.empty():
            media = availablePicturesQueue.get()
        
            if media['is_video']:
                #url = looter.get_post_info(media['code'])['video_url'] --> Download mp4 video
                continue
            else:
                url = media['display_src']
                
            dataToWrite = http.request("GET",url).data
            picturePath = '{}\{}{}.jpg'.format(self.userFolder, self.userName, str(threading.current_thread().ident) * randint(1, 10))
            with open(picturePath, 'wb') as picture:
                 picture.write(dataToWrite)
            availablePicturesQueue.task_done()
            self.donePicturesQueue.put({picturePath : url})
            self.pics_dic[picturePath] = url
            self.donePicturesQueue.task_done()

if __name__ == "__main__":
    donePicturesQueue = queue.Queue()
    user = Instagram(donePicturesQueue, 'stavharan_')
    user.scan()

