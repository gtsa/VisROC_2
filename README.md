
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
# VISROC 2.0: Software for the Visualization of the significance of the ROC curve based on confidence ellipses

This is a twin full implementation in Python and R of a Graphical User Interface (GUI), an update of the wider VISROC project and an upgrade of its initial implementation in FORTRAN (CPC Program Library in 2014). The GUI can be invoked either as a standalone application available for Windows, Mac, and GNU/Linux operating systems or as an R Shiny web application. The goal of the project and this implementation is to simplify the evaluation of the statistical significance of the accuracy of a binary prediction method. What is used for the evaluation of the diagnostic accuracy of such a binary prediction test in a broad spectrum of disciplines (including medicine, physics of complex systems, geophysics, meteorology, etc.) is the Receiver Operating Characteristics (ROC) method. The estimation of the statistical significance of the ROC is usually approximated by Monte Carlo calculations. **VISROC 2.0 addresses the problem by calculating and visualising the p-value on the ROC plane as well as the k-ellipses corresponding to the (*p=*)10%, 5% and 1% significance levels using as input the number of the positive \(P\) and negative (Q) cases to be predicted**.



## Table of contents
* [**Credits**](#credits)
* [**Requirements & Deployment**](#requirementsdeployment)
    * [Python Standalone GUI Application](#python-standalone-gui-application)
    * [Python Source code Deployment](#python-source-code-deployment)
    * [R Shiny Web Application](#r-shiny-web-application)
    * [Run R code locally](#run-r-code-locally)
* [**Usage**](#usage)
* [**Possible Issues**](#fix-possible-display-issues)
    * [False Positive Virus Alert (Windows & Cloud) and Permission to unauthorized apps (macOS)](#securityissues)
    * [Fix Possible Display Issues](#possible-display-issues)
        * [View-Scale issue on macOS](#view-scale-issue-on-macos)
        * [Font Type issue when running source code in Anaconda Python on Linux](#font-type-issue-when-running-source-code-in-anaconda-python-on-linux)
* [**Files Description**](#files-description)
* [**License**](#license)

## Credits
- **[Tkinter](https://docs.python.org/3/library/tkinter.html)**:
For the implementation of the VISROC 2.0 standalone Python-based application, we turned to the help of the Tkinter package (“Tk interface”), the standard Python interface to the Tcl/Tk GUI toolkit (built-in into Python's Standard Library). There are other packages available for creating GUIs, like wxPython, Qt and GTK. Tkinter was considered more appropriate, easier to learn/use —with a big and diverse coding community— and a lighter module in relation to the requirements of our mid-sized GUI of our project.
- **[PyInstaller](https://pyinstaller.org/en/stable/)**:
We also needed to use the PyInstaller application to go from the Python code to the standalone executable. PyInstaller is a free and open-source project, created and maintained by volunteers, which analyzes the code, discovers every other module and library the script needs in order to execute, collects copies of all those files –including the active Python interpreter– and then puts them with our script in a single executable file (or in a single folder).
- **[Shiny](https://shiny.rstudio.com/)**:
For the implementation of the VISROC 2.0 web R-based application, we turned to the help of the Tkinter package Shiny. Shiny is a free and open-source R package (developed and maintained by RStudio) for developing interactive web applications straight from R, via its own engine to build HTML tags. For the needs of the project, apart from HTML and CSS, we had to resort to very limited scale use of JavaScript





## Requirements & Deployment <a name="requirementsdeployment" />
### Python Standalone GUI Application
The standalone GUI applications for each of the basic Operating Systems —Windows, GNU/Linux, and macOS— are respectively the VISROC_2.exe, VISROC_2.elf, and VISROC_2.app files. They are developed in Python and bundled (using the Python package [PyInstaller](https://www.pyinstaller.org)) along with all their dependencies into three single executable files. That simply means they can be executed by simply being double-clicked, can be dragged and dropped, copied, cut and paste among different directories and machines of the corresponding OS, regardless of having or not previously installed Python, in any of its versions or any specific module/package. ***The user has just to download/paste the .exe (Windows), .elf (Linux), or .app (MacOS) file and double-click on it (or execute it via console)***.

Minimum OS Requirements:
- Ubuntu 18.04 LTS, Linux Mint 20.x, Elementary OS 6 and other related or later Debian-based distributions
- Microsoft Windows 10 Home/Pro or later
- macOS Catalina (version 10.15) or later

Minimum System Requirements:
- 2GB RAM
<br>


### Python source code deployment
Our Python code is developed in Python 3 and can be supported by any of its versions (Python 3.x). 

Depending also on the subset of the Python language installed in their system, the user may also need to manualy install the following packages: 
***pip3** (python3-pip)*, 
***tkinter** (python3-tk)*,
***venv** (python3-venv)* and
***python3-dev***


We recommend it is executed in a virtual environment. This can be done in two ways:

**1\.**  Either using the *load_environment_linux.sh* bash script file to create the virtual environement and then activating it:
```
source load_environment_linux.sh
source venv/ben/activate
```
**2\.**  Or more explicitly:
- first, creating the virtual environment, 
```
python3 -m venv our_virtual_environment_name
```
- then activating it
```
#linux/macos (bash/zsh)
source our_virtual_environment_name/bin/activate
```
```
#windows (cmd.exe)
our_virtual_environment_name\Scripts\activate.bat
```
- finally, installing the required Python packages and modules.

  This can be done either by installing in bulk using the requirements.txt file:
```
pip install -r requirements.txt
```
<br>


***The user can then run the source code via the command:***

```
python3 VISROC_2.0.py
```
<br>

### R Shiny Web application
The [R Shiny Web application](#) will be accessed online (thanks to *ShinyApps.io*, a cloud service run by RStudio) and used via the user's desktop, laptop or even mobile device, and it's compatible with all major browsers, regardless of having or not installed R, in any of its versions or any specific module/package.
The minimum browser screen size for the best visual matching with the dimensions of the application (and therefore the non-necessity of zooming only to see different parts of the application) is 760 pixels wide and 840 pixels high
<br>

### Run R code locally
Our R code can be supported by any machine where an R-4.x.y version is installed. The user has nevertheless to install, before executing it, the following prerequisite libraries (library version used for the development, the user must make sure that these or newer versions are installed on their machine):
 - shiny (1.7.1)
 - shinyjs (2.1.0)
 - shinyBS (0.61.1)
 - ggplot2 (3.3.6)
 - here (1.0.1)
using the command

```r
install.packages(c("shiny", "shinyjs", "shinyBS", "ggplot2", "here"))
```

The user has then two options to run the source code:

* either via the command

```bash
Rscript VISROC_2.0.r

```
and then copying and pasting the url of the output
```bash
Listening on http://127.0.0.1:6397

```
into a web browser,

* or by opening the VISROC_2.0.r file with RStudio IDE, where they have to select "Run App".

----

&#x26a0;&#xfe0f; To bundle a new version of code or helper files using the same pipeline, it's important to know that PyInstaller supports Python 3.7 and newer

<br>

## Usage
Both GUI applications have, in a visible place, a special "Help" button where the user can refer to the instructions regarding the program's input parameters, as well as the output files and results, the different menus, and the potential error outputs.
In an equally visible place, they also have an additional button that helps the user to refer to the interpretation of the graph whenever they want
<br>

## Known issues
### False Positive Virus Alert (Windows & Cloud) and Permission to unauthorized apps (macOS)<a name="securityissues" />

Due to innate features of PyInstaller's executables' architecture, some antivirus software —either locally or of some cloud service (when we are about to download)— can give a False Positive/Alarm for the VISROC executable files (.exe, .app, .elf). Unfortunately, the problem cannot for the moment be solved. The user has to ignore or/and temporarily or permanently disable the antivirus software security check for the specific files.

Similarly, the macOS user should exceptionally allow GateKeeper software, which attempts to prevent downloading unauthorized apps, to open the application. To do so, the user must go to "Security & Privacy" and click the "Open Anyway" button in the "General" panel to confirm their intent.

**Theoretically, even the exceptional relaxation of the security mechanisms exposes the user to the download and use of files that mimic our executables (in name, size, dates, etc.) but are decisively modified so that they are now malware. To protect the user from this eventuality, here are the hashes (using SHA-256 algorithm) of our three VISROC 2.0 applications**:

- VISROC_2.0.exe (Windows): **ba3fb5b6a15b9f5be6733cb02a2efd185c6e1b7ff20e94ebc39e0643ae7a5d31**

- VISROC_2.0.app (macOS):   **9094f3f72a736e94886afd6227a00c2b18301b798c796de607a1dd1392b7ad32**
- VISROC_2.0.elf (Linux):   **8bc1e79b9e060dcf1080235b12ab56a19d92f9a8a487d10286d27eaabd3f26a2**
- VISROC_2.0.py (source code):   **244b0e482ed996910560619e8dcae186af28dc932d88ceceee8e3767b4093f87**

SHA-256 hashes are fixed size 256-bit (32-byte) unique values, a kind of 'signature' for a text or a data file.
Comparing these values, with the ones generated by the files the user wants to use, will ensure them regarding the identity, thus the security, of the files. To generate the SHA-256 hashes of the files available in the user's system, they have to use the following commands (depending on the OS):

```
#windows
certutil -hashfile VISROC_2.0.exe SHA256
```
```
#macos
shasum -a 256 VISROC_2.0.app/Contents/MacOS/VISROC_2.0
```
```
#linux
sha256sum VISROC_2.0.elf
```
<br>

### Fix Possible Display Issues
#### View-Scale issue on macOS
An issue with as yet unexplained causes occurs on some macOS machines when either the standalone application (.app) or the source code (.py) starts with a window of completely irrelevant dimensions, thus displaying only a small part (upper left corner) which does not include any of the input, output and control elements, rendering the application unusable. Until fixed, however, **the user can work around the issue by selecting "*Full-Screen Mode*" from the "*View*" menu of the application's top-level menu bar** (the application does not is not aesthetically optimized for full-screen mode but is nevertheless fully functional)
#### Font Type issue when running source code in Anaconda Python on Linux
In Linux machines that use Anaconda Python distribution, the Tkinter can load no more than the legacy bitmapped X fonts that are available on the user's system. As such, and because of the domino effect on the dimensions of its graphic elements, the application is heavily affected regarding not only its display but also its functionality. The issue occurs because Anaconda is not built against the Freetype library and does not include Freetype support in the Tk DLL. Moreover, Anaconda Inc. [admits](https://github.com/ContinuumIO/anaconda-issues/issues/6833) that they will not be able to change this approach to address this issue.
As such, the correct approach to address the issue is for the user to ensure they use their system Python and not Anaconda Python. To do so they should:
 - either, when creating their virtual environment, call Python using explicitly the whole path to its location in the user's filesystem
 
```
/user/bin/python3 -m venv our_virtual_environment_name
```
 - or, either for the session or permanently, to modify appropriately their system's $PATH prioritizing system's Python over Anaconda Python.
 #### Display issue due to Display Server's settings (on Virtual Machines)
Display issues have been observed due to deregulation of system display server settings (X, Wayland, Quartz). The issue seems to occur on virtual machines configured in a different display environment than the one in use. The issue is resolved by explicitly setting/updating the dimensions and resolution (pixels, DPI) of the display server settings.
<br>
 
## Files Description
```
VISROC_2.0
├── README.md
├── R_Shiny_Web_App
│   ├── VISROC_2.0.r
│   └── www
│       ├── graph_interpretation.html
│       ├── graph_interpretation.svg
│       └── HelpR.html
└── Python_GUI
    ├── VISROC_2.0.elf
    ├── VISROC_2.0.exe
    ├── VISROC_2.0.app
    ├── source_code
    │   ├── VISROC_2.0.py
    │   ├── graph_interpretation.png
    │   ├── Help.html
    │   ├── LOGO_VISROC_75x75.icns
    │   ├── LOGO_VISROC_75x75.ico
    │   ├── LOGO_VISROC_75x75.png
    │   ├── load_environment_linux.sh
    │   └── requirements.txt
    └── pyi_files_to_build_executable
         ├── pyi_spec_file_linx.spec
         ├── pyi_spec_file_macos.spec
         └── pyi_spec_file_mswin.spec

11 directories, 22 files
```
The directories *R_Shiny_Web_app* and *Python_GUI* contain all the related files with the R and Python implementation respectively.

Regarding R:
- *VISROC_2.0.r* is the source code file,
- while in the folder *www* are included image and HTML files used by the code.

As for Python, we have:
- an executable clickable standalone file *VISROC_2.0.elf* for GNU/Linux operating systems,
- an executable clickable standalone file *VISROC_2.0.exe* for Windows,
- an executable clickable standalone bundle file *VISROC_2.0.app* for macOS (which is viewed as a directory by other cloud or local storage filesystems),
- a *source_code* folder which includes:
    - the source code *VISROC_2.0.py* file,
    - the image and HTML files to which the code refers,
    - the *requirements.txt* file which contains the packages necessary for the code, either for information or for bulk installation (see above: [Python source code deployment](#requirementstext)),
    - as well as a *load_environment_linux.sh* bash script file that can be used ⁠for a more automated creation of the necessary virtual environement,
- and the *pyi_files_to_build_executable* folder, which contains the special file manifests, one for each operating system, that PyInstaller uses to build standalone executables from Python code (they are not ready to use, as their file paths need specification according to the file architecture of each user)

## License
VISROC 2.0 is available under the GNU Affero General Public License v3.0. See the LICENSE file for more info.
