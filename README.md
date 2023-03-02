# H5PTranslator
H5PTranslator - Translation of H5P content files to different languages

Authors: Michael Munz, Harald Groß, THU (University of Applied Sciences, Ulm)
Licence: This project is licensed under the terms of the MIT license.

This is part of the project MedTec+ -"medical engineering for medical professionals".
This work has been co-funded by the Erasmus+ Programme of the European Union
Project website: <a href="http://medtecplus.eu/" target="_blank">http://medtecplus.eu/</a>

Releases can be downloaded from the release page as windows executable.

## Overview
H5PTranslator can tranlate [H5P](https://h5p.org/)content files from English into a target language. For this, the H5P file needs to be downloaded and processed with H5PTranslator.
Currently, we are using Goolge Translate for doing the translation. Images and all content is automatically translated.
The application also does a change-tracking. This means, if you change (add, delete, modify) H5P elements in the original (english) file, H5PTranslator automatically detects which elements have been changed in the original version and updates only those elements. If you in turn change elements in the target languag file, e.g. if you are not happy with the translation or you need to change the size of an element, this will be not touched by the translator.


## Workflow 
- Download the base file (English version) of your H5P-based course.
- Start the program and select your target language. 
- Open your downloaded base H5P file

The translated file is created as a H5P output file. The name of the base file is kept and the prefix "_<target_lang>" is added. E.g. when translating file "mycourse.h5p" into German, the output will be "mycourse_de.h5p".
In addition to translating the H5P content, you can also exchange the images contained in the H5P file. For this, you need to prepare a folder containing a sub-folder of the original images with the name "en" and an additional subfolder with the target language (currently, "de" or "hu").
The image names of the target and base language should be identical. The application then matches the images of the base language with the images contained in the H5P file. For every mathing file, the target language file will be replaced in the target H5P object.
After uploading the new translated H5P file to the LMS (e.g. Moodle), you need to use the H5P L10n functionality to change the language of the H5P elements.
For Moodle, this works as follows:
- Edit the H5P file in Moodle
- Click on "Text overrides and translations"
- Switch to the target language
- Save 

## Supported functionalities
Currently the following languages are supported: 
- German
- Hungarian

Currently, only _Course Presentation_ is supported.


