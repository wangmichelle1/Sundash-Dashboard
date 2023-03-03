"""
Michelle Wang
DS 3500
SunDash - HW2
2/10/2023

sundash.py: runs the general script of the dashboard
"""

# import libraries and files
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import utils as ut

app = Dash(__name__)

# define the layout
app.layout = html.Div([
    # children one
    html.Div(children=
        # heading for the dashboard
        [html.H1("Interactive SunDash Dashboard Using Dash"),

        html.Br(),
        # label and slider for years
        html.Label("Select a range of years"),
        dcc.RangeSlider(id="num_years", min=1749, max=2022, value=(1749, 2022),
                        marks={
                        1749: "1749",
                        1788: "1788",
                        1827: "1827",
                        1866: "1866",
                        1905: "1905",
                        1944: "1944",
                        1983: "1983",
                        2022: "2022"
                        }, tooltip={"placement": "bottom", "always_visible": True}),

        html.Br(),
        # label and slider for months
        html.Label("Select the number of months (number of observation periods) for smoothing line: "),
        dcc.Slider(id="num_months", min=1, max=24, step=1, value=6),

        html.Br(),
        # label and slider for cycle period
        html.Label("Select number of years for each cycle period"),
        dcc.Slider(id="cycle_years", min=9, max=13, step=1/10, value=11),

        html.Br(),
        # label and dropdown for image filter
        html.Label("Select an image filter"),
        dcc.Dropdown(id="dropdown", options=["EIT 171", "EIT 195", "EIT 284", "EIT 304",
                                              "SDO/HMI Continuum", "SDO/HMI Magnetogram", "LASCO C2",
                                              "LASCO C3"], value="SDO/HMI Continuum", clearable=False),
        html.Img(id="image"),],
        # styling for this children
        style={"padding": 10, "flex": 1}),

    # children two
    html.Div(children=[
        # instruction with which filters to use
        html.Label("For the visualization below, use the first two sliders on the left to adjust "
                   "for range of years and number of months for smoothing."),
        # two graphs - one line graph and one scatter plot
        dcc.Graph(id="graph"),
        html.Label("For the visualization below, use the third slider to adjust for number of "
                   "years for each cycle period."),
        dcc.Graph(id="var_graph"),],
        # styling for this children
        style={"padding": 10, "flex": 1}),],

    # styling for entire flexbox
    style={"display": "flex", "flex-direction": "row"})


# callback for line_graph function below
@app.callback(
    Output("graph", "figure"),
    Input("num_years", "value"),
    Input("num_months", "value")
)
def line_graph(num_years, num_months):
    """ Create a line graph with two lines depicting monthly sunspots and smoothed average line

    Args:
        num_years (tuple): desired date range
        num_months (int): desired number of months for averaging

    Returns:
        fig (px.line): line graph figure
    """
    # read sundash file and filter only including the user-specified date range
    df_sundash = ut.read_file("SN_m_tot_V2.0.csv", ["year", "month", "date_frac", "total_spot_num",
                                                    "st_dev", "observation", "marker"])
    df_sundash = ut.filter_data(df_sundash, "year", num_years)

    # create new column with rolling_avg based on user defined months
    df_sundash["rolling_avg"] = df_sundash["total_spot_num"].rolling(num_months).mean()

    # create figure - line graph with two lines
    # specify width, height, title, and labels for x- and y-axis
    fig = px.line(df_sundash, x="year", y=["total_spot_num", "rolling_avg"], width=891, height=540,
                  title="International sunspot number Sn: monthly mean and " + str(num_months) +
                        "-month smoothed number",
                  labels={"year": "Time(years)", "value": "Sunspot Number"})

    # re-naming legend
    newnames = {'total_spot_num': 'Monthly', 'rolling_avg': 'Smoothed'}
    fig.for_each_trace(lambda t: t.update(name=newnames[t.name]))

    # removing title from legend
    fig.update_layout(legend_title_text=None)

    return fig


# callback function for variable_graph function below
@app.callback(
    Output("var_graph", "figure"),
    Input("num_years", "value"),
    Input("cycle_years", "value")
)
def variable_graph(num_years, cycle_years):
    """ Create a scatter plot showing variability of sunspot cycle

    Args:
        num_years (tuple): desired date range
        cycle_years (int): number of years of sunspot cycle

    Returns:
        fig (px.scatter): scatter plot figure
    """
    # read sundash file and filter only including the user-specified date range
    df_sundash = ut.read_file("SN_m_tot_V2.0.csv", ["year", "month", "date_frac", "total_spot_num",
                                                    "st_dev", "observation", "marker"])
    df_sundash = ut.filter_data(df_sundash, "year", num_years)

    # create cycle column based on user specified cycle_year
    df_sundash["cycle"] = df_sundash["date_frac"] % cycle_years

    # create figure - scatter plot
    # specify width, width, title, labels for x- and y-axis
    fig = px.scatter(df_sundash, x="cycle", y="total_spot_num", width=891, height=540,
                     title="Sunspot Cycle: " + str(cycle_years),
                     labels={"cycle": "Years", "total_spot_num": "# of Sunspots"})

    return fig


# callback for display_image function below
@app.callback(
    Output("image", "src"),
    Input("dropdown", "value")
)
def display_image(dropdown):
    """ Display an image based on selected image filter

    Args:
        dropdown (string): dropdown specifying which image filter
    Returns:
        src (string): source value for image id
    """
    # execute following conditionals based on dropdown (image filter)
    if dropdown == "EIT 171":
        return app.get_asset_url("EIT 171.jpg")
    elif dropdown == "EIT 195":
        return app.get_asset_url("EIT 195.jpg")
    elif dropdown == "EIT 284":
        return app.get_asset_url("EIT 284.jpg")
    elif dropdown == "EIT 304":
        return app.get_asset_url("EIT 304.jpg")
    elif dropdown == "SDO/HMI Continuum":
        return app.get_asset_url("SDO.jpg")
    elif dropdown == "SDO/HMI Magnetogram":
        return app.get_asset_url("SDO2.jpg")
    elif dropdown == "LASCO C2":
        return app.get_asset_url("LASCO C2.jpg")
    elif dropdown == "LASCO C3":
        return app.get_asset_url("LASCO C3.jpg")
    else:
        return None


def main():
    # run app
    app.run_server(debug=True)


main()

