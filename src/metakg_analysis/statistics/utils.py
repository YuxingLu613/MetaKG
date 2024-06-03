import matplotlib.pyplot as plt

def draw_statistics(counter, name, topk=20):
        """Draws a bar chart to visualize the top-k most frequent items in a counter.

        Args:
            counter (collections.Counter): The counter object containing the frequency count of items.
            name (str): The title of the plot.
            topk (int): The number of top-k items to plot. Default is 20.

        Returns:
            None.

        """
        counter_sorted = sorted(counter.items(), key=lambda x: x[1], reverse=True)[:topk]
        keys = [k[:20] for k, v in counter_sorted]
        values = [v for k, v in counter_sorted]

        # Plot the bar chart
        plt.title(name)
        plt.xticks(rotation=45)
        plt.bar(keys, values)
        plt.show()
