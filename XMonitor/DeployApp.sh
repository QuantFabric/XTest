#!/bin/sh
# 发布程序的名称（参数1，执行脚本时输入）
AppName=$1
# 修改输出可执行文件路径（当前路径）
CurrentDir=`pwd`
# ldd将所有依赖库生成字符串组(#注意if后的空格只有一个）
DependentLibsList=$(ldd $AppName | awk '{if (match($3,"/")){ printf("%s "),$3 } }')
# 将字符串组里面的库拷贝到目标文件夹
cp $DependentLibsList $CurrentDir/Lib/
