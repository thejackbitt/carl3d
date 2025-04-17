#include <windows.h>
#include <iostream>

int main() {
    const char* bufferName = "Local\\C3DBUFFER";
    const size_t bufferSize = 1024;

    HANDLE hFile = CreateFileMappingA(
        INVALID_HANDLE_VALUE,
        nullptr,
        PAGE_READWRITE,
        0,
        bufferSize,
        bufferName
    );

    if (hFile == nullptr) {
        std::cerr << "[Helper] Could not create buffer " << GetLastError() << '\n' << std::endl;
        return 1;
    }

    LPVOID hView = MapViewOfFile(
        hFile,
        FILE_MAP_ALL_ACCESS,
        0,
        0,
        bufferSize
    );

    if (hView == nullptr) {
        std::cerr << "[Helper] Could not create view of file " << GetLastError() << '\n' << std::endl;
        CloseHandle(hFile);
        return 1;
    }

    const char* message = "Hello world!";
    CopyMemory(hView, message, strlen(message) + 1);

    std::cout << "[Helper] Shared memory created.  Press enter to quit.\n" << std::endl;
    std::cin.get();
    
    UnmapViewOfFile(hView);
    CloseHandle(hFile);

    return 0;
}