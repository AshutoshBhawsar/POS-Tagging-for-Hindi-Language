
import codecs
import os
import sys
import time

tags = ['NN', 'NST', 'NNP', 'PRP', 'DEM', 'VM', 'VAUX', 'JJ', 'RB', 'PSP', 'RP', 'CC', 'WQ', 'QF', 'QC', 'QO', 'CL', 'INTF', 'INJ', 'NEG', 'UT', 'SYM', 'COMP', 'RDP', 'ECH', 'UNK', 'XC']

#--------------------------FUNCTIONS------------------------------------

# max_connect() performs the viterbi decoding. Choosing which tag for the current word leads to a better tag sequence.
def max_connect(x, y, viterbi_matrix, emission, transmission_matrix):
	max = -99999
	path = -1

	for k in range(len(tags)):
		val = viterbi_matrix[k][x-1] * transmission_matrix[k][y]
		if val * emission > max:
			max = val
			path = k
	return max, path

# 1. Extract Unique words from training data
# 2. Count of occurence of each tag
# 3. Find Emission & Transmission matrix
# 4. Test it on some data
# 5. For this we need to decode hindi text using viterbi decoding

emission_matrix = []
transmission_matrix = []
languages = ["hindi"]
exclude = ["<s>", "</s>", "START", "END"]
wordtypes = []
tagscount = []

def main():

#-----------------TRAINING-----------------------

	start_time = time.time()

	# Path of training files
	filepath = ["./data/hindi_training.txt"]
	languages = ["hindi"]
	exclude = ["<s>", "</s>", "START", "END"]
	wordtypes = []
	tagscount = []

	# Open training file to read the contents
	f = codecs.open(filepath[0], 'r', encoding='utf-8')
	file_contents = f.readlines()

	# Initialise count of each tag to Zero's
	for x in range(len(tags)):
		tagscount.append(0)

	# Calculate count of each tag in the training corpus and also the wordtypes in the corpus
	for x in range(len(file_contents)):
		line = file_contents.pop(0).strip().split(' ')
		for i, word in enumerate(line):
			if i == 0:
				if word not in wordtypes and word not in exclude:
					wordtypes.append(word)
			else:
				if word in tags and word not in exclude:
					tagscount[tags.index(word)] += 1
	f.close()

	# Declare variables for emission and transmission matrix
	emission_matrix = []
	transmission_matrix = []

	# Initialize emission matrix
	for x in range(len(tags)):
		emission_matrix.append([])
		for y in range(len(wordtypes)):
			emission_matrix[x].append(0)

	# Initialize transmission matrix
	for x in range(len(tags)):
		transmission_matrix.append([])
		for y in range(len(tags)):
			transmission_matrix[x].append(0)

	# Open training file to update emission and transmission matrix
	f = codecs.open(filepath[0], 'r', encoding='utf-8')
	file_contents = f.readlines()

	# Update emission and transmission matrix with appropriate counts
	row_id = -1
	for x in range(len(file_contents)):
		line = file_contents.pop(0).strip().split(' ')

		if line[0] not in exclude:
			col_id = wordtypes.index(line[0])
			prev_row_id = row_id
			row_id = tags.index(line[1])
			emission_matrix[row_id][col_id] += 1
			if prev_row_id != -1:
				transmission_matrix[prev_row_id][row_id] += 1
		else:
			row_id = -1

	# Divide each entry in emission matrix by appropriate tag count to store probabilities in each entry instead of just count
	for x in range(len(tags)):
		for y in range(len(wordtypes)):
			if tagscount[x] != 0:
				emission_matrix[x][y] = float(emission_matrix[x][y]) / tagscount[x]

	# Divide each entry in transmission matrix by appropriate tag count to store probabilities in each entry instead of just count
	for x in range(len(tags)):
		for y in range(len(tags)):
			if tagscount[x] != 0:
				transmission_matrix[x][y] = float(transmission_matrix[x][y]) / tagscount[x]

	print (time.time() - start_time, "seconds to learn POS tags")

#-----------------TESTING-----------------------

def test():

	start_time = time.time()

	# Open the testing file to read test sentences
	testpath = "./data/hindi_testing.txt"
	file_test = codecs.open(testpath, 'r', encoding='utf-8')
	test_input = file_test.readlines()

	# Declare variables for test words and pos tags
	test_words = []
	pos_tags = []

	# Create an output file to write the output tags for each sentences
	file_output = codecs.open("./output/"+ languages[0] +"_tags.txt", 'w', 'utf-8')
	file_output.close()

	# For each line POS tags are computed
	for j in range(len(test_input)):

		test_words = []
		pos_tags = []

		line = test_input.pop(0).strip().split(' ')

		for word in line:
			test_words.append(word)
			pos_tags.append(-1)

		viterbi_matrix = []
		viterbi_path = []

		# Initialize viterbi matrix of size |tags| * |no of words in test sentence|
		for x in range(len(tags)):
			viterbi_matrix.append([])
			viterbi_path.append([])
			for y in range(len(test_words)):
				viterbi_matrix[x].append(0)
				viterbi_path[x].append(0)

		# Update viterbi matrix column wise
		for x in range(len(test_words)):
			for y in range(len(tags)):
				if test_words[x] in wordtypes:
					word_index = wordtypes.index(test_words[x])
					tag_index = tags.index(tags[y])
					emission = emission_matrix[tag_index][word_index]
				else:
					emission = 0.001

				if x > 0:
					max, viterbi_path[y][x] = max_connect(x, y, viterbi_matrix, emission, transmission_matrix)
				else:
					max = 1
				viterbi_matrix[y][x] = emission * max

		# Identify the max probability in last column i.e. best tag for last word in test sentence
		maxval = -999999
		maxs = -1
		for x in range(len(tags)):
			if viterbi_matrix[x][len(test_words)-1] > maxval:
				maxval = viterbi_matrix[x][len(test_words)-1]
				maxs = x

		# Backtrack and identify best tags for each words
		for x in range(len(test_words)-1, -1, -1):
			pos_tags[x] = maxs
			maxs = viterbi_path[maxs][x]

		# Display POS Tags in the console.
		# print pos_tags

		# Print output to the file.
		file_output = codecs.open("./output/"+ languages[0] +"_tags.txt", 'a', 'utf-8')
		for i, x in enumerate(pos_tags):
			file_output.write(test_words[i] + "_" + tags[x] + " ")
		file_output.write("\n")

	f.close()
	file_output.close()
	file_test.close()

#------------START------------------

main()
