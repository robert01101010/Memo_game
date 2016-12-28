# -*- coding: utf-8 -*-
import shutil
import sys
import os

def vueCopySampleApp(fromPath, targetPath):
    if (os.path.exists(fromPath) == False):
        print(fromPath + ' catalog does not exist, please build your app correct')
        return
    if (os.path.exists(fromPath + '/index.html') == False):
        print(fromPath + '/index.html does not exist, please rename your main html file to index.html')
        return
    if (os.path.exists(targetPath)):
        shutil.rmtree(targetPath)

    shutil.copytree(fromPath + '/static', targetPath)
    shutil.copy(fromPath + '/index.html', 'indexDemo.html')
    source = open('indexDemo.html').readlines()
    targetFile = open('indexDemo.html', 'w')
    for s in source:
        targetFile.write(s.replace('href=/', 'href=').replace('src=/', 'src='))
    targetFile.close()

vueCopySampleApp(sys.argv[1], sys.argv[2])
