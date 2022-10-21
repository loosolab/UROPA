import pandas as pd
import matplotlib as mp
import matplotlib.pyplot as plt
import seaborn as sns
import os.path as pt
import upsetplot as up
import numpy as n

# -------------------- plot functions -------------------- #


def distribution_plot(table, var, kind="histogram", title=None, output=None, dpi=300):
    """
    Plot distribution of the selected numerical variable.
    Distribution can be shown as boxplot, violinplot or histogram/kde.

    Parameters
    ----------
    table : pd.DataFrame
        Pandas dataframe containing the data
    var : string
        Column to be displayed
    kind : string, default "histogram"
        Kind of plot: "histogram", "boxplot" or "violin"
    title : string, default None
        Title of the plot
    output : string, default None
        Path where the plot should be saved
    dpi : Int, default 300
        Resolution of the plot

    Returns
    -------
    matplotlib.axes._subplots.AxesSubplot :
        Plot object for further processing
    """
    # Check if var is a valid column name
    if var not in table.columns:
        raise Exception(
            f"Please use a valid column name for parameter \"var\".")
            
    # Check if var is a numerical column
    if not pd.api.types.is_numeric_dtype(table[var]):
        raise Exception(
            f"Please select a numerical column using parameter \"var\". \"{var}\" is not numerical column.")

    sns.set_style("darkgrid")
    sns.set(rc={"figure.dpi": dpi, "savefig.dpi": dpi})

    match kind:
        case "histogram":
            distPlot = sns.histplot(data=table[var])
        case "boxplot":
            distPlot = sns.boxplot(y=table[var])
        case "violin":
            distPlot = sns.violinplot(x=table[var])
        case _:
            raise Exception(
                f"\"{kind}\" not supported. Consider using one of the supported plots (histogram, boxplot or violin).")

    if title:
        distPlot.set(title=title)

    if output:
        plt.savefig(output)

    return distPlot


def count_plot(table, var="feature", kind="pie", title=None, title_size=20, path=None, dpi=300.0, label_rot=45):
    """
    Count and plot the occurence of the selected categorical variable.
    Either shown as a pie chart or bar plot.
    
    Parameters
    ----------
    table : pd.DataFrame
        Pandas dataframe containing the data.
    var : String, default="feature"
        Value naming column along which to group peaks
    kind : String, default="pie"
        Value naming plot type (pie, bar)
    title : String, default=None
        Value for title of plot. If None plot has no title.
    title_size: Integer, default=20
        Value for size in points of figure title.
    path : String, default=None
        Value with path to save plot at including file name and ending. If None plot is not saved.
    dpi : Float, default=300.0
        Value with DPI to save plot with. If default 300.0 DPI is set.
    label_rot: Integer, default=45
        Value deciding degree to which to rotate x-labels for bar plot. Valid values are 0 - 360.
    
    Returns
    -------
    matplotlib.figure.Figure fig :
        Returns the plotting object.
    """
    
    # Check if parameter var is valid column name
    if var not in table.columns: # List of valid column names from input table
        raise ValueError("Incorrect var parameter. Please choose a valid column name to group by.")
    
    # Change type of column to String for better NaN handling
    table[var] = table[var].astype(str)
    categories = table[var].unique() # List of Unique categories in given column
    counts_dict = table[var].value_counts(dropna=False).to_dict() # Dict of category as key and count per category as value
    counts = [] # List of counts for each variable in categories
    # Fill counts
    for category in categories:
        counts.append(counts_dict[category])
    
    fig, ax = plt.subplots(dpi=dpi)
    
    if kind == "pie":
        ax.pie(counts, labels=categories, autopct='%1.1f%%')
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    elif kind == "bar":
        sns.barplot(x=categories, y=counts, ax=ax)
        plt.xticks(rotation=label_rot)
    else:
        raise ValueError("Incorrect kind parameter. Please choose either \"pie\" or \"bar\".")
    
    # Set title if given
    if title is not None:
        ax.set_title(title, size=title_size)
        
    if path is not None:
        # check if path to folder in which to save plot is valid
        folder_path = pt.split(path)[0]
        if folder_path != "" and not pt.exists(folder_path):
            raise OSError("Invalid file path for saving plot.")

        # Save figure (if file ending is not valid method savefig() will raise an Error)
        plt.savefig(path, bbox_inches="tight")
    
    # return plotting object
    return fig


