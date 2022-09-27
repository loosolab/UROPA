# TODO imports
import pandas as pd
import matplotlib as mp
import matplotlib.pyplot as plt
import seaborn as sb
import os.path as pt

# -------------------- plot functions -------------------- #


def distribution_plot(table, var, kind):
    """
    Plot distribution of the selected numerical variable.
    Distribution can be shown as boxplot, violinplot or histogram/kde.

    Parameters
    ----------
    table : pd.DataFrame
        Pandas dataframe containing the data.
    var : <datatype>, <default value>
        <param description>
    kind : <datatype>, <default value>
        <param description>
    TODO add more parameters

    Returns
    -------
    <datatype> :
        <return description>
    TODO should return the plotting object
    """
    pass

def count_plot(table, var, kind, title=None, path=None, dpi="figure"):
    """
    Count and plot the occurence of the selected categorical variable.
    Either shown as a pie chart or bar plot.
    Parameters
    ----------
    table : pd.DataFrame
        Pandas dataframe containing the data.
    var : String value
        String value naming column along which to group peaks
    kind : String value
        String value naming plot type (pie, bar)
    title : String value, default=None
        String value for title of plot. If None plot has no title.
    path : String value, default=None
        String value with path to save plot at. If None plot is not saved.
    dpi : Float value, default="figure"
        Float value with DPI to save plot with. If "figure" the figure's DPI is used.
    TODO test function and add par plot option
    Returns
    -------
    <datatype> :
        <return description>
    TODO should return the plotting object
    """
    valid_columns = table.keys() # List of valid column names from input table
    categories = table[var].unique() # List of Unique categories in given column
    counts = table[var].value_counts(dropna=False).to_dict() # Dict of category as key and count per category as value
    
    fig, ax = plt.subplots()
    
    if kind == "pie":
        ax.pie(data, labels=categories, autopct='%1.1f%%')
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        if title is not None:
            ax.set_title(title)
    elif kind == "bar":
        pass
    else:
        raise ValueError("Incorrect type parameter. Please choose either \"pie\" or \"bar\".")
    
    if path is not None:
        # check if path to folder in which to save plot is valid
        folder_path = pt.split(path)[0]
        
        if not pt.exists(folder_path):
            raise OSError("Invalid file path for saving plot.")
        
        # Save figure
        plt.savefig(path, dpi=dpi)
        
    plt.show()


def peak_count_plot(table, var, kind):
    """
    Count and plot occurence of selected variable by peak.

    Parameters
    ----------
    table : pd.DataFrame
        Pandas dataframe containing the data.
    var : <datatype>, <default value>
        <param description>
    kind : <datatype>, <default value>
        <param description>
    TODO add more parameters

    Returns
    -------
    <datatype> :
        <return description>
    TODO should return the plotting object
    """
    pass


def upset_plot(table, var):
    """
    Visualize overlaps in a set with an upset plot.
    Similar to a Venn diagram but more readable especially with higher category count.

    For more information see: https://ieeexplore.ieee.org/document/6876017

    https://upsetplot.readthedocs.io/en/stable/

    Parameters
    ----------
    table : pd.DataFrame
        Pandas dataframe containing the data.
    var : <datatype>, <default value>
        <param description>
    TODO add more parameters

    Returns
    -------
    <datatype> :
        <return description>
    TODO should return the plotting object
    """
    pass


def plot_grid(table, groupby, func, ncol=3, **kwargs):
    """
    Create a grid of plots.
    Data is split by selected variable then forwarded to the plotting function.

    Parameters
    ----------
    table : pd.DataFrame
        Pandas dataframe containing the data.
    groupby : str
        Name of a column in `table` the data should be split by.
    func : function
        Plotting function with which the grid is populated.
    ncol : int, default 3
        Number of plots per row.
    kwargs :
        Additional parameters forwarded to `func`.

    Returns
    -------
    matplotlib.figure.Figure :
        Figure
    matplotlib.axes.Axes or array of Axes :
        Each ax contains a plot of the grid.
    """
    pass

# -------------------- plot summary -------------------- #


def summary(allhits, finalhits, config, call, output):
    """
    Create a multi-page summary pdf for the given UROPA run.

    Parameters
    ----------
    allhits : pd.DataFrame
        DataFrame version of the allhits.txt. Contains all peaks with all found annotations.
    finalhits : pd.DataFrame
        DataFrame version of the finalhits.txt. Contains all peaks with only the best (closest) annotation.
    config : dict
        Dict representation of the UROPA config.json
    call : str
        UROPA cmdline call as string.
    output : str
        Path to output pdf.

    Returns
    -------
    None
    """
    # create pdf document
    
    # ----- title page ----- #
    # contains number of annotated peaks
    # cmd call
    # query overview

    # ----- plot pages ----- #
    # ---------------------- #
    # distribution plot(s)

    # ---------------------- #
    # count plot(s)
    
    # ---------------------- #
    # peak count plot(s)
    
    # ---------------------- #
    # upset plot(s)

    # ------ save pdf ------ #
    pass
