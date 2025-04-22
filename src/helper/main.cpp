#include <windows.h>
#include <iostream>
#include "reader.h"
#include "writer.h"

int main() {
    //inits the buffer info for the reader 
    const char* readBufferName = "Local\\C3DINPUT";
    const size_t readBufferSize = 1024;
    //inits the buffer info for the writer 
    const char* writeBufferName = "Local\\C3DOUTPUT";
    const size_t writeBufferSize = 1024;

    read(readBufferName, readBufferSize, writeBufferName, writeBufferSize);
}