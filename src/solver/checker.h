//------------------------------------------------------------------------------
// Copyright (c) 2016 by contributors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//------------------------------------------------------------------------------

/*
Author: Chao Ma (mctt90@gmail.com)

This file defines the Checker class, which can check and parse
the command line arguments.
*/

#ifndef XLEARN_SOLVER_CHECKER_H_
#define XLEARN_SOLVER_CHECKER_H_

#include <vector>
#include <string>

#include "src/base/common.h"
#include "src/data/hyper_parameters.h"

namespace xLearn {

typedef std::vector<std::string> StringList;

//------------------------------------------------------------------------------
// Checker is used to check and parse command line arguments for xLearn.
//------------------------------------------------------------------------------
class Checker {
 public:
  // Constructor and Destructor
  Checker() { }
  ~Checker() { }

  // Initialize Checker
  void Initialize(int argc, char* argv[]);

  // Check and parse arguments
  bool Check(HyperParam& hyper_param);

 private:
  StringList menu_;  // Store all the options
  StringList args_;  // User input command line

  std::string option_help() const;
  bool check_train_options(HyperParam& hyper_param);
  bool check_inference_options(HyperParam& hyper_param);

  DISALLOW_COPY_AND_ASSIGN(Checker);
};

} // namespace xLearn

#endif // XLEARN_SOLVER_CHECKER_H_