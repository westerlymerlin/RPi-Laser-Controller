# None

<a id="contact_message"></a>

# contact\_message

Provides functionality to send emails using the Microsoft Graph API.

This module defines a function that sends an email through the Microsoft Graph API by authenticating
via Microsoft Authentication Library (MSAL). It uses OAuth2-based client authentication and constructs
an email payload dynamically based on input data. The email can include sender, recipient, subject, and
message body details. Logs and errors are appropriately recorded.

Functions:
    - send_email_via_graph: Sends an email using Microsoft Graph API with the provided payload.

<a id="contact_message.msal"></a>

## msal

<a id="contact_message.requests"></a>

## requests

<a id="contact_message.logger"></a>

## logger

<a id="contact_message.settings"></a>

## settings

<a id="contact_message.SECRETS"></a>

## SECRETS

<a id="contact_message.send_email_via_graph"></a>

#### send\_email\_via\_graph

```python
def send_email_via_graph(body)
```

Sends an email using Microsoft Graph API based on the provided email payload.

This function utilises the MSAL library to authenticate using client credentials
and obtain an OAuth2 token, which is used to send the email through the API.
Email details such as the subject, body, sender, and recipient are customised
based on the input data.

