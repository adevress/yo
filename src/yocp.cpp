/**
    yo, parallel I/O utilities
    Copyright (C) 2018 Adrien Devresse

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*/


#include <iostream>
#include <yo/yo.hpp>

using namespace yo;

void print_help(const char * progname){
    std::cerr << "Usage: " << progname << " [file_src] [file_dst]" << std::endl;
    std::cerr << "\n";
    std::cerr << "version: " << yo::version() << std::endl;
}


int main(int argc, char** argv){

    int ret = 1;
    if(argc <  3){
        print_help(argv[0]);
        exit(1);
    }

    try{
        const std::string filename_src(argv[1]), filename_dst(argv[2]);

        context yo_context;
        options opts;

        yo_context.copy_file(opts, filename_src, filename_dst);
        ret = 0;
    }catch(std::exception & e){
        std::cerr << argv[0] << ": "<< e.what() << std::endl;
        ret = 1;
    }

    std::flush(std::cout);
    return ret;
}

