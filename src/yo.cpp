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
#include <algorithm>
#include <numeric>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <numeric>
#include <thread>
#include <future>


#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>


#include <hadoken/format/format.hpp>
#include <hadoken/executor/thread_pool_executor.hpp>



#include <digestpp.hpp>

#include <yo/yo.hpp>

namespace fmt = hadoken::format;

using namespace digestpp;


constexpr std::size_t block_size = 1 << 24;  // 16Mi


namespace yo {



std::string version(){
    return YO_VERSION_MAJOR "." YO_VERSION_MINOR ;
}


options::options() :
    _threads(std::thread::hardware_concurrency()*2),
    _block_size(block_size)

{

}

void options::set_concurrency(int threads){
    _threads = threads;
}

int options::get_concurrency() const{
    return _threads;
}

std::size_t options::get_block_size() const{
    return _block_size;
}


struct context::internal{
    internal() : executor(std::thread::hardware_concurrency()*2)
    {}

    hadoken::thread_pool_executor executor;
};


context::context() : _pimpl(new internal()){

}

context::~context(){

}


int open_file(const std::string & filename, int flags){
    int fd = open(filename.c_str(), flags | O_CLOEXEC, 0755 );

    if(fd < 0){
        throw std::system_error(errno, std::generic_category(), fmt::scat("[open] ", filename));
    }
    return fd;
}


struct stat stat_file(int fd){
    struct stat st;

    if( fstat(fd, &st) < 0){
        throw std::system_error(errno, std::generic_category(), fmt::scat("[fstat]"));
    }
    return st;
}


void copy_chunk(const options & opts, int fd_dst, int fd_src, off_t offset, std::size_t size){
    const std::size_t chunk_size = opts.get_block_size();

    std::vector<char> buffer(chunk_size);

    while(size > 0){
        const std::size_t r_size = std::min(size, chunk_size);
        do{
            int status = pread(fd_src, buffer.data(), r_size, offset);
            if(status < 0 ){
                if(errno  == EINTR || errno == EAGAIN){
                    continue;
                }
                throw std::system_error(errno, std::generic_category(), fmt::scat("[pread]"));
            }
            break;
        }while(1);

        do{
            int status = pwrite(fd_dst, buffer.data(), r_size, offset);
            if(status < 0 ){
                if(errno  == EINTR || errno == EAGAIN){
                    continue;
                }
                throw std::system_error(errno, std::generic_category(), fmt::scat("[pwrite]"));
            }
            break;
        }while(1);

        offset += r_size;
        size -= r_size;
    }

}

void context::copy_file(const options & opts, const std::string & src, const std::string & dst){
    int fd_src = open_file(src, O_RDONLY);
    int fd_dst = open_file(dst, O_WRONLY | O_CREAT);

    struct stat st = stat_file(fd_src);
    const std::size_t size_file = st.st_size;

    if( ftruncate(fd_dst, size_file) < 0){
        throw std::system_error(errno, std::generic_category(), "[ftruncate]");
    }


    // get concurrency
    const std::size_t n_workers = opts.get_concurrency();
    std::vector<std::future<void>> futures;
    futures.reserve(n_workers);

    // size of block to process per worker
    const std::size_t worker_block = size_file / n_workers;

    for(std::size_t i =0; i < n_workers; ++i){
        off_t worker_offset = i * worker_block;
        std::size_t read_size = std::min<std::size_t>( (i + 1) * worker_block, size_file) - size_t(worker_offset);

        futures.emplace_back(  _pimpl->executor.twoway_execute( [&opts, fd_dst, fd_src, worker_offset, read_size]{
            copy_chunk(opts, fd_dst, fd_src, worker_offset, read_size);

        }));
    }


    for(auto & f : futures){
        f.get();
    }


}

} // yo


