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
