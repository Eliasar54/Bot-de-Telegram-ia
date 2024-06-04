import requests
import telepot
from telepot.loop import MessageLoop
import time
from colorama import init, Fore, Style

# Inicializa colorama
init()

# Función para solicitar y validar el token de acceso del bot
def obtener_token():
    while True:
        opcion = input("Presiona 1 para ver un tutorial sobre cómo obtener el token de bot de Telegram, o presiona 2 para ingresar tu token directamente: ").strip()
        
        if opcion == '1':
            mostrar_tutorial()
        elif opcion == '2':
            token = input("Por favor, ingresa tu token de bot de Telegram: ").strip()
            if len(token) > 30:
                return token
            else:
                print("Token inválido. Asegúrate de ingresar un token válido.")
        else:
            print("Opción no válida. Por favor, selecciona 1 o 2.")

def mostrar_tutorial():
    print(Fore.YELLOW + Style.BRIGHT + "\nTutorial para obtener el token de bot de Telegram:")
    print("1. Abre Telegram y busca 'BotFather'.")
    print("2. Inicia una conversación con BotFather y sigue las instrucciones para crear un nuevo bot.")
    print("3. Una vez creado, copia el token generado y pégalo cuando se solicite.")
    print(Style.RESET_ALL)

# Obtener el token de bot de Telegram
BOT_TOKEN = obtener_token()

if BOT_TOKEN:
    # URL base de la API de ChatGPT
    API_BASE_URL = 'https://api.cafirexos.com/api/chatgpt'

    # Inicializar el bot de Telegram
    bot = telepot.Bot(BOT_TOKEN)

    # Manejar los mensajes entrantes
    def handle_message(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == 'text':
            # Obtener el nombre del usuario
            user_name = msg['from']['first_name']

            # Obtener el texto del mensaje
            user_message = msg['text']

            # Obtener el ID del mensaje
            message_id = msg['message_id']

            # Mostrar el mensaje del usuario en la terminal
            print_user_message(user_name, user_message)

            # Notificar al usuario que el bot está escribiendo
            bot.sendChatAction(chat_id, 'typing')

            # Construir la URL de la API
            api_url = f"{API_BASE_URL}?text={user_message}"

            # Enviar solicitud a la API de ChatGPT
            response = requests.get(api_url)

            # Obtener la respuesta de la API
            response_data = response.json()
            if response_data.get('status'):
                chatgpt_response = response_data.get('resultado', 'Lo siento, no pude obtener una respuesta. 😢')
            else:
                chatgpt_response = "Lo siento, ocurrió un error al procesar tu solicitud. 😢"

            # Agregar emojis a la respuesta
            chatgpt_response += " 😊🚀✨"

            # Mostrar el mensaje de respuesta en la terminal
            print_bot_response(chatgpt_response)

            # Enviar la respuesta de ChatGPT al usuario, respondiendo al mensaje original
            bot.sendMessage(chat_id, chatgpt_response, reply_to_message_id=message_id)

    # Función para imprimir el mensaje del usuario en la terminal
    def print_user_message(user_name, user_message):
        print(Fore.CYAN + Style.BRIGHT + f"Usuario: {user_name}")
        print(Fore.YELLOW + f"Mensaje: {user_message}")
        print(Style.RESET_ALL)

    # Función para imprimir la respuesta del bot en la terminal
    def print_bot_response(response_message):
        print(Fore.GREEN + Style.BRIGHT + "Respuesta del bot:")
        print(Fore.MAGENTA + f"{response_message}")
        print(Style.RESET_ALL)

    # Iniciar el bot
    MessageLoop(bot, handle_message).run_as_thread()

    print(Fore.GREEN + Style.BRIGHT + 'YuGi-BOT está en línea y listo para ayudarte.' + Style.RESET_ALL)

    # Mantener el programa en ejecución
    while True:
        time.sleep(10)
else:
    print("Operación cancelada. El bot no se ejecutará.")
