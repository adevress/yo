/**
    yo, parallel I/O utilities
    Copyright (C) 2018 Adrien Devresse

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
**/





#include <iostream>
#include <cstddef>
#include <stdexcept>
#include <array>
#include <tuple>

#include <hadoken/format/format.hpp>
#include <hadoken/geometry/geometry.hpp>

#include <boost/geometry/index/indexable.hpp>
#include <boost/geometry/index/rtree.hpp>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>


#include <yo/yo.hpp>

using namespace yo;

void py_copyfile(const std::string & src, const std::string & dst){
    context c;
    options opts;

    c.copy_file(opts, src, dst);
}


PYBIND11_MODULE(_yo, m) {
    m.doc() = "YO toolkit and utilities for parallel io";

    m.def("copyfile", &py_copyfile, "copy a file using parallel I/O");
}
