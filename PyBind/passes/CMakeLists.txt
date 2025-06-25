add_library(Passes SHARED PrintOpPass.cpp)
target_link_libraries(Passes PUBLIC MLIRIR)