# Language service demos for Build 2023

This repo contains a set of demos for the Azure language services.

## Web sample

This sample is a web app that demonstrates the different language services. The web app is written in Python using Flask

### Run the sample

1. Either open the sample in a Codespace, or a VS Code remote container. You can also run it locally.

    To run it locally, you will need Python installed, and a virtual environment set up. Install the Pip packages from the `/web_sample/requirements.txt` file.

1. Create a language service resource on Azure. You will need to enable Custom text classification / Custom Named Entity Recognition during creation.

1. Rename the `.env.example` file to `.env` and set the values:

    * `AZURE_LANGUAGE_ENDPOINT` - this is the endpoint of your language service from the *Keys and endpoint* section.
    * `AZURE_LANGUAGE_KEY` - this is the key of your language service from the *Keys and endpoint* section.
 
1. Run the web server using flask:

    `flask run`

The web server will start up and host the site. You can then navigate to the different tabs to test out the 