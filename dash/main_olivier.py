import dash
from dash import html, dcc, Input, Output, State
from dash.dependencies import Input, Output, State, MATCH, ALL
import plotly.express as px
import pymongo
import pandas as pd
from bson.objectid import ObjectId

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client['biblio']

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=['assets/style.css'])

app.layout = html.Div(className="container", children=[
    html.Div(className="navbar", children=[
        html.Div(id='logo', className='logo', children=[
            html.Img(src='assets/icons/logo.svg', alt=''),
            html.H1("Bookle"),
        ]),
        html.Div(className='searchbarContainer', children=[
            dcc.Input(id='search-input', type='text', placeholder='Enter book title'),
            html.Button(id='search-button', className="search-button", children=[
                html.Img(src="assets/icons/search_icon.svg", className="button-image")
            ]),
        ]),
    ]),
    
    html.Div(className='resultsContainer', children=[
        html.Div(className='search-results', children=[
            html.Div(id='search-output'),
        ]),
        html.Div(id='book-details', className='book-details')
    ]),
    
    html.Div(className="plot", children=[
        dcc.Graph(id='category-plot')
    ]),
])

@app.callback(
    Output('search-output', 'children'),
    Input('search-button', 'n_clicks'),
    [State('search-input', 'value')],
)
def update_search_output(n_clicks, search_value):
    if n_clicks is None or not search_value:
        return

    search_query = {"title": {"$regex": search_value, "$options": "i"}}
    results = list(db.books.find(search_query))
    results = [{**doc, '_id': str(doc['_id'])} for doc in results]

    if results:
        return html.Ul([
            html.Li(html.A(
                f"Title: {book['title']}, Category: {book['category']}, Price: {book['price']}",
                href='#',
                id={'type': 'book-item', 'index': book['_id']}
            )) for book in results
        ])
    else:
        return "No books found"

@app.callback(
    Output('book-details', 'children'),
    [Input({'type': 'book-item', 'index': ALL}, 'n_clicks')],
    [State({'type': 'book-item', 'index': ALL}, 'id')]
)
def display_book_details(n_clicks, ids):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "Book details not found."

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    book_id = eval(button_id)['index']
    book = db.books.find_one({"_id": ObjectId(book_id)})

    if book:
        return html.Div([
            html.H3(book['title']),
            html.P(f"Rating: {book['rating']}"),
            html.P(f"Price: {book['price']}"),
            html.P(f"Category: {book['category']}"),
            html.P(f"Description: {book['description']}"),
            html.P(f"UPC: {book['upc']}")
        ])
    else:
        return "Book details not found."

@app.callback(
    Output('category-plot', 'figure'),
    Input('search-button', 'n_clicks')
)
def update_category_plot(n_clicks):
    data = list(db.books.find({}, {"_id": 0, "category": 1}))
    df = pd.DataFrame(data)
    category_counts = df['category'].value_counts().reset_index()
    category_counts.columns = ['category', 'count']

    fig = px.bar(category_counts, x='category', y='count', title='Number of Books by Category', color='category')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_color='white',
        font_color='white',
        xaxis=dict(color='white'),
        yaxis=dict(color='white'),
    )
    fig.update_layout(legend=dict(font=dict(color='white')))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

