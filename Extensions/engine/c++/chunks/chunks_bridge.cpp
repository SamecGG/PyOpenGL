#include <python.h>
#include <boost/python.hpp>
#include "chunks.h"

namespace py = boost::python;

// https://stackoverflow.com/questions/6157409/stdvector-to-boostpythonlist
template <class T>
py::list std_vector_to_py_list(const std::vector<T> &v)
{
    py::object get_iter = py::iterator<std::vector<T>>();
    py::object iter = get_iter(v);
    py::list l(iter);
    return l;
}

// Parse list
std::vector<int> py_list_to_int_vector(PyObject* obj, int& reserve)
{
    std::vector<int> vector;
    vector.reserve(reserve);

    PyObject *iter = PyObject_GetIter(obj);
    if (!iter)
        return std::vector<int>();
    
    while (true) {
        PyObject *next = PyIter_Next(iter);
        if (!next) {
            // nothing left in the iterator
            break;
        }

        if (!PyLong_Check(next)) {
            // error, we were expecting a Long point value
        }

        int&& foo = (int)PyLong_AsLong(next);
        vector.emplace_back(foo);
    }

    return vector;
}

// python, c++ bridge
// method linking
static PyObject *pySetChunkSize(PyObject *self, PyObject *args)
{
    int x, y, z;

    if (!PyArg_ParseTuple(args, "(iii)", &x, &y, &z))
        return NULL;

    setChunkSize(Vector3<int>(x, y, z));

    return Py_BuildValue("i", 0);
}

static PyObject *pyGenerateChunkData(PyObject *self, PyObject *args)
{
    std::vector<int> chunkDataVector = generateChunkData();

    return std_vector_to_py_list(chunkDataVector).ptr();
}

static PyObject *pyGenerateChunkMesh(PyObject *self, PyObject *args)
{
    PyObject *obj;

    if (!PyArg_ParseTuple(args, "O", obj))
        return NULL;

    std::vector<int>* chunkData = &py_list_to_int_vector(obj, chunkSize.x * chunkSize.y * chunkSize.z);

    std::vector<int*> meshData = generateMeshData(*chunkData);

    return Py_BuildValue("i", std_vector_to_py_list<int*>(meshData).ptr());
}

static PyObject *pySaveChunk(PyObject *self, PyObject *args)
{
    int x, y, z;
    PyObject *obj;

    if (!PyArg_ParseTuple(args, "(iii) O", &x, &y, &z, obj))
        return NULL;

    Vector3<int> position(x, y, z);
    std::vector<int>* chunkData = &py_list_to_int_vector(obj, chunkSize.x * chunkSize.y * chunkSize.z);

    saveChunk(position, *chunkData);

    // return 0
    return Py_BuildValue("i", 0);
}

static PyObject *pyLoadChunk(PyObject *self, PyObject *args)
{
    int x, y, z;
    PyObject *obj;

    if (!PyArg_ParseTuple(args, "(iii) O", &x, &y, &z, obj))
        return NULL;

    Vector3<int> position(x, y, z);
    std::vector<int*> chunkData = loadChunk(position);

    // return 0
    return std_vector_to_py_list<int*>(chunkData).ptr();
}

static PyObject *version(PyObject *self)
{
    return Py_BuildValue("s", "Chunks - Version 1.0");
}

// methods def
static PyMethodDef myMethods[] = {
    {"set_chunk_size", pySetChunkSize, METH_VARARGS, "Sets chunk size."},
    {"generate_data", pyGenerateChunkData, METH_NOARGS, "Terrain generation."},
    {"generate_mesh", pyGenerateChunkMesh, METH_VARARGS, "Generates chunk mesh from chunk data."},
    {"save_chunk", pySaveChunk, METH_VARARGS, "Adds one"},
    {"load_chunk", pyLoadChunk, METH_VARARGS, "Adds one"},
    {"version", (PyCFunction)version, METH_NOARGS, "Returns the version"},
    {NULL, NULL, 0, NULL}};

// module def
static struct PyModuleDef myModule = {
    PyModuleDef_HEAD_INIT,
    "myModule",     // module name
    "First module", // docs
    -1,
    myMethods};

// func name must be - PyInit_<module>(void)
PyMODINIT_FUNC PyInit_myModule(void)
{
    return PyModule_Create(&myModule);
}