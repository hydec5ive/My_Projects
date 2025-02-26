import plotly.graph_objects as go
import pandas as pd

def _code_mapping(df, src, targ):
    """ Helper method used by make_sankey.
    (Not to be called outside of this library)
    """
    # Get the distinct labels
    labels = list(set(df[src]).union(set(df[targ])))

    # Generate integer codes
    codes = list(range(len(labels)))

    # Create a label-to-code mapping
    lc_map = dict(zip(labels, codes))

    # Substitute labels for codes in the dataframe
    df = df.replace({src: lc_map, targ: lc_map}).infer_objects(copy=False)
    return df, labels

def stacking(df, *cols, vals=None):
    '''
    :param df: the original dataframe
    :param cols: column names
    :param vals: could be none or the values from the dataframe
    :return: new stacked dataframe with a source column, target column, and artist count column
    '''

    # create pairs for each column name given
    pairs = [(cols[i], cols[i + 1]) for i in range(len(cols) - 1)]
    pre_stacked = None

    # count the number of grouped values and create a new column counts with the counted values stored
    for col1, col2 in pairs:
        if vals is None:
            grouping = df[[col1, col2]].groupby([col1, col2]).size().reset_index(name="counts")
        else:
            grouping = df[[col1, col2, vals]].groupby([col1, col2]).sum().reset_index(name="counts")

        # rename the three column names
        grouping.columns = ["src", "targ", "counts"]

        # replace the none with the first group stack
        if pre_stacked is None:
            pre_stacked = grouping

        # concat additional stacks
        else:
            pre_stacked = pd.concat([pre_stacked, grouping], axis=0)
    return pre_stacked

def make_sankey(df, *cols, vals=None, **kwargs):
    '''

    :param df: cleaned_df
    :param cols: strings (column names)
    :param vals: strings or None (Artist Count Column Name)
    :param kwargs: sankey customization
    :return: sankey diagram
    '''

    stacked_df = stacking(df, *cols, vals=vals)
    src, targ, vals = "src", "targ", "counts"
    val_min = kwargs.get("min_value", 5)
    df, labels = _code_mapping(stacked_df, src, targ)

    # remove rows where count values are below the min_value
    if vals and val_min > 0:
        df = df[df[vals] > val_min]
    if vals:
        values = df[vals]
    else:
        values = [1] * len(df)

    # Construct Sankey Diagram
    link = {"source": df[src], "target": df[targ], "value": values}
    pad = kwargs.get("pad", 25)
    node = {"label": labels, "pad": pad}

    # Generate Sankey Diagram
    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk,
                    layout=go.Layout(title="Museum of Contemporary Art Chicago Sankey Diagram"))
    fig.show()
