#!/bin/bash
# تحميل أداة تفكيك تطبيقات الأندرويد
mkdir -p bin
curl -L https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool -o bin/apktool
curl -L https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.9.3.jar -o bin/apktool.jar
chmod +x bin/apktool bin/apktool.jar
echo "Tools installed successfully"
