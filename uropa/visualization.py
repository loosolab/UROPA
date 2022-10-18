import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

    sns.set_style("darkgrid")

    match kind:
        case "histogram":
            distPlot = sns.histplot(data=table[var])
        case "boxplot":
            distPlot = sns.boxplot(y=table[var])
        case "violin":
            distPlot = sns.violinplot(x=table[var])
        case _:
            raise Exception(
                f"{kind} not supported. Consider using one of the supported plots (histogram, boxplot or violin).")

    if title:
        distPlot.set(title=title)

    if output:
        plt.savefig(output, dpi=dpi)

    return distPlot


def peak_count_plot(table, var="feature", peak_type="exon", group_by=["peak_chr", "peak_start", "peak_end", "peak_strand"], stacked=False, color_by=None, title=None, output=None, dpi=300):
    """
    Count and plot occurence of selected variable by peak.

    Parameters
    ----------
    table : pd.DataFrame
        Pandas dataframe containing the data
    var : string, default "feature"
        Column which table is filtered by
    peak_type : string, default "exon"
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

    sns.set_style("darkgrid")

    # Filter DataFrame by column var and peak_type
    df = table[table[var] == peak_type]

    if color_by:
        group_by.append(color_by)
        # Count the number of equal columns which belong to the group_by list and add the column to the DataFrame
        df = df.groupby(group_by).size().to_frame(peak_type)
        # Count the corresponding numbers of the color_by values and add the column to the DataFrame ("count")
        df = df.groupby([peak_type, color_by]).size().to_frame(
            "count").reset_index()

        # Generate stacked barplot
        if stacked:
            pcPlot = df.pivot(index=peak_type, columns=color_by, values="count").plot(
                kind="bar", stacked=True, rot=0)
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
        plt.savefig(output, dpi=dpi)

    return pcPlot


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
