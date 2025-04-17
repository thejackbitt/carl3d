@echo off
echo Building Carl3D executable...

g++ src/helper/main.cpp -o src/blender/C3D_HELPER.EXE

if errorlevel 1 (
    echo Epic fail.  Something went wrong...
    pause
) else (
    echo Success!  C3D_HELPER.EXE was compiled.
)

IF EXIST "./C3D_ADDON.zip" DEL "./C3D_ADDON.zip"
powershell -command "Compress-Archive -Path './src\*' -DestinationPath './C3D_ADDON.zip'"