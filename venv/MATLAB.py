import DEFINES
import subprocess

def makeMATLAB(fileName,listList,minX,maxX, minY,maxY,xlabel,ylabel,zlabel, gapX, gapY):
    # type: (string, list, integer, integer, integer, integer, string, string, string, string) -> None
    """
        this function creates an mathlab file from the results collected via the muscle anylzer
        plots 4 bar graphs
    :param fileName: the name of the file would be saved in mathlab format
    :param listList:  the data base of the muscle result (Z axi)
    :param minX:  the min X axi value
    :param maxX: the max X axi value
    :param minY: the min Y axi value
    :param maxY: the min y axi value
    :param xlabel: xlabel
    :param ylabel: ylabel
    :param zlabel: zlabel
    :param gapX: yael step in X axi
    :param gapY: yael step in Y axi
    """
    # this code make anylezation of the muscle tool using MATLAB
    #https://stackoverflow.com/questions/6657005/matlab-running-an-m-file-from-command-line
    f=open(DEFINES.PATH_FILES + fileName + ".m", 'w')
    f.write("Z=[")
    for list in listList:
        f.write(str(list))
        f.write(";")
    f.write("];\n")
    f.write("y=[" + str(minY) + ":" + str(gapY) + ":" + str(maxY) + "];\n")
    f.write("%%PRINT RESULT OBJECT AS IS\n")
    f.write("figure(1)\n")
    f.write("h=bar3(y, Z);\n")
    f.write("colorbar;\n")
    f.write("colormap Parula;\n")
    f.write("for k = 1:length(h)\n")
    f.write("    zdata = h(k).ZData;\n")
    f.write("    h(k).CData = zdata;\n")
    f.write("    h(k).FaceColor = 'interp';\n")
    f.write("end\n")
    f.write("set(gca,'XTick',[1:1:"+str(maxX)+"],'XTickLabel',["+str(minX)+":"+str(gapX)+":"+str(maxX)+"],'fontsize',4);\n")
    f.write("axis tight\n")
    f.write("xlabel('"+xlabel+"');\n")
    f.write("ylabel('"+ylabel+"');\n")
    f.write("zlabel('"+zlabel+"');\n")
    f.write("savefig('"+fileName+"1')\n")


    f.write("%%PRINT RESULT OBJECT WITH SATTISTICS\n")
    f.write("figure(2)\n")
    f.write("ZZ = Z;\n")
    f.write("ZZ(ZZ >= 100) = 100;\n")
    f.write("ZZ(ZZ == 0) = 0;\n")
    f.write("ZZ(ZZ == -1) = -30;\n")
    f.write("h=bar3(y, ZZ);\n")
    f.write("colorbar;\n")
    f.write("colormap jet;\n")
    f.write("for k = 1:length(h)\n")
    f.write("    zdata = h(k).ZData;\n")
    f.write("    h(k).CData = zdata;\n")
    f.write("    h(k).FaceColor = 'interp';\n")
    f.write("end\n")

    f.write("set(gca,'XTick',[1:1:"+str(maxX)+"],'XTickLabel',["+str(minX)+":"+str(gapX)+":"+str(maxX)+"],'fontsize',3);\n")
    f.write("axis tight\n")
    f.write("xlabel('"+xlabel+"');\n")
    f.write("ylabel('"+ylabel+"');\n")
    f.write("zlabel('"+zlabel+"');\n")
    f.write("savefig('"+fileName+"2')\n")


    f.close()




def run_MATLAB(title):
    subprocess.call([r"C:\\Programs\MATLAB\R2017b\bin\matlab.exe", "-nodisplay", "-nosplash", "-nodesktop", "-r","\"run('" + DEFINES.MUSCLE_PATH + title + ".m')\""])