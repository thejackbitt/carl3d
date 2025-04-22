@echo off
echo Building Carl3D executable...

g++ ^ -I "src\helper" ^ -std=c++17 ^ -O2 ^ src\helper\main.cpp ^ src\helper\reader.cpp ^ src\helper\writer.cpp ^ -o "src\blender\C3D_HELPER.EXE"

if errorlevel 1 (
    echo Epic fail.  Something went wrong...
    pause
) else (
    echo Success!  C3D_HELPER.EXE was compiled.
)

IF EXIST "./C3D_ADDON.zip" DEL "./C3D_ADDON.zip"
powershell -command "Compress-Archive -Path './src\*' -DestinationPath './C3D_ADDON.zip'"