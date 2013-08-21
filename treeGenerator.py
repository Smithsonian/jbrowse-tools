#!/usr/bin/python
import re
import argparse
import sys
import zipfile
import os
import zipfile
from Bio import Phylo

def getAllBranchLength(tree):
    lengths = {}
    i = 0
    for clade in tree.find_clades(terminal=False, order ='level'):
        for child in clade:
            if child.branch_length:
    		  lengths[i] = child.branch_length
        	  i = i+1
    return lengths

def changeLength(tree):
    temp = tree
    for clade in temp.find_clades(terminal=False, order='level'):
        for child in clade:
            if child.branch_length:
                child.branch_length = child.branch_length*1000
    return temp

def checkLength(treeFile):
    tree = Phylo.parse(treeFile, 'phyloxml').next()
    i = 0
    sum = 0
    totalBranch = 0
    branchList = getAllBranchLength(tree)
    for branch in branchList:
        sum = sum+branchList[i]
        i = i+1
        totalBranch = totalBranch+1
    avg = sum/totalBranch
    if avg < 1:
        return False
    return True

def writeHeaderFile(outputFileName):
    outputFile = open(outputFileName, 'a')
    outputFile.write(
        '<html>\n'
        '<head>\n'
	'\t<script type="text/javascript" src="http://code.jquery.com/jquery-1.7.1.min.js" ></script>\n' 
	'\t<script type="text/javascript" src="https://raw.github.com/DmitryBaranovskiy/raphael/master/raphael-min.js" ></script>\n' 
	'\t<script type="text/javascript" src="http://bioinfolab.unl.edu/emlab/Gsignal/files/js/jsphylosvg-min.js"></script>\n' 
	'\n\t<script type="text/javascript">\n'
	'\t$(document).ready(function(){\n'
    		     )
    
    outputFile.close()

def writeEndofFile(outputFileName,xmlFileName):
    outputFile = open(outputFileName, 'a')
    outputFile.write(
    					'\t\t$.get("'+ xmlFileName + '", function(data) {\n'
						'\t\t\tvar dataObject = {\n'
						'\t\t\t\txml: data,\n'
						'\t\t\t\tfileSource: true\n'
						'\t\t\t};\n'		
						'\t\t\tphylocanvas = new Smits.PhyloCanvas(\n'
						'\t\t\t\tdataObject,\n'
						"\t\t\t\t'svgCanvas',\n" 
						'\t\t\t\t800, 800,\n'
						'\t\t\t);\n'
						'\t\t});\n'
						'\t});\n'
						'\t</script>\n'

						'</head>\n'
						'<body>\n'
						'\t<div id="svgCanvas"> </div>\n'
						'</body>\n'
						'</html>\n'

    				)
    
    outputFile.close()
def __main__():
	aZip = zipfile.ZipFile(sys.argv[1],'r')
	aZip.extractall('.')
	id = 0
	for name in aZip.namelist():
		treeFile = name
		if not checkLength(treeFile):
			tree = Phylo.parse(treeFile, 'phyloxml').next()
			newTree = changeLength(tree)
			newTName = treeFile.split('.')[0]+'_adj.xml'
    			Phylo.write(newTree,newTName,'phyloxml')
			treeFile = newTName
		outputFileName = 'tree_'+ str(id) + '.html'
		writeHeaderFile(outputFileName)
		writeEndofFile(outputFileName,treeFile)
		id = id+1
if __name__=="__main__":__main__()
