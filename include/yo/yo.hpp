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

#ifndef LIBYO_HPP
#define LIBYO_HPP


#include <string>
#include <memory>

// yo namespace
namespace yo{

///
/// container for YO I/O options
///
class options{
public:

    ///
    options();

    ///
    void set_concurrency(int threads);

    ///
    int get_concurrency() const;

    ///
    std::size_t get_block_size() const;

private:
    int _threads;
    std::size_t _block_size;
};

// string of YO version
std::string version();


///
/// \brief main libyo context
///
class context{

    struct internal;

public:
    context();
    virtual ~context();

    ///
    /// copy file using parallel compabilities
    ///
    void copy_file(const options & opts, const std::string & src, const std::string & dst);
private:
    std::unique_ptr<internal> _pimpl;
};




} // yo

#endif // YO_HPP
