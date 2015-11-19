import search 
from pprint import pprint


default_best_ordering = {'models': 4, 'makes':3, 'engines':2, 'transmissions':1, 'types':0}




def uphold_ratio_threshold(d, ratio) : 
	d = {k : v for k, v in d.items() if len(v) > 1}
	n_d = dict()

	for k, v in d.items() :
		for i in  v: 
			if isinstance(i, dict) : 
				if i['ratio'] >= ratio : 
					if k not in n_d :
						n_d[k] = list()
					if i['row'] not in n_d[k] : 
						n_d[k].append(i['row']['id'])
	return n_d if len(n_d) > 0 else None

def get_best_ordering(d) : 
	ordering_list = list()
	max_len = 1
	for k, v in d.items() : 
		ordering_list.append((k, len(v)))
		if len(v) > max_len : 
			max_len = len(v)
	ordering_list = sorted(ordering_list, 
		key=lambda x: x[1] if x[1] > default_best_ordering[x[0]] 
		else default_best_ordering[x[0]], reverse=True)
	return [x[0] for x in ordering_list]


def optimized_search(query) : 
	q = search.query(query)
	ratio = 50
	q_ratio_threshold = uphold_ratio_threshold(q, ratio)
	while q_ratio_threshold is None and ratio > 0 :
		ratio -= 10
		q_ratio_threshold = uphold_ratio_threshold(q, ratio)
	q_best_ordering = get_best_ordering(q_ratio_threshold)
	return q_best_ordering, q_ratio_threshold


if __name__ == "__main__" : 
	pprint(optimized_search('Corvette or GMC'))



