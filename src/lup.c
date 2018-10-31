#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>
#include <Python.h>
#include <patchlevel.h>

/*
 *  Python API
 */

#if PY_MAJOR_VERSION == 3
#define PY3
#define PyString_FromString PyUnicode_FromString
#endif


void eval_code(lua_State * L, const char * code) {
  lua_pushfstring(L, "print(%s)", code);
  if (luaL_dostring(L, lua_tostring(L, -1)) != 0) {
    if (luaL_dostring(L, code) != 0) {
      fprintf(stderr, "%s", lua_tostring(L, -1));
    }
  }
  lua_settop(L, 0);
}


static void py_print(PyObject * py_print_cbk, const char * str) {
  PyObject * args = Py_BuildValue("(s)", str);
  PyObject * result = PyEval_CallObject(py_print_cbk, args);
  Py_DECREF(args);
  Py_DECREF(result);
}


int print_cb(lua_State * L, PyObject * py_cbk) {
  lua_getglobal(L, "tostring");
  for (int i = 1; i <= lua_gettop(L)-1; ++i) {
    lua_pushvalue(L, -1);
    lua_pushvalue(L, i);
    lua_call(L, 1, 1);
    const char * tostr = lua_tostring(L, -1);
    if (tostr == NULL) { 
      return luaL_error(L, "'tostring' returned NULL value\n");
    }
    if (i > 1) { py_print(py_cbk, "\t"); }
    py_print(py_cbk, "l:");
    py_print(py_cbk, tostr);
    lua_pop(L, 1);
  }
  py_print(py_cbk, "\n");
  return 0;
}


int py_print_lua_cb(lua_State * L) {
  PyObject * py_cbk = lua_touserdata(L, lua_upvalueindex(1));
  return print_cb(L, py_cbk);
}


typedef struct {
  PyObject_HEAD // ';' isn't need, it can cause compiler issues
  lua_State * L;
  PyObject * py_print_cbk;
} PyLuaState;


static PyObject * lua_new(PyTypeObject * type, PyObject * args, PyObject * kwargs) {
  PyLuaState * self = (PyLuaState *)type->tp_alloc(type, 0);
  if (self != NULL) {
    self->L = NULL;
    self->py_print_cbk = NULL;
  }

  return (PyObject *)self;
}


static int lua_init(PyLuaState * self, PyObject * args, PyObject * kwargs) {
  PyObject * cbk = NULL;
  if (!PyArg_ParseTuple(args, "O", &cbk)) {
    return 0;
  }

  if (!PyCallable_Check(cbk)) {
    PyErr_SetString(PyExc_TypeError, "expected callable");
    return 0;
  }

  // TOOD: handle self->py_print_cbk
  if (self->L) {
    lua_close(self->L);
    self->L = NULL;
  }

  Py_INCREF(cbk);
  self->py_print_cbk = cbk;
  self->L = luaL_newstate();
  luaL_openlibs(self->L);
  lua_pushlightuserdata(self->L, self->py_print_cbk);
  lua_pushcclosure(self->L, py_print_lua_cb, 1);
  lua_setglobal(self->L, "print");

  return 0;
}


static void lua_dealloc(PyLuaState * self) {
  lua_close(self->L);
  Py_XDECREF(self->py_print_cbk);
  Py_TYPE(self)->tp_free((PyObject *)self);
}


static PyObject * lua_eval(PyLuaState * self, PyObject * args) {
  const char * code;
  if (!PyArg_ParseTuple(args, "s", &code)) {
    PyErr_SetString(PyExc_TypeError, "expected string");
    return NULL;
  }
  eval_code(self->L, code);

  return Py_None;
}


static PyMethodDef pylua_methods[] = {
   {"eval", (PyCFunction)lua_eval, METH_VARARGS, "Evaluate Lua String"},
   {NULL}
};


static PyTypeObject PyLuaStateType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  .tp_name = "lup.LuaState",
  .tp_doc = "LuaState used for Jupyter Kernels",
  .tp_basicsize = sizeof(PyLuaState),
  .tp_flags = Py_TPFLAGS_DEFAULT,
  .tp_new = lua_new,
  .tp_init = (initproc)lua_init,
  .tp_dealloc = (destructor)lua_dealloc,
  .tp_methods = pylua_methods,
};


static PyModuleDef lup_module = {
  PyModuleDef_HEAD_INIT,
  .m_name = "lup",
  .m_doc = "Lua Python object",
  .m_size = -1,
};


PyMODINIT_FUNC PyInit_lup() {
  if (PyType_Ready(&PyLuaStateType) < 0) { return NULL; }

  PyObject * m = PyModule_Create(&lup_module);
  if (m == NULL) { return NULL; }

  Py_INCREF(&PyLuaStateType);
  PyModule_AddObject(m, "LuaState", &PyLuaStateType);
  return m;
}
