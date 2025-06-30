import requests
import time
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import logging
import json
import ssl
from datetime import datetime

# === SETUP LOGGING ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# === LOAD ENV ===
load_dotenv()

BITCOIN_WALLET = os.getenv('BITCOIN_WALLET')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 300))  # Default 300 seconds

SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
EMAIL_TO = os.getenv('EMAIL_TO')

# Blockchain.com API configuration
BLOCKCHAIN_API = "https://blockchain.info"

# Validate required settings
if not BITCOIN_WALLET:
    logger.error("BITCOIN_WALLET is not set in .env")
    exit(1)

if not all([EMAIL_USER, EMAIL_PASS, EMAIL_TO]):
    logger.error("Missing email configuration in .env")
    exit(1)

ALREADY_ALERTED = set()

def send_email_alert(tx_data):
    try:
        # Convert satoshi to BTC
        value_satoshi = abs(tx_data['result'])
        value_btc = value_satoshi / 10**8
        
        # Format date
        tx_time = datetime.fromtimestamp(tx_data['time'])
        
        subject = f'ALERT: Outgoing Bitcoin Transaction!'
        body = (
            f'CRITICAL: Bitcoin movement detected from monitored wallet!\n\n'
            f'Transaction Hash: {tx_data["hash"]}\n'
            f'Blockchain: Bitcoin\n'
            f'From: {BITCOIN_WALLET}\n'
            f'Amount: {value_btc:.8f} BTC\n'
            f'Date: {tx_time.strftime("%Y-%m-%d %H:%M:%S")}\n\n'
            f'Confirmations: {tx_data["confirmations"]}\n'
            f'Verify transaction: https://www.blockchain.com/explorer/transactions/btc/{tx_data["hash"]}'
        )
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_TO

        context = ssl.create_default_context()
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, [EMAIL_TO], msg.as_string())
        
        logger.info(f"Email alert sent for BTC TX: {tx_data['hash']}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication failed: {e.smtp_error.decode()}")
        return False
    except Exception as e:
        logger.error(f"Failed to send email alert: {str(e)}")
        return False

def get_bitcoin_transactions():
    """Fetch Bitcoin transactions using Blockchain.com API"""
    url = f"{BLOCKCHAIN_API}/rawaddr/{BITCOIN_WALLET}?limit=50"
    
    try:
        logger.info(f"Requesting Bitcoin transactions for {BITCOIN_WALLET}")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # Log raw response for debugging
        logger.debug(f"API response: {json.dumps(data, indent=2)}")
        
        transactions = data.get('txs', [])
            
        logger.info(f"Received {len(transactions)} Bitcoin transactions")
        return transactions
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    
    return []

def check_transactions():
    try:
        transactions = get_bitcoin_transactions()
        new_alerts = 0
        
        for tx in transactions:
            tx_hash = tx.get('hash', '')
            if not tx_hash or tx_hash in ALREADY_ALERTED:
                continue
                
            # Check if outgoing transaction
            outgoing = False
            tx_value = 0
            
            # Check inputs to see if our wallet is sending
            for inp in tx.get('inputs', []):
                if inp.get('prev_out', {}).get('addr', '') == BITCOIN_WALLET:
                    outgoing = True
                    # Sum all outputs that are not change back to our wallet
                    for out in tx.get('out', []):
                        if out.get('addr', '') != BITCOIN_WALLET:
                            tx_value += out.get('value', 0)
                    break
            
            if outgoing and tx_value > 0:
                logger.warning(f"OUTGOING BTC TX DETECTED: {tx_hash}")
                # Add value to transaction data for alert
                tx['result'] = tx_value
                if send_email_alert(tx):
                    ALREADY_ALERTED.add(tx_hash)
                    new_alerts += 1
        
        logger.info(f"Checked {len(transactions)} transactions. New alerts: {new_alerts}")
        return new_alerts
        
    except Exception as e:
        logger.error(f"Error checking transactions: {str(e)}")
        return 0

def main():
    logger.info(f"Starting Bitcoin Monitor")
    logger.info(f"Wallet: {BITCOIN_WALLET}")
    logger.info(f"Check interval: {CHECK_INTERVAL} seconds")
    logger.info(f"API: {BLOCKCHAIN_API}")
    
    try:
        while True:
            start_time = time.time()
            alerts = check_transactions()
            
            elapsed = time.time() - start_time
            sleep_time = max(1, CHECK_INTERVAL - elapsed)
            time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
    except Exception as e:
        logger.error(f"Critical error: {str(e)}")

if __name__ == '__main__':
    main()
