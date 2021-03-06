#!/usr/bin/python
##########################################################################################
#
# 1. Be sure to install ete2 or ete3 python library on your computer with this link: http://etetoolkit.org/download/
# 2. Input argument is a directory that contains trees starting with "RAxML_bipartitions.", if it's not this pattern, the user is welome to change the pattern 
# on the line that contains "for tree in tree_files:"

# 3. This script searches for nodes where parasitic genes (Triphysaria versicolor genes start with TrVeBC3, Striga hermonthica genes start with StHeBC3, and Orobanche
# aegyptiaca genes start with OrAeBC5) strongly group with donor genes from Rosids. This is a stringent approach that requires two nodes that strongly support the grouping
# of parasite sequences with donor genes. Strong is supported by two criteria: 1) the node is exclusively composed of donor and parasite sequences; 2) bootstrap support 
# values exceed or equal 50 or 80. It screens for trees that fit model 1 and model 2 of Figure 1 in the paper. 


##########################################################################################
import sys, os, string, re
#from ete2 import PhyloTree
class SuppressAllOutput (object):
    def __enter__(self):
        sys.stderr.flush()
        self.old_stderr = sys.stderr
        sys.stderr = open('/dev/null', 'a+', 0)
        sys.stdout.flush()
        self.old_stdout = sys.stdout
        sys.stdout = open('/dev/null', 'a+', 0)
 
    def __exit__(self, exc_type, exc_value, traceback):
        sys.stderr.flush()
        sys.stderr = self.old_stderr
        sys.stdout.flush()
        sys.stdout = self.old_stdout
 
print >>sys.stdout, "printing to stdout before suppression"
print >>sys.stderr, "printing to stderr before suppression"
         
#it can be ete2 or ete3 library, make sure it works with both versions

with SuppressAllOutput():
    try:
        from ete2 import PhyloTree
        from ete2 import Tree
        print >>sys.stdout, "printing to stdout during suppression"
        print >>sys.stderr, "printing to stderr during suppression"
    except:
        pass
    try:
        from ete3 import PhyloTree
        from ete3 import Tree
        print >>sys.stdout, "printing to stdout during suppression"
        print >>sys.stderr, "printing to stderr during suppression"
    except:
        pass

print >>sys.stdout, "printing to stdout after suppression"
print >>sys.stderr, "printing to stderr after suppression"

# check for user input - tree directory
if (len(sys.argv) != 2 ):
    print "get_HGT_from_rosids2parasites_strigent2nodes.py <newick_trees_dir>"
    exit()
	
# create output directory
events_dir = '%s''/events' % (str(sys.argv[1]))
if not os.path.exists(events_dir):
	os.makedirs(events_dir)
	
# get tree files from directory
tree_files = os.listdir(str(sys.argv[1]))
for tree in tree_files:
    if tree.startswith('RAxML_bipartitions.'):
    	# get orthogroup id
    	ortho = re.sub(r'\D', "", tree)  
        # load newick tree
        #print(tree)
        t = PhyloTree(tree)
        #print(t)
        evts = file('%s''/''%s''.temp' %(events_dir,tree), "w")
