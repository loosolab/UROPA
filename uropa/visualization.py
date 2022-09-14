# TODO imports

# -------------------- plot functions -------------------- #


def distribution(table):
    """
    #TODO add description here

    Parameters
    ----------
    table : pd.DataFrame
        Pandas dataframe containing the data.

    Returns
    -------
    """
    pass


def peak_count(table):
    """
    #TODO add description here

    Parameters
    ----------
    table : pd.DataFrame
        Pandas dataframe containing the data.

    Returns
    -------
    """
    pass


def upset(table):
    """
    #TODO add description here

    Parameters
    ----------
    table : pd.DataFrame
        Pandas dataframe containing the data.

    Returns
    -------
    """
    pass


def coverage(table):
    """
    #TODO add description here

    Parameters
    ----------
    table : pd.DataFrame
        Pandas dataframe containing the data.

    Returns
    -------
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
    # query overview

    # ----- plot pages ----- #
    # ---------------------- #
    # distribution
    # ---------------------- #

    # ----- save pdf ----- #
    pass