def peak_count_plot(table, var, peak_type, group_by=["peak_chr", "peak_start", "peak_end", "peak_strand"], stacked=False, color_by=None, title=None, output=None, dpi=300):
    """
    Count and plot occurence of selected variable by peak.

    Parameters
    ----------
    table : pd.DataFrame
        Pandas dataframe containing the data
    var : string
        Column which table is filtered by
    peak_type : string
        Value of the selected column (var)
    group_by : list of string, default ["peak_chr", "peak_start", "peak_end", "peak_strand"]
        Columns which table is grouped by
    stacked : bool, default False
        If true, display a stacked barplot (only works if color_by is not None), else display an unstacked barplot
    color_by : string, default None
        Column by whose values the plot should be colored
    title : string, default None
        Title of the plot
    output : string, default None
        Path where the plot should be saved
    dpi : Int, default 300
        Resolution of the plot

    Returns
    -------
    matplotlib.axes._subplots.AxesSubplot :
        Plot object for further processing
    """

    # Check if all parameters are present in data
    params = group_by
    params.append(var)
    if color_by:
        params.append(color_by)
    if any(p not in table.columns for p in params):
        raise Exception(
            f"Please use valid column names only for parameters \"var\", \"group_by\" and \"color_by\".")

    if peak_type not in table[var].unique():
        raise Exception(
            f"peak_type \"{peak_type}\" is not a valid value of column \"{var}\".")

    sns.set_style("darkgrid")
    sns.set(rc={"figure.dpi": dpi, "savefig.dpi": dpi})

    # Filter DataFrame by column var and peak_type
    if peak_type == "nan":
        df = table[table[var].isna()]
    else:
        df = table[table[var] == peak_type]

    if color_by:
        group_by.append(color_by)
        # Count the number of equal columns which belong to the group_by list and add the column to the DataFrame
        df = df.groupby(group_by).size().to_frame(peak_type)
        # Count the corresponding numbers of the color_by values and add the column to the DataFrame ("count")
        df = df.groupby([peak_type, color_by]).size().to_frame("count").reset_index()
        # Generate stacked barplot
        if stacked:
            pcPlot = df.pivot(index=peak_type, columns=color_by, values="count").plot(kind="bar", stacked=True, rot=0)
            pcPlot.set_ylabel("count")
        # Generate barplot
        else:
            pcPlot = sns.barplot(data=df, x=peak_type, y="count", hue=color_by)
            sns.move_legend(pcPlot, "upper right")
    else:
        # Count the number of equal columns which belong to the group_by list
        df = df.groupby(group_by).size()
        # Generate histogram
        pcPlot = sns.histplot(data=df, discrete=True)
        pcPlot.set(xlabel=peak_type, ylabel="count")

    if title:
        pcPlot.set(title=title)

    if output:
        plt.savefig(output)

    return pcPlot


def upset_plot(table, var="feature", peak_columns=["peak_chr", "peak_start", "peak_end", "peak_strand"], title=None, title_size=20, path=None, dpi=300.0, **kwargs):
    """
    Visualize overlaps in a set with an upset plot.
    Similar to a Venn diagram but more readable especially with higher category count.
    For more information see: https://ieeexplore.ieee.org/document/6876017
    https://upsetplot.readthedocs.io/en/stable/
    
    Parameters
    ----------
    table : pd.DataFrame
        Pandas dataframe containing the data.
    var : String, default="feature"
        Column which's values to list per peak and plot as categories.
    peak_columns: List of Strings, default=["peak_chr", "peak_start", "peak_end", "peak_strand"]
        Colums in table which identify peaks, to be used in group_by function.
    title : String, default=None
        Value for title of plot. If None plot has no title.
    title_size: Integer, default=20
        Value for size in points of figure title.
    path : String, default=None
        Value with path to save plot at including plot name and file type ending. If None plot is not saved.
    dpi : Float, default=300.0
        Value with DPI to save plot with. If default 300.0 DPI is set.
    **kwargs : Additional arguments
        Any additional arguments will be passed on to the upsetplot.plot() function. For a list of possible arguments check
        here: https://upsetplot.readthedocs.io/en/stable/api.html#upsetplot.UpSet
    
    Returns
    -------
    matplotlib.figure.Figure fig :
        Returns the plotting object.
    """
    
    # Check if parameter var is valid column name
    if var not in table.columns:
        raise ValueError("Incorrect var parameter. Please choose a valid column name to group by.")
    
    # Check if values for peak_columns are valid column names
    for column in peak_columns:
        if column not in table.columns:
            raise ValueError("Incorrect peak_columns parameter. Please choose valid column names to identify peaks by.")
        
    # Convert var column to String for better handling of NaN values while plotting
    table[var] = table[var].astype(str)
    
    # Creat new data frame that groupes by peaks and lists values for selected colum per peak
    grouped_table = table.groupby(peak_columns, as_index=False)[var].agg(lambda x: list(x))
    
    # Create new data frame in correct format as plotting input
    plot_table = up.from_memberships(grouped_table[var], data=grouped_table)
    
    fig = plt.figure(dpi=dpi)
    
    # Make upset plot
    up.plot(plot_table, fig=fig, **kwargs)
    
    # Set title if given
    if title is not None and type(title) is str and type(title_size) is int:
        fig.suptitle(title, size=title_size)
        
    if path is not None:
        # check if path to folder in which to save plot is valid
        folder_path = pt.split(path)[0]
        if folder_path != "" and not pt.exists(folder_path):
            raise OSError("Invalid file path for saving plot.")

        # Save figure (if file ending is not valid method savefig() will raise an Error)
        plt.savefig(path)
    
    return fig


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
