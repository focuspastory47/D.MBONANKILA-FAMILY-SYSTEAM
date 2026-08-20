import json
import os
from datetime import datetime
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ADMIN_PASSWORD = "admin123"
DATA_FILE = "wanachama.json"

MIEZI_INFO = [
    {"name": "April", "deadline": "2026-04-30"},
    {"name": "May", "deadline": "2026-05-31"},
    {"name": "June", "deadline": "2026-06-30"},
    {"name": "July", "deadline": "2026-07-31"},
    {"name": "August", "deadline": "2026-08-31"},
    {"name": "September", "deadline": "2026-09-30"},
    {"name": "October", "deadline": "2026-10-31"},
    {"name": "November", "deadline": "2026-11-30"},
    {"name": "December", "deadline": "2026-12-31"},
]

DEFAULT_WANACHAMA = {
    "255795085702": {
        "jina": "MARCELINA DAUDI",
        "cheo": "ASSISTANT SECRETARY",
        "malipo": {},
    },
    "255766222670": {"jina": "LEONARD DAUDI", "cheo": "CHAIRPERSON", "malipo": {}},
    "255610491863": {
        "jina": "ALPHONSINA PASTORY DAUD",
        "cheo": "MEMBER",
        "malipo": {},
    },
    "255618281365": {
        "jina": "LILIAN EDWARD MBONANKIRA",
        "cheo": "MEMBER",
        "malipo": {},
    },
    "255621342705": {
        "jina": "ANGERO PASTORY DAUD",
        "cheo": "MEMBER",
        "malipo": {},
    },
    "255652915225": {"jina": "JERONIM DAUDI", "cheo": "MEMBER", "malipo": {}},
    "255683888136": {
        "jina": "PASCHAL MBONANKIRA",
        "cheo": "MEMBER",
        "malipo": {},
    },
    "255684393735": {"jina": "LILIAN MBONANKIRA", "cheo": "MEMBER", "malipo": {}},
    "255684557133": {"jina": "GIVEN MBONANKIRA", "cheo": "MEMBER", "malipo": {}},
    "255685892522": {"jina": "DAUDI DAUDI", "cheo": "MEMBER", "malipo": {}},
    "255688172336": {"jina": "DAVID MBONANKIRA", "cheo": "MEMBER", "malipo": {}},
    "255714010746": {"jina": "JERONIM DAUDI (1)", "cheo": "MEMBER", "malipo": {}},
    "255717200526": {"jina": "JOVINI DAUDI", "cheo": "MEMBER", "malipo": {}},
    "255740132920": {"jina": "ANTHONY SIMON", "cheo": "MEMBER", "malipo": {}},
    "255741339799": {"jina": "MANASE ZAKAYO", "cheo": "TREASURER", "malipo": {}},
    "255741506978": {"jina": "JESCA NYANDA", "cheo": "MEMBER", "malipo": {}},
    "255741545913": {"jina": "POSIAN DAUD", "cheo": "MEMBER", "malipo": {}},
    "255745173529": {"jina": "VEREDIANA DAUDI", "cheo": "MEMBER", "malipo": {}},
    "255745684828": {"jina": "EGBERT MWAIJUNGA", "cheo": "MEMBER", "malipo": {}},
    "255745729472": {
        "jina": "VEREDIANA DAUDI (2)",
        "cheo": "MEMBER",
        "malipo": {},
    },
    "255755047203": {
        "jina": "SIYAFUATI NDABWONDEYE",
        "cheo": "MEMBER",
        "malipo": {},
    },
    "255757735396": {"jina": "JERONIM DAUDI (2)", "cheo": "MEMBER", "malipo": {}},
    "255758164049": {
        "jina": "STANSILAUS KAVULA",
        "cheo": "MEMBER",
        "malipo": {},
    },
    "255759036521": {"jina": "ANETI KASISI", "cheo": "MEMBER", "malipo": {}},
    "255760543600": {"jina": "JENIPHER PASTORY", "cheo": "MEMBER", "malipo": {}},
    "255761040386": {
        "jina": "ANASTAZIA CHECHELI",
        "cheo": "MEMBER",
        "malipo": {},
    },
    "255762867398": {"jina": "PASTORY MBONAKILA", "cheo": "MEMBER", "malipo": {}},
    "255763380002": {"jina": "CHRIAN DAUDI", "cheo": "MEMBER", "malipo": {}},
    "255765061681": {"jina": "BENJAMINI NGELEJA", "cheo": "MEMBER", "malipo": {}},
    "255768199694": {
        "jina": "YOLANDA MBONANKILA",
        "cheo": "MEMBER",
        "malipo": {},
    },
    "255784449892": {"jina": "SCARION KONYA", "cheo": "MEMBER", "malipo": {}},
    "255788856900": {"jina": "DEDAN PHILIPO", "cheo": "MEMBER", "malipo": {}},
    "255790972543": {"jina": "FLORENCE EDWARD", "cheo": "MEMBER", "malipo": {}},
    "255791692415": {"jina": "MARIANA MMASI", "cheo": "MEMBER", "malipo": {}},
    "255794043237": {"jina": "ADELIFINA PASTORY", "cheo": "MEMBER", "malipo": {}},
    "255796600718": {
        "jina": "VEREDIANA DAUDI (3)",
        "cheo": "MEMBER",
        "malipo": {},
    },
    "255796788724": {
        "jina": "JENIPHER PASTORY (2)",
        "cheo": "MEMBER",
        "malipo": {},
    },
    "255752014677": {"jina": "FOCUS DAUDI", "cheo": "SECRETARY", "malipo": {}},
    "255754260651": {"jina": "TRIPHONIA DAUDI", "cheo": "MEMBER", "malipo": {}},
}


