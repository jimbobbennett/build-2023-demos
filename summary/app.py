import os

from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

from dotenv import load_dotenv
from flask import Flask, render_template, request

# Load the envitonment variables
load_dotenv()
endpoint = os.environ['AZURE_LANGUAGE_ENDPOINT']
key = os.environ['AZURE_LANGUAGE_KEY']

# Create the text analytics client
text_analytics_client = TextAnalyticsClient(endpoint, AzureKeyCredential(key))

app = Flask(__name__)

def create_abstractive_summary(document: str) -> str:
    '''
    Creates an abstractive summary of the document using the Text Analytics service

    :param document: The document to summarize
    :type document: str
    :return: The summary of the document
    :rtype: str
    '''
    # Start processing the document for an abstractive summary
    poller = text_analytics_client.begin_abstractive_summary([document])

    # Get the results
    abstractive_summary_results = poller.result()

    full_summary = ''

    for result in abstractive_summary_results:
        if result.kind == "AbstractiveSummarization":
            # If we have summaries, add them to the overall summary
            for summary in result.summaries:
                full_summary += summary.text
        elif result.is_error is True:
            # If we have an error, return the error
            return f"Error with code '{result.error.code}' and message '{result.error.message}'"
    
    return full_summary

def create_extractive_summary(document: str) -> str:
    '''
    Creates an extractive summary of the document using the Text Analytics service

    :param document: The document to summarize
    :type document: str
    :return: The summary of the document
    :rtype: str
    '''
    # Start processing the document for an extractive summary
    poller = text_analytics_client.begin_extract_summary([document])

    # Get the results
    extractive_summary_results = poller.result()

    full_summary = ''

    for result in extractive_summary_results:
        if result.kind == "ExtractiveSummarization":
            # If we have summaries, add them to the overall summary
            for sentence in result.sentences:
                full_summary += sentence.text
        elif result.is_error is True:
            # If we have an error, return the error
            return f"Error with code '{result.error.code}' and message '{result.error.message}'"
    
    return full_summary

def summarization(template: str, summary_func) -> str:
    data = {
        'document': '',
        'summary': '',
        'documentCount': '',
        'summaryCount': ''
    }

    if request.method == "POST" and 'documentEntry' in request.form:
        data['document'] = request.form.get('documentEntry')
        data['documentCount'] = f'{len(data["document"])} characters'
        data['summary'] = summary_func(data['document'])
        data['summaryCount'] = f'{len(data["summary"])} characters'

    return render_template(template, data=data)

@app.route('/abstractive', methods=['GET', 'POST'])
def abstractive() -> str:
    return summarization('abstract_summary.html', create_abstractive_summary)

@app.route('/extractive', methods=['GET', 'POST'])
def extractive() -> str:
    return summarization('extract_summary.html', create_extractive_summary)

@app.route('/language_detection', methods=['GET', 'POST'])
def language_detection() -> str:
    data = {
        'document': '',
        'lamguage': ''
    }

    if request.method == "POST" and 'documentEntry' in request.form:
        data['document'] = request.form.get('documentEntry')
        data['language'] = text_analytics_client.detect_language([data['document']])[0].primary_language.name

    return render_template('language_detection.html', data=data)

@app.route('/entity_linking', methods=['GET', 'POST'])
def entity_linking() -> str:
    data = {
        'document': '',
        'entities': []
    }

    if request.method == "POST" and 'documentEntry' in request.form:
        data['document'] = request.form.get('documentEntry')

        entities_result = text_analytics_client.recognize_linked_entities(documents = [data['document']])[0]

        for entity in entities_result.entities:
            entity_card = {
                "name": entity.name,
                "url": entity.url,
                "data_source": entity.data_source,
            }
            data['entities'].append(entity_card)

    return render_template('entity_linking.html', data=data)

@app.route('/named_entity_recognition', methods=['GET', 'POST'])
def named_entity_recognition() -> str:
    data = {
        'document': '',
        'entities': []
    }

    if request.method == "POST" and 'documentEntry' in request.form:
        data['document'] = request.form.get('documentEntry')

        entities_result = text_analytics_client.recognize_entities(documents = [data['document']])[0]

        for entity in entities_result.entities:
            entity_card = {
                "name": entity.text,
                "category": entity.category,
                "subcategory": entity.subcategory,
            }
            data['entities'].append(entity_card)

    return render_template('named_entity_recognition.html', data=data)

@app.route('/key_phrase_extraction', methods=['GET', 'POST'])
def key_phrase_extraction() -> str:
    data = {
        'document': '',
        'key_phrases': []
    }

    if request.method == "POST" and 'documentEntry' in request.form:
        data['document'] = request.form.get('documentEntry')

        key_phrases_result = text_analytics_client.extract_key_phrases(documents = [data['document']])[0]

        for key_phrase in key_phrases_result.key_phrases:
            data['key_phrases'].append(key_phrase)

    return render_template('key_phrase_extraction.html', data=data)

@app.route('/')
def home() -> str:
    return render_template('index.html')