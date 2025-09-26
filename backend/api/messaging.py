"""
External messaging endpoints for WhatsApp and SMS
"""

from flask import Blueprint, request, jsonify, current_app
from .messaging_services import WhatsAppService, SMSService
from ..models.order_channel import OrderChannel, OrderChannelType
from functools import wraps
import hmac
import hashlib
from .whatsapp_service import handle_incoming_message
from twilio.twiml.messaging_response import MessagingResponse # New import

messaging = Blueprint('messaging', __name__)

# TODO: Add back request validation
# def validate_twilio_request(f):
#     """Validate that the request came from Twilio"""
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         # Get the request values
#         twilio_signature = request.headers.get('X-Twilio-Signature', '')
#         url = request.url
#         params = request.form.to_dict()

#         # Get your auth token from config
#         auth_token = current_app.config['TWILIO_AUTH_TOKEN']

#         # Create the validator
#         validator = RequestValidator(auth_token)

#         # Check the signature
#         if not validator.validate(url, params, twilio_signature):
#             return jsonify({'error': 'Invalid request signature'}), 403

#         return f(*args, **kwargs)
#     return decorated_function

@messaging.route('/webhook/whatsapp', methods=['POST'])
# @validate_twilio_request
def whatsapp_webhook():
    """Handle incoming WhatsApp messages"""
    try:
        message_body = request.form.get('Body')
        sender_id = request.form.get('From')

        if not message_body or not sender_id:
            return jsonify({'error': 'Missing message body or sender ID'}), 400

        # Call the service to get the response message
        response_data = handle_incoming_message(message_body, sender_id)
        
        # Create a Twilio MessagingResponse object
        resp = MessagingResponse()
        resp.message(response_data['message'])
        
        return str(resp) # Return the TwiML XML
    except Exception as e:
        current_app.logger.error(f"WhatsApp webhook error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@messaging.route('/webhook/sms', methods=['POST'])
# @validate_twilio_request
def sms_webhook():
    """Handle incoming SMS messages"""
    try:
        # Initialize SMS service
        sms_service = SMSService(current_app.config['SMS_CONFIG'])
        
        # Handle the message
        result = sms_service.handle_incoming(request.form)
        
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"SMS webhook error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@messaging.route('/channels/status', methods=['GET'])
def get_channel_status():
    """Get the status of all messaging channels"""
    try:
        channels = OrderChannel.find()
        return jsonify({
            'status': 'success',
            'channels': [OrderChannel(**c).to_dict() if isinstance(c, dict) else c.to_dict() for c in channels]
        })
    except Exception as e:
        current_app.logger.error(f"Error getting channel status: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@messaging.route('/send/whatsapp', methods=['POST'])
def send_whatsapp():
    """Send a WhatsApp message"""
    try:
        data = request.get_json()
        to_number = data.get('to')
        message = data.get('message')
        
        if not to_number or not message:
            return jsonify({'error': 'Missing required fields'}), 400
        
        whatsapp_service = WhatsAppService(current_app.config['WHATSAPP_CONFIG'])
        success = whatsapp_service.send_message(to_number, message)
        
        if success:
            return jsonify({'status': 'success'})
        else:
            return jsonify({'error': 'Failed to send message'}), 500
    except Exception as e:
        current_app.logger.error(f"Error sending WhatsApp message: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@messaging.route('/send/sms', methods=['POST'])
def send_sms():
    """Send an SMS message"""
    try:
        data = request.get_json()
        to_number = data.get('to')
        message = data.get('message')
        
        if not to_number or not message:
            return jsonify({'error': 'Missing required fields'}), 400
        
        sms_service = SMSService(current_app.config['SMS_CONFIG'])
        success = sms_service.send_message(to_number, message)
        
        if success:
            return jsonify({'status': 'success'})
        else:
            return jsonify({'error': 'Failed to send message'}), 500
    except Exception as e:
        current_app.logger.error(f"Error sending SMS: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500