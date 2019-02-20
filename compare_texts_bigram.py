import nltk
import numpy as np
nltk.download('punkt')
nltk.download('stopwords')
import matplotlib.pyplot as plt
import scipy.misc
import scipy.ndimage
import scipy.signal
PLOTTING = True


#######################
# Config
#######################

EPSILON = 10**(-10)

#######################
# Create Word Distance Matrix
#######################

def clean_text(text):
    text = text.replace('\n', ' ').replace('\r', '').replace('\t', ' ')
    for _ in range(30):
        text = text.replace('  ',' ')
    text = text.replace(' . ','. ')
    text = text.replace(' , ', ', ')
    return text

def clean_word(word):
    from nltk.tokenize import word_tokenize
    tokens = word_tokenize(word)
    tokens = [w.lower() for w in tokens]
    import string
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    stripped = sorted(stripped, key=lambda x: -len(x))
    return stripped[0]


def word_similarity(w1, w2):
    if w1 == w2:
        return 1.0 - EPSILON
    return EPSILON
    w1 = clean_word(w1)
    w2 = clean_word(w2)
    if w1 == w2:
        return 1.0
    return EPSILON

def compute_similarity_matrix(text1, text2):
    distance_matrix = np.zeros([len(text1), len(text2)])
    for i, w1 in enumerate(text1):
        for j, w2 in enumerate(text2):
            distance_matrix[i, j] = word_similarity(w1, w2)
    return distance_matrix


#######################
# Analyze Matrix
#######################

def plot_matrix(matrix):
    if not PLOTTING:
        return
    plt.clf()
    plt.imshow(matrix, cmap="YlGnBu", interpolation='none')
    plt.colorbar()
    plt.show()


def analyze_matrix(matrix):
    counter = 0
    score_new = 0.0
    index_list = [-4,-3,-2,-1,0,1,2,3, 4]
    max_value = len(index_list)
    matrix_plag = matrix.copy()
    matrix_plag.fill(0.0)

    for (i,j), x in np.ndenumerate(matrix):
        try:
            c = 0
            for shift in index_list:
                try:
                    c += matrix[i+shift, j+shift]
                except:
                    pass
            if c >= 2.9 and matrix[i,j] > 0.5:
                counter += 1
                matrix_plag[i,j] = c
                score_new += (c/max_value)**(0.3)
        except:
            pass

    return score_new, matrix_plag


#######################
# Post Processing
#######################


def color_text(text1, text2, matrix):
    text1 = clean_text(text1)
    text2 = clean_text(text2)
    text1 = text1.split()
    text2 = text2.split()
    colmax = matrix.max(axis=0).flatten()
    rowmax = matrix.max(axis=1).flatten()
    colmax = colmax.flatten().tolist()[0]
    rowmax = rowmax.flatten().tolist()[0]

    for i, w1 in enumerate(text1):
        if rowmax[i] > 5.9:
            text1[i] = '<span style="color:red;"> {} </span>'.format(text1[i])
        elif rowmax[i] > 4.9:
            text1[i] = '<span style="color:orange;"> {} </span>'.format(text1[i])
        elif rowmax[i] > 0.9:
            text1[i] = '<span style="color:red;"> {} </span>'.format(text1[i])

    for i, w1 in enumerate(text2):
        if colmax[i] > 5.9:
            text2[i] = '<span style="color:red;"> {} </span>'.format(text2[i])
        elif colmax[i] > 4.8:
            text2[i] = '<span style="color:orange;"> {} </span>'.format(text2[i])
        elif colmax[i] > 0.8:
            text2[i] = '<span style="color:red;"> {} </span>'.format(text2[i])

    return text1, text2





#######################
# Main
#######################

def analyze(text1, text2):
    text1 = clean_text(text1)
    text2 = clean_text(text2)
    text1 = text1.split()
    text2 = text2.split()

    matrix = compute_similarity_matrix(text1, text2)
    plot_matrix(matrix)
    simmilarity_matrix = matrix.copy()

    score_new, matrix = analyze_matrix(matrix)
    plot_matrix(matrix)

    #path image
    import PIL
    from PIL import Image
    img = Image.fromarray(matrix)
    width, height = img.size
    img = img.resize((int(width/30), int(height/30)), PIL.Image.ANTIALIAS)
    img = np.matrix(img)
    plot_matrix(img)

    img[img<0.04] = 0
    img[img >= 0.04] = 1.0
    plot_matrix(img)
    img = Image.fromarray(img)
    img = img.resize((width, height), PIL.Image.NEAREST)
    img = np.matrix(img)
    plot_matrix(img)
    #plot_matrix(img)



    matrix = np.multiply(simmilarity_matrix, img)

    plot_matrix(matrix)

    score_new = matrix[matrix > 0.5].sum()

    print('score: ', score_new)
    return matrix, score_new


def main(text1, text2, plot=True):
    if len(text1) < 3 or len(text2) < 3:
        return text1, text2, 0
    global PLOTTING
    PLOTTING = plot
    matrix, score = analyze(text1, text2)
    t1, t2 = color_text(text1, text2, matrix)
    return ' '.join(t1), ' '.join(t2), score

def start_main(text1path, text2path, plot=True):
    global PLOTTING
    PLOTTING=plot
    print('start analysis')
    text1 = open(text1path).read()
    text2 = open(text2path).read()
    t1, t2, score = main(text1, text2, plot)
    return score


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-text1',  help="text1", default='examples/text1.txt')
    parser.add_argument('-text2', help="text2", default='examples/text2.txt')
    args = parser.parse_args()
    start_main(args.text1, args.text2)
