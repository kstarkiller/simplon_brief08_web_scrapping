import dash
from dash import html, dcc, Input, Output, State
from dash.dependencies import Input, Output, State, MATCH, ALL
import plotly.express as px
import pymongo
import pandas as pd
from bson.objectid import ObjectId
import sys
sys.path.append('../../')
from hidden import *
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG level for debug mode
    format='%(asctime)s [%(levelname)s] - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)


# Connect to MongoDB
client = pymongo.MongoClient("mongodb://"+MONGO_USR+":"+MONGO_PWD+"@localhost:27017/")
db = client['scraped_books']

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=['assets/style.css'])

app.layout = html.Div(className="container", children=[
    html.Div(className="navbar", children=[
        html.Div(id='logo', className='logo', children=[
            html.Img(id='', children=[], src='assets/icons/logo.svg', alt=''),
            html.H1("Bookle"),
        ]),
        html.Div(className='searchbarContainer', children=[
            dcc.Input(id='search-input', type='text', placeholder='Enter book title'),
            html.Button(id='search-button', className="search-button", children=[
                html.Img(src="assets/icons/search_icon.svg", className="button-image")
            ]),
        ]),
    ]),
    
    html.Div(className='hidden', id='resultsContainer', children=[
        html.Div(className='search-results', children=[
            html.Div(id='search-output'),
        ]),
        html.Div(id='book-details', className='book-details')
    ]),
    
    html.Div(className="categoriesCountPlot", children=[
        dcc.Graph(id='categoriescount-plot')
    ]),

    html.Div(className="booksRatePlot", children=[
        dcc.Graph(id='booksrate-plot')
    ])
])

@app.callback(
    Output('resultsContainer', 'className'),
    [Input('search-button', 'n_clicks'), Input('search-input', 'n_submit')],
)
def update_class(n_clicks, n_submit):
    if n_clicks or n_submit:
        return 'resultsContainer'
    else:
        return 'hidden'

@app.callback(
    Output('search-output', 'children'),
    [Input('search-button', 'n_clicks'), Input('search-input', 'n_submit')],
    [State('search-input', 'value')],
)
def update_output_onClick(n_clicks, n_submit, value):
    if n_clicks or n_submit :
        results = list(db.books.find({"title": {"$regex": value, "$options": "i"}}))
        results = [{**doc, '_id': str(doc['_id'])} for doc in results]
        results_count = len(results)
        if results_count > 0:
            return html.Ul([
                html.Li(html.A(
                    f"Title: {book['title']}, Category: {book['category']}, Price: {book['price']}",
                    href='#',
                    id={'type': 'book-item', 'index': book['_id']}
                )) for book in results
            ])
        else:
            return "No books found"
    else:
        return "Please enter a book title"

