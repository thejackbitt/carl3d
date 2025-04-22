#include <windows.h>
#include <iostream>
#include <cstring>
#include "writer.h"

int write(char* data, char* view, const size_t bufferSize) {
    // std::cout << "[Helper] JSON: " << '\n' << view << '\n' << std::endl;
    std::memcpy(view, data, bufferSize);
    return 0;
};