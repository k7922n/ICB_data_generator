import jieba

template_file = open("./data/template.txt", 'r')
movie_name_file = open("./data/movie_name.txt", 'r')
theater_name_file = open("./data/theater_name.txt", 'r')
time_file = open("./data/time.txt", 'r')

#load dict
jieba.load_userdict("data/movie_name.txt")
jieba.load_userdict("data/time.txt")
jieba.load_userdict("data/theater_name.txt")

output_file = open("./data/training_data.txt", 'w')
target_file = open("./data/target.txt", 'w')

movie_slot = "[movie name]"
theater_slot = "[theater name]"
time_slot = "[time]"

# Generate lists
templates = []
for line in template_file:
    templates.append(line.rstrip('\n'))

movie_names = []
for line in movie_name_file:
    movie_names.append(line.rstrip('\n'))

theater_names = []
for line in theater_name_file:
    theater_names.append(line.rstrip('\n'))

times = []
for line in time_file:
    times.append(line.rstrip('\n'))

# Generate training data
for movie_name in movie_names:
    for theater_name in theater_names:
        for time in times:
            for template in templates:
                sentence = template.replace(movie_slot, movie_name)
                sentence = sentence.replace(theater_slot, theater_name)
                sentence = sentence.replace(time_slot, time)
                seq_list = list(jieba.cut(sentence))
                index_m = seq_list.index(movie_name) if movie_name in seq_list else -1
                index_h = seq_list.index(theater_name) if theater_name in seq_list else -1
                index_t = seq_list.index(time) if time in seq_list else -1
                output_file.write(" ".join(seq_list) + '\n')
                temp = ["O"] * len(seq_list)
                if index_m != -1: temp[index_m] = movie_slot
                if index_h != -1: temp[index_h] = theater_slot
                if index_t != -1: temp[index_t] = time_slot
                #print(sentence)
                #print(seq_list)
                #print(index_m, index_h, index_t)
                #print(temp)
                target_file.write(" ".join(temp) + '\n')
