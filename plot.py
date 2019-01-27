import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class Data(object):

    plot_annot = False

    dataframe = None

    def plot(self, src):
        self._load_data(src)
        self._process_data()
        self._plot_data()

    def _load_data(self, src):

        colnames = ['X', 'Y', 'MINUS', 'PLUS']
        self.dataframe = pd.read_csv(src, sep='\t', lineterminator='\n', names=colnames, header=0)

    def _process_data(self):

        dataframe = self.dataframe

        dataframe['average'] = (dataframe['PLUS'] + -dataframe['MINUS']) / 2

        mean = dataframe["average"].mean()

        dataframe['de_meaned'] = dataframe["average"] - mean

        dataframe['normalised'] = 2 * ( (dataframe['de_meaned']-dataframe['de_meaned'].min())/(dataframe['de_meaned'].max()-dataframe['de_meaned'].min())) - 1 # (df-df.min())/(df.max()-df.min())

    def _clean_data(self):
        dataframe = self.dataframe

        dataframe.drop(columns=['MINUS', 'PLUS', 'average', 'de_meaned'], inplace=True)

        data = dataframe.pivot_table('normalised', index='Y', columns='X' )

        return data

    def _plot_data(self):

        d = self._clean_data().T

        # plot heatmap
        ax = sns.heatmap(d, cmap="Greys", annot=self.plot_annot, annot_kws={"size": 7})

        # turn the axis label
        for item in ax.get_yticklabels():
            item.set_rotation(0)

        # for item in ax.get_xticklabels():
        #     item.set_rotation(90)

        # save figure
        plt.savefig('out/map.png', dpi=100)
        plt.show()


d = Data()

d.plot('data/example_data.tsv')
