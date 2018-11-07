"""
Testing UPaperclip
"""

import sys
import numpy as np
import random
import os
import string
import cv2


sys.path.insert(0, '..')
import muniverse  as mu # noqa: E402


def main():
    print('Looking up environment...')
    spec = mu.spec_for_name('UPaperClips-v0')
    # Hard coded docker container built with UPaperClips
    container = 'muniverse:02.gg'
    print('Creating environment...')
    env = mu.Env(spec, container, None, None, True)
    print('Starting recording')
    newdir = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
    os.mkdir(newdir)
    filenumber = 0
    try:
        print('Resetting environment...')
        env.reset()
        print('Playing game...')
        runtime = 0
        while runtime < 300:
            # Random click a location and release at the same location
            xval = random.randint(1, 960)
            yval = random.randint(1, 720)
            action1 = mu.MouseAction('mousePressed', x=xval, y=yval, click_count=1)
            action2 = mu.MouseAction('mouseReleased', x=xval, y=yval)
            reward, done = env.step(0.1, action1)
            print('reward: ' + str(reward))
            # Write a click obs
            filenumber = saveimg(env.observe(),newdir,filenumber)
            runtime += 0.1
            reward, done = env.step(0.1, action2)
            print('reward: ' + str(reward))
            # Write a obs after release
            filenumber = saveimg(env.observe(),newdir,filenumber)
            runtime += 0.1
            if done:
                break

    finally:
        env.close()
# Save the image and update the file number
def saveimg(img, dir, filenum):
    filename = str(filenum) + '.png'
    cv2.imwrite(os.path.join(dir, filename), img)
    filenum += 1
    return filenum


if __name__ == '__main__':
    main()

