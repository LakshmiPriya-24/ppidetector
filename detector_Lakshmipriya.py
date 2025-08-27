#!/usr/bin/env python3
import sys, csv, json, re
phonerec = re.compile(r"\b\d{10}\b")
aadharrec = re.compile(r"\b\d{12}\b")
passrec = re.compile(r"\b[A-Z][0-9]{7}\b", re.I)
upirec = re.compile(r"\b[\w.\-]+@\w+\b")
emailrec = re.compile(r"\b[\w\.\-]+@[A-Za-z0-9\-]+\.[A-Za-z]{2,}\b")
pinrec = re.compile(r"\b\d{6}\b")
iprec = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")

def maskphone(val: str) -> str:
    return val[:2] + "XXXXXX" + val[-2:]

def mask_aadhar(val: str) -> str:
    return "XXXX XXXX " + val[-4:]

def maskpass(val: str) -> str:
    return val[0] + "XXXXXXX"

def maskupi(val: str) -> str:
    try:
        name, bank = val.split("@")
        return (name[:2] + "***@" + bank)
    except:
        return "[REDACTED_PII]"

def maskemail(val: str) -> str:
    try:
        local, domain = val.split("@")
        return local[:2] + "***@" + domain
    except:
        return "[REDACTED_PII]"

def mask_name(val: str) -> str:
    parts = val.split()
    masked = []
    for p in parts:
        masked.append(p[0] + "XXX")
    return " ".join(masked)

def redact_record(js: dict):
    found = {"phone": False, "aadhar": False, "passport": False,
             "upi": False, "email": False, "name_full": False,
             "address": False, "device_ip": False}


    if "phone" in js and phonerec.fullmatch(str(js["phone"])):
        js["phone"] = maskphone(js["phone"])
        found["phone"] = True
    if "aadhar" in js and aadharrec.fullmatch(str(js["aadhar"])):
        js["aadhar"] = mask_aadhar(js["aadhar"])
        found["aadhar"] = True
    if "passport" in js and passrec.fullmatch(str(js["passport"])):
        js["passport"] = maskpass(js["passport"])
        found["passport"] = True
    if "upi_id" in js and upirec.fullmatch(str(js["upi_id"])):
        js["upi_id"] = maskupi(js["upi_id"])
        found["upi"] = True


    if "email" in js and emailrec.fullmatch(str(js["email"])):
        found["email"] = True


    if "name" in js and len(js["name"].split()) >= 2:
        found["name_full"] = True


    if "address" in js and (pinrec.search(js["address"]) or any(city in js["address"].lower() for city in ["road", "street", "place"])):
        found["address"] = True


    if ("ip_address" in js and iprec.fullmatch(str(js["ip_address"]))) or ("device_id" in js and js["device_id"]):
        found["device_ip"] = True


    device_tied = found["device_ip"] and (found["email"] or found["name_full"] or found["phone"])
    standalone = found["phone"] or found["aadhar"] or found["passport"] or found["upi"]
    combinatorial = sum([found["email"], found["name_full"], found["address"]]) >= 2 or device_tied
    is_pii = standalone or combinatorial


    if is_pii:
        if found["email"]:
            js["email"] = maskemail(js["email"])
        if found["name_full"]:
            js["name"] = mask_name(js["name"])
        if found["address"]:
            js["address"] = "[REDACTED_PII]"
        if "ip_address" in js and found["device_ip"]:
            js["ip_address"] = "[REDACTED_PII]"
        if "device_id" in js and found["device_ip"]:
            js["device_id"] = "[REDACTED_PII]"

    return js, is_pii

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 detector_<YourFullName>.py input.csv output.csv")
        sys.exit(1)

    inp, out = sys.argv[1], sys.argv[2]

    with open(inp, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    output = []
    for row in rows:
        try:
            js = json.loads(row["data_json"])
        except:
            js = {}
        red_js, is_pii = redact_record(js)
        output.append({
            "record_id": row["record_id"],
            "redacted_data_json": json.dumps(red_js, ensure_ascii=False),
            "is_pii": str(is_pii)
        })

    with open(out, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["record_id", "redacted_data_json", "is_pii"])
        writer.writeheader()
        writer.writerows(output)

    print(f"Wrote {out}")

if __name__ == "__main__":
    main()

