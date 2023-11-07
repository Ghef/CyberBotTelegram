from maga import Maga.maga as magui
from ast import Pass
from telegram import Update
import random
import pymysql
import asyncio
import os
import qrcode
from datetime import datetime
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,  ConversationHandler, MessageHandler 
from telegram.ext import filters



###########variables globales
INPUT_QR_CODE = 0

#######Funciones del bot
def connect(update, context, delay=6):
    db = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='Telegram')
    #update.message.reply_text('Conectado a la base de datos')
    print("conectado a la base de datos")
    cursor = db.cursor()
    return db, cursor
    

def create_table(update, context):
    db, cursor = connect(update, context)
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS users (
            name text,
            username text,
            id INTEGER,
            vencidas INTEGER,
            perdidas INTEGER
        )
    """)
    #update.message.reply_text('Tabla creada')
    db.commit()
    db.close()

async def delete_table(update, context):
    db, cursor = connect(update, context)
    cursor.execute(f"""
        DROP TABLE users
    """)
    update.message.reply_text('Tabla eliminada')
    db.close()
    

def usuarios(update, context):
    db, cursor = connect(update, context)
    cursor.execute(f"""
        SELECT name, username, vencidas, perdidas FROM users
    """)
    db.commit()
    db.close()
    return update.message.reply_text("nombre |"+ "usuario |" + "vencidas |" + "perdidas \n" f'{cursor.fetchall()}')
    
    

async def register(update, context, delay=6):
    name = update.effective_user.first_name
    username = update.effective_user.username
    id = update.effective_user.id
    perdidas = 1
    vencidas = 1
    db, cursor = connect(update, context)
    cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'""")
    if cursor.fetchall():
        await update.message.reply_text('Usuario ya existe')
    elif name is None or username is None:
        await update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos y intente registrar de nuevo 👍🏻')
    else:
        cursor.execute(f"""
            INSERT INTO users (name, username, id, vencidas, perdidas )
            VALUES ('{name}', '{username}', '{id}','{vencidas}', '{perdidas}')
        """)
        await update.message.reply_text('Usuario registrado 🎉')
        db.commit()
        db.close()
        asyncio.sleep(delay)

def logout(update, context):
    db, cursor = connect(update, context)
    name = update.effective_user.first_name
    username = update.effective_user.username
    id = update.effective_user.id
    cursor.execute(f"""
        DELETE FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'
    """)
    db.commit()
    db.close()
    return update.message.reply_text('Usuario eliminado')
    

async def puntaje(update, context):
    db, cursor = connect(update, context)
    id = update.effective_user.id
    cursor.execute(f"""
        SELECT name FROM users WHERE  id = '{id}'
    """)
    name = cursor.fetchall()
    for a in name:
        a = a[0]
    cursor.execute(f"""
        SELECT username FROM users WHERE  id = '{id}'
    """)
    username = cursor.fetchall()
    for b in username :
        b = b[0]
    cursor.execute(f"""
        SELECT vencidas FROM users WHERE  id = '{id}'
    """)
    vencidas = cursor.fetchall()
    for c in vencidas:
        c = c[0]
    cursor.execute(f"""
        SELECT perdidas FROM users WHERE  id = '{id}'
    """)
    perdidas = cursor.fetchall()
    for d in perdidas:
        d = d[0]
    db.commit()
    db.close()
    
    await update.message.reply_text(f'nombre: {a} \nusuario: {b} \nvencidas: {c} \nperdidas: {d}' )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hola {update.effective_user.first_name}')

