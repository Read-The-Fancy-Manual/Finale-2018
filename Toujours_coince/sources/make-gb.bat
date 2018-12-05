if exist %1.gb del %1.gb
if exist %1.o del %1.o

wla-gb.exe -ox %1.s %1.o

echo [objects]>linkfile
echo %1.o>>linkfile

wlalink.exe -vs linkfile %1.gb