# Function ya kusoma data kutoka kwenye faili
def load_data():
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  else:
    save_data(DEFAULT_WANACHAMA)
    return DEFAULT_WANACHAMA


# Function ya kuhifadhi data permanent kwenye faili la JSON
def save_data(data):
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)


wanachama_db = load_data()


def process_mwanachama(namba, data):
  today = datetime.now().strftime("%Y-%m-%d")
  total_pesa = 0
  total_faini = 0
  total_target = 15000
  miezi_processed = {}

  for item in MIEZI_INFO:
    mwezi = item["name"]
    deadline = item["deadline"]

    m_data = data["malipo"].get(mwezi, {})
    kiingilio = float(m_data.get("kiingilio", 0)) if mwezi == "April" else 0
    ada = float(m_data.get("ada", 0))
    tarehe = m_data.get("tarehe", "")

    faini = 0
    if tarehe:
      try:
        if datetime.strptime(tarehe, "%Y-%m-%d") > datetime.strptime(
            deadline, "%Y-%m-%d"
        ):
          faini = 2000
      except ValueError:
        pass

    total_pesa += kiingilio + ada
    total_faini += faini

    is_past_or_current = (
        deadline <= today or tarehe != "" or ada > 0 or kiingilio > 0
    )
    if is_past_or_current:
      total_target += 10000

    miezi_processed[mwezi] = {
        "kiingilio": kiingilio,
        "ada": ada,
        "faini": faini,
        "tarehe": tarehe,
    }

  total_deni = max(0, total_target - total_pesa) + total_faini

  return {
      "namba": namba,
      "jina": data["jina"],
      "cheo": data["cheo"],
      "miezi": miezi_processed,
      "total_pesa": total_pesa,
      "total_faini": total_faini,
      "total_deni": total_deni,
  }


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/admin")
def admin():
  return render_template("admin.html")


@app.route("/api/mwanachama/<namba>")
def get_mwanachama(namba):
  db = load_data()
  if namba in db:
    res = process_mwanachama(namba, db[namba])
    return jsonify({"success": True, "mwanachama": res})
  return jsonify({"success": False, "message": "Namba hii haijasajiliwa!"}), 404


@app.route("/api/admin/login", methods=["POST"])
def admin_login():
  req = request.json or {}
  if req.get("password") == ADMIN_PASSWORD:
    db = load_data()
    res = [process_mwanachama(k, v) for k, v in db.items()]
    res.sort(key=lambda x: x["jina"])
    return jsonify({"success": True, "wanachama": res})
  return jsonify({"success": False, "message": "Password si sahihi!"}), 401


@app.route("/api/admin/update-malipo", methods=["POST"])
def update_malipo():
  req = request.json or {}
  namba = req.get("namba")
  mwezi = req.get("mwezi")

  db = load_data()

  if namba in db and mwezi:
    if mwezi not in db[namba]["malipo"]:
      db[namba]["malipo"][mwezi] = {}

    if "kiingilio" in req:
      db[namba]["malipo"][mwezi]["kiingilio"] = req["kiingilio"]
    if "ada" in req:
      db[namba]["malipo"][mwezi]["ada"] = req["ada"]
    if "tarehe" in req:
      db[namba]["malipo"][mwezi]["tarehe"] = req["tarehe"]

    # Hifadhi mabadiliko kwenye faili la wanachama.json
    save_data(db)

    updated = process_mwanachama(namba, db[namba])
    return jsonify({"success": True, "mwanachama": updated})

  return jsonify({"success": False, "message": "Imeshindikana kuhifadhi."}), 400


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
