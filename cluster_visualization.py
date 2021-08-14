from sklearn.decomposition import PCA
import time
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import itertools

def hi():
    print("hi")
def run_PCA(features_list=None, n_components=None):
    time_start = time.time()
    pca = PCA(n_components=n_components)
    results = pca.fit_transform(features_list)
    # print('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_))
    print('Total explained variation: {}'.format(sum(pca.explained_variance_ratio_)))
    print(results.shape)
    print('PCA done in {} seconds'.format(time.time() - time_start))
    return results


def run_TSNE(features_list=None, n_components=None):
    time_start = time.time()
    tsne = TSNE(n_components=n_components, verbose=1, perplexity=40, n_iter=300)
    results = tsne.fit_transform(features_list)
    print('t-SNE done in {} seconds'.format(time.time() - time_start))
    return results


def visualize_2D(df=None, results=None, palette=None, avgpal=None, save=None, avg=None):
    plt.figure(figsize=(16, 10))

    sns.scatterplot(
        x=results[:, 0], y=results[:, 1],
        hue="labels",
        palette=palette,
        data=df,
        legend="full",
        alpha=1
    )
    sns.scatterplot(
        x=avg[:, 0], y=avg[:, 1],
        c=avgpal,
        alpha=1,
        marker="X"
    )
    if save == True:
        print("save not implemented yet")


def colors(fl=None, ml=None, label_names=None, n_split=None):
    colorset = []
    for label in label_names:
        if label[0] == "h":
            colorset.append("green")
        if label[0] == "i":
            colorset.append("red")
        if label[0] == "o":
            colorset.append("blue")

    if fl == "all":
        flcolors = colorset
    elif isinstance(fl, str):
        flcolors = [fl] * len(label_names)
        if fl in label_names:
            flcolors = []
            for label in label_names:
                if label == fl:
                    flcolors.append("gray")
                else:
                    flcolors.append("white")

    if ml == "all":
        mlcolors = colorset
    elif isinstance(ml, str):
        mlcolors = [ml] * len(label_names)
        if fl in label_names:
            mlcolors = []
            for label in label_names:
                if label == fl:
                    mlcolors.append("gray")
                else:
                    mlcolors.append("white")

    repeated_mlcolors = list(
        itertools.chain.from_iterable(itertools.repeat(mlcolors[i], n_split[i]) for i in range(len(mlcolors))))
    return flcolors, repeated_mlcolors


def visualize_3D(results=None, labels=None, save=None):
    colors = []
    for i in labels["labels"]:
        if i[0] == "h":
            colors.append("green")
        if i[0] == "i":
            colors.append("red")
        if i[0] == "o":
            colors.append("blue")
        if i[0] == "P":
            colors.append("green")
        if i[0] == "U":
            colors.append("red")

    ax = plt.figure(figsize=(16, 10)).gca(projection='3d')
    ax.scatter(
        xs=results[:, 0], ys=results[:, 1], zs=results[:, 2],
        c=colors
    )
    ax.set_xlabel('dim-one')
    ax.set_ylabel('dim-two')
    ax.set_zlabel('dim-three')
    plt.show()
    if save == True:
        print("save not implemented yet")