@app.callback(
    Output('book-details', 'children'),
    [Input({'type': 'book-item', 'index': ALL}, 'n_clicks')],
    [State({'type': 'book-item', 'index': ALL}, 'id')]
)
def display_book_details(n_clicks, ids):
    ctx = dash.callback_context
    if not ctx.triggered:
        return

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    book_id = eval(button_id)['index']
    book = db.books.find_one({"_id": ObjectId(book_id)})

    if book:
        match book['rating']:
            case 'One':
                return html.Div([
                    html.H3(book['title']),
                    html.Span(f"Rating : "),
                    html.Span(className="fa fa-star checked"),
                    html.Span(className="fa fa-star"),
                    html.Span(className="fa fa-star"),
                    html.Span(className="fa fa-star"),
                    html.Span(className="fa fa-star"),
                    html.P(f"Price: {book['price']}"),
                    html.P(f"Category: {book['category']}"),
                    html.P(f"Description: {book['description']}"),
                    html.P(f"UPC: {book['upc']}")
                ])
            case 'Two':
                return html.Div([
                    html.H3(book['title']),
                    html.Span(f"Rating : "),
                    html.Span(className="fa fa-star checked"),
                    html.Span(className="fa fa-star checked"),
                    html.Span(className="fa fa-star"),
                    html.Span(className="fa fa-star"),
                    html.Span(className="fa fa-star"),
                    html.P(f"Price: {book['price']}"),
                    html.P(f"Category: {book['category']}"),
                    html.P(f"Description: {book['description']}"),
                    html.P(f"UPC: {book['upc']}")
                ])
            case 'Three':
                return html.Div([
                    html.H3(book['title']),
                    html.Span(f"Rating : "),
                    html.Span(className="fa fa-star checked"),
                    html.Span(className="fa fa-star checked"),
                    html.Span(className="fa fa-star checked"),
                    html.Span(className="fa fa-star"),
                    html.Span(className="fa fa-star"),
                    html.P(f"Price: {book['price']}"),
                    html.P(f"Category: {book['category']}"),
                    html.P(f"Description: {book['description']}"),
                    html.P(f"UPC: {book['upc']}")
                ])
            case 'Four':
                return html.Div([
                    html.H3(book['title']),
                    html.Span(f"Rating : "),
                    html.Span(className="fa fa-star checked"),
                    html.Span(className="fa fa-star checked"),
                    html.Span(className="fa fa-star checked"),
                    html.Span(className="fa fa-star checked"),
                    html.Span(className="fa fa-star"),
                    html.P(f"Price: {book['price']}"),
                    html.P(f"Category: {book['category']}"),
                    html.P(f"Description: {book['description']}"),
                    html.P(f"UPC: {book['upc']}")
                ])
            case 'Five':
                return html.Div([
                    html.H3(book['title']),
                    html.Span(f"Rating : "),
                    html.Span(className="fa fa-star checked"),
                    html.Span(className="fa fa-star checked"),
                    html.Span(className="fa fa-star checked"),
                    html.Span(className="fa fa-star checked"),
                    html.Span(className="fa fa-star checked"),
                    html.P(f"Price: {book['price']}"),
                    html.P(f"Category: {book['category']}"),
                    html.P(f"Description: {book['description']}"),
                    html.P(f"UPC: {book['upc']}")
                ])
            case _:
                return html.Div([
                    html.H3(book['title']),
                    html.Span(f"Rating : No rating yet for this book"),
                    html.P(f"Price: {book['price']}"),
                    html.P(f"Category: {book['category']}"),
                    html.P(f"Description: {book['description']}"),
                    html.P(f"UPC: {book['upc']}")
                ])
    else:
        return "Book details not found."

@app.callback(
    Output('categoriescount-plot', 'figure'),
    Input('search-button', 'n_clicks')
)
def update_category_plot(n_clicks):
    data = list(db.books.find({}, {"_id": 0, "category": 1}))
    df = pd.DataFrame(data)
    category_counts = df['category'].value_counts().reset_index()
    category_counts.columns = ['category', 'count']

    fig = px.bar(category_counts, x='category', y='count', title='Number of Books by Category', color='category',
                category_orders={'category': sorted(category_counts['category'].unique())})
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_color='white',
        font_color='white',
        xaxis=dict(color='white'),
        yaxis=dict(color='white'),
        xaxis_tickangle=-45
    )
    fig.update_layout(legend=dict(font=dict(color='white')))
    return fig

@app.callback(
    Output('booksrate-plot', 'figure'),
    Input('search-button', 'n_clicks')
)
def update_booksrate_plot(n_clicks):
    data = list(db.books.find({}, {"_id": 0, "rating": 1}))
    df = pd.DataFrame(data)
    df['rating'].replace(['One', 'Two', 'Three', 'Four', 'Five'], ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'], inplace=True)
    ratings_counts = df['rating'].value_counts().reset_index()
    ratings_counts.columns = ['rating', 'count']

    fig = px.pie(ratings_counts, values='count', names='rating',
                title='Number of Books by their rating',
                category_orders={'rating': ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars']})
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
