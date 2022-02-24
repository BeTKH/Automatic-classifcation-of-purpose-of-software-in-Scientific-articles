from pathlib import Path

def _read_text_file(path, bef, aft, read_empty=False):
    
    def add_neighbours(*sentcs):
        
        # unpack list of sentcs passed
        lis_sents = list(sentcs)
    
        joined_tokens = []

        for i in range(len(lis_sents)):
        
            joined_tokens.extend(lis_sents[i].split())
        
            joined_sent = ' '.join(joined_tokens)
    
        return joined_sent

    def contextWindow(text, bef, aft):
        
        #xB, yA   --- where  x,y > len(text)
        if (bef >= len(text)-1) or (aft >= len(text)-1):

            # reset the context within paragrapgh , returns the whole paragrapgh 

            bef = len(text)- 1
            aft = len(text)- 1

            contxt_txt = []        

            for i in range(len(text)):  

                contxt_txt.append( ' '.join(text))

            return contxt_txt
            
        # 0B, OA --- no change
        elif (bef == 0) and (aft == 0):
            return text
        # 0B, 1A --- 2 conditions  
        elif (bef == 0) and (aft == 1):
            contxt_txt = []
            for i in range(len(text)):
                # 0B, 1A
                if (i >= 0) and (i < len(text)-1):
                    contxt_txt.append( add_neighbours(text[i], text[i+1])) 

                # 0B, 0A
                elif (i == len(text)-1):
                    contxt_txt.append(text[i]) 

            return contxt_txt

        #OB, 2A --- 3 conditions
        elif (bef == 0) and (aft == 2):
            contxt_txt = []
            for i in range(len(text)):
                #OB, 2A
                if (i >= 0) and (i <len(text)-2):
                    contxt_txt.append( add_neighbours(text[i], text[i+1], text[i+2]))

                elif i == (len(text)-2):
                    contxt_txt.append( add_neighbours(text[i], text[i+1] ))

                elif i == (len(text)-1):
                    contxt_txt.append(text[i])

            return contxt_txt

        #1B, 0A --- 2 conditions
        elif (bef == 1) and (aft == 0):
            contxt_txt = []
            for i in range(len(text)):
                #0B, 0A
                if (i == 0):
                    contxt_txt.append(text[i])

                elif (i >0):
                    contxt_txt.append(add_neighbours(text[i-1], text[i]))

            return contxt_txt

        #1B, 1A --- 3 conditions 
        elif ( bef == 1 ) and ( aft == 1):
            contxt_txt = []
            for i in range(len(text)):
                if i == 0:   # 0B, 1A
                    contxt_txt.append(add_neighbours (text[i], text[i+1]))

                elif (i >= 1) and ( i < len(text)-1):  # 1B ,1A
                    contxt_txt.append(add_neighbours(text[i-1], text[i], text[i+1]))

                elif (i == len(text)-1):  #1B, 0A
                    contxt_txt.append(add_neighbours(text[i-1], text[i]))
            return contxt_txt

        #1B, 2A --- 4 conditions
        elif (bef ==1 ) and (aft == 2):
            contxt_txt = []
            for i in range(len(text)):
                if i ==0:
                    contxt_txt.append(add_neighbours(text[i], text[i+1], text[i+2]))  #0B, 2A

                elif (i > 0) and (i < len(text)-2):
                    contxt_txt.append(add_neighbours(text[i-1], text[i], text[i+1],text[i+2]))     #1B, 2A

                elif (i == len(text)-2):
                    contxt_txt.append(add_neighbours(text[i-1], text[i],text[i+1]))               #1B, 1A

                elif i == (len(text)-1):
                    contxt_txt.append(add_neighbours(text[i-1], text[i]))                         #1B,0A
            return contxt_txt

        #2B, 0A   -- 3 cases 
        elif( bef ==2) and ( aft == 0):
            contxt_txt = []
            for i in range(len(text)):
                if i == 0:       
                    contxt_txt.append(text[i])         #0B, 0A
                elif i == 1:
                    contxt_txt.append(add_neighbours(text[i-1], text[i]))            #1B, 0A
                elif i > 1:
                    contxt_txt.append(add_neighbours(text[i-2], text[i-1], text[i]))  #2B, 0A
            return contxt_txt

        #2B, 1A -- 3 cases
        elif ( bef == 2 ) and (aft == 1):
            contxt_txt = []
            for i in range(len(text)):
                if i ==0: 
                    contxt_txt.append(add_neighbours(text[i], text[i+1]) )                     #0B, 1A

                elif i ==1:
                    contxt_txt.append(add_neighbours(text[i-1], text[i], text[i+1]) )          #1B, 1A

                elif (i > 1) and (i < len(text)-1):
                    contxt_txt.append(add_neighbours(text[i-2], text[i-1], text[i], text[i+1]))  # 2B, 1A

                elif i == len(text)-1:
                    contxt_txt.append(add_neighbours(text[i-2], text[i-2], text[i]))           #2B, 0A

            return contxt_txt

        #2B, 2A --- 5 conditions
        elif (bef == 2) and (aft == 2):        
            contxt_txt = []        
            for i in range(len(text)):    

                #print(f' there are {len(text)} sentences in {text}')

                if i == 0:    # 0B, 2A
                    contxt_txt.append(add_neighbours(text[i] , text[i+1] , text[i+2]))  

                elif i == 1:  # 1B, 2A
                    contxt_txt.append(add_neighbours(text[i-1] , text[i] , text[i+1] , text[i+2]))

                elif (i >=1) and (i < len(text)-2):   # 2B , 2A 
                    contxt_txt.append(add_neighbours(text[i-2], text[i-1], text[i], text[i+1], text[i+2]))

                elif (i == len(text)-2):             #2B, 1A
                    contxt_txt.append(add_neighbours(text[i-2], text[i-1], text[i], text[i+1]))

                elif i == len(text)-1:                #2B, 0A  
                    contxt_txt.append(add_neighbours(text[i-2], text[i-1], text[i]))

            return contxt_txt

        #3B, 3A --- 7 conditions
        elif (bef == 3) and (aft == 3):

            contxt_txt = []        
            for i in range(len(text)):

                if i == 0:  #0B, 3A
                    contxt_txt.append(add_neighbours(text[i] , text[i+1] , text[i+2] , text[i+3] ))

                elif i ==1: #1B, 3A
                    contxt_txt.append(add_neighbours(text[i-1] , text[i] , text[i+1] , text[i+2] , text[i+3] ))

                elif i ==2: #2B, 3A
                    contxt_txt.append(add_neighbours(text[i-2] , text[i-1] , text[i] , text[i+1] , text[i+2] ,text[i+3] ))

                elif (i >=3) and (i < len(text)-3): #3B, 3A
                    contxt_txt.append(add_neighbours(text[i-3], text[i-2] , text[i-1] , text[i] , text[i+1] , text[i+2] , text[i+3] ))

                elif (i == len(text)-3): #3B, 2A
                    contxt_txt.append(add_neighbours(text[i-3], text[i-2] , text[i-1] , text[i] , text[i+1] , text[i+2] ))

                elif (i == len(text)-2): #3B, 1A
                    contxt_txt.append(add_neighbours(text[i-3], text[i-2] , text[i-1] , text[i] , text[i+1]))

                elif (i == len(text)-1): #3B, 0A
                    contxt_txt.append(add_neighbours(text[i-3], text[i-2] , text[i-1] , text[i] ))

            return contxt_txt

        elif (bef == 0) and (aft == 3):

            contxt_txt = []        
            for i in range(len(text)):

                if (i >= 0) and (i < len(text)-3): #0B3A
                    contxt_txt.append(add_neighbours(text[i] , text[i+1] , text[i+2] , text[i+3] ))

                elif (i == len(text)-3):  # 0B2A
                    contxt_txt.append(add_neighbours(text[i] , text[i+1] , text[i+2]))  

                elif (i == len(text)-2):  #0B1A
                    contxt_txt.append(add_neighbours(text[i] , text[i+1]))

                elif (i == len(text)-1):
                    contxt_txt.append(text[i])  

            return contxt_txt

        elif (bef == 1) and (aft == 3):
            contxt_txt = []        
            for i in range(len(text)):

                if (i == 0): #0B3A
                    contxt_txt.append(add_neighbours(text[i] , text[i+1] , text[i+2] ,  text[i+3] ))

                elif (i > 0) and(i < len(text)-3):  # 1B3A
                    contxt_txt.append(add_neighbours(text[i-1] , text[i] , text[i+1] , text[i+2], text[i+3] ))  

                elif (i == len(text)-3):  #1B2A
                    contxt_txt.append(add_neighbours(text[i] , text[i+1], text[i+2]))

                elif (i == len(text)-2):  #1B1A
                    contxt_txt.append(add_neighbours(text[i-1] , text[i] , text[i+1]))

                elif (i == len(text)-1):  #1B0A
                    contxt_txt.append(add_neighbours(text[i-1] , text[i]))

            return contxt_txt

        elif (bef == 2) and (aft == 3):

            contxt_txt = []        
            for i in range(len(text)):

                if (i == 0): #0B3A
                    contxt_txt.append(add_neighbours(text[i] , text[i+1] , text[i+2] ,  text[i+3] ))

                elif (i == 1):  # 1B3A
                    contxt_txt.append(add_neighbours(text[i-1] , text[i] , text[i+1] , text[i+2], text[i+3] ))  

                elif (i > 1) and (i < len(text)-3):  #2B3A
                    contxt_txt.append(add_neighbours(text[i-2], text[i-1], text[i] , text[i+1], text[i+2],text[i+3]))

                elif (i == len(text)-3):  #2B2A
                    contxt_txt.append(add_neighbours(text[i-2], text[i-1] , text[i] , text[i+1], text[i+2]))

                elif (i == len(text)-2):  #2B1A
                    contxt_txt.append(add_neighbours(text[i-2], text[i-1] , text[i] , text[i+1]))

                elif (i == len(text)-1): #2B0A
                    contxt_txt.append(add_neighbours(text[i-2], text[i-1] , text[i]))

            return contxt_txt

        elif (bef == 3) and (aft == 2):

            contxt_txt = []        
            for i in range(len(text)):

                if (i == 0): #0B2A
                    contxt_txt.append(add_neighbours(text[i] , text[i+1] , text[i+2]))

                elif (i == 1):  # 1B2A
                    contxt_txt.append(add_neighbours(text[i-1] , text[i] , text[i+1] , text[i+2]))  

                elif (i > 1) and (i < len(text)-3):  #2B2A
                    contxt_txt.append(add_neighbours(text[i-2], text[i-1], text[i] , text[i+1], text[i+2]))

                elif (i == len(text)-3):  #3B2A
                    contxt_txt.append(add_neighbours(text[i-3], text[i-2], text[i-1] , text[i] , text[i+1], text[i+2]))

                elif (i == len(text)-2):  #3B1A
                    contxt_txt.append(add_neighbours(text[i-3], text[i-2], text[i-1] , text[i] , text[i+1]))

                elif (i == len(text)-1): #3B0A
                    contxt_txt.append(add_neighbours(text[i-3] , text[i-2], text[i-1] , text[i]))

            return contxt_txt 

        elif (bef == 3) and (aft == 1):

            contxt_txt = []        
            for i in range(len(text)):

                if (i == 0): #0B1A
                    contxt_txt.append(add_neighbours(text[i] , text[i+1]))

                elif (i == 1):  # 1B1A
                    contxt_txt.append(add_neighbours(text[i-1] , text[i] , text[i+1]))

                elif (i == 2):  # 2B1A
                    contxt_txt.append(add_neighbours(text[i-2], text[i-1] , text[i] , text[i+1]))  

                elif (i > 2) and (i < len(text)-1):  #3B1A
                    contxt_txt.append(add_neighbours(text[i-3] , text[i-2], text[i-1], text[i] , text[i+1]))

                elif (i == len(text)-1):  #3B0A
                    contxt_txt.append(add_neighbours(text[i-3], text[i-2], text[i-1] , text[i] ))

            return contxt_txt

        elif (bef == 3) and (aft == 0):
            contxt_txt = []        
            for i in range(len(text)):

                if (i == 0): #0B0A
                    contxt_txt.append(text[i])

                elif (i == 1):  # 1B0A
                    contxt_txt.append(add_neighbours(text[i-1] , text[i] ))

                elif (i > 1) and ( i < len(text)-1):  # 2B0A
                    contxt_txt.append(add_neighbours(text[i-2], text[i-1] , text[i]))  

                elif (i == len(text)-1):  #3B0A
                    contxt_txt.append(add_neighbours(text[i-3], text[i-2], text[i-1] , text[i] ))

            return contxt_txt
        
    txt_with_context = []
    with path.open(mode='r') as in_f:

        # read new line separated txt
        cont = in_f.read()

        #create paraggraphs
        par_list = cont.split('\n\n')


        for par_ in par_list:

            # list of sentences in the paragrapgh
            snt_lst_ = par_.split('\n')

            # remove empty strings
            snt_lst_ = list(filter(None, snt_lst_))

            # sentence with context
            sen_contkx = contextWindow(snt_lst_, bef, aft)
            
            #print(sen_contkx)

            txt_with_context.extend(sen_contkx)
            
    return txt_with_context