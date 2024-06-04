import googletrans
import LangCodes
from googletrans import Translator
from LangCodes import CodeDict

tl = Translator()


def translate(msg: str) -> str:
    msg = msg.lower()

    if (msg == "/thelp"):
      return("""Type '/t [ENGLISH] - [LANGUAGE]'
if language not specified, will auto-translate to english!
Type '/tlangs' to see all current available languages!""")
    
    if(msg == "/tlangs"):
      lang_str = "Afrikaans"
      for value in CodeDict.values():
        if(value != "afrikaans"):
          lang_str += " , " + value.capitalize()
      return("The available languages are:\n"+lang_str+".")


    elif(msg[:2] == "/t"):
      dest = ""
      msg = msg[2:]
      if (msg.find("-") == -1):
        user_msg = msg
        dest = "en"
        user_lang = "English"
      else:
        user_msg = msg[:msg.find("-")]
        user_lang = msg[msg.find("-")+2:]

      if(dest != "en"):
        for code, language in CodeDict.items():
            if(language == user_lang.lower()):
              dest = code
        if dest == "":
          return("Not a valid language or not spelled correctly ; Please try again")

      trans_msg = tl.translate(user_msg, dest)
      src = trans_msg.src
      trans_msg = trans_msg.text

      src_lang = ""
      for code, language in CodeDict.items():
        if(code == src):
          src_lang = language
        if src_lang == "":
          src_lang = "Not found"

      return(f"""{src_lang.capitalize()} : {user_msg} 
**{user_lang.capitalize()} : {trans_msg}**""")