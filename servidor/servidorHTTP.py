#!/usr/bin/env python3
import socket

myHost =  'localhost'

myPort = 50008

# parametros (familia de protocolo, tipo de protocolo)
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPV4, TCP

servidor.bind((myHost, myPort)) #vincula servidor e porta

servidor.listen() #modo de escuta

print('Servidor online! Acesse: http://localhost:50005')

while True:
    conexao , endereco = servidor.accept()
    print('Servidor conectado em ', endereco)
    request = conexao.recv(1024).decode('utf-8')
   
    string_list = request.split(' ')
    method = string_list[0] #metodo do meu request
    requesting_file = string_list[1] #arquivo solicitado

    myfile = requesting_file.lstrip('/') #tirar a barra
  
    if(myfile == ''): #aqui fica o nosso arquivo padrao que vai ser um html basico só para visualização inicial
        myfile = 'index.html'
    print('Arquivo solicitado', myfile)
    try:
        file = open(myfile , 'rb') #aqui vamos abrir o arquivo para leitura
        response = file.read() #ler e guarda o arquivo
        file.close()

        header = 'HTTP/1.1 200 OK\n' #se nao tiver nenhum erro, temos um status 200 para o cabeçalho
        if(myfile == 'index.html'):
            MIMEtype = 'text/html' #MIME type é o mecanismo para dizer ao cliente a variedade de documentos transmitidos
        elif(myfile == 'flor.jpg' or myfile == 'minion.jpg'):
            MIMEtype = 'image/jpeg'
        else:
            MIMEtype = 'text/plain'
        header += 'Content-Type: '+str(MIMEtype)+'\n\n' #adicionamos ele ao header
        print('header final: \n', header)

    except Exception as e: #se der algum erro ele entra aqui, se o arquivo não existir por exemplo
        print("-")
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body>Error 404: File not found</body></html>'.encode('utf-8')

    final_response = header.encode('utf-8')
    final_response += response
    conexao.send(final_response) #o que vai aparecer coomo resposta para o cliente
    conexao.close()