##########################################################################################
# 			evolutionary events involving all taxa
##########################################################################################
        # Alternatively, you can scan the whole tree topology
        events = t.get_descendant_evol_events()
        # print its orthology and paralogy relationships
        for ev in events:
            if ev.etype == "S":
                evts.write( ",".join(ev.in_seqs))
                evts.write("<===>")
                evts.write(",".join(ev.out_seqs))
                evts.write("\n")
            elif ev.etype == "D":
                evts.write( ",".join(ev.in_seqs))
                evts.write("<===>")
                evts.write(",".join(ev.out_seqs))
                evts.write("\n")
        evts.close()      

        evts = file('%s''/''%s''.temp' %(events_dir,tree), "r")

        output_count =0
        for row in evts:

            pair = row.split("<===>" )
            left = "".join(pair[0].split())
            right = "".join(pair[1].split())
            if (len(left) > 0 and len(right) > 0):
            	child_left = left.split(",")
            	child_right = right.split(",")
            	ancestor_1 = t.get_common_ancestor(child_left[0], child_right[0])
                #print child_left[0] + "\t" + child_right[0] 
                #print ancestor_1
                #a counter to score the number of monocots genes
                mono_left =0 
                mono_right = 0
                para_left = 0
                para_right= 0
                rosid_left = 0
                rosid_right=0
                asterid_left=0
                asterid_right =0 
                other_left = 0
                other_right =0
                para_list = list()

                for i in child_left:
                    if i.startswith("gnl_Phypa"):   other_left +=1
                    if i.startswith("gnl_Selmo"):   other_left +=1
                    if i.startswith("gnl_Ambtr"):   other_left +=1
                    if i.startswith("gnl_Nelnu"):   other_left +=1
                    if i.startswith("gnl_Aquco"):   other_left +=1
                    if i.startswith("gnl_Arath"):   rosid_left +=1
                    if i.startswith("gnl_Thepa"):   rosid_left +=1
                    if i.startswith("gnl_Carpa"):   rosid_left +=1
                    if i.startswith("gnl_Theca"):   rosid_left +=1
                    if i.startswith("gnl_Poptr"):   rosid_left +=1
                    if i.startswith("gnl_Frave"):   rosid_left +=1                   
                    if i.startswith("gnl_Glyma"):   rosid_left +=1
                    if i.startswith("gnl_Medtr"):   rosid_left +=1
                    if i.startswith("gnl_Vitvi"):   rosid_left +=1
                    if i.startswith("gnl_Solly"):   asterid_left +=1
                    if i.startswith("gnl_Soltu"):   asterid_left +=1
                    if i.startswith("gnl_Mimgu"):   asterid_left +=1
                    if i.startswith("LiPhGnB2"):    asterid_left +=1
                    if i.startswith("HeAn"):    asterid_left +=1
                    if i.startswith("LaSa"):    asterid_left +=1
                    if i.startswith("TrVeBC3"):
                        para_left+=1
                        para_list.append(i)
                    if i.startswith("StHeBC3"):
                        para_left+=1
                        para_list.append(i)
                    if i.startswith("OrAeBC5"):
                        para_left+=1
                        para_list.append(i)
                    if i.startswith("gnl_Orysa"):   mono_left +=1
                    if i.startswith("gnl_Bradi"):   mono_left +=1
                    if i.startswith("gnl_Sorbi"):   mono_left +=1
                    if i.startswith("gnl_Musac"):   mono_left +=1
                    if i.startswith("gnl_Phoda"):   mono_left +=1

                for i in child_right:
                    if i.startswith("gnl_Phypa"):   other_right +=1
                    if i.startswith("gnl_Selmo"):   other_right +=1
                    if i.startswith("gnl_Ambtr"):   other_right +=1
                    if i.startswith("gnl_Nelnu"):   other_right +=1
                    if i.startswith("gnl_Aquco"):   other_right +=1
                    if i.startswith("gnl_Arath"):   rosid_right +=1
                    if i.startswith("gnl_Thepa"):   rosid_right +=1
                    if i.startswith("gnl_Carpa"):   rosid_right +=1
                    if i.startswith("gnl_Theca"):   rosid_right +=1
                    if i.startswith("gnl_Poptr"):   rosid_right +=1
                    if i.startswith("gnl_Frave"):   rosid_right +=1                   
                    if i.startswith("gnl_Glyma"):   rosid_right +=1
                    if i.startswith("gnl_Medtr"):   rosid_right +=1
                    if i.startswith("gnl_Vitvi"):   rosid_right +=1
                    if i.startswith("gnl_Solly"):   asterid_right +=1
                    if i.startswith("gnl_Soltu"):   asterid_right +=1
                    if i.startswith("gnl_Mimgu"):   asterid_right +=1
                    if i.startswith("LiPhGnB2"):    asterid_right +=1
                    if i.startswith("HeAn"):    asterid_right +=1
                    if i.startswith("LaSa"):    asterid_right +=1
                    if i.startswith("TrVeBC3"):
                        para_right+=1
                        para_list.append(i)
                    if i.startswith("StHeBC3"):
                        para_right+=1
                        para_list.append(i)
                    if i.startswith("OrAeBC5"):
                        para_right+=1
                        para_list.append(i)
                    if i.startswith("gnl_Orysa"):   mono_right +=1
                    if i.startswith("gnl_Bradi"):   mono_right +=1
                    if i.startswith("gnl_Sorbi"):   mono_right +=1
                    if i.startswith("gnl_Musac"):   mono_right +=1
                    if i.startswith("gnl_Phoda"):   mono_right +=1


                #the node that each row is traversing is ancestor_1
                if (rosid_left >0 and rosid_right >0 and mono_left ==0 and mono_right ==0 and asterid_left ==0 and asterid_right==0 and other_left==0 and other_right==0) or (rosid_left >0 and rosid_right ==0 and mono_left ==0 and mono_right ==0 and asterid_left ==0 and asterid_right==0 and other_left==0 and other_right==0) or (rosid_left ==0 and rosid_right >0 and mono_left ==0 and mono_right ==0 and asterid_left ==0 and asterid_right==0 and other_left==0 and other_right==0):
                    #print "yes"
                    if (para_left >0 and para_right ==0) or (para_right >0 and para_left ==0) or (para_left >0 and para_right >0):
                        # if the node has only 1 parasite gene
                        
                        if len(para_list) ==1:
                            #print "yes"
                            node = t&para_list[0]
                            node1 = node.up
                            ances_dict = dict()
                            ances_dict[1] = node1
                            index =1
                            have_upper_node =True
                        
                            while have_upper_node:
                                try:
                                    index = index + 1
                                    node_previous= ances_dict[index-1]
                                    ances_dict[index] =node_previous.up
                                    
                                except:
                                    have_upper_node = False

                            if int(node1.support) >= 50:
                                bs_value_list = list()

                                for i in ances_dict.keys():
                                    if i >1:
                                        if ances_dict[i] is None:
                                            pass
                                        else:
                                            node = ances_dict[i]
                                            if node in ancestor_1 or node == ancestor_1:
                                                bs_value_list.append(node.support)

                                #as long as one of the bs_value_list(which has already excluded the node1) is greater than 50, then it is a puative HGT event
                                bs_count = 0
                                for bs in bs_value_list:
                                    if bs >=50:
                                        bs_count = bs_count + 1
                                    if bs_count >=1:
                                        output_count = output_count + 1
                                        if output_count == 1:
                                            print "Orthogroup number: " + ortho + " has the big node shown as:"
                                            print ancestor_1
                                            print "the node1 support consisting the parasite gene and the rosid donor is " + str(node1.support) + " with the node shown as:"
                                            print node1

                                            node2 = ""
                                            max_value = max(bs_value_list)
                                            node2 = ""
                                            #print str(max_value)
                                            for i in ances_dict.keys():
                                                if i >1:
                                                    if ances_dict[i] is None:
                                                        pass
                                                    else:
                                                        node = ances_dict[i]
                                                        if node in ancestor_1 or node == ancestor_1:
                                                            if node.support == max_value:
                                                                #print node
                                                                node2 = node
                                            print "the 2nd highly supported node consisting the parasite gene and the rosid donor is " + str(node2.support) + " with the node shown as:"
                                            print node2
                        elif len(para_list) ==2:
                            #print "yes"
                            node = t.get_common_ancestor(para_list[0],para_list[1])
                            #print node
                            node1 = node.up
                            #print node1
                            ances_dict = dict()
                            ances_dict[1] = node1
                            index =1
                            have_upper_node =True
                        
                            while have_upper_node:
                                try:
                                    index = index + 1
                                    node_previous= ances_dict[index-1]
                                    ances_dict[index] =node_previous.up
                                    
                                except:
                                    have_upper_node = False

                            if int(node1.support) >= 50:
                                #print "yes"
                                bs_value_list = list()

                                for i in ances_dict.keys():
                                    if i >1:
                                        if ances_dict[i] is None:
                                            pass
                                        else:
                                            node = ances_dict[i]
                                            #print node
                                            if node in ancestor_1 or node == ancestor_1:
                                                #print "yes"
                                                bs_value_list.append(node.support)

                                #as long as one of the bs_value_list(which has already excluded the node1) is greater than 50, then it is a puative HGT event
                                bs_count = 0

                                for bs in bs_value_list:
                                    if bs >=50:
                                        bs_count = bs_count + 1
                                    if bs_count >=1:
                                        output_count = output_count + 1
                                        if output_count == 1:
                                            print "Orthogroup number: " + ortho + " has the big node shown as:"
                                            print ancestor_1
                                            print "the node1 support consisting the parasite gene and the rosid donor is " + str(node1.support) + " with the node shown as:"
                                            print node1

                                            node2 = ""
                                            max_value = max(bs_value_list)
                                            node2 = ""
                                            #print str(max_value)
                                            for i in ances_dict.keys():
                                                if i >1:
                                                    if ances_dict[i] is None:
                                                        pass
                                                    else:
                                                        node = ances_dict[i]
                                                        if node in ancestor_1 or node == ancestor_1:
                                                            if node.support == max_value:
                                                                #print node
                                                                node2 = node
                                            print "the 2nd highly supported node consisting the parasite gene and the rosid donor is " + str(node2.support) + " with the node shown as:"
                                            print node2

                        
                        elif len(para_list) ==3:
                            node = t.get_common_ancestor(para_list[0],para_list[1],para_list[2])
                            node1 = node.up
                            ances_dict = dict()
                            ances_dict[1] = node1
                            index =1
                            have_upper_node =True
                        
                            while have_upper_node:
                                try:
                                    index = index + 1
                                    node_previous= ances_dict[index-1]
                                    ances_dict[index] =node_previous.up
                                    
                                except:
                                    have_upper_node = False

                            if int(node1.support) >= 50:
                                bs_value_list = list()

                                for i in ances_dict.keys():
                                    if i >1:
                                        if ances_dict[i] is None:
                                            pass
                                        else:
                                            node = ances_dict[i]
                                            if node in ancestor_1 or node == ancestor_1:
                                                bs_value_list.append(node.support)

                                #as long as one of the bs_value_list(which has already excluded the node1) is greater than 50, then it is a puative HGT event
                                bs_count = 0
                                for bs in bs_value_list:
                                    if bs >=50:
                                        bs_count = bs_count + 1
                                    if bs_count >=1:
                                        output_count = output_count + 1
                                        if output_count == 1:
                                            print "Orthogroup number: " + ortho + " has the big node shown as:"
                                            print ancestor_1
                                            print "the node1 support consisting the parasite gene and the rosid donor is " + str(node1.support) + " with the node shown as:"
                                            print node1

                                            node2 = ""
                                            max_value = max(bs_value_list)
                                            node2 = ""
                                            #print str(max_value)
                                            for i in ances_dict.keys():
                                                if i >1:
                                                    if ances_dict[i] is None:
                                                        pass
                                                    else:
                                                        node = ances_dict[i]
                                                        if node in ancestor_1 or node == ancestor_1:
                                                            if node.support == max_value:
                                                                #print node
                                                                node2 = node
                                            print "the 2nd highly supported node consisting the parasite gene and the rosid donor is " + str(node2.support) + " with the node shown as:"
                                            print node2

                        elif len(para_list) ==4:
                            node = t.get_common_ancestor(para_list[0],para_list[1],para_list[2],para_list[3])
                            node1 = node.up
                            ances_dict = dict()
                            ances_dict[1] = node1
                            index =1
                            have_upper_node =True
                        
                            while have_upper_node:
                                try:
                                    index = index + 1
                                    node_previous= ances_dict[index-1]
                                    ances_dict[index] =node_previous.up
                                    
                                except:
                                    have_upper_node = False

                            if int(node1.support) >= 50:
                                bs_value_list = list()

                                for i in ances_dict.keys():
                                    if i >1:
                                        if ances_dict[i] is None:
                                            pass
                                        else:
                                            node = ances_dict[i]
                                            if node in ancestor_1 or node == ancestor_1:
                                                bs_value_list.append(node.support)

                                #as long as one of the bs_value_list(which has already excluded the node1) is greater than 50, then it is a puative HGT event
                                bs_count = 0
                                for bs in bs_value_list:
                                    if bs >=50:
                                        bs_count = bs_count + 1
                                    if bs_count >=1:
                                        output_count = output_count + 1
                                        if output_count == 1:
                                            print "Orthogroup number: " + ortho + " has the big node shown as:"
                                            print ancestor_1
                                            print "the node1 support consisting the parasite gene and the rosid donor is " + str(node1.support) + " with the node shown as:"
                                            print node1

                                            node2 = ""
                                            max_value = max(bs_value_list)
                                            node2 = ""
                                            #print str(max_value)
                                            for i in ances_dict.keys():
                                                if i >1:
                                                    if ances_dict[i] is None:
                                                        pass
                                                    else:
                                                        node = ances_dict[i]
                                                        if node in ancestor_1 or node == ancestor_1:
                                                            if node.support == max_value:
                                                                #print node
                                                                node2 = node
                                            print "the 2nd highly supported node consisting the parasite gene and the rosid donor is " + str(node2.support) + " with the node shown as:"
                                            print node2

                        elif len(para_list) ==5:
                            node = t.get_common_ancestor(para_list[0],para_list[1],para_list[2],para_list[3],para_list[4])
                            node1 = node.up
                            ances_dict = dict()
                            ances_dict[1] = node1
                            index =1
                            have_upper_node =True
                        
                            while have_upper_node:
                                try:
                                    index = index + 1
                                    node_previous= ances_dict[index-1]
                                    ances_dict[index] =node_previous.up
                                    
                                except:
                                    have_upper_node = False

                            if int(node1.support) >= 50:
                                bs_value_list = list()

                                for i in ances_dict.keys():
                                    if i >1:
                                        if ances_dict[i] is None:
                                            pass
                                        else:
                                            node = ances_dict[i]
                                            if node in ancestor_1 or node == ancestor_1:
                                                bs_value_list.append(node.support)

                                #as long as one of the bs_value_list(which has already excluded the node1) is greater than 50, then it is a puative HGT event
                                bs_count = 0
                                for bs in bs_value_list:
                                    if bs >=50:
                                        bs_count = bs_count + 1
                                    if bs_count >=1:
                                        output_count = output_count + 1
                                        if output_count == 1:
                                            print "Orthogroup number: " + ortho + " has the big node shown as:"
                                            print ancestor_1
                                            print "the node1 support consisting the parasite gene and the rosid donor is " + str(node1.support) + " with the node shown as:"
                                            print node1

                                            node2 = ""
                                            max_value = max(bs_value_list)
                                            node2 = ""
                                            #print str(max_value)
                                            for i in ances_dict.keys():
                                                if i >1:
                                                    if ances_dict[i] is None:
                                                        pass
                                                    else:
                                                        node = ances_dict[i]
                                                        if node in ancestor_1 or node == ancestor_1:
                                                            if node.support == max_value:
                                                                #print node
                                                                node2 = node
                                            print "the 2nd highly supported node consisting the parasite gene and the rosid donor is " + str(node2.support) + " with the node shown as:"
                                            print node2

        evts.close()




  