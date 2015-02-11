#Extracts type II supernovae matches only

#Define appropriate files
#SN_LIST:           IAU listing of all supernovae to date
#MATCH_FILE:        Listing of singg galaxy hosts and supernovae matches
#MATCH_FILE_OUT:    Reduced matched file with only type II supernovae
SN_LIST='../data/out_iau_supernovae_get.txt'
MATCH_FILE='../data/out_supernovae_match.csv'
MATCH_FILE_OUT='../data/out_supernovae_match_typeII.csv'

sn_list=open(SN_LIST, "r")
data=open(MATCH_FILE, "r")
buff=open(MATCH_FILE_OUT, "w")

#Write header to output
buff_header = "#Produced from comparing %s and %s\n" % (SN_LIST, MATCH_FILE)
buff.write(buff_header)

#loop through match file
for line in data.readlines():
    parts=line.split(',')
    supernova=parts[1].strip()

    #loop through sn_list
    for another_line in sn_list:
        if supernova in another_line:
            sn_type=another_line[130:136].strip()
            if (sn_type == ''):
                print supernova
            elif ('II' in sn_type):
                buff_line=line.strip()+',%s\n' % sn_type
                buff.write(buff_line)
    sn_list.seek(0);

#Save buffers
sn_list.close()
data.close()
buff.close()
