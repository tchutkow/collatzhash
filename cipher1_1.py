
collatz = lambda n : int(n/2) if n % 2 == 0 else n*3+1

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def CHash(string):

    bsize = 128
    
    #first we break the input into blocks of 128 characters
    bigblocks = [string[bsize*i:bsize*(i+1)] for i in range(len(string)//bsize+1)]
    if bigblocks[len(bigblocks)-1] == '':
        bigblocks.pop(len(bigblocks)-1)
    count = 0
    while len(bigblocks[len(bigblocks)-1]) < bsize:
        bigblocks[len(bigblocks)-1] += "%s"%(letters[count%26])
        count += 3



    hashedblocks = []
    
    #now we will perform a set of operations over each block of 128


    bigcount = 0
    for x in bigblocks:


        #to begin, we will break our block of 128 into 8 blocks of 16 characters

        blocks = [x[16*i:16*(i+1)] for i in range(8)]



        #next, we compute this sequence of functions on each of the 8 blocks
        #this function was designed based on empircal tests to maximize collision resistance
        if bigcount == len(bigblocks)-1:
            c = [collatz(ordstr_s(i)**16+ordstr_s2(i)**8+ordstr_a(i)**2) for i in blocks]
        else:
            c = [collatz(ordstr_s(i)**16+ordstr_s2(i)**8) for i in blocks]


        #now, we XOR the 8 blocks in a predetermined pattern
        #this leaves us with 4 blocks
        
        sums = [c[0]^c[7],c[1]^c[6],c[2]^c[5],c[3]^c[4]]

        #now, we run each block through the collatz function x times
        #where x is the numerical value of the block modulo 13
        cols = []
        for i in sums:
            for j in range(i%13):
                i = collatz(i)
            cols.append(i)



        
        #then, we perform another function on each block
        #first, we run a block through the collatz function
        #then, we run it through another function called "jumble"
        #finally, we run it back through the collatz function
        ok = [collatz(jumble(collatz(i))) for i in cols]

        #the jumble function is a function that takes an integer of any length,
        #divides it into 8 blocks, then rearranges these blocks in a predetermined way

        #finally, we run our 4 blocks through the last combination function
        #this function adds (integer adds) blocks 0 and 3 then runs it through the jumble function
        #it then adds blocks 1 and 2 and runs them through the jumble function
        #finally, it adds the two results and runs them through the jumble function
        
        final = jumble(jumble(ok[0]+ok[3])+jumble(ok[1]+ok[2]))

        #the goal in each iteration of this loop is to go from our initial 8 blocks
        #to just one block (or integer) that appears random and is greatly responsive
        #to even the smallest changes in the input text
                
        #now, this hashed block is added to a list of other hashed blocks
        #remember, the original input was a block of length 128
        #there are likely still many more blocks of length 128 to be hashed
        hashedblocks.append(final)

    #finally, all blocks have been run through the hash function
    #now, we sum them all together and raise the result to the 8th power
    #(in order to give us a string that is approximately the desired length ~128)
    #(the ultimate goal of this function is to spit out a string of length 128)
    now = sum(hashedblocks) ** 8

    #we set our upper and lower bounds (these are the decimal equivalents of the largest
    #and smallest 128 digit hexadecimal numbers)
    upper = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084095
    lower = 837987995621412318723376562387865382967460363787024586107722590232610251879596686050117143635431464230626991136655378178359617675746660621652103062880256

    #finally, we mod our result by the upperbound
    last = now % upper

    #then, square our result and mod it by the upperbound until it is within
    #the upper and lower bounds, giving us a 128 character string
    while last < lower:
        last = (last**2)%upper

    #finally, we return our 128 character string in hex format
    return hex(last)[2:]


#these are the functions used

def ordstr_a(string):
    out = ""
    for i in string:
        out += str(ord(i))
    return int(out)

#this takes a string, computes the ascii value of each character, then returns their sum
def ordstr_s(string):
    out = 0
    for i in string:
        out += ord(i)
    return out

# " " " ... ", then returns the sum of their squares
def ordstr_s2(string):
    out = 0
    for i in string:
        out += ord(i)**2
    return out


#this is our jumble function as previously described
def jumble(integer):
    string = str(integer)
    length = len(string) // 7
    x = [string[length*i:length*(i+1)] for i in range(8)]
    jumbled = x[3]+x[6]+x[1]+x[7]+x[0]+x[5]+x[4]+x[2]
    if jumbled == "":
        return 0
    return int(jumbled)
    



