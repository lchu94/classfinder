import math
from django.core.cache import cache
from django.db.models import Q
from models import CompleteEnrollmentData, SharedClassesByMajor, SubjectInfo
from gensim.models import Word2Vec



"""
Use network flow to determine unsatisfied requirements of a given major
"""
def get_new_classes(major, student_classes):
    import json
    from sets import Set
    import networkx as nx
    from networkx.algorithms.flow import edmonds_karp, build_residual_network

    # Read requirements from file
    return ["6.022", "6.023", "6.025", "6.035", "6.036", "6.045", "6.047", "6.049", "6.061", "6.101", "6.111", "6.115", "6.131", "6.141", "6.170", "6.172", "6.207", "6.301", "6.302", "6.502", "6.503", "6.602", "6.701", "6.717", "6.801", "6.802", "6.803", "6.804", "6.805", "6.806", "6.813", "6.814", "6.815", "6.816", "6.819", "6.835", "6.837", "6.857", "6.905", "16.36", "21M.359", "6.241", "6.251", "6.255", "6.262", "6.267", "6.334", "6.336", "6.341", "6.344", "6.345", "6.374", "6.375", "6.376", "6.436", "6.437", "6.438", "6.450", "6.453", "6.521", "6.522", "6.551", "6.555", "6.561", "6.631", "6.632", "6.634", "6.641", "6.685", "6.720", "6.728", "6.730", "6.774", "6.775", "6.777", "6.820", "6.823", "6.824", "6.828", "6.829", "6.830", "6.831", "6.832", "6.839", "6.840", "6.845", "6.850", "6.852", "6.854", "6.856", "6.857", "6.858", "6.863", "6.864", "6.866", "6.867", "6.869", "6.874", "6.875"]


"""
Create hash table that maps each class to the total number of students enrolled in that class
"""
def create_totals_table(all_classes, shared_classes_table):
    totals = {}
    count = 0
    for row in shared_classes_table:
        row_num = [int(x) for x in row]
        totals[all_classes[count]] = sum(row_num)
        count += 1
    print totals
    return totals


"""
TODO
"""
def create_shared_classes_table(major, class_table, all_classes):
    num_classes = len(all_classes)
    student_class_dict = {}
    pairs = CompleteEnrollmentData.objects.filter(Q(major1=major) | Q(major2=major)).values_list("identifier","subject")
    
    for identifier, cls in pairs:
        if identifier not in student_class_dict and cls in all_classes:
            student_class_dict[identifier] = [cls]
        elif cls in all_classes:
            student_class_dict[identifier].append(cls)


    matrix = [[0 for x in xrange(num_classes)] for y in xrange(num_classes)]
    for student, classes in student_class_dict.iteritems():
        index = 0
        while index < len(classes):
            sc1 = classes[index]
            sc1_pos = class_table[sc1]
            for sc2 in classes:
                matrix[sc1_pos][class_table[sc2]] += 1
            index += 1

    return matrix



"""
Driver function to generate recommendations
"""
def generate_recommendations(major, cur_semester, student_classes, keywords, term_relevance = False):
    student_classes_list = student_classes.split()
    # new_classes = [x for x in classes if x not in student_classes_list]
    new_classes = get_new_classes(major, student_classes_list)
    all_classes = student_classes_list + new_classes
    class_table = {k:v for k, v in zip(all_classes, xrange(len(all_classes)))}

    try:
        # NOTE: cached result must be changed when the student changes majors
        shared_classes_table = cache.get('shared_classes_table')
        if shared_classes_table == None:
            # shared_classes_table = SharedClassesByMajor.objects.filter(major=maj).values_list("matrix", flat=True)[0]
            shared_classes_table = create_shared_classes_table(major, class_table, all_classes)
            cache.add('shared_classes_table', shared_classes_table, 300)    # store in cache
            print "Added table"
    except:
        print "Error loading shared_classes_table"

    cur_term = "term%s" % cur_semester
    totals = create_totals_table(all_classes, shared_classes_table)
    term_data = get_term_relevance_data(cur_term)       # SHOULD BE CACHED

    importance_ratings = generate_recommendations_by_importance(new_classes, student_classes_list, shared_classes_table, class_table, totals, keywords, term_data, term_relevance = False)
    sorted_importance_ratings = sorted(importance_ratings, key=importance_ratings.get, reverse=True)
    return sorted_importance_ratings


