from flask import Flask
import datetime
import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
import json
import requests
import dash_bootstrap_components as dbc

gfonts = {
    'href': 'https://fonts.googleapis.com/css2?family=Satisfy&display=swap',
    'rel': 'stylesheet',
}

chriddyp = 'https://codepen.io/chriddyp/pen/bWLwgP.css'
external_stylesheets = [dbc.themes.BOOTSTRAP]

server = Flask(__name__)
app = dash.Dash(__name__, server= server, external_stylesheets=external_stylesheets)

navbar = dbc.Navbar(
    dbc.Row([
        dbc.Col(dbc.NavbarBrand(
            "Come play with GPT3 - The most advanced AI Model right now", className="ml-2")),
    ],
        align="center",
        no_gutters=True,
    ),
    color="dark",
    dark=True,
)

story_input_form = dbc.FormGroup([
    dbc.Col(
        dbc.Input(id='story_input',
                  placeholder='Write a story on'),
        width=9),
    dbc.Col(
        dbc.Button('Generate a story', id='story_button',
                   color='primary'),
        width=3)
], row=True)
story_output_form = dbc.FormGroup([
    dbc.Col(
        dbc.Textarea(id='story_output', style={'height': '100%'}),
        width=9)],
    row=True,
    style={'height': '70%'})

story_form = dbc.Form(
    [story_input_form, story_output_form], style={'height': '100%'})

haiku_input_form = dbc.FormGroup([
    dbc.Col(
        dbc.Input(id='haiku_input',
                  placeholder='Write a haiku on'),
        width=9),
    dbc.Col(
        dbc.Button('Write a Haiku', id='haiku_button',
                   color='primary'),
        width=3)
], row=True)
haiku_output_form = dbc.FormGroup([
    dbc.Col(
        dbc.Textarea(id='haiku_output', style={'height': '100%'}), width=9)],
    row=True,
    style={'height': '70%'})

haiku_form = dbc.Form(
    [haiku_input_form, haiku_output_form], style={'height': '100%'})


simplify_input_form = dbc.FormGroup([
    dbc.Col(
        dbc.Input(id='simplify_input',
                  placeholder='Do you want to check if your grammar is correct? Enter a sentence in your style'),
        width=9),
    dbc.Col(
        dbc.Button('Check Grammar', id='simplify_button',
                   color='primary'),
        width=3)
], row=True)
simplify_output_form = dbc.FormGroup([
    dbc.Col(
        dbc.Textarea(id='simplify_output', style={'height': '100%'}), width=9)],
    row=True,
    style={'height': '70%'})

simplify_form = dbc.Form(
    [simplify_input_form, simplify_output_form], style={'height': '100%'})


# Ask Anything

askany_input_form = dbc.FormGroup([
    dbc.Col(
        dbc.Textarea(id='askany_input',
                     placeholder='You can ask any question to GPT3! Need to ELI5 a concept? Want to translate to French? Want to generate a recipe? Shoot any question!'),
        width=10),
    dbc.Col(
        dbc.Button('Ask GPT', id='askany_button',
                   color='primary'),
        width=2)
], row=True)
askany_output_form = dbc.FormGroup([
    dbc.Col(
        dbc.Textarea(id='askany_output', style={'height': '100%'}), width=10)],
    row=True,
    style={'height': '100%'})

askany_form = dbc.Form(
    [askany_input_form, askany_output_form], style={'height': '100%'})


app.layout = html.Div([
    # ('Come play with GPT3 - The most advanced AI Model right now!'),
    navbar,
    html.Div([
        html.Div([
            # First Section
            html.Div([  # Input
                story_form
            ], id='first_section', style={'height': '70%',
                                          'padding': '10px'}),

            # Second Section
            html.Div([
                haiku_form
            ], id='second_section', style={'height': '70%',
                                           'padding': '10px'}),

            # Third Section
            html.Div([
                # Input
                simplify_form
            ], id='third-section', style={'height': '70%',
                                          'padding': '10px'})
        ], id='left-div', style={'width': '100%'}),

        html.Div([
            html.Div([
                askany_form
            ], style={'height': '185%',
                      'padding': '10px'})
        ], id='right-div', style={'width': '100%'}),
    ], id='outer-div', style={'display': 'flex',

                              'width': '100%'})

])


def ask_gpt(prompt):
    url = "https://api.openai.com/v1/engines/davinci-instruct-beta/completions"
    payload = json.dumps({
        "prompt": prompt,
        "temperature": 0.5,
        "max_tokens": 120,
        "top_p": 1,
        "frequency_penalty": 0.5,
        "presence_penalty": 0.5
    })
    headers = {
        'Authorization': 'Bearer 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',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_dict = json.loads(response.text)
    haiku = response_dict['choices'][0]['text']

    return haiku

# Story


@ app.callback([Output('story_output', 'value'),
               Output('story_input', 'value')],
               Input('story_button', 'n_clicks'),
               State('story_input', 'value'),
               )
def update_story(n_clicks, topic):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if changed_id == 'story_button.n_clicks':
        prompt = f'Write a fictional short story on {topic}'
        res = ask_gpt(prompt)
        res = prompt + "\n" + res
        return res, ''
    else:
        return '', ''

# Haiku


@ app.callback([Output('haiku_output', 'value'),
               Output('haiku_input', 'value')],
               Input('haiku_button', 'n_clicks'),
               State('haiku_input', 'value'),
               )
def update_haiku(n_clicks, topic):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if changed_id == 'haiku_button.n_clicks':
        prompt = f'Write a haiku on {topic}'
        res = ask_gpt(prompt)
        res = prompt + "\n" + res
        return res, ''
    else:
        return '', ''

# Simplify


def simplify_gpt(prompt):
    url = "https://api.openai.com/v1/engines/davinci/completions"
    payload = json.dumps({
        "prompt": prompt,
        "temperature": 0,
        "max_tokens": 60,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        'stop': ["\n"]
    })
    headers = {
        'Authorization': 'Bearer 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',
        'Content-Type': 'application/json'
    }

    print(prompt)
    response = requests.request("POST", url, headers=headers, data=payload)
    response_dict = json.loads(response.text)
    print(response_dict)
    haiku = response_dict['choices'][0]['text']

    return haiku


@ app.callback([Output('simplify_output', 'value'),
               Output('simplify_input', 'value')],
               Input('simplify_button', 'n_clicks'),
               State('simplify_input', 'value'),
               )
def update_simplify(n_clicks, topic):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if changed_id == 'simplify_button.n_clicks':
        prompt = f'Original: {topic} \n Standard American English:'
        res = simplify_gpt(prompt)
        res = 'Your sentence: ' + topic + '\n' + \
            'GPT thinks the correct sentence is:' + res
        return res, ''
    else:
        return '', ''


@ app.callback([Output('askany_output', 'value'),
               Output('askany_input', 'value')],
               Input('askany_button', 'n_clicks'),
               State('askany_input', 'value'),
               )
def update_askany(n_clicks, topic):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if changed_id == 'askany_button.n_clicks':
        prompt = 'Q: ' + topic + '\nA: '
        res = simplify_gpt(prompt)
        res = 'Your question: ' + topic + '\n' + \
            'GPT responds:' + res
        return res, ''
    else:
        return 'Ask anything', ''


if __name__ == '__main__':
    app.run_server(debug=True)
