import os

def score(matches, ground_truth, num_samples):
    i = 0
    score = 0
    idl_score = 0

    num_sample = len(os.listdir(ground_truth[:ground_truth.rindex('/')]))
    print(num_sample)
    for match in matches:
        i += 1
        idl_rank = ideal_rank(i, num_samples)
        
        rank = 0
        if same_file(match[0], ground_truth):
            rank = 3
        elif same_path(match[0], ground_truth):
            rank = 2
        else:
            print(match[0], ground_truth)
        
        score += dcg_score(rank, i)
        idl_score += dcg_score(idl_rank, i)
    if(idl_score == 0):
        return 0
    return (score/idl_score)
       
def same_file(path1, path2):
    path1_sp = path1.strip("./")
    path2_sp = path2.strip("./")
    return (path1_sp==path2_sp)

def same_path(path1, path2):
    path1_sp = path1.strip("./").split('/')
    path2_sp = path2.strip("./").split('/')
    for i in range(min(len(path1_sp)-1, len(path2_sp)-1)):
        #print(path1_sp[i], "\t", path2_sp[i])
        if path1_sp[i] != path2_sp[i]:
            return False
    return True
       
def ideal_rank(i, num):
    if(i == 1):
        return 3
    elif(i < num):
        return 2
    return 0

    #NCDG_LOG = max(1,log2(i))
NCDG_LOG = [1,1,1.584962501,2,2.321928095,2.584962501,2.807354922,3,3.169925001,3.321928095,3.459431619,3.584962501,3.700439718,3.807354922,3.906890596,4,4.087462841,4.169925001,4.247927513,4.321928095,4.392317423,4.459431619,4.523561956,4.584962501,4.64385619]
def dcg_score(rank, i):
    discount = NCDG_LOG[-1]  
    if(i>0 and i < len(NCDG_LOG)):
        discount = NCDG_LOG[i]
    return (rank/discount)

def bash_same_path(a,b):
    if same_path(a,b):
        print(1)
    else:
        print(0)
