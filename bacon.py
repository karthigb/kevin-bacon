def start():
    
    try:
        pickled = open("bacon.data", "r")
        actor_dict, movie_dict, connections_dict, names_dict = cPickle.load(pickled)
        
    except IOError:
        mdb = open("large_actor_data.txt", "r")
        actor_dict = parse_actor_data(mdb)
        movie_dict = invert_actor_dict(actor_dict)
        connections_dict = {}
        names_dict = lower_actor_name(actor_dict)
    
    largest = 0
    while 1:
        
        actor_name = raw_input("Please enter an actor (or blank to exit): ").strip().lower()
        
        if actor_name == "":
                print "Thank you for playing! The largest Bacon Number you found was:",+ largest
                f = open("bacon.data","w")
                cPickle.dump((actor_dict,movie_dict,connections_dict,names_dict),f)                
                f.close()
                break            
        
        connection = find_connection(actor_name, actor_dict, movie_dict, connections_dict,)
        
        if connection == []:
            if actor_name == "kevin bacon":
                print "Kevin Bacon has a Bacon Number of 0."
            elif actor_name in names_dict:
                print names_dict[actor_name] + " has a Bacon Number of Infinity"
            else:
                print actor_name.title() + " has a Bacon Number of Infinity."
        
        else:
            show_connections(connection)
            for tup in connection:
                connections_dict[tup[0]] = connection[connection.index(tup):]
                   
            bacon_number = len(connections_dict[(connection[0][0])][1:])
            if bacon_number > largest:
                largest = bacon_number
                
def find_connection(actor_name, actor_dict, movie_dict, connections_dict):
    '''Return a list of (movie, actor) tuples (both elements of type string)
    that represent a shortest connection between actor_name and Kevin Bacon
    that can be found in the actor_dict and movie_dict.
    '''
    
    try:
        pickled = open("names_dict.data", "r")
        names_dict = cPickle.load(pickled)
        
    except IOError:
        names_dict = lower_actor_name(actor_dict)
        f = open("names_dict.data","w")
        cPickle.dump(names_dict,f)                
        f.close()
    
    if actor_name.lower() not in names_dict or actor_name == "":#included in case find_connections is being imported
        return []
    
    actor_name = names_dict[actor_name.lower()]
    
    if actor_name in connections_dict:
        return connections_dict[actor_name]
    
    investigated = []
    not_investigated = [actor_name]
    distance_d = {}
    distance_d[actor_name] = [(actor_name,actor_dict[actor_name][0])]
    shortcut = []
    
    while len(not_investigated) > 0:
                
        movie_list = actor_dict[not_investigated[0]]
        investigated.append(not_investigated[0])
        not_investigated.pop(0)
        
        if shortcut != [] and len(shortcut) == len(distance_d[investigated[-1]])+1:
            return shortcut
        
        for movie in movie_list:
            for co_star in movie_dict[movie]:
                if co_star not in distance_d:
                    if co_star == "Kevin Bacon":
                        tup = (co_star,movie)
                        current_path = distance_d[investigated[-1]][:]
                        current_path.append(tup)
                        distance_d[co_star] = current_path
                        return distance_d[co_star]
                    
                    tup = (co_star,movie)
                    not_investigated.append(co_star)
                    current_path = distance_d[investigated[-1]][:]
                    
                    current_path.append(tup)
                    distance_d[co_star] = current_path
                    
                    if co_star in connections_dict:
                        shortcut = current_path[:]
                        for item in connections_dict[co_star][1:]:
                            shortcut.append(item)
                    
    return []
                    
def parse_actor_data(actor_data):
    '''Return the actor information in the open reader actor_data as a dictionary. actor_data contains movie and actor information in IMDB's format. The returned dictionary contains the names of actors (string) as keys and lists of movies (string) the actor has been in as values.'''
    
    actor_info = {}
    
    while "THE ACTORS LIST" not in actor_data.readline():
        continue
      
    for num in range(4):
        actor_data.readline()
        
    line = actor_data.readline()   
    while "--------" not in line:
        
        if (")") not in line:
            pass
        
        elif line[0] != "\t" and line[0] != "\n":
            name = process_name(line[:line.find("\t")].strip())
            title = process_title(line)
            
            if name not in actor_info:
                actor_info[name] = [title]
            else:
                if title not in actor_info[name]:
                    actor_info[name].append(title)
                    
        else: #line contains new movie for an actor already dictionary
            title = process_title(line)
            
            if title not in actor_info[name]:
                actor_info[name].append(title)     

        line = actor_data.readline()
    
    return actor_info

def invert_actor_dict(actor_dict):
    '''Return a dictionary that is the inverse of actor_dict.
    actor_dict maps actors (string) to lists of movies (string) in which they have appeared.
    The returned dictionary maps movies (string) to lists of actors appearing in the movie.
    '''
    inverted = {}
    for key in actor_dict:
        for mov in actor_dict[key]:
            inverted.setdefault(mov, []).append(key)
    
    return inverted

def show_connections(tup_list):
    print tup_list[0][0] + " has a Bacon Number of", + len(tup_list[1:]),"."
    i = 0
    while i < len(tup_list[1:]):
        print "%s was in %s with %s." % (tup_list[i][0], tup_list[i+1][1], tup_list[i+1][0])
        i+=1

def lower_actor_name(actor_dict):
    new_dict = {'':''}
    for key in actor_dict:
        new_dict[key.lower()] = key
    return new_dict        

def process_name(s):
    """Return a str with the reformatted name in str s."""

    step1 = s.split(",")
    if len(step1) == 2: 
        step2 = step1[1][1:] + " " + step1[0]
    else:
        step2 = step1[0]
    if "(" in step2:
        step3 = step2[: step2.find("(") - 1] + step2[step2.find(")") + 1:]
        return step3
    
    return step2

def find_end(line):
    x = line.find("(")
    if not line[x+1:x+5].isdigit():
        x = (line[x+1:].find("(")) + x + 1
    return line[x:].find(")")+x

def process_title(line):
    
    title = line[line.find("\t"):find_end(line)].strip() + ")"
    if title[0] == '"':
        title = title[1:title[1:].find('"')+1] + " " + title[title.find("("):title.find(")")+1]
    
    return title

import cPickle                    
if __name__ == "__main__":
    import doctest
    doctest.testfile("test_find_connections.txt", False)
