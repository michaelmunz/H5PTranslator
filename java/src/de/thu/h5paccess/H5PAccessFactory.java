package de.thu.h5paccess;

import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;

public class H5PAccessFactory {

    private PyObject h5paccesClass;

    public H5PAccessFactory() {
        PythonInterpreter interpreter = new PythonInterpreter();
        interpreter.exec("from h5paccess.h5paccess import H5PAccessImpl");
        h5paccesClass = interpreter.get("H5PAccessImpl");
    }

    public H5PAccess create() {
        PyObject buildingObject = h5paccesClass.__call__();
        return (H5PAccess) buildingObject.__tojava__(H5PAccess.class);
    }

}
