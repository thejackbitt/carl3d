#include <windows.h>
#include <iostream>
#include <thread>
#include <chrono>
#include <cstring>
#include "writer.h"

int read(const char* bufferName, const size_t bufferSize, const char* bufferName2, const size_t bufferSize2) {
    //setting up data buffer

    HANDLE hMap = CreateFileMappingA(
        INVALID_HANDLE_VALUE,
        nullptr,
        PAGE_READWRITE,
        0,
        bufferSize,
        bufferName
    );

    if(!hMap) {
        std::cerr << "[Helper] CreateFileMapping failed: " << GetLastError() << '\n' << std::endl;
        return 1;
    }

    char* hView = static_cast<char*>(
        MapViewOfFile(
            hMap,
            FILE_MAP_ALL_ACCESS,
            0,
            0,
            bufferSize
        )
    );

    if (!hView) {
        std::cerr << "[Helper] MapViewOfFile failed: " << GetLastError() << '\n' << std::endl;
        CloseHandle(hMap);
        return 1;
    }

    //setting up render buffer

    HANDLE rMap = CreateFileMappingA(
        INVALID_HANDLE_VALUE,
        nullptr,
        PAGE_READWRITE,
        0,
        bufferSize2,
        bufferName2
    );

    if(!rMap) {
        std::cerr << "[Helper] CreateFileMapping failed: " << GetLastError() << '\n' << std::endl;
        return 1;
    };

    char* rView = static_cast<char*>(
        MapViewOfFile(
            rMap,
            FILE_MAP_ALL_ACCESS,
            0,
            0,
            bufferSize2
        )
    );

    if(!rView) {
        std::cerr << "[Helper] MapViewOfFile failed: " << GetLastError() << '\n' << std::endl;
        CloseHandle(rMap);
        return 1;
    }

    //execution loop

    std::string last;
    while (true) {
        char buf[bufferSize];
        memcpy(buf, hView, bufferSize);
        buf[bufferSize-1] = '\0';

        if(std::strlen(buf) > 0 && buf != last) {
            write(buf, rView, bufferSize2);
            last = buf; 
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    };
    
    UnmapViewOfFile(hView);
    UnmapViewOfFile(rView);
    CloseHandle(hMap);
    CloseHandle(rMap);

    return 0;
}