"""
Generate recommendations for a given student using the "importance" method.
Recommendations are for the current semester and are based upon all classes taken by the student.

TODO: error handling for invalid class?
TODO: some classes renamed (i.e. 18.440 to 18.600)
"""
def generate_recommendations_by_importance(new_classes, student_classes_list, shared_classes_table, class_table, totals, keywords, term_data, term_relevance = False):
    # Calculate "importance" of each class that hasn't been taken by the student
    importance_ratings = {}

    for cl in new_classes:
        total = 1
        for s in student_classes_list:
            total_number_class = totals[s]
            if total_number_class == 0:
                break

            try:
                shared_number = int(shared_classes_table[class_table[cl]][class_table[s]])
                total *= math.exp(0.5 * shared_number / total_number_class)
            except:
                print (cl, s)


            # Term relevance
            if term_relevance:
                try:
                    tr_multiplier = term_data[cl]
                    total *= tr_multiplier
                except:
                    continue


            # Keyword match
            if len(keywords) > 0:
                try:
                    class_keywords = SubjectInfo.objects.filter(subject=cl).values_list("keywords", flat=True)[0]
                except:
                    continue

                if len(class_keywords) > 0:
                    sim_rating = w2v_model.n_similarity(class_keywords, keywords.split())
                    total *= sim_rating
                else:
                    total *= .1


        importance_ratings[cl] = total       # record total for this class

    return importance_ratings



"""
Generate recommendations for a given student using the "similarity/Amazon" method.
Recommendations are for the current semester and are based upon all classes taken by the student.
"""
def generate_recommendations_by_similarity(new_classes, class_table, student_classes_list, totals, shared_classes_table):
    from scipy import spatial

    MAJOR_TRIM = '6.'
    relevant_classes = [str(x) for x in classes if (str(x).startswith(MAJOR_TRIM) or str(x) in student_classes_list)]
    num_rel_classes = len(relevant_classes)

    # Create nxn similarity table
    similarity_table = [[0 for x in xrange(num_rel_classes)] for y in xrange(num_rel_classes)]

    # Populate similarity_table with the similarity rating between each pair of classes
    for cls in relevant_classes:
        cls_pos = class_table[cls]
        for c in relevant_classes:
            # compute similarity between cls and c
            cls_list = shared_classes_table[cls_pos]
            c_list = shared_classes_table[class_table[c]]
            
            if sum(cls_list) == 0 or sum(c_list) == 0:
                similarity = 0
            else:
                similarity = spatial.distance.cosine(cls_list, c_list)  # CONSIDER PEARSON INSTEAD!

            similarity_table[cls_pos][class_table[c]] = similarity

    # Populate a dictionary mapping each class to its rating
    ratings = {}
    for cls in relevant_classes:
        ratings[cls] = 0

    for cls in student_classes_list:
        cls_pos = class_table[cls]
        row = similarity_table[cls_pos]

        i = 0
        for c in relevant_classes:
            ratings[c] += similarity_table[cls_pos][i]
            i += 1

    sorted_ratings = sorted(ratings, key=ratings.get, reverse=True)
    for i in sorted_ratings[0:20]:
        print ratings[i]
    return sorted_ratings


"""
Determine the likelihood of a class being taken given the current term.
"""
def get_term_relevance_data(cur_term):
    try:
        subject_info = SubjectInfo.objects.values("subject", cur_term, "total")     # maybe also "title"?
    except:
        print "Error"   # need better error handling

    term_data = {}
    for sub in subject_info:
        cur_term_count = sub[cur_term] + 1
        total_count = sub["total"] + 16
        time_modifier = float(cur_term_count) / total_count
        term_data[sub["subject"]] = time_modifier
        
    return term_data


"""
Find classes that are most similar to the given keywords
"""
def keyword_similarity(keywords):
    sim_ratings = {}
    for cl in classes:
        try:
            class_keywords = SubjectInfo.objects.filter(subject=cl).values_list("keywords", flat=True)[0]
        except:
            continue

        if len(class_keywords) == 0:
            sim_ratings[cl] = 0

        else:
            sim_rating = w2v_model.n_similarity(class_keywords, keywords.split())
            sim_ratings[cl] = sim_rating

    # sort and return
    sorted_sim_ratings = sorted(sim_ratings, key=sim_ratings.get, reverse=True)
    return sorted_sim_ratings


"""
The following is executed upon import
"""
# Get list of all classes
try:
    classes = CompleteEnrollmentData.objects.order_by().values_list("subject", flat=True).distinct()
except:
    print "Error loading classes"


# # Load Word2Vec model for keyword matching
# try:
#     w2v_model = cache.get('word2vec_model')
#     if w2v_model == None:
#         w2v_model = Word2Vec.load_word2vec_format('/Users/lambertchu/Documents/MIT/SuperUROP/NLP_Data/GoogleNews-vectors-negative300.bin', binary=True)
#         #cache.add('word2vec_model', w2v_model, 600)    # store in cache
# except:
#     print "Error loading Word2Vec model"