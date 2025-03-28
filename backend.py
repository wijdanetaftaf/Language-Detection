from flask import Flask, request, jsonify
from flask_cors import CORS
import fasttext

# Charger le modèle FastText
MODEL_PATH = "lid.176.bin"
model = fasttext.load_model(MODEL_PATH)

# Initialiser Flask
app = Flask(__name__)
CORS(app) 

# Dictionnaire pour convertir les codes en noms de langue
LANGUAGE_MAP = {
    "af": "Afrikaans",
    "als": "Alemannic",
    "am": "Amharic",
    "an": "Aragonese",
    "ar": "Arabic",
    "arz": "Egyptian Arabic",
    "as": "Assamese",
    "ast": "Asturian",
    "av": "Avar",
    "az": "Azerbaijani",
    "azb": "South Azerbaijani",
    "ba": "Bashkir",
    "bar": "Bavarian",
    "bcl": "Central Bicolano",
    "be": "Belarusian",
    "bg": "Bulgarian",
    "bh": "Bihari",
    "bn": "Bengali",
    "bo": "Tibetan",
    "bpy": "Bishnupriya Manipuri",
    "br": "Breton",
    "bs": "Bosnian",
    "bxr": "Buriat",
    "ca": "Catalan",
    "cbk": "Chavacano",
    "ce": "Chechen",
    "ceb": "Cebuano",
    "ckb": "Central Kurdish",
    "co": "Corsican",
    "cs": "Czech",
    "cv": "Chuvash",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "diq": "Zazaki",
    "dsb": "Lower Sorbian",
    "dty": "Doteli",
    "dv": "Dhivehi",
    "el": "Greek",
    "eml": "Emilian-Romagnol",
    "en": "English",
    "eo": "Esperanto",
    "es": "Spanish",
    "et": "Estonian",
    "eu": "Basque",
    "fa": "Persian",
    "fi": "Finnish",
    "fr": "French",
    "frr": "North Frisian",
    "fy": "Frisian",
    "ga": "Irish",
    "gd": "Scottish Gaelic",
    "gl": "Galician",
    "gn": "Guarani",
    "gom": "Goan Konkani",
    "gu": "Gujarati",
    "gv": "Manx",
    "he": "Hebrew",
    "hi": "Hindi",
    "hif": "Fiji Hindi",
    "hr": "Croatian",
    "hsb": "Upper Sorbian",
    "ht": "Haitian Creole",
    "hu": "Hungarian",
    "hy": "Armenian",
    "ia": "Interlingua",
    "id": "Indonesian",
    "ie": "Interlingue",
    "ilo": "Ilocano",
    "io": "Ido",
    "is": "Icelandic",
    "it": "Italian",
    "ja": "Japanese",
    "jbo": "Lojban",
    "jv": "Javanese",
    "ka": "Georgian",
    "kk": "Kazakh",
    "km": "Khmer",
    "kn": "Kannada",
    "ko": "Korean",
    "krc": "Karachay-Balkar",
    "ku": "Kurdish",
    "kv": "Komi",
    "kw": "Cornish",
    "ky": "Kyrgyz",
    "la": "Latin",
    "lb": "Luxembourgish",
    "lez": "Lezgian",
    "li": "Limburgish",
    "lmo": "Lombard",
    "lo": "Lao",
    "lrc": "Northern Luri",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mai": "Maithili",
    "mg": "Malagasy",
    "mhr": "Meadow Mari",
    "min": "Minangkabau",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mn": "Mongolian",
    "mr": "Marathi",
    "mrj": "Hill Mari",
    "ms": "Malay",
    "mt": "Maltese",
    "mwl": "Mirandese",
    "my": "Burmese",
    "myv": "Erzya",
    "mzn": "Mazanderani",
    "nah": "Nahuatl",
    "nap": "Neapolitan",
    "nds": "Low German",
    "ne": "Nepali",
    "new": "Newar",
    "nl": "Dutch",
    "nn": "Norwegian Nynorsk",
    "no": "Norwegian",
    "oc": "Occitan",
    "or": "Odia",
    "os": "Ossetian",
    "pa": "Punjabi",
    "pam": "Pampanga",
    "pfl": "Palatine German",
    "pl": "Polish",
    "pms": "Piedmontese",
    "pnb": "Western Punjabi",
    "ps": "Pashto",
    "pt": "Portuguese",
    "qu": "Quechua",
    "rm": "Romansh",
    "ro": "Romanian",
    "ru": "Russian",
    "rue": "Rusyn",
    "sa": "Sanskrit",
    "sah": "Yakut",
    "sc": "Sardinian",
    "scn": "Sicilian",
    "sco": "Scots",
    "sd": "Sindhi",
    "sh": "Serbo-Croatian",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "sq": "Albanian",
    "sr": "Serbian",
    "su": "Sundanese",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "tg": "Tajik",
    "th": "Thai",
    "tk": "Turkmen",
    "tl": "Tagalog",
    "tr": "Turkish",
    "tt": "Tatar",
    "tyv": "Tuvinian",
    "ug": "Uyghur",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "uz": "Uzbek",
    "vec": "Venetian",
    "vep": "Veps",
    "vi": "Vietnamese",
    "vls": "West Flemish",
    "vo": "Volapük",
    "wa": "Walloon",
    "war": "Waray",
    "wuu": "Wu Chinese",
    "xal": "Kalmyk",
    "xmf": "Mingrelian",
    "yi": "Yiddish",
    "yo": "Yoruba",
    "yue": "Cantonese",
    "zh": "Chinese"
}


# Endpoint API pour détecter la langue
@app.route("/detect", methods=["POST"])
def detect_language():
    data = request.get_json()
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "Le texte ne peut pas être vide"}), 400

    prediction = model.predict(text)
    lang_code = prediction[0][0].replace("__label__", "")  # Supprimer "__label__"
    lang_name = LANGUAGE_MAP.get(lang_code, "Unknown Language")

    return jsonify({"language": lang_name})

# Endpoint pour vérifier si l'API fonctionne
@app.route("/")
def home():
    return jsonify({"message": "it is running"})

# Lancer Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
