import sys #to get arguments from the terminal

'''
read_csv
DESCRIPTION: read the semi-colon separated data and put data into a list
INPUT: 
    path: the path to the csv file data with semicolon separated (";") format
RETURN:
    table: A list of lists of data from the csv file
            This list will also be filtered so that only the data with case_status as certified will be included
    count: number of certified rows or entries within this data
    header: a list of column headers
'''

def read_csv(path):
    #read the csv file
    table = []
    count = 0 #keep track of number of entries
    first = 0 #keep track of the very first header
    status_ind = -1 #the index of the case_status column
    header = ''
    num_attr = 0 #number of attributes
    with open(path, 'r') as file:
        for data in file:
            entry = data.split(';')
            
            #get rid of the '\n' in the original_cert_date attribute
            entry[-1] = entry[-1][:-2]
                    
            #get only the data that case_status == certified
            #need only the values, not the index in the first column
            
            #find index of case_status if it is the very first line (the column headers)
            ## note that every single data might have different names for the status column
            ## but in all cases, the column name will contain the word 'status'
            ## so we will use this keyword to find the column that holds the application status
            if first == 0: 
                num_col = len(entry)
                for index in range(num_col):
                    #compare the lowercase version because not all data 
                    if 'status' in entry[index].lower():
                        status_ind = index
                        header = entry
                        num_attr = num_col
                
                #if there is no status column, this data cannot be used
                if status_ind == -1:
                    print('There is no case status in the data')
                    return -1, -1, -1
                first = 1
            
            if entry[status_ind] == 'CERTIFIED':
                #there are some entries where the string contains ';', and the string will be splitted by our previous operation
                #so we now check for such entry by noting that such strings always begin with " and the next entry begins with space
                #the first column is always index, so we can omit it
                for i in range(1, num_attr-1):
                    #check if the entry is empty
                    if len(entry[i])>0 and len(entry[i+1])>0:
                        #check for spaces so we know for sure the split is with the delimiter ';'
                        if entry[i][0] == '"' and entry[i+1][0] == ' ':
                            entry[i] = entry[i] + ';' + entry[i+1]
                            trash = entry.pop(i+1)
                table.append(entry)
                count = count + 1
            
            
    return table, count, header

'''
get_occupations
DESCRIPTION: get the top 10 occupations that are certified
INPUT:
    data: the list of data returned from read_csv, note that the data contains only certified entries
    total: the total number of entries in the data that is certified
    header: list of column headers
    outputfile: file path for the output
OUTPUT:
    top 10 occupations in the form of [application, number application name, percentage]
    stored in outputfile
RETURNS:
    0: successful
    -1: error
'''
def get_occupations(data, total, header, outputfile):
    #count the occurrences for each job type
    soc_ind = -1
    #find index of SOC_NAME
    ## because some data's soc_name column is not name SOC_NAME, we will look for the column that has the keywords 'soc' and 'name'
    #in the case of multiple work states, we will only use location 1
    num_col = len(header)
    for index in range(num_col):
        #convert to lowercase because the comparison is case-sensitive
        if 'soc' in header[index].lower() and 'name' in header[index].lower():
            soc_ind = index
    
    #if the soc_name column is not in data, we cannot use it, thus return -1
    if soc_ind == -1:
        print('No soc_name column in data.')
        return -1
    
    #set up a dictionary to count the frequency
    occup = {}
    
    #keep track of the total number of applications
    total_app = 0
    
    #go through the data and start counting
    for row in data:
        #increment count if the occupation is recorded in the diction
        #sometimes the SOC_title is in double quotes, so we remove that, because it will interfere with the sorting later on
        soc_title = row[soc_ind].strip('"')
        
        #if the title is an empty string, we do not care about it
        if len(soc_title)>0:
            try: 
                occup[soc_title] = occup[soc_title] + 1
            except KeyError:
            #if the job is not in the dictionary, add it to the dictionary
                occup[soc_title] = 1
            
        total_app = total_app + 1
    
    #get the top 10 jobs
    job_tuples = occup.items()
    sorted_jobs = sorted(job_tuples, key = lambda x:(-x[1], x[0]))
    top_jobs = sorted_jobs[:10]
    
    #write to text file
    with open(outputfile, 'w') as f:
        f.write('TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
        for j in top_jobs:
            f.write(j[0]+';'+str(j[1])+';'+str(round((j[1]/total)*100, 1))+'%\n')
    return 0


'''
get_states
DESCRIPTION: get the top 10 states that are certified
INPUT:
    data: the list of data returned from read_csv, note that the data contains only certified entries
    total: the total number of entries in the data that is certified
    header: list of column headers
    outputfile: file path of output
OUTPUT:
    top 10 states in the form of [TOP_STATES, number application name, percentage]
    stored in outputfile
RETURNS:
    0: successful
    -1: error
'''
def get_states(data, total, header, outputfile):
    #count the occurrences for each job type
    state_ind = -1
    #find index of work state
    #because not all data name the column 'WORK_STATE', we will search for the keywords 'work' and 'state'
    num_col = len(header)
    for index in range(num_col):
        #convert to lowercase because the comparison is case-sensitive
        if 'work' in header[index].lower() and 'state' in header[index].lower():
            state_ind = index
    
    #if the soc_name column is not in data, we cannot use it, thus return -1
    if state_ind == -1:
        print('No work_state column in data.')
        return -1
    
    #set up a dictionary to count the frequency
    occup = {}
    
    #keep track of the total number of applications
    total_app = 0
    
    #go through the data and start counting
    for row in data:
        #increment count if the occupation is recorded in the diction
        #in case of double quotes, we remove that so not to interfere with the sorting later
        state = row[state_ind].strip('"')
        
        #we do not count if the state is not recorded in the data, that is, 
        #if the state is an empty string we do not care about that entry
        if len(state)>0: 
            try: 
                occup[state] = occup[state] + 1
            except KeyError:
            #if the job is not in the dictionary, add it to the dictionary
                occup[state] = 1
            
        total_app = total_app + 1
    
    #get the top 10 states
    job_tuples = occup.items()
    
    #first sort by the frequency
    sorted_jobs = sorted(job_tuples, key = lambda x:(-x[1], x[0]))
    
    
    top_jobs = sorted_jobs[:10]
    
    #write to text file
    with open(outputfile, 'w') as f:
        f.write('TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
        for j in top_jobs:
            
            f.write(j[0].strip('"')+';'+str(j[1])+';'+str(round((j[1]/total)*100, 1))+'%\n')
            
    return 0

'''
top_10_jobs
DESCRIPTION: get the top 10 occupations for certified visa applications
INPUT: 
    datapath: the path to the csv file
OUTPUT:
    will write to top_10_occupations.txt the top 10 occupations in the format
    {TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE}
'''
def top_10_jobs():
    #sys.argv[0] = program name
    #sys.argv[1] = csv data file path
    #sys.argv[2] = output job title file path
    #sys.argv[3] = output states file path
    data, total, header = read_csv(sys.argv[1])
    #if the data did not have the columns that we want to analyze, return no occupation
    if data != -1 and total != -1 and header != -1:
        occup_success = get_occupations(data, total, header, sys.argv[2])
        #if getting the occupations is not successful
        if occup_success == -1:
            print('data did not have data concerning soc_name')
        
        states_success = get_states(data, total, header, sys.argv[3])
        
        #if getting states is not successful
        if states_success == -1:
            print('data did not have data concerning work_states')
        
    else:
        print('data did not have the application status.')




##### MAIN FUNCTION ###########
top_10_jobs()

