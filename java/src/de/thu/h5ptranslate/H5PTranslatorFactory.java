package de.thu.h5ptranslate;

import org.python.core.PyObject;
import org.python.util.PythonInterpreter;

public class H5PTranslatorFactory {

    private PyObject h5ptranslateClass;

    public H5PTranslatorFactory() {
        PythonInterpreter interpreter = new PythonInterpreter();
        interpreter.exec("from h5ptranslate.h5ptranslate import H5PTranslatorImpl");
        h5ptranslateClass = interpreter.get("H5PTranslatorImpl");
    }

    public H5PTranslator create() {
        PyObject buildingObject = h5ptranslateClass.__call__();
        return (H5PTranslator) buildingObject.__tojava__(H5PTranslator.class);
    }

}
