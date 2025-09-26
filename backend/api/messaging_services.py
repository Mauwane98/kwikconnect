"""
External messaging service configurations and utilities
"""

from typing import Dict, Any
import requests
from flask import current_app
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

class WhatsAppService:
    def __init__(self, config: Dict[str, Any]):
        self.client = Client(config['account_sid'], config['auth_token'])
        self.from_number = config['whatsapp_number']

    def send_message(self, to_number: str, message: str) -> bool:
        """Send a WhatsApp message using Twilio"""
        try:
            message = self.client.messages.create(
                from_=f'whatsapp:{self.from_number}',
                body=message,
                to=f'whatsapp:{to_number}'
            )
            return True
        except TwilioRestException as e:
            current_app.logger.error(f"WhatsApp message failed: {str(e)}")
            return False

    def handle_incoming(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming WhatsApp message"""
        message = data.get('Body', '').lower()
        from_number = data.get('From', '').replace('whatsapp:', '')
        
        # Handle different message types
        if message.startswith('order'):
            return self._handle_order(from_number, message)
        elif message.startswith('status'):
            return self._handle_status(from_number)
        elif message.startswith('menu'):
            return self._handle_menu(from_number)
        else:
            return self._handle_help(from_number)

    def _handle_order(self, from_number: str, message: str) -> Dict[str, Any]:
        # Process order message
        # Implementation will depend on your order processing logic
        pass

    def _handle_status(self, from_number: str) -> Dict[str, Any]:
        # Get order status
        pass

    def _handle_menu(self, from_number: str) -> Dict[str, Any]:
        # Send vendor menu
        pass

    def _handle_help(self, from_number: str) -> Dict[str, Any]:
        help_message = """
        Welcome to KwikConnect! You can:
        - Type 'order' followed by your items to place an order
        - Type 'status' to check your order status
        - Type 'menu' to see available vendors and items
        """
        self.send_message(from_number, help_message)
        return {'status': 'success', 'message': 'Help message sent'}


class SMSService:
    def __init__(self, config: Dict[str, Any]):
        self.client = Client(config['account_sid'], config['auth_token'])
        self.from_number = config['sms_number']

    def send_message(self, to_number: str, message: str) -> bool:
        """Send an SMS using Twilio"""
        try:
            message = self.client.messages.create(
                from_=self.from_number,
                body=message,
                to=to_number
            )
            return True
        except TwilioRestException as e:
            current_app.logger.error(f"SMS failed: {str(e)}")
            return False

    def handle_incoming(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming SMS"""
        message = data.get('Body', '').lower()
        from_number = data.get('From', '')

        # Similar structure to WhatsApp handling
        if message.startswith('order'):
            return self._handle_order(from_number, message)
        elif message.startswith('status'):
            return self._handle_status(from_number)
        elif message.startswith('menu'):
            return self._handle_menu(from_number)
        else:
            return self._handle_help(from_number)

    def _handle_order(self, from_number: str, message: str) -> Dict[str, Any]:
        # Process order message
        pass

    def _handle_status(self, from_number: str) -> Dict[str, Any]:
        # Get order status
        pass

    def _handle_menu(self, from_number: str) -> Dict[str, Any]:
        # Send vendor menu
        pass

    def _handle_help(self, from_number: str) -> Dict[str, Any]:
        help_message = """
        KwikConnect commands:
        ORDER <items>: Place an order
        STATUS: Check order status
        MENU: See available items
        """
        self.send_message(from_number, help_message)
        return {'status': 'success', 'message': 'Help message sent'}