import requests
from twilio.rest import Client
import schedule

# Função para converter a direção do vento em texto
def converter_direcao_vento(deg):
        direcoes = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 
                'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        idx = int((deg / 22.5) + 0.5) % 16
        return direcoes[idx]

# Função para obter a previsão e enviar a mensagem
def enviar_previsao():
    # Informações da API OpenWeatherMap
    API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXX"
    cidade = "XXXXXXXXXXXXXXXXXXXXXXXX"
    link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&lang=pt_br"
    resposta = requests.get(link).json()

    # Extraindo dados
    descricao = resposta['weather'][0]['description']
    temperatura = resposta['main']['temp'] - 273.15
    umidade = resposta['main']['humidity']
    vento = resposta['wind']['speed']
    direcao_vento = resposta['wind']['deg']
    direcao_vento_texto = converter_direcao_vento(direcao_vento)
    pressao = resposta['main']['pressure']
    sensacao_termica = resposta['main']['feels_like'] - 273.15
    nebulosidade = resposta['clouds']['all']
    direcao_vento = resposta['wind']['deg']


    from datetime import datetime
    nascer_sol = datetime.fromtimestamp(resposta['sys']['sunrise']).strftime('%H:%M:%S')
    por_sol = datetime.fromtimestamp(resposta['sys']['sunset']).strftime('%H:%M:%S')

    # Mensagem formatada
    mensagem = f"""
    Previsão do tempo para {cidade}:
    Descrição: {descricao}
    Temperatura: {temperatura:.2f}ºC
    Sensação Térmica: {sensacao_termica:.2f}ºC
    Umidade: {umidade}%
    Pressão Atmosférica: {pressao} hPa
    Vento: {vento} m/s, Direção: {direcao_vento_texto}
    Nebulosidade: {nebulosidade}%
    Nascer do Sol: {nascer_sol}
    Pôr do Sol: {por_sol}
    """

    # Configurações do Twilio
    account_sid = 'XXXXXXXXXXXXXXXXXXXXXXXX'
    auth_token = 'XXXXXXXXXXXXXXXXXXXXXXXX'
    client = Client(account_sid, auth_token)

    # Enviar mensagem via WhatsApp
    client.messages.create(
        body=mensagem,
        from_='XXXXXXXXXXXXXXXXXXXXXXXX',  # Número do Twilio
        to='XXXXXXXXXXXXXXXXXXXXXXXX'    # Seu número com código do país
    )

    print("Mensagem de previsão enviada com sucesso!")

# Função para enviar o comando 'join' e renovar o acesso ao Twilio Sandbox
def renovar_sandbox():
    # Configurações do Twilio
    account_sid = 'XXXXXXXXXXXXXXXXXXXXXXXX'
    auth_token = 'XXXXXXXXXXXXXXXXXXXXXXXX'
    client = Client(account_sid, auth_token)

    # Nome do seu Sandbox
    sandbox_name = 'inside-snow'  # Mensagem que precisa enviar
    # Enviar a mensagem 'join' para renovar a conexão
    mensagem = f'join {sandbox_name}(Copiar e enviar essa mensagem a cada 48 horas para renovar o Twilio)'
    client.messages.create(
        body=mensagem,
        from_='XXXXXXXXXXXXXXXXXXXXXXXX',  # Número do Twilio
        to='XXXXXXXXXXXXXXXXXXXXXXXX'    # Seu número com código do país
    )

    print("Mensagem 'join' enviada para renovar o acesso ao Sandbox!")

# Agendar a execução diária para enviar a previsão
schedule.every().day.at("10:30").do(enviar_previsao)  # Horário alterado para 10:30, esperando chegar mensagem as 07:30

# Agendar a execução a cada 48 horas para renovar a conexão com o Sandbox
schedule.every(48).hours.do(renovar_sandbox)

# Executa as tarefas agendadas imediatamente
schedule.run_all()
