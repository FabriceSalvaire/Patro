py310

append_to_python_path_if_not ${PWD}
append_to_python_path_if_not ${PWD}/examples
append_to_python_path_if_not ${PWD}/tools

if [ -e ${PWD}/non-public-submodule/setenv.sh ]; then
  source ${PWD}/non-public-submodule/setenv.sh
fi
