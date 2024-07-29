# items
I = ['item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'item7', 'item8']

# cơ sở dữ liệu transactions
D = [
    ['item1', 'item2', 'item3'],
    ['item2', 'item4'],
    ['item1', 'item5'],
    ['item6', 'item7'],
    ['item2', 'item3', 'item4', 'item7'],
    ['item2', 'item3', 'item4', 'item8'],
    ['item2', 'item4', 'item5'],
    ['item2', 'item3', 'item4'],
    ['item4', 'item5'],
    ['item6', 'item7']
]

def find_freq_1_itemsets(D, I, minsup):
    F_1is = []
    for i in I:
        i_count = 0 
        for j in D:
            if i in j:
                i_count += 1
        if i_count >= minsup:
            F_1is.append(i)
    return F_1is

from itertools import combinations
def sub_lists(mlist, k):
    subs = []
    for i in range(0, len(mlist) + 1):
        temp = [list(x) for x in combinations(mlist, i)]
        if len(temp) > 0:
            subs.extend(temp)
    res = []
    if k == -1:
        for e in subs:
            if len(e) == 0:
                continue
            if len(e) < len(mlist):
                res.append(e)
    else:
        for e in subs:
            if len(e) == k:
                res.append(e)
    return res

def has_infrequent_subset(C, F):
    on_set = C if len(C) <= 2 else sub_lists(C, len(F[0]))
    for e in on_set:
        if e not in F:
            return True
    return False

def apriori_gen(F):
   C_k = []
   for i in range(0, len(F)-1):
       for j in range(i+1, len(F)):
           if isinstance(F[i], str) or isinstance(F[j], str):
               C = [F[i], F[j]]
           else:
               C = F[i].copy()
               for item in F[j]:
                   if item not in F[i]:
                       C.append(item)
                       break
           if has_infrequent_subset(C, F) == False and C not in C_k:
               C_k.append(C)
   return C_k

def subsets_of_T(C_k, T):
   C_T = []
   for C in C_k:
       net = False
       for c in C:
           if c not in T:
               net = True
               break
       if net == True:
           continue
       C_T.append(C)
   return C_T

def spread_itemsets_frequency(a):
   elements = [a[0]]
   for i in range(1, len(a)):
       if a[i] not in elements:
           elements.append(a[i])
   freq = []
   for i in elements:
       i_count = 0
       for j in a:
           if i == j:
               i_count += 1
       freq.append(i_count)
   return [elements, freq]

def get_freq(D, itemset_s):
    C_T_reached = []
    for i in range(0, len(D)):
        C_T = subsets_of_T(itemset_s, D[i])
        if len(C_T) > 0:
            C_T_reached = [*C_T_reached, *C_T]
    C_T_reached = spread_itemsets_frequency(C_T_reached)
    return C_T_reached

# Hàm tìm tập các itemset phổ biến
def apriori(D, I, minsup):
    F = [find_freq_1_itemsets(D, I, minsup)]
    for k in range(1, 1000):
        print('F_%d:' % (k), F[k-1])
        C_k = apriori_gen(F[k-1])
        print('C_%d:' % (k+1), C_k)
        if len(C_k) == 0:
            break
        C_T_reached = get_freq(D, C_k)
        F_k = []
        for i in range(0, len(C_T_reached[1])):
            if C_T_reached[1][i] >= minsup:
                F_k.append(C_T_reached[0][i])
        F.append(F_k)
    freq_itemsets = []
    for f_k in F:
        for itemset in f_k:
            freq_itemsets.append(itemset)
    return freq_itemsets


def find_maximal_elements_itemset(itemsets):
    max_elements_itemset = itemsets[0]
    for i in range(len(itemsets)):
        if len(itemsets[i]) > len(max_elements_itemset):
            max_elements_itemset = itemsets[i]
    return max_elements_itemset


	# Hàm sinh luật mạnh từ tập phổ biến trả về bởi hàm apriori
def gen_freq_strong_rules(F, minconf):
    R = []
    for f in F:
        # print('\nf:', f)
        if isinstance(f, str) == False:
            X = sub_lists(f, -1)
            # print('\nX:', X)
            while len(X) > 0:
                Y = find_maximal_elements_itemset(X)
                # print('\nY:', Y)
                X.remove(Y)
                # print('\nX con lai:', X)
                rest_F = [i for i in f if i not in Y]
                ts = get_freq(D, [[*Y, *rest_F]])
                ms = get_freq(D, [Y])
                if ts[1][0] / ms[1][0] > minconf:
                    R.append({"vt": Y, "vp": rest_F})
                else:
                    childs_Y = sub_lists(Y, -1)
                    for child in childs_Y:
                        if child in X:
                            X.remove(child)
    return R


# Kiểm tra kết quả và thuật toán
freq_itemsets = apriori(D, I, 3)
print('\nF:', freq_itemsets)

strong_rules = gen_freq_strong_rules(freq_itemsets, 0.8)
print('\nrules:')
for rule in strong_rules:
    print(rule)
