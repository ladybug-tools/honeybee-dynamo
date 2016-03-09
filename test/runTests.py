"""This script opens Rhino and executes all the gh files inside test folder.

Every gh file in expected to have a logger component that writes the test report
to "filename.log". Script merges the reports together and generates a final report
of testing.

http://developer.rhino3d.com/guides/cpp/running_rhino_from_command_line/
"""
import os
import subprocess
import datetime


def main():
    """Open Rhino and executes all the gh files inside test folder.

    Every gh file in expected to have a logger component that writes the test report
    to "filename.log". Script merges the reports together and generates a final report
    of testing.
    """
    # base command for the RhinoPython script that will be executed inside RhinoScript
    # this script replace ghFiles with a list of gh files in this folder.
    testpy = """
from Rhino import RhinoApp, RhinoDoc
import rhinoscriptsyntax as rs
import scriptcontext as sc

ghFiles = %s
gh = RhinoApp.GetPlugInObject("Grasshopper")

gh.LoadEditor()
gh.CloseAllDocuments()
gh.ShowEditor()
for ghFile in ghFiles:
    gh.OpenDocument(ghFile)
    gh.CloseDocument()

gh.HideEditor()

sc.doc = RhinoDoc.ActiveDoc
rs.DocumentModified(False)
rs.Exit()
    """

    # base command to open Rhino and run the script. %s should be replaced by path to test.py
    command = '"C:\Program Files\Rhinoceros 5 (64-bit)\System\Rhino" /nosplash /notemplate /runscript="_-RunPythonScript %s'

    _path = os.path.split(os.path.realpath(__file__))[0]

    # find all the grasshopper files in this folder
    ghFiles = [os.path.join(_path, f) for f in os.listdir(_path) if (f.endswith(".gh") or f.endswith(".ghx"))]

    # update test.py file in directory
    testpyf = os.path.join(_path, "grasshopper_test.py")
    with open(testpyf, "w") as tf:
        tf.write(testpy % str(ghFiles))

    # run the script inside Rhinoceros
    subprocess.call(command % testpyf)

    # read log files and put a final report together
    logFiles = [os.path.join(_path, f) for f in os.listdir(_path) if f.endswith(".log")]
    report = []

    # TODO: Better reporting
    for lf in logFiles:
        with open(lf, "r") as lin:
            # find number of fails
            header = lin.readline().rstrip()
            fCount = int(header.split(" ")[0])
            if fCount != 0:
                report.append("Failed! :: %s in %s" % (header, lf))
            else:
                report.append("Passed! :: %s in %s" % (header, lf))

    reportf = os.path.join(_path, "report.txt")
    with open(reportf, "w") as rf:
        rf.write("\n".join(report) + "\n" + str(datetime.datetime.utcnow()))

    # remove temp python script
    try:
        os.remove(testpyf)
    except:
        pass

if __name__ == "__main__":
    main()
