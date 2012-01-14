/****************************
 PIXEL PICS
 2011/2012 STOMPY BLONDIE GAMES
 ****************************
 Handles all the python interfacing code
 ****************************/

#ifndef _PYTHON_INTERFACE_H_
#define _PYTHON_INTERFACE_H_


class Main_App;


/*
 * One instance of this class is created by the Main init method.
 * It then calls the method to set up python.
 */
class Python_Interface
{

private:
    Main_App* game;

public:

    Python_Interface(Main_App* game);
    bool initialise_python_interpreter();

};


// This is a huge chunk of code I found that accurately wraps maps for exposure in Python.
// For whatever reason I couldn't get map_indexing_suite to play nice. Here we go anyway.
// 
// Usage:
//   If you want to wrap a map that holds pointers.
//   STL_MAP_WRAPPING_PTR(KeyObject, *ObjectToWrap, "Python_Name");
// 
//   If you want to wrap a map that holds values.
//   STL_MAP_WRAPPING(KeyObject, ObjectToWrap, "Python_Name");


template<class Key, class Val>
struct map_item {
    typedef std::map<Key,Val> Map;

    static Val get(Map & self, const Key idx) {
      if (self.find(idx) == self.end()) {
          PyErr_SetString(PyExc_KeyError,"Map key not found");
          boost::python::throw_error_already_set();
      }
      return self[idx];
    }

    static void set(Map& self, const Key idx, const Val val) { self[idx]=val; }
    static void del(Map& self, const Key n)                  { self.erase(n); }
    static bool in (Map const& self, const Key n)            { return self.find(n) != self.end(); }

    static boost::python::list keys(Map const& self) {
        boost::python::list t;
        for(typename Map::const_iterator it = self.begin() ; it!=self.end() ; ++it)
            t.append(it->first);
        return t;
    }

    static boost::python::list values(Map const& self) {
        boost::python::list t;
        for(typename Map::const_iterator it=self.begin(); it!=self.end(); ++it)
            t.append(it->second);
        return t;
    }

    static boost::python::list items(Map const& self) {
        boost::python::list t;
        for(typename Map::const_iterator it=self.begin(); it!=self.end(); ++it)
            t.append( boost::python::make_tuple(it->first, it->second) );
        return t;
    }
};

#define STL_MAP_WRAPPING_PTR(KEY_TYPE, VALUE_TYPE, PYTHON_TYPE_NAME)               \
    class_<std::pair<const KEY_TYPE, VALUE_TYPE> >((std::string(PYTHON_TYPE_NAME)+std::string("DATA")).c_str()) \
        .def_readonly ("key"  , &std::pair<const KEY_TYPE, VALUE_TYPE>::first ) \
        .def_readwrite("value", &std::pair<const KEY_TYPE, VALUE_TYPE>::second) \
    ;                                                                          \
    class_<std::map<KEY_TYPE, VALUE_TYPE> >(PYTHON_TYPE_NAME)                  \
        .def("__len__"     , &std::map<KEY_TYPE, VALUE_TYPE>::size)            \
        .def("__iter__"    , boost::python::iterator<std::map<KEY_TYPE, VALUE_TYPE>, boost::python::return_internal_reference<> >()) \
        .def("__getitem__" , &map_item<KEY_TYPE, VALUE_TYPE>().get, boost::python::return_internal_reference<>()) \
        .def("__setitem__" , &map_item<KEY_TYPE, VALUE_TYPE>().set   )         \
        .def("__delitem__" , &map_item<KEY_TYPE, VALUE_TYPE>().del   )         \
        .def("__contains__", &map_item<KEY_TYPE, VALUE_TYPE>().in    )         \
        .def("clear"       , &std::map<KEY_TYPE, VALUE_TYPE>::clear  )         \
        .def("has_key"     , &map_item<KEY_TYPE, VALUE_TYPE>().in    )         \
        .def("keys"        , &map_item<KEY_TYPE, VALUE_TYPE>().keys  )         \
        .def("values"      , &map_item<KEY_TYPE, VALUE_TYPE>().values)         \
        .def("items"       , &map_item<KEY_TYPE, VALUE_TYPE>().items )         \
    ;

#define STL_MAP_WRAPPING(KEY_TYPE, VALUE_TYPE, PYTHON_TYPE_NAME)               \
    class_<std::pair<const KEY_TYPE, VALUE_TYPE> >((std::string(PYTHON_TYPE_NAME)+std::string("DATA")).c_str()) \
        .def_readonly ("key"  , &std::pair<const KEY_TYPE, VALUE_TYPE>::first ) \
        .def_readwrite("value", &std::pair<const KEY_TYPE, VALUE_TYPE>::second) \
    ;                                                                          \
    class_<std::map<KEY_TYPE, VALUE_TYPE> >(PYTHON_TYPE_NAME)                  \
        .def("__len__"     , &std::map<KEY_TYPE, VALUE_TYPE>::size)            \
        .def("__iter__"    , boost::python::iterator<std::map<KEY_TYPE, VALUE_TYPE>, boost::python::return_internal_reference<> >()) \
        .def("__getitem__" , &map_item<KEY_TYPE, VALUE_TYPE>().get   )         \
        .def("__setitem__" , &map_item<KEY_TYPE, VALUE_TYPE>().set   )         \
        .def("__delitem__" , &map_item<KEY_TYPE, VALUE_TYPE>().del   )         \
        .def("__contains__", &map_item<KEY_TYPE, VALUE_TYPE>().in    )         \
        .def("clear"       , &std::map<KEY_TYPE, VALUE_TYPE>::clear  )         \
        .def("has_key"     , &map_item<KEY_TYPE, VALUE_TYPE>().in    )         \
        .def("keys"        , &map_item<KEY_TYPE, VALUE_TYPE>().keys  )         \
        .def("values"      , &map_item<KEY_TYPE, VALUE_TYPE>().values)         \
        .def("items"       , &map_item<KEY_TYPE, VALUE_TYPE>().items )         \
    ;


#endif
