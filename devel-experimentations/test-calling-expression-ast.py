####################################################################################################

# cf. http://stackoverflow.com/questions/28244921/how-can-i-get-the-calling-expression-of-a-function-in-python

import inspect
import ast

####################################################################################################

def _find_caller_node(root_node, func_name, last_lineno):

    # init search state
    found_node = None
    lineno = 0

    def _luke_astwalker(parent):
        nonlocal found_node
        nonlocal lineno
        for child in ast.iter_child_nodes(parent):
            # break if we passed the last line
            if hasattr(child, "lineno"):
                lineno = child.lineno
            if lineno > last_lineno:
                break

            # is it our candidate?
            if (isinstance(child, ast.Name)
                    and isinstance(parent, ast.Call)
                    and child.id == func_name):
                # we have a candidate, but continue to walk the tree
                # in case there's another one following. we can safely
                # break here because the current node is a Name
                found_node = parent
                break

            # walk through children nodes, if any
            _luke_astwalker(child)

    # dig recursively to find caller's node
    _luke_astwalker(root_node)
    return found_node

####################################################################################################

def print_callexp(*args, **kwargs):

    # get some info from 'inspect'
    frame = inspect.currentframe()
    backf = frame.f_back
    this_func_name = frame.f_code.co_name

    # get the source code of caller's module
    # note that we have to reload the entire module file since the
    # inspect.getsource() function doesn't work in some cases (i.e.: returned
    # source content was incomplete... Why?!).
    # --> is inspect.getsource broken???
    #     source = inspect.getsource(backf.f_code)
    #source = inspect.getsource(backf.f_code)
    with open(backf.f_code.co_filename, "r") as f:
        source = f.read()

    # get the ast node of caller's module
    # we don't need to use ast.increment_lineno() since we've loaded the whole
    # module
    ast_root = ast.parse(source, backf.f_code.co_filename)
    #ast.increment_lineno(ast_root, backf.f_code.co_firstlineno - 1)

    # find caller's ast node
    caller_node = _find_caller_node(ast_root, this_func_name, backf.f_lineno)

    # now, if caller's node has been found, we have the first line and the last
    # line of the caller's source
    if caller_node:
        #start_index = caller_node.lineno - backf.f_code.co_firstlineno
        #end_index = backf.f_lineno - backf.f_code.co_firstlineno + 1
        print("Hoooray! Found it!")
        start_index = caller_node.lineno - 1
        end_index = backf.f_lineno
        lineno = caller_node.lineno
        for ln in source.splitlines()[start_index:end_index]:
            print("  {:04d} {}".format(lineno, ln))
            lineno += 1

####################################################################################################

a_var = "but"
print_callexp(
    a_var, "why?!",
    345, (1, 2, 3), hello="world")
