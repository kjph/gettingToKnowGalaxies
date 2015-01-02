SN_LIST='../data/out_iau_supernovae_get.txt'
MATCH_FILE='../data/out_supernovae_match.csv'
MATCH_FILE_TMP='../data/out_supernovae_match_typeII.csv'

sn_list=open(SN_LIST, "r")
data=open(MATCH_FILE, "r")
buff=open(MATCH_FILE_TMP, "w")

buff.write("#Produced from comparing out_iau_supernovae_get and out_supernovae_match through a tmp script in python\n")

for line in data.readlines():
    parts=line.split(',')
    supernova=parts[1].strip()
    for another_line in sn_list:
        if supernova in another_line:
            sn_type=another_line[130:136].strip()
            if (sn_type == ''):
                print supernova
            elif ('II' in sn_type):
                buff_line=line.strip()+',%s\n' % sn_type
                buff.write(buff_line)
    sn_list.seek(0);

sn_list.close()
data.close()
buff.close()