def dado(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    return update.message.reply_dice()
###################################################################################
async def  qr_command_handler(update, context) :
    await update.message.reply_text('Enviame el texto para generate un codigo QR')

    return INPUT_QR_CODE

def generate_qr(text):
    
    filename = text + '.jpg'

    img = qrcode.make(text)
    img.save(filename)

    return filename

async def send_qr(filename, chat):
   # chat.send_action(
    #    action = ChatAction.UPLOAD_PHOTO,
     #   timeout=None
    #)

    await chat.send_photo(
        photo=open(filename, 'rb')
    )
    os.unlink(filename)

    

async def input_text(update, context) :
    text = update.message.text
    print(text)

    filename = generate_qr(text)
    chat = update.message.chat
    print(chat)
    print(filename)
    await send_qr(filename, chat)

    return ConversationHandler.END


    

###################################################################################

def efemerides(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    now = datetime.now().strftime('%d-%m')
    if now == "19-06":
        return update.message.reply_text("hoy se celebra el dia de los gays, feliz dia!!!")
    #Junio
    elif now == "23-06":
        return update.message.reply_text("hoy se celebra el dia de los gays, feliz dia!!!")
    elif now == "24-06":
        return update.message.reply_text("hoy se celebra el dia de los gays, feliz dia!!!")
    elif now == "25-06":
        return update.message.reply_text("hoy se celebra el dia de los gays, feliz dia!!!")
    elif now == "26-06":
        return update.message.reply_text("hoy se celebra el dia de los gays, feliz dia!!!")
    elif now == "27-06":
        return update.message.reply_text("hoy se celebra el dia de los gays, feliz dia!!!")
    elif now == "28-06":
        return update.message.reply_text("hoy se celebra el dia de los gays, feliz dia!!!")
    elif now == "29-06":
        return update.message.reply_text("hoy se celebra el dia de los gays, feliz dia!!!")
    elif now == "30-06":
        return update.message.reply_text("hoy se celebra el dia de los gays, feliz dia!!!")
    #Julio
    #Agosto
    #septiempre
    #octubre
    #Noviembre
    #Diciembre
    else:
        return update.message.reply_text("hoy no se celebra nada")
    #return  update.message.reply_text(now)


def yankenpo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    name = update.effective_user.first_name
    username = update.effective_user.username
    id = update.effective_user.id
    db, cursor = connect(update, context)
    respuesta = update.message.text
    yankenpo = "/yankenpo "
    opciones = [
        "piedra",
        'tijera',
        'papel',
        'spock',
        'lagarto'
    ]
    resultado = random.choice(opciones)
    if respuesta == yankenpo + resultado or respuesta == yankenpo + resultado + " ":
        return update.message.reply_text(resultado + "\n" + " empate")

        #piedra
    elif respuesta == yankenpo + "papel" and resultado == "piedra" or  respuesta == yankenpo + "papel " and  resultado == "piedra":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', vencidas= vencidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()         
            return update.message.reply_text(resultado + "\n" + " ganaste, papel tapa la piedra")           
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')
              

    elif respuesta == yankenpo + "tijera"  and  resultado == "piedra" or  respuesta == yankenpo + "tijera " and  resultado == "piedra":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', perdidas= perdidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()         
            return update.message.reply_text(resultado + "\n" + " perdiste, piedra rompe la tijera")          
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')
        

    elif respuesta == yankenpo + "spock"  and  resultado == "piedra" or  respuesta == yankenpo + "spock " and  resultado == "piedra":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', vencidas= vencidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()         
            return update.message.reply_text(resultado + "\n" + " ganaste, spock vaporiza la piedra")
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')

    elif respuesta == yankenpo + "lagarto"  and  resultado == "piedra" or  respuesta == yankenpo + "lagarto " and  resultado == "piedra":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', perdidas= perdidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()         
            return update.message.reply_text(resultado + "\n" + " perdiste, piedra aplasta al lagarto")
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')
        #papel 
    elif respuesta == yankenpo + "piedra"  and resultado == "papel" or  respuesta == yankenpo + "piedra " and resultado == "papel":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', perdidas= perdidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()         
            return update.message.reply_text(resultado + "\n" + " perdiste, papel tapa a la piedra")
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')

    elif respuesta == yankenpo + "tijera"  and resultado == "papel" or  respuesta == yankenpo + "tijera " and resultado == "papel":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', vencidas= vencidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()         
            return update.message.reply_text(resultado + "\n" + " ganaste, tijera corta al papel")
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')

    elif respuesta == yankenpo + "spock"   and resultado == "papel" or  respuesta == yankenpo + "spock " and resultado == "papel":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', perdidas= perdidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()         
            return update.message.reply_text(resultado + "\n" + " perdiste, papel desautoriza a spock")
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')

    elif respuesta == yankenpo + "lagarto"   and resultado == "papel" or  respuesta == yankenpo + "lagarto " and resultado == "papel":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', vencidas= vencidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()       
            return update.message.reply_text(resultado + "\n" + " ganaste, lagarto devora el papel")
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')
        #tijera
    elif respuesta == yankenpo + "papel"   and resultado == "tijera" or  respuesta == yankenpo + "papel " and resultado == "tijera":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', perdidas= perdidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()         
            return update.message.reply_text(resultado + "\n" + " perdiste, tijera corta al papel")
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')

    elif respuesta == yankenpo + "piedra"  and resultado == "tijera" or  respuesta == yankenpo + "piedra " and resultado == "tijera":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', vencidas= vencidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()       
            return update.message.reply_text(resultado + "\n" + " ganaste, piedra rompe la tijera")
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')

    elif respuesta == yankenpo + "spock"  and resultado == "tijera" or  respuesta == yankenpo + "spock " and resultado == "tijera":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', vencidas= vencidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()       
            return update.message.reply_text(resultado + "\n" + " ganaste, spock rompe la tijera")
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')

    elif respuesta == yankenpo + "lagarto"  and resultado == "tijera" or  respuesta == yankenpo + "lagarto " and resultado == "tijera":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', perdidas= perdidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()         
            return update.message.reply_text(resultado + "\n" + " perdiste, tijera decapita al lagarto ")
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')
        #spock
    elif respuesta == yankenpo + "piedra"  and resultado == "spock" or  respuesta == yankenpo + "piedra " and resultado == "spock":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', perdidas= perdidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()         
            return update.message.reply_text(resultado + "\n" + " perdiste, spock vaporiza la piedra")
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')

    elif respuesta == yankenpo + "papel"  and resultado == "spock" or  respuesta == yankenpo + "papel " and resultado == "spock":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', vencidas= vencidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()       
            return update.message.reply_text(resultado + "\n" + " ganaste, papel desautoriza a spock")
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')

    elif respuesta == yankenpo + "tijera"  and resultado == "spock" or  respuesta == yankenpo + "tijera " and resultado == "spock":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', perdidas= perdidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()         
            return update.message.reply_text(resultado + "\n" + " perdiste, spock rompe la tijera")
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')

    elif respuesta == yankenpo + "lagarto"  and resultado == "spock" or  respuesta == yankenpo + "lagarto " and resultado == "spock":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', vencidas= vencidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()       
            return update.message.reply_text(resultado + "\n" + " ganaste, lagarto envenena a spock")
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')

        #lagarto
    elif respuesta == yankenpo + "piedra"  and resultado == "lagarto" or  respuesta == yankenpo + "piedra " and resultado == "lagarto":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', vencidas= vencidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()       
            return update.message.reply_text(resultado + "\n" + " ganaste, piedra aplasta al lagarto")
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')

    elif respuesta == yankenpo + "papel"  and resultado == "lagarto" or  respuesta == yankenpo + "papel " and resultado == "lagarto":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', perdidas= perdidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()         
            return update.message.reply_text(resultado + "\n" + " perdiste, lagarto devora el papel")
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')

    elif respuesta == yankenpo + "tijera"  and resultado == "lagarto" or  respuesta == yankenpo + "tijera " and resultado == "lagarto":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', vencidas= vencidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()       
            return update.message.reply_text(resultado + "\n" + " ganaste, tijera decapita al lagarto")
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')

    elif respuesta == yankenpo + "spock"  and resultado == "lagarto" or  respuesta == yankenpo + "spock " and resultado == "lagarto":
         cursor.execute(f"""SELECT * FROM users WHERE name = '{name}' AND username = '{username}' AND id = '{id}'  """)
         if cursor.fetchall():
            cursor.execute(f"""
                  UPDATE users SET name='{name}', username= '{username}', perdidas= perdidas+1  
                  WHERE id = '{id}'
                  """)
            #update.message.reply_text('usuario actualizado🎉')
            print('usuario actualizado🎉')
            db.commit()
            db.close()         
            return update.message.reply_text(resultado + "\n" + " perdiste, lagarto envenena a spock")
         else:
            return  update.message.reply_text('Te falta usuario o nombre, por favor verifique estos datos e intente registrar de nuevo 👍🏻')
    else:
         return update.message.reply_text(f'escoge piedra, papel, tijera, spock o lagarto, Lince!!!!!! {update.effective_user.first_name}')


   


async def maguimedimela(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    usuario = update._effective_user.id
    medida_h = ['=','==','===','====','=====','======','=======','========','=========','==========']
    medida_m = [ '{}','{ }','{  }','{   }','{    }','{     }','{      }']
    #    id Miembros
    teddy = 154493455
    rata = 1393540381
    bakura = 245239663
    seventh = 657505698
    roma = 666679533
    # Finaliza id Miembros
    print("----------------------------------------")
    print(update.effective_user.id)
    print(update.effective_user.first_name)
    #print(type(update.effective_user.id))
    
    if  (
        usuario ==  teddy or 
        usuario == rata or 
        usuario == seventh or  
        usuario == roma
        ):
        medidaresultado = random.choice(medida_m)
        await update.message.reply_text("(" + medidaresultado + ")")
        print("es mujer")

        """elif usuario == rata:
        medidaresultado = random.choice(medida_m)
        await update.message.reply_text("(" + medidaresultado + ")")
        print("es mujer")
    elif usuario == roma:
        medidaresultado = random.choice(medida_m)
        await update.message.reply_text("(" + medidaresultado + ")")
        print("es mujer")"""

    else: 
        medidaresultado = random.choice(medida_h)
        await update.message.reply_text("8" + medidaresultado + "D")
        print("es hombre")

async def maguiwhoreo(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    fotos = [
            'https://pbs.twimg.com/media/ElZLdaAW0AIqQuv?format=jpg&name=large',
            'https://pbs.twimg.com/media/El3K0CxXgAALGNL?format=jpg&name=large',
            'https://pbs.twimg.com/media/El3K0CzW0AEtRTa?format=jpg&name=large',
            'https://pbs.twimg.com/media/El3K0CzW0AIivpZ?format=jpg&name=large',
            'https://pbs.twimg.com/media/EnEqllaXEAIqtBi?format=jpg&name=large',
            'https://pbs.twimg.com/media/EnEqllZWEAE3bx_?format=jpg&name=large',
            'https://pbs.twimg.com/media/EnObQkUW4AMGUAW?format=jpg&name=large',
            'https://pbs.twimg.com/media/EnObQivW4AYI9S8?format=jpg&name=large',
            'https://pbs.twimg.com/media/EnTpZRrW8AMcCs1?format=jpg&name=large',
            'https://pbs.twimg.com/media/EnXMf2FXUAMflUx?format=jpg&name=large',
            'https://pbs.twimg.com/media/EnXMf2FXEAAU3Kd?format=jpg&name=large',
            'https://pbs.twimg.com/media/EneGQXMXEAIzXoL?format=jpg&name=large',
            'https://pbs.twimg.com/media/EneGQXLW8AcOBXr?format=jpg&name=large',
            'https://pbs.twimg.com/media/EnoYuCTXEAANHWw?format=jpg&name=large',
            'https://pbs.twimg.com/media/EnoYuCUWEAEJnZ8?format=jpg&name=large',
            'https://pbs.twimg.com/media/EnoYuCWXMAQCev_?format=jpg&name=large',
            'https://pbs.twimg.com/media/En8gqsAXMAU6BO5?format=jpg&name=large',
            'https://pbs.twimg.com/media/En8gqsBXIAIUvJ3?format=jpg&name=large',
            'https://pbs.twimg.com/media/Eo41AtFW8AIzLmY?format=jpg&name=large',
            'https://pbs.twimg.com/media/Eo41AtFXcAM8eQI?format=jpg&name=large',
            'https://pbs.twimg.com/media/Eo41AtHXcAAM70W?format=jpg&name=large',
            'https://pbs.twimg.com/media/EpNfZw_XEAIj8UH?format=jpg&name=large',
            'https://pbs.twimg.com/media/EpNfZw_XIAELjUu?format=jpg&name=large',
            'https://pbs.twimg.com/media/EpNfZw_WMAEcaUF?format=jpg&name=large',
            'https://pbs.twimg.com/media/EpfMrDXU8AEAf7w?format=jpg&name=large',
            'https://pbs.twimg.com/media/EpzpphyXEAAghib?format=jpg&name=medium',
            'https://pbs.twimg.com/media/EqCQXCFW8AExpus?format=jpg&name=large',
            'https://pbs.twimg.com/media/EqCQXCFWMAYZdZS?format=jpg&name=large',
            'https://pbs.twimg.com/media/EqCQXCDXMAE0ZyE?format=jpg&name=large',
            'https://pbs.twimg.com/media/Eq7-nWDWMAEA8Ns?format=jpg&name=large',
            'https://pbs.twimg.com/media/Eq7-nWAXEAE70kN?format=jpg&name=large',
            'https://pbs.twimg.com/media/Eq7-nWHWMAYce04?format=jpg&name=large',
            'https://pbs.twimg.com/media/Esx4djJXAA0wLUG?format=jpg&name=large',
            'https://pbs.twimg.com/media/Esx4djIXMAAzyDe?format=jpg&name=large',
            'https://pbs.twimg.com/media/EtHFMVjXMAIxrxr?format=jpg&name=large',
            'https://pbs.twimg.com/media/EtHFMWDW8AE1AyB?format=jpg&name=large',
            'https://pbs.twimg.com/media/EtQu57-WQAI785O?format=jpg&name=large',
            'https://pbs.twimg.com/media/EtQu57_XIAEFw_b?format=jpg&name=large',
            'https://pbs.twimg.com/media/Et_PQAjXYAQS4uP?format=jpg&name=large',
            'https://pbs.twimg.com/media/Et_PQAjXIAAWQfw?format=jpg&name=large',
            'https://pbs.twimg.com/media/Et_PQAoWYAMt7-c?format=jpg&name=large',
            'https://pbs.twimg.com/media/EvBBNitWQAEopJn?format=jpg&name=large',
            'https://pbs.twimg.com/media/EvBBNisWQAEMmr-?format=jpg&name=large',
            'https://pbs.twimg.com/media/EvWuEWYWgAMVj6U?format=jpg&name=large',
            'https://pbs.twimg.com/media/EvWuEWVWgAMssn6?format=jpg&name=large',
            'https://pbs.twimg.com/media/EvWuEWVWQAAW-Ec?format=jpg&name=large',
            'https://pbs.twimg.com/media/EvWuEWWWQAUFxGt?format=jpg&name=large',
            'https://pbs.twimg.com/media/Ev_7WmrWYAcxZMJ?format=jpg&name=large',
            'https://pbs.twimg.com/media/Ev_7WmrXAAcQnFK?format=jpg&name=large',
            'https://pbs.twimg.com/media/Ev_7WmqWQAMjkle?format=jpg&name=large',
            'https://pbs.twimg.com/media/Ew5mhpFXAAMVhiR?format=jpg&name=large',
            'https://pbs.twimg.com/media/Ew5mhpDWEAIvE4b?format=jpg&name=large',
            'https://pbs.twimg.com/media/ExC7djOWYAE1gZJ?format=jpg&name=large',
            'https://pbs.twimg.com/media/ExC7djMWQAMzw4d?format=jpg&name=large',
            'https://pbs.twimg.com/media/ExC7djNWYAEXW2H?format=jpg&name=large',
            'https://pbs.twimg.com/media/Eyabf1PXIAA2VWa?format=jpg&name=large',
            'https://pbs.twimg.com/media/EypPQnCWQAUBcwl?format=jpg&name=large',
            'https://pbs.twimg.com/media/E0LNQ4gWYAApaan?format=jpg&name=large',
            'https://pbs.twimg.com/media/E0LNQ4fWUAQ7wyF?format=jpg&name=large',
            'https://pbs.twimg.com/media/E0LNQ4gXoAc0bK1?format=jpg&name=large',
            'https://pbs.twimg.com/media/E0WgSwsWUAUdU2j?format=jpg&name=large',
            'https://pbs.twimg.com/media/E0WgSwtXMAM87c1?format=jpg&name=large',
            'https://pbs.twimg.com/media/E1OgX22WYAMC6vn?format=jpg&name=large',
            'https://pbs.twimg.com/media/E1OgX22WUAESVBm?format=jpg&name=large',
            'https://pbs.twimg.com/media/E1pMbdJWYAAHoyc?format=jpg&name=medium',
            'https://pbs.twimg.com/media/E2QL8YFXEAA4InR?format=jpg&name=large',
            'https://pbs.twimg.com/media/E4N1uhqXwAEPq0-?format=jpg&name=large',
            'https://pbs.twimg.com/media/E4N1uhhX0AIL_i4?format=jpg&name=large',
            'https://pbs.twimg.com/media/E4N1uhkXwAgsA9J?format=jpg&name=large',
            'https://pbs.twimg.com/media/E4YZ-sfWEAYgLJk?format=jpg&name=large',
            'https://pbs.twimg.com/media/E4YZ-tbXoAEbGtL?format=jpg&name=large',
            'https://pbs.twimg.com/media/E4mK2r_WQAQqLyx?format=jpg&name=large',
            'https://pbs.twimg.com/media/E4mK2sAWEAECBeR?format=jpg&name=large',
            'https://pbs.twimg.com/media/E5-2ZPTXIAI2EO1?format=jpg&name=large',
            'https://pbs.twimg.com/media/E5FfiOoXIAECovy?format=jpg&name=medium',
            'https://pbs.twimg.com/media/E5-olzxWUAI4JFF?format=jpg&name=large',
            'https://pbs.twimg.com/media/E5-olzyWYAEGL_Z?format=jpg&name=large',
            'https://pbs.twimg.com/media/E5-olz4WYAAZLIz?format=jpg&name=large',
            'https://pbs.twimg.com/media/E4cm4KNWEAMx6pC?format=jpg&name=large',
            'https://pbs.twimg.com/media/E4cm4KOXIAAO8f-?format=jpg&name=large',
            'https://pbs.twimg.com/media/E9ChQ52WUAEUgxB?format=jpg&name=large',
            'https://pbs.twimg.com/media/E9ChQ6oWYAED-f9?format=jpg&name=large',
            'https://pbs.twimg.com/media/E9ChQ6pXIAYoJFD?format=jpg&name=large',
            'https://pbs.twimg.com/media/FMtt33CXoAAAGKM?format=jpg&name=large',
            'https://pbs.twimg.com/media/FMtt33IXsAQqkDJ?format=jpg&name=large',
            'https://pbs.twimg.com/media/FQw5aFPXEAMu2q1?format=jpg&name=large',
            'https://pbs.twimg.com/media/FQw6ZglXwAUNKyx?format=jpg&name=large',
            'https://pbs.twimg.com/media/FRI3MexXEAMaU89?format=jpg&name=large',
            'https://pbs.twimg.com/media/FRI3MewX0AAVLBE?format=jpg&name=large',
            'https://pbs.twimg.com/media/FRO0fcZWUAAsXKe?format=jpg&name=large',
            'https://pbs.twimg.com/media/FRO0fcSWYAcmD_o?format=jpg&name=large',
            'https://pbs.twimg.com/media/FSISqRlXMAAd0Ti?format=jpg&name=large',
            'https://pbs.twimg.com/media/FSISqRdXIAA1YBj?format=jpg&name=large',
            'https://pbs.twimg.com/media/FSid48JWQAE-mVq?format=jpg&name=large',
            'https://pbs.twimg.com/media/FSlpBANXwBUTigY?format=jpg&name=large',
            'https://pbs.twimg.com/media/FTDuu2GXoAAyiNl?format=jpg&name=large',
            'https://pbs.twimg.com/media/FTDv6q4WQAAAbhD?format=jpg&name=large',
            'https://pbs.twimg.com/media/FTDwezHXEAUi6ei?format=jpg&name=large',
            'https://pbs.twimg.com/media/FTD47tRWIAEjGxX?format=jpg&name=large',
            'https://pbs.twimg.com/media/FTD4FdYXwAAdXkK?format=jpg&name=large',
            'https://pbs.twimg.com/media/FVaNL9oWIAIfd_m?format=jpg&name=large',
            'https://pbs.twimg.com/media/FVaNL9mXoAMyhoz?format=jpg&name=large',
            'https://pbs.twimg.com/media/FVWc37_WYAA1Xug?format=jpg&name=large',
            'https://pbs.twimg.com/media/FVv6w6zXoAACRxd?format=jpg&name=large',
            'https://pbs.twimg.com/media/FVv6w62XEAEE_jk?format=jpg&name=large',
            'https://pbs.twimg.com/media/FVv6w64WYAAoK9U?format=jpg&name=large',
            'https://pbs.twimg.com/media/FVaNL9oWIAIfd_m?format=jpg&name=large',
            'https://pbs.twimg.com/media/FVaNL9mXoAMyhoz?format=jpg&name=large',
            'https://pbs.twimg.com/media/Fg_pPi8XEAA78ww?format=jpg&name=large',
            'https://pbs.twimg.com/media/FhKXHN8XEAgFvfR?format=jpg&name=large',
            'https://pbs.twimg.com/media/FhKXHN-WAAMObE-?format=jpg&name=large',
            'https://pbs.twimg.com/media/FhKXHN_XoAAeirw?format=jpg&name=large',
            'https://pbs.twimg.com/media/FhP0OnnXwAAboxM?format=jpg&name=large',
            'https://pbs.twimg.com/media/FigdM7AWIAAp09w?format=jpg&name=large',
            'https://pbs.twimg.com/media/FigdM7BXkAEIpYG?format=jpg&name=large',
            'https://pbs.twimg.com/media/Fihk3E2XgAEtWLw?format=jpg&name=large',
            'https://pbs.twimg.com/media/FifxPD7WAAIkD3c?format=jpg&name=large',
            'https://pbs.twimg.com/media/FifxPD6WIAYXqf6?format=jpg&name=large',
            'https://pbs.twimg.com/media/Fii4vnUWYAIJrLL?format=jpg&name=large',
            'https://pbs.twimg.com/media/FjGjJfIWQAM05Ly?format=jpg&name=large',
            'https://pbs.twimg.com/media/FjkdgZHWIAEz-Xk?format=jpg&name=large',
            'https://pbs.twimg.com/media/FjkdgZBWAAEeQuN?format=jpg&name=large',
            'https://pbs.twimg.com/media/Fj4y1JeXEAMkDJj?format=jpg&name=large',
            'https://pbs.twimg.com/media/Fj4y1JiXoAAng5_?format=jpg&name=large',
            'https://pbs.twimg.com/media/Fj590TlWYAEzxgR?format=jpg&name=large',
            'https://pbs.twimg.com/media/Fkob4BqX0AMnAMo?format=jpg&name=large',
            'https://pbs.twimg.com/media/Flqm4S5WQAI_pFM?format=jpg&name=large',
            'https://pbs.twimg.com/media/Flqm4S9XgAAT8xg?format=jpg&name=large',
            'https://pbs.twimg.com/media/FoQk7LNXwAAQ4C9?format=jpg&name=large',
            'https://pbs.twimg.com/media/FpDB0zpXwAAJrk3?format=jpg&name=large',
            'https://pbs.twimg.com/media/FpDB0zoWYAASmSG?format=jpg&name=large',
            'https://pbs.twimg.com/media/Frd7nOSWIAA6D6Q?format=jpg&name=large',
            'https://pbs.twimg.com/media/Frd7nOEXoAAKa6L?format=jpg&name=large',
            'https://pbs.twimg.com/media/Fr3IPbPWYAE9_Vp?format=jpg&name=large',
            'https://pbs.twimg.com/media/Fr3IPbRXgAEjMpf?format=jpg&name=large',
            'https://pbs.twimg.com/media/FsCc6kMX0AAtYDx?format=jpg&name=large',
            'https://pbs.twimg.com/media/FtP8jG5WAAArVhD?format=jpg&name=large',
            'https://pbs.twimg.com/media/FtP6WFuXwAMT7Fr?format=jpg&name=large',
            'https://pbs.twimg.com/media/FuWy5KEXwAEXoeD?format=jpg&name=large',
            'https://pbs.twimg.com/media/FuXLanTWwAE6V-5?format=jpg&name=large',
            'https://pbs.twimg.com/media/FuXLQEzXwAAC5jE?format=jpg&name=large',
            'https://pbs.twimg.com/media/FuxYy_MWwAAKHk4?format=jpg&name=large',
            'https://pbs.twimg.com/media/Fu3IJC9XwAAHoWN?format=jpg&name=large',
            'https://pbs.twimg.com/media/Fu3FewDXsAAlZOZ?format=jpg&name=large',
            'https://pbs.twimg.com/media/Fu7kfSJWYAE9aJd?format=jpg&name=large',
            'https://pbs.twimg.com/media/FvQQoTVX0AIgmk5?format=jpg&name=large',
            'https://pbs.twimg.com/media/Fva8FK8XsAAq4e2?format=jpg&name=large',
            'https://pbs.twimg.com/media/FvznNmHXwAM8S4y?format=jpg&name=large',
            'https://pbs.twimg.com/media/Fv0kjsaWcAEMuY-?format=jpg&name=large',
            'https://pbs.twimg.com/media/Fv0kSNNXwAM4zDd?format=jpg&name=large',
            'https://pbs.twimg.com/media/FwIE12XX0AE6yOH?format=jpg&name=large',
            'https://pbs.twimg.com/media/FwIE12WWcAw_HKq?format=jpg&name=large',
            'https://pbs.twimg.com/media/FwIE12WWcAMVWb1?format=jpg&name=large',
            'https://pbs.twimg.com/media/FwORTsrXwAAnf54?format=jpg&name=large',
            'https://pbs.twimg.com/media/FwYw-6gX0AAOBjQ?format=jpg&name=medium',
            'https://pbs.twimg.com/media/FwYw-5vWwAELJl5?format=jpg&name=medium',
            'https://pbs.twimg.com/media/FwtY510XsAApv6g?format=jpg&name=large',
            'https://pbs.twimg.com/media/FxBkcLSWcAAVXH9?format=jpg&name=large',
            'https://pbs.twimg.com/media/FxGugNxXsAIOrCl?format=jpg&name=large',
            'https://pbs.twimg.com/media/FxMc5EIXwAA_hPw?format=jpg&name=large',
            'https://pbs.twimg.com/media/FxMb-sCXoAA6C3K?format=jpg&name=large',
            'https://pbs.twimg.com/media/FxMb-sAXsAISmUr?format=jpg&name=large',
            'https://pbs.twimg.com/media/FxRAjF_WYAAKLHF?format=jpg&name=large',
            'https://pbs.twimg.com/media/FxmDjmZWcAAYxwx?format=jpg&name=large',
            'https://pbs.twimg.com/media/FyO6gJaX0AEecio?format=jpg&name=large',
            'https://pbs.twimg.com/media/FyYvxduWAAMoNQB?format=jpg&name=large',
            'https://pbs.twimg.com/media/FydRGpXX0AUALMz?format=jpg&name=large',
            'https://pbs.twimg.com/media/Fyii0LbX0AEf4Ys?format=jpg&name=large',
            'https://pbs.twimg.com/media/FyjKuUgWAAAkqD-?format=jpg&name=large',
            'https://pbs.twimg.com/media/FyjG3H4XwAAR8ZN?format=jpg&name=large',
            'https://pbs.twimg.com/media/F0AdtCzXsAIAcOF?format=jpg&name=large',
            'https://pbs.twimg.com/media/F0kOxsaXgAAWMM-?format=jpg&name=large',
            'https://pbs.twimg.com/media/F0n6vAyWcAA5YcV?format=jpg&name=large',
            'https://pbs.twimg.com/media/F0n6vAuX0AAVTTj?format=jpg&name=large',
            'https://pbs.twimg.com/media/F0txcQEWAAIuHWz?format=jpg&name=large',
            'https://pbs.twimg.com/media/F1IPWUwXgAUPZnV?format=jpg&name=large',
            'https://pbs.twimg.com/media/F1IO13EXsAAxDfl?format=jpg&name=large',
            'https://pbs.twimg.com/media/F1IkNlBWwAAWOUc?format=jpg&name=large',
            'https://pbs.twimg.com/media/F1NR0YhX0AA8TcC?format=jpg&name=large',
            'https://pbs.twimg.com/media/F1nN9ksXgAI9ld0?format=jpg&name=large',
            'https://pbs.twimg.com/media/F1nN9ksXgAI9ld0?format=jpg&name=large',
            'https://pbs.twimg.com/media/F11rGPhX0AE8Eif?format=jpg&name=large',
            'https://pbs.twimg.com/media/F16wZ5WX0AAahll?format=jpg&name=large',
            'https://pbs.twimg.com/media/F16u9gjWEAMArkI?format=jpg&name=large',
            'https://pbs.twimg.com/media/F2E4yfVXQAAAop5?format=jpg&name=large',
            'https://pbs.twimg.com/media/F2E4ygaXIAATn8t?format=jpg&name=large',
            'https://pbs.twimg.com/media/F3N_JJUWcAAZzkf?format=jpg&name=large',
            'https://pbs.twimg.com/media/F3yHgKRWYAADhJk?format=jpg&name=large',
            'https://pbs.twimg.com/media/F38ds9xW4AABrP7?format=jpg&name=large',
            'https://pbs.twimg.com/media/F4BPVVcWoAEs41b?format=jpg&name=large',
            'https://pbs.twimg.com/media/F4BPVWTXcAAeqTw?format=jpg&name=large',
            'https://pbs.twimg.com/media/F4G0M0iXUAAaJCR?format=jpg&name=large',
            'https://pbs.twimg.com/media/F4QolmAWsAAutgS?format=jpg&name=large',
            'https://pbs.twimg.com/media/F4ugczkXIAAktLk?format=jpg&name=large',
            'https://pbs.twimg.com/media/F5EZiihXYAE5G6d?format=jpg&name=large',
            'https://pbs.twimg.com/media/F5EZJBnXUAA_iLn?format=jpg&name=large',
            'https://pbs.twimg.com/media/F5sx5yCaUAA0Mn-?format=jpg&name=large',
            'https://pbs.twimg.com/media/F5swr1Ba0AAFTBx?format=jpg&name=large',
            'https://pbs.twimg.com/media/F6aqCCZXkAAJX9I?format=jpg&name=large'
            
            
            
            
            

    ]
    whoreo = random.choice(fotos)
    await update.message.reply_text(whoreo)

def becho(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    return update.message.reply_text('https://pbs.twimg.com/media/FVv6w62WYAA_FV4?format=jpg&name=large')




########
app = ApplicationBuilder().token("magui").build()


########Comandos para la jecucion del bot ############
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("maguimedimela", maguimedimela))
app.add_handler(CommandHandler("maguiwhoreo", maguiwhoreo))
app.add_handler(CommandHandler ("yankenpo", yankenpo))
app.add_handler(CommandHandler ("efemerides", efemerides))
app.add_handler(CommandHandler ("dado", dado))
app.add_handler(CommandHandler ("becho", becho))

#############QR##############
app.add_handler(ConversationHandler(
    entry_points=[
        CommandHandler('qr', qr_command_handler)
    ],

    states={
        INPUT_QR_CODE: [MessageHandler(filters.TEXT, input_text)]
    },

    fallbacks=[]
))
########Base de datos#######################
app.add_handler(CommandHandler ('connect', connect))
app.add_handler(CommandHandler ('create_table', create_table))
app.add_handler(CommandHandler ('delete_table', delete_table))
app.add_handler(CommandHandler ('usuarios', usuarios))
app.add_handler(CommandHandler ('register', register))
app.add_handler(CommandHandler ('logout', logout))
app.add_handler(CommandHandler ('puntaje', puntaje))


######ejecucion del bot
print("bot en ejecucion")
app.run_polling()

print("cancelada la ejecucion del bot")
