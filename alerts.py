def send_whatsapp_alert(hazards, risk_level):
    """
    Integrate with Twilio or WhatsApp API in production
    """
    if hazards:
        print(f"[ALERT] WhatsApp: {risk_level} risk detected! Hazards: {', '.join(hazards)}")
