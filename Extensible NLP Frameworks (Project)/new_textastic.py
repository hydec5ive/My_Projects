"""
File: GovSnatch.py

Description: A reusable, extensible framework
for comparitive text analysis designed to work
with any arbitrary collection of related documents.

"""


from collections import Counter, defaultdict
import re 
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import textblob as tb


class GovSnatch:

    def __init__(self):
        """ Contructor """
        self.data = defaultdict(dict)
        self.stop_words = set()

    def load_stop_words(self, stopfile):
        '''Registers words in a provided stopfiles to ignore for future use'''
        with open(stopfile, 'r') as f:
            self.stop_words = set(word.strip().lower() for word in f.readlines())

    def simple_text_parser(self, filename):
        """ For processing simple, unformatted text documents """

        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()

        words = re.findall(r'\b\w+\b', text.lower())
        filtered_words = [word for word in words if word not in self.stop_words]
        wordcount = Counter(filtered_words)
        numwords = len(filtered_words)

        blob = tb.TextBlob(text)
        sentences = blob.sentences
        polarity = [sentence.sentiment.polarity for sentence in sentences]
        subjectivity = [sentence.sentiment.subjectivity for sentence in sentences]
        avg_polarity = sum(polarity) / len(polarity)
        avg_subjectivity = sum(subjectivity) / len(subjectivity)
        avg_sent_len = sum(len(sentence.words) for sentence in sentences) / len(sentences)
        #implement a readability score by looking at the average length of words.

        total_characters = sum(len(word) for word in filtered_words)
        avg_word_len = total_characters / numwords if numwords > 0 else 0

        #track bigrams and trigrams
        bigrams = [(w1, w2) for w1, w2 in zip(words, words[1:]) if w1 not in self.stop_words and w2 not in self.stop_words]
        bigramcount = Counter(bigrams)

        trigrams = [(w1, w2, w3) for w1, w2, w3 in zip(words, words[1:], words[2:]) if w1 not in self.stop_words and w2 not in self.stop_words and w3 not in self.stop_words]
        trigramcount = Counter(trigrams)

        #store in results dictionary
        results = {
            'wordcount': wordcount,
            'numwords': numwords,
            'bigramcount': bigramcount,
            'trigramcount': trigramcount,
            'avg polarity': avg_polarity,
            'avg subjectivity': avg_subjectivity,
            'avg sentence length': avg_sent_len,
            'readability score': avg_word_len
        }

        print("Parsed:", filename, ":", results)
        return results

    def load_text(self, filename, label=None, parser=None):
        """ Register a document with the framework and
        store data extracted from the document to be used
        later in visualizations """

        results = self.simple_text_parser(filename) # default
        if parser is not None:
            results = parser(filename)

        if label is None:
            label = filename

        for k, v in results.items():
            self.data[k][label] = v

    def compare_num_words(self, metric):
        """ A very simplistic visualization that creats a bar
        chart comparing the counted of selected metric in each file.
         """

        dict = self.data[metric]
        # for words, count in dict.items():
        #     if count <= 20:
        #         continue
        #     plt.bar(count, x=words)
        # plt.show()
        print(dict.keys())

    def wordcount_sankey(self, word_list=None, k=5):
        """
        Create a Sankey diagram showing the relationship between text sources and words.
        
        Parameters:
        - word_list: Optional list of specific words to include
        - k: If word_list is None, include the top k words from each document
        
        Returns:
        - Displays a Sankey diagram
        """
        # Get wordcount data
        wordcount_data = self.data['wordcount']
        
        # Get document labels
        doc_labels = list(wordcount_data.keys())
        
        # If no specific words provided, get top k words from each document
        if word_list is None:
            # Get top k words from each document
            all_top_words = set()
            for doc, counter in wordcount_data.items():
                top_words = [word for word, _ in counter.most_common(k)]
                all_top_words.update(top_words)
            word_list = list(all_top_words)
        
        # Create sources, targets, and values for Sankey diagram
        sources = []
        targets = []
        values = []
        
        # Create a mapping of labels to indices
        doc_indices = {doc: i for i, doc in enumerate(doc_labels)}
        word_indices = {word: i + len(doc_labels) for i, word in enumerate(word_list)}
        
        # Create the links
        for doc, counter in wordcount_data.items():
            doc_idx = doc_indices[doc]
            for word in word_list:
                if word in counter and counter[word] > 0:
                    word_idx = word_indices[word]
                    sources.append(doc_idx)
                    targets.append(word_idx)
                    values.append(counter[word])
        
        # Create labels for the nodes
        node_labels = doc_labels + word_list
        
        # Create the Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=node_labels
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values
            )
        )])
        
        # Conservative vs. Liberal color scheme
        conservative_color = 'rgba(178, 34, 34, 0.4)'  # Dark red with opacity
        liberal_color = 'rgba(30, 144, 255, 0.4)'      # Dodger blue with opacity
        gray = 'rgba(128, 128, 128, 0.4)' # Gray for others

        node_colors = []
        # Split doc labels into liberal and conservative
        liberal_docs = [doc for doc in doc_labels if 'liberal' in doc.lower()]
        conservative_docs = [doc for doc in doc_labels if 'conservative' in doc.lower()]

        for label in node_labels:
            if label in doc_labels:
                # Document node
                if label in conservative_docs:
                    node_colors.append(conservative_color)
                elif label in liberal_docs:
                    node_colors.append(liberal_color) 
            else:
                node_colors.append(gray)


        # Assign colors to links based on whether the source document is conservative or liberal
        link_colors = []

        for src in sources:
            doc_label = node_labels[src]
            if doc_label in conservative_docs:
                link_colors.append(conservative_color)
            elif doc_label in liberal_docs:
                link_colors.append(liberal_color)
            else:
                link_colors.append('rgba(160, 160, 160, 0.4)')

        # Add colors to the nodes and links
        fig.data[0].link.color = link_colors
        fig.data[0].node.color = node_colors

        # Update the layout
        fig.update_layout(
            title_text="Text-to-Word Sankey Diagram: Conservative vs. Liberal Language",
            font_size=10,
            height=800
        )
            
        fig.show()   

    def bigram_visualization(self, top_n=8, figsize=(15, 10)):
        """
        Create a grid of subplots, each showing the top N bigrams for a document.

        Parameters:
        - top_n: Number of top bigrams to display per document (default: 8)
        - figsize: Tuple for figure size (width, height)
        """
        # Get bigram data
        bigram_data = self.data['bigramcount']
        doc_labels = list(bigram_data.keys())
        num_docs = len(doc_labels)

        rows = (num_docs + 1) // 2  
        cols = 2

        # Create figure with subplots
        fig, axes = plt.subplots(rows, cols, figsize=figsize, constrained_layout=True)
        axes = axes.flatten()  

        # Colors for conservative (red) and liberal (blue)
        conservative_color = '#B22222'  # Dark red
        liberal_color = '#1E90FF'  # Dodger blue

        # Plot each document's bigrams
        for i, (doc, bigrams) in enumerate(bigram_data.items()):
            # Get top N bigrams
            top_bigrams = bigrams.most_common(top_n)
            bigram_labels = [' '.join(bigram) for bigram, _ in top_bigrams]
            frequencies = [count for _, count in top_bigrams]

            # Choose color based on document type
            color = conservative_color if 'conservative' in doc.lower() else liberal_color

            # Create bar chart
            axes[i].bar(bigram_labels, frequencies, color=color)
            axes[i].set_title(doc, fontsize=10)
            axes[i].set_ylabel('Frequency')
            axes[i].tick_params(axis='x', rotation=45, labelsize=8)


        fig.suptitle(f'Top {top_n} Bigrams per Document', fontsize=16)
        plt.show()
        
    def compare_documents(self, k=15, words=None, figsize=(18, 10)):
        """
        Create a grouped bar chart comparing word usage across all documents,
        and a scatter plot comparing polarity and subjectivity across all documents.

        Parameters:
        - k: Number of top words to compare if words=None (default: 15)
        - words: Optional list of specific words to analyze
        - figsize: Tuple for figure size (width, height)
        """
        # Get wordcount data
        wordcount_data = self.data['wordcount']
        doc_labels = list(wordcount_data.keys())

        # Determine words to compare
        if words is None:
            # Get top k words across all documents
            all_words = Counter()
            for counter in wordcount_data.values():
                all_words.update(counter)
            words = [word for word, _ in all_words.most_common(k) if word not in self.stop_words]

        # Prepare data for plotting
        word_freqs = {word: [] for word in words}
        for doc in doc_labels:
            counter = wordcount_data[doc]
            for word in words:
                word_freqs[word].append(counter.get(word, 0))

        # Set up plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)
        plt.rcParams.update({'font.size': 8})
        bar_width = 0.08
        index = np.arange(len(words))

        # Colors
        cmap = plt.get_cmap("tab10") 

        for i, doc in enumerate(doc_labels):
            frequencies = [word_freqs[word][i] for word in words]
            color = cmap(i % cmap.N)
            bar_position = [x + bar_width * i for x in index]
            ax1.bar(bar_position, frequencies, bar_width, label=doc, color=color)
            polarities = self.data['avg polarity'][doc]
            subjectivities = self.data['avg subjectivity'][doc]
            ax2.scatter(polarities, subjectivities, color=color, label=doc)

        
        ax1.set_xlabel('Words')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Comparative Word Usage Across Documents', fontsize=16)
        ax1.set_xticks(index + bar_width * (len(doc_labels) - 1) / 2)
        ax1.set_xticklabels(words, rotation=45, ha='right')
        ax1.legend()
        ax1.tick_params(axis='x', labelsize=8)

        ax2.set_xlabel('Polarity')
        ax2.set_ylabel('Subjectivity')
        ax2.grid(True)
        ax2.set_title('Sentiment Analysis Across Documents')

        plt.tight_layout()
        plt.show()

