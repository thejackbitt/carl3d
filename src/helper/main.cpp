#include <windows.h>
#include <iostream>
#include <thread>
#include <chrono>
#include <cstring>

int main() {
    const char* bufferName = "Local\\C3DBUFFER";
    const size_t bufferSize = 1024;

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

    std::string last;
    while (true) {
        char buf[bufferSize];
        memcpy(buf, hView, bufferSize);
        buf[bufferSize-1] = '\0';

        if(std::strlen(buf) > 0 && buf != last) {
            std::cout << "[Helper] JSON: " << '\n' << buf << '\n' << std::endl;
            last = buf; 
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    
    UnmapViewOfFile(hView);
    CloseHandle(hMap);

    return 0;
}